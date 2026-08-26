#!/usr/bin/env python3
"""Run the RLM base library end-to-end on the OpenAI backend, and prove it.

The OpenAI counterpart to scripts/verify_rlm_vertex.py, and the first thing to
run if docs/17-OPENAI_PIVOT.md is approved. Same three checks, so the two
scripts' outputs are directly comparable:

  1. quickstart.py            -- needle in a haystack: the library moves a large
                                context into the REPL and searches it with code
                                rather than attention. The base paper's central
                                mechanism; if it fails, nothing downstream is
                                worth building.
  2. logger_example.py        -- trajectory capture in `completion.metadata`.
  3. depth_metadata_example.py -- depth > 1: a parent spawns a child via
                                `rlm_query()`, and the child's own trajectory
                                comes back nested in the parent's metadata.

Plus one check the Vertex script has no need for:

  0. sampling-parameter probe -- settles empirically whether this model accepts
     `temperature`, instead of assuming. eval/backends.py currently drops it on
     the GPT-5-generation precedent and marks that [UNVERIFIED]; this check is
     how that gets verified rather than inherited. It also prints the reported
     token split, which is the only way to see whether reasoning tokens are
     being billed into `completion_tokens` -- if they are not, every OpenAI
     output cost this project reports is understated.

Note what these checks cannot tell you. Nine of the fourteen examples in
`.vendor/rlm/examples` are hardcoded to `OPENAI_API_KEY`
(docs/RLM_BASELINE_SURVEY.md) -- under this backend they become runnable for
the first time, so if these three pass it is worth running the real examples
too. That was impossible on Vertex and is a genuine gain, not a formality:
upstream's own examples exercise paths this script only approximates.

Cost is deliberately small: a reduced haystack and low iteration ceilings. It
is not free, and unlike the Vertex script it spends cash rather than credit.
Budget roughly $0.10-0.30 (six checks, two of them on each tier).

Usage:
    MARD_BACKEND=openai python scripts/verify_rlm_openai.py
"""

from __future__ import annotations

import os
import random
import string
import sys

from dotenv import load_dotenv
from rlm import RLM
from rlm.logger import RLMLogger

from eval.backends import active_profile

load_dotenv()

PROFILE = active_profile()

# Overridable so the W5 optional 2x2 sweep can reuse this script unchanged.
TIER1_MODEL = os.getenv("MARD_TIER1_MODEL", PROFILE.tier1_model)
TIER2_MODEL = os.getenv("MARD_TIER2_MODEL", PROFILE.tier2_model)

# 10k lines rather than quickstart's 50k, matching verify_rlm_vertex.py so the
# two scripts' costs and outcomes compare directly. The mechanism under test is
# "does the library search a variable with code instead of reading it", which
# 10k demonstrates identically while costing less to get wrong.
HAYSTACK_LINES = 10_000


def rule(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def kwargs_for(model: str) -> dict[str, object]:
    return PROFILE.backend_kwargs(model)


def check_0_sampling_probe() -> bool:
    """Temperature support, and where reasoning tokens actually land.

    Deliberately calls the raw SDK handle rather than `.completion()`. Only
    `usage.completion_tokens_details.reasoning_tokens` answers debt item 2, and
    `BaseLM`'s `ModelUsageSummary` does not carry it -- `OpenAIClient._track_cost`
    reads `completion_tokens` alone, which is exactly the quantity under
    suspicion.

    The prompt is chosen to FORCE reasoning. The first version of this check
    used "reply with the digit 7", measured 4 output tokens, and concluded
    nothing: a prompt needing no reasoning produces no reasoning tokens whether
    or not they would be disclosed, so it cannot separate "not billed" from
    "billed but not reported". A prompt that provokes reasoning can.
    """
    rule("0. sampling probe -- temperature, and where reasoning tokens land")

    client = PROFILE.client_class()(
        **kwargs_for(TIER1_MODEL), sampling_args=PROFILE.sampling_params(11)
    )
    prompt = (
        "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the "
        "ball. How much does the ball cost? Reply with just the amount."
    )

    try:
        raw = client.client.chat.completions.create(
            model=TIER1_MODEL,
            messages=[{"role": "user", "content": prompt}],
            **PROFILE.sampling_params(11),
        )
    except Exception as exc:  # noqa: BLE001 -- the point is to report, not raise
        print(f"  FAIL -- the configured sampling args were rejected: {type(exc).__name__}")
        print(f"         {exc}")
        return False

    usage = raw.usage
    details = getattr(usage, "completion_tokens_details", None)
    reasoning = getattr(details, "reasoning_tokens", None)
    visible = raw.choices[0].message.content

    print(f"  configured args   : {PROFILE.sampling_params(11)}")
    print(f"  response          : {str(visible).strip()[:60]!r}")
    print(f"  prompt_tokens     : {usage.prompt_tokens}")
    print(f"  completion_tokens : {usage.completion_tokens}   <- the only figure runlog bills")
    print(f"  reasoning_tokens  : {reasoning}")

    if reasoning is None:
        print("  INCONCLUSIVE -- no reasoning-token breakdown in the response. Debt item 2")
        print("     stays open; reconcile this call against the OpenAI dashboard by hand.")
        accounting_ok = False
    elif reasoning == 0:
        print("  INCONCLUSIVE -- this prompt provoked no reasoning, so the question is")
        print("     untested. Try a harder prompt or reasoning_effort='high'.")
        accounting_ok = False
    elif reasoning < usage.completion_tokens:
        print(f"  VERIFIED -- {reasoning} reasoning tokens sit INSIDE {usage.completion_tokens}")
        print("     completion tokens, so runlog's output count already bills them.")
        print("     Debt item 2 closes: OpenAI output costs are complete, not understated.")
        accounting_ok = True
    else:
        print(f"  PROBLEM -- reasoning_tokens ({reasoning}) >= completion_tokens")
        print(f"     ({usage.completion_tokens}). Reasoning is billed on top of what runlog")
        print("     counts, so EVERY OpenAI output cost this project reports is low.")
        print("     Do not quote a cost figure until runlog reads this field.")
        accounting_ok = False

    with_temp = PROFILE.client_class()(
        **kwargs_for(TIER1_MODEL),
        sampling_args={**PROFILE.sampling_params(11), "temperature": 0.0},
    )
    try:
        with_temp.completion("Reply with exactly the digit 7 and nothing else.")
    except Exception as exc:  # noqa: BLE001
        print(f"\n  temperature=0.0 : REJECTED ({type(exc).__name__})")
        print("  -> eval/backends.py's supports_temperature=False is correct.")
        return accounting_ok

    print("\n  temperature=0.0 : ACCEPTED")
    print("  -> set supports_temperature=True in eval/backends.py and re-run.")
    print("     Pinning temperature to 0.0 restores a determinism lever the")
    print("     OpenAI profile currently gives up.")
    return accounting_ok


def check_1_haystack() -> bool:
    rule("1. quickstart -- needle in a haystack (Tier 1)")

    secret = random.randint(100_000_000, 999_999_999)
    lines = [
        "".join(random.choices(string.ascii_lowercase + " ", k=120)) for _ in range(HAYSTACK_LINES)
    ]
    lines.insert(random.randint(len(lines) // 3, 2 * len(lines) // 3), f"SECRET_NUMBER={secret}")
    haystack = "\n".join(lines)

    rlm = RLM(
        backend=PROFILE.name,
        backend_kwargs=kwargs_for(TIER1_MODEL),
        environment="local",
        max_iterations=10,
        sampling_args=PROFILE.sampling_params(11),
    )
    result = rlm.completion(
        "The context contains ~10k lines of random text with a single line "
        "matching the pattern SECRET_NUMBER=<digits>. Find and return ONLY the "
        f"numeric value.\n\n{haystack}"
    )

    found = str(secret) in result.response
    print(f"  planted : {secret}")
    print(f"  returned: {result.response.strip()[:80]}")
    print(f"  {'PASS' if found else 'FAIL'} -- needle {'found' if found else 'not found'}")
    report_usage(result)
    return found


def check_2_trajectory(model: str, tier: str) -> bool:
    rule(f"2. logger_example -- does {tier} ({model}) actually drive the REPL?")

    rlm = RLM(
        backend=PROFILE.name,
        backend_kwargs=kwargs_for(model),
        environment="local",
        max_iterations=5,
        sampling_args=PROFILE.sampling_params(11),
        logger=RLMLogger(),
    )
    result = rlm.completion(
        "Compute 17 * 23 using Python in the REPL, then set answer['content'] "
        "to the result and answer['ready'] = True."
    )

    # 17 * 23 = 391. The earlier criterion was `iterations > 0`, which a model
    # that refuses to touch the REPL satisfies perfectly -- it iterates, logs
    # nothing useful, and gives up. Checking for the arithmetic result is what
    # distinguishes "the harness works" from "the model used the harness".
    iterations = len((result.metadata or {}).get("iterations", []))
    computed = "391" in result.response
    ok = computed and iterations > 0
    print(f"  response  : {result.response.strip()[:100]}")
    print(f"  iterations captured in metadata: {iterations}")
    print(f"  computed 17*23=391 : {'yes' if computed else 'NO -- did not use the REPL'}")
    verdict = "REPL driven" if ok else "model did not drive the REPL"
    print(f"  {'PASS' if ok else 'FAIL'} -- {verdict}")
    report_usage(result)
    return ok


def check_3_depth(model: str, tier: str) -> bool:
    rule(f"3. depth_metadata -- recursion on {tier} ({model})")

    rlm = RLM(
        backend=PROFILE.name,
        backend_kwargs=kwargs_for(model),
        environment="local",
        max_depth=2,
        max_iterations=5,
        sampling_args=PROFILE.sampling_params(11),
        logger=RLMLogger(),
    )
    result = rlm.completion(
        "Use rlm_query() to ask a sub-model: 'What are the first 5 prime "
        "numbers? Reply with just the numbers separated by commas.' Store the "
        "reply in a variable named primes, then set answer['content'] = primes "
        "and answer['ready'] = True."
    )

    subcalls = 0
    nested = 0
    for iteration in (result.metadata or {}).get("iterations", []):
        for block in iteration.get("code_blocks", []):
            for call in block.get("result", {}).get("rlm_calls", []):
                subcalls += 1
                if call.get("metadata"):
                    nested += 1

    ok = subcalls > 0
    print(f"  response      : {result.response.strip()[:80]}")
    print(f"  child calls   : {subcalls}")
    print(f"  of which carry their own nested metadata: {nested}")
    print(f"  {'PASS' if ok else 'FAIL'} -- recursion {'exercised' if ok else 'never triggered'}")
    if ok:
        print(
            "  note: the child's trajectory flows UP into the parent's metadata.\n"
            "        Nothing flowed DOWN -- the child gets a fresh empty logger and\n"
            "        root_prompt=None. That gap is MARD."
        )
    report_usage(result)
    return ok


def report_usage(result: object) -> None:
    usage = getattr(result, "usage_summary", None)
    if not usage or not getattr(usage, "model_usage_summaries", None):
        return
    for model, summary in usage.model_usage_summaries.items():
        cost = getattr(summary, "total_cost", None)
        cost_str = f"  cost=${cost:.6f}" if cost else "  cost=unreported"
        print(
            f"  usage[{model}]: calls={summary.total_calls} "
            f"in={summary.total_input_tokens} out={summary.total_output_tokens}{cost_str}"
        )


def main() -> int:
    if PROFILE.name != "openai":
        print(f"!! MARD_BACKEND resolves to {PROFILE.name!r}, not 'openai'.")
        print("   This script verifies the OpenAI path. For Vertex use")
        print("   scripts/verify_rlm_vertex.py.")
        return 2
    if not os.getenv("OPENAI_API_KEY"):
        print("!! OPENAI_API_KEY is not set. Add it to .env before running.")
        return 2

    print(f"Backend: {PROFILE.name}   Tier 1: {TIER1_MODEL}   Tier 2: {TIER2_MODEL}")
    print(f"Sampling: {PROFILE.sampling_params(11)}")
    print("Spends real money (~$0.10-0.30). Ctrl-C now if that is not intended.")

    # 2 and 3 run on BOTH tiers. The first pass of this script ran them on Tier 2
    # only (inherited from verify_rlm_vertex.py, to keep cost down) and produced
    # a failure that could not be attributed: is the harness broken, or does that
    # one model decline to drive the REPL? Running both answers it for ~$0.05.
    checks = [
        ("sampling", check_0_sampling_probe),
        ("haystack", check_1_haystack),
        ("trajectory:tier1", lambda: check_2_trajectory(TIER1_MODEL, "Tier 1")),
        ("trajectory:tier2", lambda: check_2_trajectory(TIER2_MODEL, "Tier 2")),
        ("depth:tier1", lambda: check_3_depth(TIER1_MODEL, "Tier 1")),
        ("depth:tier2", lambda: check_3_depth(TIER2_MODEL, "Tier 2")),
    ]

    results = {}
    for name, check in checks:
        try:
            results[name] = check()
        except Exception as exc:  # noqa: BLE001 -- one failed check must not hide the rest
            print(f"  ERROR -- {type(exc).__name__}: {exc}")
            results[name] = False

    rule("summary")
    for name, ok in results.items():
        print(f"  {name:<18} {'PASS' if ok else 'FAIL'}")
    if results.get("depth:tier1") and not results.get("depth:tier2"):
        print(
            "\n  Tier 1 drives the REPL and Tier 2 does not. That is a model-capability\n"
            "  finding, not a harness bug -- see docs/17 debt item 9. It does not block\n"
            "  the vanilla-RLM control, which is single-backend on Tier 1."
        )
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
