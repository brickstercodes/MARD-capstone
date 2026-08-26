"""One real provider call, wrapped in RunLogger, read back and checked.

docs/TRACK3_HANDOFF.md's sign-off checklist asks for exactly this before the
last box on issue #11 closes: "you can wrap one baseline in RunLogger without
contorting your code" and "token accounting matches what your provider
reports for the same call". This script is that evidence, run against a live
endpoint rather than a mock, so the numbers it prints are real.

**Re-run this after any backend change.** The check it performs -- that
runlog's logged token counts equal what the provider itself reported for the
same call -- is a claim about one provider's usage reporting, not a property
of runlog. It was signed off on Vertex on 22 Aug; OpenAI reports usage through
a different field on a different response shape (`usage.prompt_tokens` /
`usage.completion_tokens` via OpenAIClient._track_cost), so the sign-off does
not carry over and has to be earned again. Costs about a cent.

One known gap it does NOT cover: OpenAI bills reasoning tokens as output, and
`usage.completion_tokens` is expected to include them, but whether that holds
for the gpt-5.6 family is unconfirmed -- if it does not, every output-token
cost this project reports on OpenAI would be understated. Flagged as
verification debt in docs/17; compare this script's figure against the OpenAI
dashboard for the same call to close it.

Not itself a pytest case: it spends real (tiny) money, and CI shouldn't do
that on every push. Run it by hand when re-confirming the harness.
"""

from __future__ import annotations

import sys
import time

from eval.backends import active_profile
from eval.rates import rate_card_for
from eval.run_vanilla_rlm import runs_root
from runlog import CAMPAIGN_SEEDS, RunLogger, load_run

PROMPT = "Reply with exactly the digit 7 and nothing else."


def main() -> int:
    profile = active_profile()
    model = profile.tier1_model
    client = profile.client_class()(**profile.backend_kwargs())

    print(f"backend: {profile.name}  model: {model}  runs_root: {runs_root()}")

    with RunLogger.start(
        runs_root=str(runs_root()),
        system="vanilla_rlm",
        document_id="runlog-signoff-smoke-test",
        seed=CAMPAIGN_SEEDS[0],
        models={"root": model},
        rate_card=rate_card_for(profile.name),
    ) as run:
        started = time.monotonic()
        response = client.completion(PROMPT)
        latency_s = time.monotonic() - started

        provider_usage = client.get_last_usage()
        run.log_call(
            role="root",
            model=model,
            prompt=PROMPT,
            response=response,
            input_tokens=provider_usage.total_input_tokens,
            output_tokens=provider_usage.total_output_tokens,
            depth=0,
            latency_s=latency_s,
        )
        run.set_result({"note": "runlog sign-off smoke test, not a scored task"})
        run_dir = run.run_dir

    # Read back exactly what docs/TRACK3_HANDOFF.md's per-number audit would:
    # everything a reader needs, from the logged run alone, no side channel.
    record = load_run(run_dir)
    logged_call = record["calls"][0]
    totals = record["summary"]["totals"]

    print(f"run_dir: {run_dir}")
    print(
        f"provider reported : {provider_usage.total_input_tokens} in / "
        f"{provider_usage.total_output_tokens} out"
    )
    print(
        f"runlog logged      : {logged_call['input_tokens']} in / "
        f"{logged_call['output_tokens']} out"
    )
    print(f"runlog totals      : {totals['input_tokens']} in / {totals['output_tokens']} out")
    print(f"cost (USD)         : {totals['cost']}")
    print(f"unpriced_models    : {totals['unpriced_models']}")

    match = (
        logged_call["input_tokens"] == provider_usage.total_input_tokens
        and logged_call["output_tokens"] == provider_usage.total_output_tokens
    )
    print("MATCH" if match else "MISMATCH -- runlog does not agree with the provider")
    return 0 if match else 1


if __name__ == "__main__":
    sys.exit(main())
