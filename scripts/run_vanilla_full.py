#!/usr/bin/env python
"""One real, fully-logged vanilla-RLM run on the complete `introcs` corpus (937
pages) — B1, the O3 headline control (Anugrah's priority order, 28 Aug 2026: B1
vanilla before A1 envelope-stripped, M MARD full, M-flat axler).

Uses `vanilla.run_vanilla_rlm` directly — the production path, not the smoke
script's truncated slice — under `system="vanilla_rlm"` (not `"vanilla_rlm_smoke"`)
so this is unambiguously a measured run in `runs/`. Seed is a run identifier, not a
decoding seed (`docs/18` §5.4, carried over: these hosted models don't expose
deterministic decoding, so the three `runlog.CAMPAIGN_SEEDS` repeats are genuine
repeats, not reproductions).

Real spend against `OPENAI_API_KEY`, gated by `SpendCap`/`SpendLedger` — refuses to
start if it would breach the cap. Run it yourself, the same way as the smoke test.
First repeat (seed 11) already ran — $0.32, see `docs/18` §4.2 addendum. Next:

    export OPENAI_API_KEY="sk-..."   # or a .env file with that line
    export MARD_SPEND_CAP_USD=120
    .venv/bin/python scripts/run_vanilla_full.py 23   # or 42 for the third repeat
"""

from __future__ import annotations

import sys
from pathlib import Path

from provider.rates import build_rate_card
from runlog import CAMPAIGN_SEEDS, RunLogger, SpendCap, SpendLedger
from vanilla.run import VANILLA_MAX_DEPTH, _count_concepts, run_vanilla_rlm

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / "corpus"
DOCUMENT_ID = "introcs"
ROOT_MODEL = "gpt-5.2"
SUB_MODEL = "gpt-5-mini"
MAX_ITERATIONS = 30  # Zhang's own default; the failed replm-era run also hit this
MAX_CONCURRENT_SUBCALLS = 4  # Zhang's own default (docs/18 §4.2 addendum)

# B1 repeat 1 (seed 11) cost $0.32 real — see docs/18 §4.2 addendum. $5 is a
# deliberately loose per-run ceiling for repeats, well under the $120 campaign cap.
ESTIMATED_USD = 5.0


def _seed_from_argv() -> int:
    if len(sys.argv) < 2:
        return CAMPAIGN_SEEDS[0]
    try:
        seed = int(sys.argv[1])
    except ValueError:
        print(f"Seed must be an integer, got {sys.argv[1]!r}", file=sys.stderr)
        raise SystemExit(2) from None
    if seed not in CAMPAIGN_SEEDS:
        print(
            f"{seed} is not one of runlog.CAMPAIGN_SEEDS {CAMPAIGN_SEEDS} — "
            "refusing rather than silently starting an untracked repeat.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return seed


def main() -> int:
    seed = _seed_from_argv()
    cap = SpendCap.from_env()
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    print(f"[full] seed {seed} (runlog.CAMPAIGN_SEEDS index {CAMPAIGN_SEEDS.index(seed)})")
    print(f"[full] spend cap ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")
    ledger.check_before_run(ESTIMATED_USD)  # raises BudgetExceededError, refuses loudly

    with RunLogger.start(
        runs_root=REPO_ROOT / "runs",
        system="vanilla_rlm",
        document_id=DOCUMENT_ID,
        seed=seed,
        models={"root": ROOT_MODEL, "sub": SUB_MODEL},
        params={
            "max_depth": VANILLA_MAX_DEPTH,
            "max_iterations": MAX_ITERATIONS,
            "max_concurrent_subcalls": MAX_CONCURRENT_SUBCALLS,
        },
        rate_card=build_rate_card(),
    ) as run:
        response = run_vanilla_rlm(
            CORPUS_DIR,
            DOCUMENT_ID,
            root_model=ROOT_MODEL,
            sub_model=SUB_MODEL,
            logger=run,
            max_iterations=MAX_ITERATIONS,
            max_concurrent_subcalls=MAX_CONCURRENT_SUBCALLS,
            verbose=True,  # console output only — no effect on the run itself
        )
        totals = run.totals()
        run_id = run.run_id
        run_dir = run.run_dir
        concept_count = _count_concepts(response.response)
        # Let __exit__ close the run (status="ok") rather than closing it here —
        # same reasoning as scripts/smoke_vanilla_rlm.py.

    import json

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    ledger.record(summary)

    print()
    print(f"[full] run_id: {run_id}")
    print(f"[full] execution_time_s: {response.execution_time:.1f}")
    print(f"[full] tokens in/out: {totals['input_tokens']:,} / {totals['output_tokens']:,}")
    print(f"[full] cost: {totals['cost']}")
    print(f"[full] concept_count: {concept_count}")
    print(f"[full] answer saved to {run_dir / 'artefacts' / 'vanilla_answer.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
