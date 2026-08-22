"""One real Vertex call, wrapped in RunLogger, read back and checked.

docs/TRACK3_HANDOFF.md's sign-off checklist asks for exactly this before the
last box on issue #11 closes: "you can wrap one baseline in RunLogger without
contorting your code" and "token accounting matches what your provider
reports for the same call". This script is that evidence, run against a live
Vertex endpoint rather than a mock, so the numbers it prints are real.

Not itself a pytest case: it spends real (tiny) money against the project's
Vertex credits, and CI shouldn't do that on every push. Run it by hand when
re-confirming the harness, same as test_vertex_auth.py.
"""

from __future__ import annotations

import sys
import time

from rlm.clients.gemini import GeminiClient

from eval.rates import TIER1_MODEL, default_rate_card
from runlog import CAMPAIGN_SEEDS, RunLogger, load_run

PROMPT = "Reply with exactly the digit 7 and nothing else."


def main() -> int:
    client = GeminiClient(model_name=TIER1_MODEL, use_vertex=True)

    with RunLogger.start(
        runs_root="runs",
        system="vanilla_rlm",
        document_id="runlog-signoff-smoke-test",
        seed=CAMPAIGN_SEEDS[0],
        models={"root": TIER1_MODEL},
        rate_card=default_rate_card(),
    ) as run:
        started = time.monotonic()
        response = client.completion(PROMPT)
        latency_s = time.monotonic() - started

        provider_usage = client.get_last_usage()
        run.log_call(
            role="root",
            model=TIER1_MODEL,
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
