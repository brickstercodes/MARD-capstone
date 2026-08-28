"""Shared run selection and `docs/30` §1 field extraction for the scoring modules.

`docs/34` Tasks A–C all score the same run directories under `runs/`, and six of
`docs/30` §1's seven fields (everything but task score, which is each task's own
axis) are identical extraction logic regardless of which task is asking. Written
once here so Tasks A/B/C cannot silently disagree about what "tokens", "calls
split by tier", or "config snapshot" means for the same run.

**Vanilla and MARD log calls at different granularities, and this module hides
that, not papers over it.** `vanilla/run.py`'s `calls.jsonl` holds two *aggregate*
rows (root, tier2_subcall) — real per-call counts live in `vanilla_root_iteration`
and `vanilla_subcall_detail` events instead (`eval/groundedness.py` already reads
these for the same reason). MARD's `calls.jsonl` is fully granular, one row per
real API call, and its own `totals.calls` in `summary.json` already matches
`len(calls.jsonl)` exactly. `extract_fields` below branches on `system` to read
the right source for each, and a test pins that both paths report the true
per-tier call count, not `summary.json`'s vanilla-side call count of 2.

Cost, input/output tokens, and wall-clock end-to-end time are read from
`summary.json["totals"]`/`["wall_clock_s"]` unchanged in both cases — that
aggregate is what `RunLogger`'s `RateCard` pricing actually depends on
(`vanilla/run.py` `_log_usage`'s docstring), so re-deriving it from a granular
walk here would risk a second, driftable copy of the same number.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runlog.run import load_run

RUNS_DIR = Path(__file__).resolve().parents[1] / "runs"

CAMPAIGN_SEEDS = (11, 23, 42)
"""Matches `runlog.seeds.CAMPAIGN_SEEDS` — duplicated as a plain tuple rather than
imported so this module has no import-time dependency on the provider stack."""


class RunSelectionError(RuntimeError):
    """No completed run exists for a requested system/seed.

    Raised rather than silently returning nothing — a missing seed is a hole in
    the 3-repeat requirement (`docs/30` §4), not an empty result to score around.
    """


def _is_completed(run_dir: Path) -> bool:
    """A run counts only if it finished `status: "ok"`. A crashed or truncated
    attempt (docs/34's pre-fix seed-11 runs, the rate-limited a1f seed-42 attempts)
    is not a result to score — it is exactly the "protocol did not execute" case
    `docs/24` §2 defines as re-runnable, not reportable."""
    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        return False
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return bool(summary.get("status") == "ok")


def select_run(system: str, seed: int, *, document_id: str = "introcs") -> Path:
    """The last completed run directory for this `system`/`seed`.

    "Last" is the run_id's leading timestamp (glob results already sort
    lexicographically in timestamp order), not directory-listing order — this is
    what makes `mard`'s three pre-fix seed-11 attempts and `mard_a1f`'s two
    rate-limited seed-42 attempts resolve to the correct, final run without
    hand-listing run ids here. Callers should still log which run id was
    resolved, per `docs/34` §2's "say in your doc which run ids you used".
    """
    pattern = f"*__{system}__{document_id}__s{seed}__*"
    completed = [path for path in sorted(RUNS_DIR.glob(pattern)) if _is_completed(path)]
    if not completed:
        raise RunSelectionError(
            f"No completed run for system={system!r} seed={seed} document_id={document_id!r} "
            f"under {RUNS_DIR} (pattern {pattern!r})"
        )
    return completed[-1]


def select_campaign(system: str, *, document_id: str = "introcs") -> dict[int, Path]:
    """The last completed run per seed, for all three campaign seeds."""
    return {seed: select_run(system, seed, document_id=document_id) for seed in CAMPAIGN_SEEDS}


@dataclass(frozen=True)
class RunFields:
    """`docs/30` §1's seven fields, minus task score — each scoring task adds its
    own quality axis on top of this."""

    run_id: str
    system: str
    document_id: str
    seed: int
    tokens_input: int
    tokens_output: int
    calls_tier1: int
    calls_tier2: int
    calls_total: int
    cost_usd: float
    wall_clock_s: float
    """End-to-end run time. Fork-join means this is not `Σ(builder latency)` —
    see `builder_wall_clock_max_s`/`builder_wall_clock_sum_s` for that half."""
    builder_wall_clock_max_s: float | None
    builder_wall_clock_sum_s: float | None
    """Both `None` when the run's log doesn't carry per-builder timing at all
    (should not happen for the runs this module targets, but reported as `None`
    rather than 0.0 if it ever does — an absent number is not a zero)."""
    config_snapshot: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system": self.system,
            "document_id": self.document_id,
            "seed": self.seed,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "calls_tier1": self.calls_tier1,
            "calls_tier2": self.calls_tier2,
            "calls_total": self.calls_total,
            "cost_usd": self.cost_usd,
            "wall_clock_s": self.wall_clock_s,
            "builder_wall_clock_max_s": self.builder_wall_clock_max_s,
            "builder_wall_clock_sum_s": self.builder_wall_clock_sum_s,
            "config_snapshot": self.config_snapshot,
        }


def _vanilla_call_counts(events: list[dict[str, Any]]) -> tuple[int, int]:
    tier1 = sum(1 for event in events if event.get("kind") == "vanilla_root_iteration")
    tier2 = sum(1 for event in events if event.get("kind") == "vanilla_subcall_detail")
    return tier1, tier2


def _vanilla_builder_wall_clock(events: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    for event in events:
        if event.get("kind") == "vanilla_run_summary":
            return event.get("subcall_wall_clock_max_s"), event.get("subcall_wall_clock_sum_s")
    return None, None


def _mard_call_counts(calls: list[dict[str, Any]]) -> tuple[int, int]:
    tier1 = sum(1 for call in calls if str(call.get("role", "")).startswith("tier1"))
    tier2 = sum(1 for call in calls if call.get("role") == "tier2")
    return tier1, tier2


def _mard_builder_wall_clock(calls: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    latencies = [
        call["latency_s"]
        for call in calls
        if call.get("role") == "tier2" and isinstance(call.get("latency_s"), int | float)
    ]
    if not latencies:
        return None, None
    return max(latencies), sum(latencies)


def extract_fields(run_dir: Path) -> RunFields:
    """Read `docs/30` §1's seven fields (minus task score) for one run directory."""
    run = load_run(run_dir)
    summary = run["summary"]
    manifest = run["manifest"]
    calls = run["calls"]
    events = run["events"]
    totals = summary["totals"]

    system = summary["system"]
    if system == "vanilla_rlm":
        calls_tier1, calls_tier2 = _vanilla_call_counts(events)
        builder_max, builder_sum = _vanilla_builder_wall_clock(events)
    else:
        calls_tier1, calls_tier2 = _mard_call_counts(calls)
        builder_max, builder_sum = _mard_builder_wall_clock(calls)

    return RunFields(
        run_id=summary["run_id"],
        system=system,
        document_id=summary["document_id"],
        seed=summary["seed"],
        tokens_input=totals["input_tokens"],
        tokens_output=totals["output_tokens"],
        calls_tier1=calls_tier1,
        calls_tier2=calls_tier2,
        calls_total=calls_tier1 + calls_tier2,
        cost_usd=totals["cost"],
        wall_clock_s=summary["wall_clock_s"],
        builder_wall_clock_max_s=builder_max,
        builder_wall_clock_sum_s=builder_sum,
        config_snapshot=manifest["config"],
    )
