#!/usr/bin/env python
"""One cheap MARD smoke run: Pass 0 on the full skeleton, Pass 1 restricted to the
first chapter only (`docs/25-HANDOFF_MARD_ARM.md` §T2 — "smoke Tier 1 on ONE
chapter... then read pass1_trace before doing anything else").

This is the check for whether the async/sync fix (`provider/sync_seams.py`) is
actually load-bearing against the real API, not just against a fake client in
tests/test_sync_seams.py: a coroutine-rejection bug would show up here as
`concepts_accepted: 0` and a `"explorer returned coroutine, expected an object"`
rejection, exactly as docs/25 §2 describes.

    export OPENAI_API_KEY="sk-..."
    export MARD_SPEND_CAP_USD=120
    .venv/bin/python scripts/smoke_mard.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from mard.run import TIER1_REASONING_EFFORT, TIER2_MAX_TOKENS, TIER2_REASONING_EFFORT, run_mard
from provider.rates import build_rate_card
from runlog import RunLogger, SpendCap, SpendLedger

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / "corpus"
DOCUMENT_ID = "introcs"
TIER1_MODEL = "gpt-5.2"
TIER2_MODEL = "gpt-5-mini"
MAX_CHAPTERS = 1

# Pass 0 (all sections) + one chapter's Pass 1 call — a small fraction of the
# projected $0.53 full-Tier-1 cost (docs/22). $2 is a deliberately loose ceiling.
ESTIMATED_USD = 2.0


def main() -> int:
    cap = SpendCap.from_env()
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    print(f"[smoke] spend cap ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")
    ledger.check_before_run(ESTIMATED_USD)

    with RunLogger.start(
        runs_root=REPO_ROOT / "runs",
        system="mard_smoke",
        document_id=DOCUMENT_ID,
        seed=0,
        models={"tier1": TIER1_MODEL, "tier2": TIER2_MODEL},
        params={
            "max_chapters": MAX_CHAPTERS,
            "smoke": True,
            "tier1_reasoning_effort": TIER1_REASONING_EFFORT,
            "tier2_reasoning_effort": TIER2_REASONING_EFFORT,
            "tier2_max_tokens": TIER2_MAX_TOKENS,
        },
        rate_card=build_rate_card(),
    ) as run:
        result = run_mard(
            CORPUS_DIR,
            DOCUMENT_ID,
            tier1_model=TIER1_MODEL,
            tier2_model=TIER2_MODEL,
            logger=run,
            max_chapters=MAX_CHAPTERS,
        )
        run.set_result(
            {
                "concepts_accepted": result.concepts_accepted,
                "edges_accepted": result.edges_accepted,
                "compiled": result.compiled,
            }
        )
        totals = run.totals()
        run_id = run.run_id
        run_dir = run.run_dir
        # Let __exit__ close the run (status="ok") — same reasoning as
        # scripts/smoke_vanilla_rlm.py.

    import json

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    ledger.record(summary)

    print()
    print(f"[smoke] run_id: {run_id}")
    print(f"[smoke] tokens in/out: {totals['input_tokens']:,} / {totals['output_tokens']:,}")
    print(f"[smoke] cost: {totals['cost']}")
    print(f"[smoke] concepts_accepted: {result.concepts_accepted}")
    print(f"[smoke] edges_accepted: {result.edges_accepted}")
    for trace in result.pass1_traces:
        rejected = trace["rejected"]
        flag = " <-- FIX NOT WORKING" if any("explorer returned" in r for r in rejected) else ""
        print(
            f"[smoke] chapter {trace['chapter_id']}: envelope "
            f"{trace['envelope']['rendered_chars']} chars, "
            f"{trace['concepts_accepted']} concepts, rejected={rejected}{flag}"
        )
    print(f"[smoke] read the full trace at {run_dir / 'events.jsonl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
