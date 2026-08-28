#!/usr/bin/env python
"""OOLONG harness check — `docs/42` §1: does the vanilla-RLM arm execute the
published benchmark end-to-end and return answers OOLONG's own scorer can parse?

**This is NOT a reproduction of the base paper's 44.0 → 56.0 OOLONG figure.** At the
n this budget affords, accuracy cannot be estimated (`docs/42` budget banner: n=40
already gives a ±16-point interval against a 12-point gap). Never compute an accuracy
figure from this script's output and compare it to 44.0/56.0.

Runs the frozen OOLONG subset's first N tasks, in file order (never sampled —
`eval/frozen_subsets.md`: the subset is immutable and sampling at this n would invite
a choice there is no budget to justify). Scores with the vendored base-paper scorer
(`eval/oolong_scorer.py`), never a reimplementation.

Stop conditions (`docs/42` §1.5), enforced here:
    - Run task 1 alone, print its actual cost.
    - Stop at 6 tasks total, or $2.50 total spent on this job, whichever first.
    - If any single task costs more than $0.80, stop after it.

    export OPENAI_API_KEY="sk-..."   # or a .env file with that line
    export MARD_SPEND_CAP_USD=37
    .venv/bin/python scripts/run_oolong_harness_check.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from eval.oolong_scorer import attempt_answer_parse, synth_score
from provider.rates import build_rate_card
from runlog import RunLogger, SpendCap, SpendLedger
from vanilla.run import VANILLA_MAX_DEPTH, run_vanilla_rlm_oolong_task

REPO_ROOT = Path(__file__).resolve().parents[1]
FROZEN_TASKS_PATH = (
    REPO_ROOT / "eval" / "frozen_subsets" / "oolong_trec_coarse_50_frozen_tasks.jsonl"
)
CONTEXT_WINDOW_PATH = REPO_ROOT / "eval" / "frozen_subsets" / "oolong_context_window_131k.txt"

ROOT_MODEL = "gpt-5.2"
SUB_MODEL = "gpt-5-mini"
MAX_ITERATIONS = 30
MAX_CONCURRENT_SUBCALLS = 4

# This harness check does not claim seed variance (`docs/42` §1.2 asks for a per-task
# table, not a 3-seed repeat) — a single `runlog.CAMPAIGN_SEEDS` value is used purely
# because `RunLogger.start` requires one, not to imply a decoding-seed guarantee these
# hosted models don't offer (same caveat `run_vanilla_full.py` carries).
HARNESS_SEED = 11

MAX_TASKS = 6
JOB_SPEND_CAP_USD = 2.50
SINGLE_TASK_STOP_USD = 0.80
ESTIMATED_USD_PER_TASK = 1.0  # loose per-call ceiling check; the real gate is JOB_SPEND_CAP_USD


def _load_tasks(n: int) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    with FROZEN_TASKS_PATH.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            tasks.append(json.loads(line))
            if len(tasks) >= n:
                break
    return tasks


def _load_context_lines() -> list[str]:
    text = CONTEXT_WINDOW_PATH.read_text(encoding="utf-8")
    return [line for line in text.split("\n") if line.strip()]


def main() -> int:
    tasks = _load_tasks(MAX_TASKS)
    context_lines = _load_context_lines()
    print(
        f"[oolong-harness] loaded {len(tasks)} tasks (file order), "
        f"{len(context_lines)} context lines"
    )

    cap = SpendCap.from_env()
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    print(f"[oolong-harness] spend cap ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")

    job_spent = 0.0
    results = []

    for i, task in enumerate(tasks, start=1):
        ledger.check_before_run(ESTIMATED_USD_PER_TASK)

        run = RunLogger.start(
            runs_root=REPO_ROOT / "runs",
            system="vanilla_rlm_oolong_harness_check",
            document_id=f"oolong_trec_coarse_task_{task['id']}",
            seed=HARNESS_SEED,
            models={"root": ROOT_MODEL, "sub": SUB_MODEL},
            params={
                "max_depth": VANILLA_MAX_DEPTH,
                "max_iterations": MAX_ITERATIONS,
                "max_concurrent_subcalls": MAX_CONCURRENT_SUBCALLS,
                "oolong_task_id": task["id"],
                "oolong_task_type": task["task"],
                "oolong_answer_type": task["answer_type"],
            },
            rate_card=build_rate_card(),
        )
        status = "ran"
        error_str = None
        score = None
        parsed = None
        wall_clock = None
        try:
            with run:
                response = run_vanilla_rlm_oolong_task(
                    context_lines,
                    task,
                    root_model=ROOT_MODEL,
                    sub_model=SUB_MODEL,
                    logger=run,
                    max_iterations=MAX_ITERATIONS,
                    max_concurrent_subcalls=MAX_CONCURRENT_SUBCALLS,
                    verbose=True,
                )
                response_text = response.response
                parsed, confidence = attempt_answer_parse(response_text)
                score = synth_score(task, response_text)
                run.log_event(
                    "oolong_score",
                    {
                        "task_id": task["id"],
                        "parsed_answer": parsed,
                        "parse_confidence": confidence,
                        "synth_score": score,
                        "gold_answer": task["answer"],
                    },
                )
                wall_clock = response.execution_time
        except Exception as err:  # noqa: BLE001 — a failed task is a result (docs/24 §2), not a crash;
            # `RunLogger.__exit__` already recorded status="failed" + traceback before re-raising.
            status = "errored"
            error_str = f"{type(err).__name__}: {err}"

        run_id = run.run_id
        summary = json.loads((run.run_dir / "summary.json").read_text(encoding="utf-8"))
        ledger.record(summary)
        task_cost = summary["totals"]["cost"]
        job_spent += task_cost

        result = {
            "task_id": task["id"],
            "run_id": run_id,
            "status": status,
            "error": error_str,
            "synth_score": score,
            "parsed_answer": parsed,
            "gold_answer": task["answer"],
            "tokens_in": summary["totals"]["input_tokens"],
            "tokens_out": summary["totals"]["output_tokens"],
            "cost_usd": task_cost,
            "wall_clock_s": wall_clock,
        }
        results.append(result)

        print()
        print(f"[oolong-harness] task {i}/{len(tasks)} id={task['id']} status={status}")
        print(f"[oolong-harness]   run_id: {run_id}")
        print(f"[oolong-harness]   cost: {task_cost:.6f}  (job total so far: {job_spent:.6f})")
        if status == "ran":
            print(
                f"[oolong-harness]   synth_score: {score}  parsed: {parsed!r}  "
                f"gold: {task['answer']}"
            )
        else:
            print(f"[oolong-harness]   error: {error_str}")

        if i == 1:
            print(
                f"[oolong-harness] first-task cost ${task_cost:.4f} — "
                "continuing per docs/42 stop rules"
            )

        if task_cost > SINGLE_TASK_STOP_USD:
            print(
                f"[oolong-harness] STOP: task cost ${task_cost:.4f} exceeds "
                f"${SINGLE_TASK_STOP_USD:.2f} single-task threshold"
            )
            break
        if job_spent >= JOB_SPEND_CAP_USD:
            print(
                f"[oolong-harness] STOP: job spend ${job_spent:.4f} reached "
                f"${JOB_SPEND_CAP_USD:.2f} cap"
            )
            break

    print()
    print(
        f"[oolong-harness] {len(results)} of {len(tasks)} loaded tasks executed, "
        f"job spend ${job_spent:.6f}"
    )
    results_path = REPO_ROOT / "runs" / "_oolong_harness_check_results.json"
    results_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[oolong-harness] per-task results written to {results_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
