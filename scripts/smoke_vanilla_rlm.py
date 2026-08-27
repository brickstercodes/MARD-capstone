#!/usr/bin/env python
"""T7 smoke test — ~20 pages of `introcs`, one real vanilla-RLM run, verbose.

Deliberately separate from `vanilla.run_vanilla_rlm`, which always reads the full
frozen corpus by design — a real measured run must never be able to silently run on
a slice. This script reuses its pieces (`split_pages`, `FROZEN_STUDY_GUIDE_PROMPT`,
`zhang_rlm_fork_sha`) but drives `rlm.core.rlm.RLM` directly on a truncated page list,
under its own `RunLogger` run (`system="vanilla_rlm_smoke"`), so a smoke run is never
mistaken for a measured one in `runs/`.

Costs real money against `OPENAI_API_KEY` — this is intentionally not something a
session runs on your behalf. Run it yourself:

    export OPENAI_API_KEY="sk-..."
    export MARD_SPEND_CAP_USD=60
    .venv/bin/python scripts/smoke_vanilla_rlm.py

Acceptance (T7 / docs/21 §7): no TOC lines, no mid-sentence titles, no "please paste
the text" responses, output reads as explanations — read the printed trajectory and
answer yourself; nothing here scores it for you.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from rlm.core.rlm import RLM
from rlm.logger.rlm_logger import RLMLogger

from ingest.manifest import verify_or_raise
from provider.rates import build_rate_card
from runlog import RunLogger, SpendCap, SpendLedger
from vanilla.openai_logging_bridge import rate_limit_visibility
from vanilla.run import (
    FROZEN_STUDY_GUIDE_PROMPT,
    VANILLA_MAX_DEPTH,
    split_pages,
    zhang_rlm_fork_sha,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / "corpus"
DOCUMENT_ID = "introcs"
SMOKE_PAGE_COUNT = 20
ROOT_MODEL = "gpt-5.2"
SUB_MODEL = "gpt-5-mini"
MAX_ITERATIONS = 10  # smoke-only cap, well under the real run's default of 30
MAX_CONCURRENT_SUBCALLS = 2


def main() -> int:
    verify_or_raise(CORPUS_DIR / DOCUMENT_ID)
    document_text = (CORPUS_DIR / DOCUMENT_ID / "document.txt").read_text(encoding="utf-8")
    pages = split_pages(document_text)[:SMOKE_PAGE_COUNT]
    print(f"[smoke] {len(pages)} pages, {sum(len(p) for p in pages):,} chars")

    cap = SpendCap.from_env()  # refuses to run if MARD_SPEND_CAP_USD is unset
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    print(f"[smoke] spend cap ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")

    with RunLogger.start(
        runs_root=REPO_ROOT / "runs",
        system="vanilla_rlm_smoke",
        document_id=DOCUMENT_ID,
        seed=0,
        models={"root": ROOT_MODEL, "sub": SUB_MODEL},
        params={
            "max_depth": VANILLA_MAX_DEPTH,
            "max_iterations": MAX_ITERATIONS,
            "page_count": len(pages),
            "smoke": True,
        },
        rate_card=build_rate_card(),
    ) as run:
        run.log_event(
            "vanilla_config",
            {
                "rlm_fork_sha": zhang_rlm_fork_sha(),
                "root_model": ROOT_MODEL,
                "sub_model": SUB_MODEL,
                "max_depth": VANILLA_MAX_DEPTH,
                "max_iterations": MAX_ITERATIONS,
                "page_count": len(pages),
                "smoke": True,
            },
        )

        def on_subcall_start(depth: int, model: str, prompt_preview: str) -> None:
            print(f"[subcall start] depth={depth} model={model} preview={prompt_preview!r}")
            run.log_event(
                "vanilla_subcall_start",
                {"depth": depth, "model": model, "prompt_preview": prompt_preview},
            )

        def on_subcall_complete(depth: int, model: str, duration: float, error: str | None) -> None:
            print(f"[subcall done ] depth={depth} model={model} {duration:.1f}s error={error}")
            run.log_event(
                "vanilla_subcall_complete",
                {"depth": depth, "model": model, "duration_s": duration, "error": error},
            )

        rlm_instance = RLM(
            backend="openai",
            backend_kwargs={"model_name": ROOT_MODEL, "max_retries": 5},
            other_backends=["openai"],
            other_backend_kwargs=[{"model_name": SUB_MODEL, "max_retries": 5}],
            max_depth=VANILLA_MAX_DEPTH,
            max_iterations=MAX_ITERATIONS,
            max_concurrent_subcalls=MAX_CONCURRENT_SUBCALLS,
            on_subcall_start=on_subcall_start,
            on_subcall_complete=on_subcall_complete,
            logger=RLMLogger(),
            verbose=True,
        )
        try:
            with rate_limit_visibility(run):
                response = rlm_instance.completion(
                    prompt=pages, root_prompt=FROZEN_STUDY_GUIDE_PROMPT
                )
        finally:
            rlm_instance.close()

        for model, usage in response.usage_summary.model_usage_summaries.items():
            run.log_call(
                role="root" if model == ROOT_MODEL else "tier2_subcall",
                model=model,
                prompt=f"<smoke aggregate of {usage.total_calls} call(s) to {model}>",
                response=response.response if model == ROOT_MODEL else "<see subcall events>",
                input_tokens=usage.total_input_tokens,
                output_tokens=usage.total_output_tokens,
            )
        run.save_artefact("vanilla_answer.md", response.response)
        run.set_result({"smoke": True})
        totals = run.totals()
        run_id = run.run_id
        run_dir = run.run_dir
        # Let the `with` block's own __exit__ close the run (status="ok") rather than
        # closing it here — close() is idempotent but only __exit__ knows the final
        # status, and SpendLedger.record() needs the written summary.json back as a
        # dict, not the Path close() returns.

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    ledger.record(summary)

    print()
    print(f"[smoke] run_id: {run_id}")
    print(f"[smoke] execution_time_s: {response.execution_time:.1f}")
    print(f"[smoke] tokens in/out: {totals['input_tokens']:,} / {totals['output_tokens']:,}")
    print(f"[smoke] cost: {totals['cost']}")
    print(f"[smoke] answer saved to {run_dir / 'artefacts' / 'vanilla_answer.md'}")
    print()
    print("=" * 72)
    print(response.response)
    print("=" * 72)
    print()
    print("[smoke] Read the answer above. Check: no TOC lines, no mid-sentence")
    print("[smoke] titles, no 'please paste the text' responses, reads as explanations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
