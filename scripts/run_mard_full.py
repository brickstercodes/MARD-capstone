#!/usr/bin/env python
"""One real, fully-logged MARD run on the complete `introcs` corpus — MARD full,
A1s (skeleton removed), or A1f (findings removed), per Anugrah's priority order
(`docs/00-START_HERE.md`: B1 done; MARD full and the two A1 cuts next — `docs/28`
§6/§7 on why the envelope ablation split into two). Seed is a run identifier, not
a decoding seed — same reasoning as `scripts/run_vanilla_full.py` (`docs/18` §5.4).

Real spend against `OPENAI_API_KEY`, gated by `SpendCap`/`SpendLedger` — refuses to
start if it would breach the cap.

    export OPENAI_API_KEY="sk-..."
    export MARD_SPEND_CAP_USD=120
    .venv/bin/python scripts/run_mard_full.py 11                 # MARD full, seed 11
    .venv/bin/python scripts/run_mard_full.py 11 --ablation a1s  # A1s (skeleton removed)
    .venv/bin/python scripts/run_mard_full.py 11 --ablation a1f  # A1f (findings removed)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mard.run import TIER1_REASONING_EFFORT, TIER2_MAX_TOKENS, TIER2_REASONING_EFFORT, run_mard
from provider.rates import build_rate_card
from runlog import CAMPAIGN_SEEDS, RunLogger, SpendCap, SpendLedger

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / "corpus"
DOCUMENT_ID = "introcs"
TIER1_MODEL = "gpt-5.2"
TIER2_MODEL = "gpt-5-mini"

# Projected ≈$0.94/run (docs/22 §"Corrected cost model"). $5 is a deliberately
# loose per-run ceiling, well under the $120 campaign cap.
ESTIMATED_USD = 5.0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", type=int, choices=CAMPAIGN_SEEDS)
    parser.add_argument("--ablation", choices=["a1s", "a1f"], default=None)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    system = f"mard_{args.ablation}" if args.ablation else "mard"

    cap = SpendCap.from_env()
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    seed_index = CAMPAIGN_SEEDS.index(args.seed)
    print(f"[{system}] seed {args.seed} (runlog.CAMPAIGN_SEEDS index {seed_index})")
    print(f"[{system}] spend cap ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")
    ledger.check_before_run(ESTIMATED_USD)

    with RunLogger.start(
        runs_root=REPO_ROOT / "runs",
        system=system,
        document_id=DOCUMENT_ID,
        seed=args.seed,
        models={"tier1": TIER1_MODEL, "tier2": TIER2_MODEL},
        params={
            "ablation": args.ablation,
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
            ablation=args.ablation,
        )
        run.set_result(
            {
                "compiled": result.compiled,
                "concepts_accepted": result.concepts_accepted,
                "edges_accepted": result.edges_accepted,
                "cross_chapter_edges": result.cross_chapter_edges,
                "never_declared_rejections": result.never_declared_rejections,
            }
        )
        totals = run.totals()
        run_id = run.run_id
        run_dir = run.run_dir
        # Let __exit__ close the run (status="ok") — same reasoning as
        # scripts/run_vanilla_full.py. A genuine failure (e.g. IncompleteArtefactError)
        # propagates instead, and __exit__ records status="failed" with the traceback.

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    ledger.record(summary)

    print()
    print(f"[{system}] run_id: {run_id}")
    print(f"[{system}] tokens in/out: {totals['input_tokens']:,} / {totals['output_tokens']:,}")
    print(f"[{system}] cost: {totals['cost']}")
    print(f"[{system}] compiled: {result.compiled}")
    print(f"[{system}] concepts_accepted: {result.concepts_accepted}")
    print(f"[{system}] edges_accepted: {result.edges_accepted}")
    print(f"[{system}] cross_chapter_edges: {result.cross_chapter_edges}")
    print(f"[{system}] never_declared_rejections: {result.never_declared_rejections}")
    if result.artefact is not None:
        print(f"[{system}] artefact saved to {run_dir / 'artefacts' / 'tier2_output.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
