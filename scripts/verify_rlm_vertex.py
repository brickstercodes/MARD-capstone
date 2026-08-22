#!/usr/bin/env python3
"""Run the RLM base library end-to-end on our own stack, and prove it.

#11 asks for "RLM library running its own examples end-to-end". Taken
literally that is impossible here: 9 of the 14 examples in `.vendor/rlm/examples`
are hardcoded to `OPENAI_API_KEY` or `PORTKEY_API_KEY`, and the other 5 target
container or sandbox runtimes MARD does not use (docs/RLM_BASELINE_SURVEY.md).
This project is Vertex-only (docs/12-MODEL_PAIR.md), so buying an OpenAI key to
tick the box would prove the library works on a stack we will never run on.

So this script runs what the three examples that matter actually *test*, against
`backend="gemini"` with `use_vertex=True`:

  1. quickstart.py            — needle in a haystack: the library moves a large
                                context into the REPL and searches it with code
                                rather than attention. This is the base paper's
                                central mechanism; if it fails, nothing downstream
                                is worth building.
  2. logger_example.py        — trajectory capture in `completion.metadata`.
  3. depth_metadata_example.py — depth > 1: a parent spawns a child via
                                `rlm_query()`, and the child's own trajectory
                                comes back nested in the parent's metadata.

Check 3 is also the evidence behind docs/RLM_BASELINE_SURVEY.md §2: metadata in
the base library flows *upward* and is observational. Watch what the child is
given — only a prompt string, never the parent's findings. That gap is MARD.

Cost is deliberately small: a reduced haystack and low iteration ceilings. It is
not free — it makes real Vertex calls against the campaign's credit balance.

Usage:
    python scripts/verify_rlm_vertex.py
"""

from __future__ import annotations

import os
import random
import string
import sys

from dotenv import load_dotenv
from rlm import RLM
from rlm.logger import RLMLogger

load_dotenv()

# docs/12-MODEL_PAIR.md. Overridable so the W5 optional 2x2 sweep can reuse this.
TIER1_MODEL = os.getenv("MARD_TIER1_MODEL", "gemini-3.6-flash")
TIER2_MODEL = os.getenv("MARD_TIER2_MODEL", "gemini-3.1-flash-lite")

# `location=global` is not the client's default (it ships us-central1), and
# gemini-3.6-flash 404s on us-central1 for this project — issue #11. Passed
# explicitly at every call site until Track 1 confirms which default is right.
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

# 10k lines rather than quickstart's 50k. The mechanism under test is "does the
# library search a variable with code instead of reading it", which 10k
# demonstrates identically while costing less to get wrong.
HAYSTACK_LINES = 10_000


def vertex_kwargs(model: str) -> dict[str, object]:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        sys.exit("GOOGLE_CLOUD_PROJECT is not set. See TRACK2.md, W0 'API keys provisioned'.")
    return {
        "model_name": model,
        "use_vertex": True,
        "project": project,
        "location": LOCATION,
    }


def rule(title: str) -> None:
    print(f"\n{'=' * 70}\n  {title}\n{'=' * 70}")


def check_1_haystack() -> bool:
    rule("1. quickstart — needle in a haystack (Tier 1)")

    secret = random.randint(100_000_000, 999_999_999)
    lines = [
        "".join(random.choices(string.ascii_lowercase + " ", k=120)) for _ in range(HAYSTACK_LINES)
    ]
    lines.insert(random.randint(len(lines) // 3, 2 * len(lines) // 3), f"SECRET_NUMBER={secret}")
    haystack = "\n".join(lines)

    rlm = RLM(
        backend="gemini",
        backend_kwargs=vertex_kwargs(TIER1_MODEL),
        environment="local",
        max_iterations=10,
    )
    result = rlm.completion(
        "The context contains ~10k lines of random text with a single line "
        "matching the pattern SECRET_NUMBER=<digits>. Find and return ONLY the "
        f"numeric value.\n\n{haystack}"
    )

    found = str(secret) in result.response
    print(f"  planted : {secret}")
    print(f"  returned: {result.response.strip()[:80]}")
    print(f"  {'PASS' if found else 'FAIL'} — needle {'found' if found else 'not found'}")
    report_usage(result)
    return found


def check_2_trajectory() -> bool:
    rule("2. logger_example — trajectory capture (Tier 2)")

    logger = RLMLogger()
    rlm = RLM(
        backend="gemini",
        backend_kwargs=vertex_kwargs(TIER2_MODEL),
        environment="local",
        max_iterations=5,
        logger=logger,
    )
    result = rlm.completion(
        "Compute 17 * 23 using Python in the REPL, then set answer['content'] "
        "to the result and answer['ready'] = True."
    )

    iterations = len((result.metadata or {}).get("iterations", []))
    ok = iterations > 0
    print(f"  response  : {result.response.strip()[:80]}")
    print(f"  iterations captured in metadata: {iterations}")
    print(f"  {'PASS' if ok else 'FAIL'} — trajectory {'captured' if ok else 'missing'}")
    report_usage(result)
    return ok


def check_3_depth() -> bool:
    rule("3. depth_metadata — recursion, and what the child is NOT given")

    logger = RLMLogger()
    rlm = RLM(
        backend="gemini",
        backend_kwargs=vertex_kwargs(TIER2_MODEL),
        environment="local",
        max_depth=2,
        max_iterations=5,
        logger=logger,
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
    print(f"  {'PASS' if ok else 'FAIL'} — recursion {'exercised' if ok else 'never triggered'}")
    if ok:
        print(
            "  note: the child's trajectory flows UP into the parent's metadata.\n"
            "        Nothing flowed DOWN — rlm.py:824 gives the child a fresh empty\n"
            "        logger, rlm.py:836 passes root_prompt=None. That gap is MARD."
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
    print(f"Tier 1: {TIER1_MODEL}   Tier 2: {TIER2_MODEL}   location: {LOCATION}")

    results = {}
    for name, check in (
        ("haystack", check_1_haystack),
        ("trajectory", check_2_trajectory),
        ("depth", check_3_depth),
    ):
        try:
            results[name] = check()
        except Exception as exc:  # noqa: BLE001 — a failed check is the finding
            print(f"  ERROR — {type(exc).__name__}: {exc}")
            results[name] = False

    rule("summary")
    for name, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
