"""Scale the vanilla-RLM control (eval.run_vanilla_rlm) across a full frozen
subset and, eventually, all three campaign seeds.

Single-task runs (eval/run_vanilla_rlm.py) proved the pipeline works end to
end. This script is the next step the W1 DoD actually asks for -- "runs
end-to-end on the fixed subsets" (plural, all of them) -- without spending
real Vertex budget blind:

  - Enforces runlog.SpendCap/SpendLedger before every task, so a batch can
    never silently exceed the ₹75,000 campaign ceiling.
  - Skips a (dataset, index, seed) combination that already has a
    successfully-completed run on disk, so an interrupted campaign resumes
    without re-billing work already paid for.
  - Isolates failures per task -- one bad task (rate limit, a genuinely
    malformed run) does not abort the rest of the batch, matching
    CLAUDE.md's "a hole in the matrix should explain itself" principle
    already built into RunLogger itself.
  - `--dry-run` prints the planned task list and, for BrowseComp-Plus, each
    query's raw size, without spending anything -- review scope before
    committing budget.

Usage:
    python -m eval.run_vanilla_rlm_campaign --dataset oolong --seeds 11
    python -m eval.run_vanilla_rlm_campaign --dataset browsecomp --seeds 11 --limit 5
    python -m eval.run_vanilla_rlm_campaign --dataset both --seeds 11 --dry-run
"""

from __future__ import annotations

import argparse
import json

from eval.backends import active_profile
from eval.run_vanilla_rlm import (
    BROWSECOMP_FILE,
    OOLONG_TASKS_FILE,
    _read_jsonl,
    run_one,
    runs_root,
)
from runlog import SpendCap, SpendLedger, UnsetSpendCapError
from runlog.budget import BudgetExceededError

# Flat, conservative per-task estimates for the pre-spend budget check.
# BrowseComp-Plus queries range ~870KB-8.3MB of embedded document text in
# this frozen file (eval/frozen_subsets.md); the observed OOLONG cost
# (~$0.07/task, 26 calls) showed the model chunks rather than resending the
# full context every call, so actual cost is usually well under these -- the
# estimate only has to be conservative enough that check_before_run() can't
# be fooled into approving a batch that then blows the ceiling.
#
# Both figures were observed on Vertex at gemini-3.6-flash rates and are
# UNVALIDATED on OpenAI. gpt-5.6-terra costs ~33% more per input token and 60%
# more per output token than the Gemini intro rate, and reasoning tokens bill
# as output, so the true OpenAI per-task cost could plausibly exceed the OOLONG
# estimate rather than sit under it. They are left unchanged deliberately --
# guessing a new number would be inventing a measurement. Re-derive them from
# the first real OpenAI runs before trusting a batch, and until then keep
# --phase-budget-usd tight.
ESTIMATED_COST_USD = {"oolong": 0.25, "browsecomp": 2.00}

DATASET_COUNTS = {"oolong": 50, "browsecomp": 20}


def dataset_size_hint(dataset: str, index: int) -> int:
    """Raw character count for one task -- the thing that actually varies
    wildly for BrowseComp-Plus and is worth seeing before spending on it."""
    if dataset == "oolong":
        return len(_read_jsonl(OOLONG_TASKS_FILE)[index]["question"])
    lines = BROWSECOMP_FILE.read_text(encoding="utf-8").splitlines()
    return len(lines[index])


def already_succeeded(dataset: str, index: int, seed: int) -> bool:
    """True if a prior run for this exact (dataset, index, seed) already
    completed with status "ok" -- resume support, so an interrupted
    campaign doesn't re-bill work it already paid for."""
    if dataset == "oolong":
        tasks = _read_jsonl(OOLONG_TASKS_FILE)
        document_id = f"oolong-trec_coarse-{tasks[index]['id']}"
    else:
        tasks = _read_jsonl(BROWSECOMP_FILE)
        document_id = f"browsecomp_plus-{tasks[index]['query_id']}"

    pattern = f"*__vanilla_rlm__{document_id}__s{seed}__*"
    for run_dir in runs_root().glob(pattern):
        summary_path = run_dir / "summary.json"
        if not summary_path.exists():
            continue
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("status") == "ok":
            return True
    return False


def run_campaign(
    dataset: str,
    indices: list[int],
    seeds: list[int],
    dry_run: bool,
    phase_budget_usd: float | None = None,
) -> None:
    try:
        cap = SpendCap.from_env()
    except UnsetSpendCapError as err:
        raise SystemExit(str(err)) from err
    ledger = SpendLedger(runs_root(), cap)

    # A phase budget is a tighter, separate ceiling on top of the campaign-wide
    # SpendCap -- e.g. "$3 for this OOLONG validation pass" out of a $780
    # total that has to cover W1 through W6. Tracked as a delta from spend at
    # the moment this script started, not an absolute ledger figure, so it
    # composes correctly across multiple invocations of this same phase.
    phase_start_spent = ledger.spent

    profile = active_profile()
    plan = [(idx, seed) for seed in seeds for idx in indices]
    print(f"Backend: {profile.name} ({profile.tier1_model})  ledger: {runs_root()}")
    print(f"Planned: {len(plan)} tasks ({dataset}, indices={indices}, seeds={seeds})")
    print(f"Spend so far: ${ledger.spent:.4f} / ${cap.ceiling_usd:.2f}")
    if phase_budget_usd is not None:
        print(f"Phase budget: ${phase_budget_usd:.2f} (starting from ${phase_start_spent:.4f})")

    if dry_run:
        for idx, seed in plan:
            size = dataset_size_hint(dataset, idx)
            skip = already_succeeded(dataset, idx, seed)
            print(
                f"  [{dataset}] index={idx:>3} seed={seed:<3} size_chars={size:>10} "
                f"{'(already done, would skip)' if skip else ''}"
            )
        return

    completed = skipped = failed = 0
    for idx, seed in plan:
        if already_succeeded(dataset, idx, seed):
            print(f"[skip] {dataset} index={idx} seed={seed} -- already completed")
            skipped += 1
            continue

        estimate = ESTIMATED_COST_USD[dataset]
        try:
            ledger.check_before_run(estimate)
        except BudgetExceededError as err:
            print(f"[stop] campaign budget check failed before {dataset} index={idx}: {err}")
            break

        if phase_budget_usd is not None:
            phase_spent = ledger.spent - phase_start_spent
            if phase_spent + estimate > phase_budget_usd:
                print(
                    f"[stop] phase budget would be exceeded: ${phase_spent:.4f} spent this "
                    f"phase + ${estimate:.2f} estimate > ${phase_budget_usd:.2f} cap. "
                    f"Stopping before {dataset} index={idx} seed={seed}."
                )
                break

        print(f"[run]  {dataset} index={idx} seed={seed} ...")
        try:
            run_dir = run_one(dataset, idx, seed)
        except Exception as exc:  # noqa: BLE001 -- isolate one task's failure from the batch
            print(f"[fail] {dataset} index={idx} seed={seed}: {type(exc).__name__}: {exc}")
            failed += 1
            continue

        summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        status = ledger.record(summary)
        completed += 1
        cost = summary["totals"]["cost"]
        score = (summary.get("result") or {}).get("task_score")
        print(
            f"[done] {dataset} index={idx} seed={seed} status={summary['status']} "
            f"cost=${cost} score={score} "
            f"spend={status['spent_usd']:.4f}/{status['ceiling_usd']:.2f} "
            f"({status['fraction_used']:.1%})"
        )
        if status["warn"]:
            print(f"[WARN] spend at {status['fraction_used']:.1%} of the campaign ceiling")

    print(f"\nCompleted: {completed}  Skipped: {skipped}  Failed: {failed}")
    print(f"Final spend: ${ledger.status()['spent_usd']:.4f} / ${cap.ceiling_usd:.2f}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["oolong", "browsecomp", "both"], required=True)
    parser.add_argument(
        "--start-index", type=int, default=0, help="First index in this batch (default: 0)."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run at most N indices starting from --start-index (default: to the end).",
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default="11",
        help="Comma-separated seeds, e.g. '11,23,42'. Default: '11' (single-seed first pass).",
    )
    parser.add_argument(
        "--phase-budget-usd",
        type=float,
        default=None,
        help="Separate, tighter ceiling for this invocation's spend, on top of the campaign cap.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    seeds = [int(s) for s in args.seeds.split(",")]
    datasets = ["oolong", "browsecomp"] if args.dataset == "both" else [args.dataset]

    for dataset in datasets:
        end = (
            min(args.start_index + args.limit, DATASET_COUNTS[dataset])
            if args.limit
            else (DATASET_COUNTS[dataset])
        )
        indices = list(range(args.start_index, end))
        run_campaign(dataset, indices, seeds, args.dry_run, args.phase_budget_usd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
