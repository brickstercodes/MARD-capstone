"""Task A — the O3 quality score: learning-objective coverage, B1 vs MARD (and ablations).

`docs/34` §2. Scores every system's generated study guide against the document-native
learning-objective reference set (`ingest.groundtruth.extract_learning_objectives`,
`docs/23-GROUNDTRUTH_SPEC.md` §3.1), never against another model's output — the
circularity `docs/23` §1 already rejected for concept/prerequisite ground truth applies
equally here.

**The reference set is 243 objectives, not 61.** `docs/23` §2's table counts 61
`learning_objectives` *marker blocks* — one per section that has a "Learning
Objectives" heading — and `docs/34`'s brief carries that "61" forward, but a marker
block is not an objective: each one introduces several `•`-delimited bullets, and
`extract_learning_objectives` returns one `LearningObjective` per bullet. Counted
directly against `corpus/introcs/document.jsonl`: 243. Reported here as the measured
figure, with the discrepancy named rather than silently resolved either way
(`docs/00`'s "mark anything unverifiable, never quietly assert, never quietly drop" —
this is the reverse case, a number that turned out to under-count, but the discipline
is the same).

**Coverage is scored against each system's whole generated document, not per-concept.**
Nothing in the ground truth or the generated artefacts aligns one objective to one
generated section — a study guide's structure is invented by the model (B1) or driven
by an extracted concept graph (MARD), neither of which is required to track the
textbook's own learning-objective boundaries. `eval.groundtruth_scoring.score_overlap`
already recommends recall against a short reference (`docs/23` §4); applying it against
the full candidate document is the same recall test at document granularity, and it is
the only granularity available without inventing an alignment step docs/23 never
specified.

**B1's answer lives at `artefacts/vanilla_answer.md`; every MARD-family system's lives
at `artefacts/tier2_output.md`** — same filename for `mard`, `mard_a1` (A1s), and
`mard_a1f` (A1f), since all three share `orchestrate.builder.join_in_plan_order`'s
output path.
"""

from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eval.groundtruth_scoring import DEFAULT_THRESHOLD, score_overlap
from eval.runs import CAMPAIGN_SEEDS, RunFields, extract_fields, select_run
from ingest.groundtruth import LearningObjective, extract_learning_objectives

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"

# docs/34 §2: DEFAULT_THRESHOLD plus two others, "so the number survives a reviewer
# who disagrees with 0.6" — eval/groundtruth_scoring.py's own module docstring
# demands exactly this.
THRESHOLDS: tuple[float, ...] = tuple(sorted({0.5, DEFAULT_THRESHOLD, 0.7}))

ANSWER_FILENAME: dict[str, str] = {
    "vanilla_rlm": "vanilla_answer.md",
    "mard": "tier2_output.md",
    "mard_a1": "tier2_output.md",
    "mard_a1f": "tier2_output.md",
}

# docs/28's naming: "mard_a1" on disk is "A1s" (skeleton removed) going forward.
SYSTEM_LABEL: dict[str, str] = {
    "vanilla_rlm": "B1 (vanilla RLM)",
    "mard": "MARD full",
    "mard_a1": "A1s (skeleton removed)",
    "mard_a1f": "A1f (findings suppressed)",
}


def load_objectives(corpus_dir: Path = CORPUS_INTROCS) -> list[LearningObjective]:
    blocks = [
        json.loads(line)
        for line in (corpus_dir / "document.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    chapters = json.loads((corpus_dir / "chapters.json").read_text(encoding="utf-8"))["chapters"]
    return extract_learning_objectives(blocks, corpus_dir.name, chapters)


@dataclass(frozen=True)
class ObjectiveCoverage:
    objective_id: str
    reference_tokens: int
    matched_tokens: int
    overlap: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective_id": self.objective_id,
            "reference_tokens": self.reference_tokens,
            "matched_tokens": self.matched_tokens,
            "overlap": self.overlap,
        }


def score_objectives(
    objectives: list[LearningObjective], candidate_text: str
) -> list[ObjectiveCoverage]:
    """Recall of each objective's tokens against the whole candidate document.

    `threshold=0.0` here is a formality — `score_overlap`'s `overlap` field is
    threshold-independent, `covered` is not, and this needs only `overlap` so it can
    be re-bucketed at every threshold in `THRESHOLDS` without re-scoring.
    """
    results = []
    for objective in objectives:
        scored = score_overlap(objective.text, candidate_text, threshold=0.0)
        results.append(
            ObjectiveCoverage(
                objective.objective_id,
                scored.reference_tokens,
                scored.matched_tokens,
                scored.overlap,
            )
        )
    return results


def coverage_at_threshold(scores: list[ObjectiveCoverage], threshold: float) -> dict[str, Any]:
    covered = sum(1 for score in scores if score.overlap >= threshold)
    total = len(scores)
    return {
        "threshold": threshold,
        "covered": covered,
        "total": total,
        "fraction": covered / total if total else 0.0,
    }


@dataclass(frozen=True)
class RunTaskScore:
    fields: RunFields
    objective_scores: list[ObjectiveCoverage]
    coverage: dict[float, dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "fields": self.fields.to_dict(),
            "coverage": {str(t): c for t, c in self.coverage.items()},
            "objective_scores": [s.to_dict() for s in self.objective_scores],
        }


def score_run(
    run_dir: Path,
    objectives: list[LearningObjective],
    thresholds: tuple[float, ...] = THRESHOLDS,
) -> RunTaskScore:
    fields = extract_fields(run_dir)
    answer_filename = ANSWER_FILENAME[fields.system]
    answer_path = run_dir / "artefacts" / answer_filename
    if not answer_path.exists():
        raise FileNotFoundError(
            f"{run_dir}: no {answer_filename} — is {fields.system!r} in ANSWER_FILENAME "
            "and did the run actually produce a joined artefact?"
        )
    text = answer_path.read_text(encoding="utf-8")
    scores = score_objectives(objectives, text)
    coverage = {threshold: coverage_at_threshold(scores, threshold) for threshold in thresholds}
    return RunTaskScore(fields, scores, coverage)


def _mean_min_max(values: list[float]) -> dict[str, float]:
    return {"mean": statistics.fmean(values), "min": min(values), "max": max(values)}


@dataclass(frozen=True)
class ConfigTaskScore:
    """One configuration (system), aggregated over its three campaign-seed runs.

    `docs/30` §4: mean and spread across the three seeds, never a single run
    presented as *the* number.
    """

    system: str
    label: str
    runs: list[RunTaskScore]
    coverage_by_threshold: dict[float, dict[str, float]]
    """threshold -> {"mean", "min", "max"} of the covered *fraction* across seeds."""
    tokens_input: dict[str, float]
    tokens_output: dict[str, float]
    cost_usd: dict[str, float]
    wall_clock_s: dict[str, float]

    def to_dict(self, *, include_objective_detail: bool = True) -> dict[str, Any]:
        def run_dict(run: RunTaskScore) -> dict[str, Any]:
            payload = run.to_dict()
            if not include_objective_detail:
                del payload["objective_scores"]
            return payload

        return {
            "system": self.system,
            "label": self.label,
            "run_ids": [r.fields.run_id for r in self.runs],
            "coverage_by_threshold": {str(t): v for t, v in self.coverage_by_threshold.items()},
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "cost_usd": self.cost_usd,
            "wall_clock_s": self.wall_clock_s,
            # docs/34 §6: "every run, every configuration, all seven docs/30 §1
            # fields plus the quality score, traceable to a run id" — the
            # per-config aggregate above is not that on its own; `runs` is.
            "runs": [run_dict(run) for run in self.runs],
        }


def score_config(
    system: str,
    objectives: list[LearningObjective],
    *,
    seeds: tuple[int, ...] = CAMPAIGN_SEEDS,
    thresholds: tuple[float, ...] = THRESHOLDS,
) -> ConfigTaskScore:
    runs = [score_run(select_run(system, seed), objectives, thresholds) for seed in seeds]

    coverage_by_threshold = {
        threshold: _mean_min_max([run.coverage[threshold]["fraction"] for run in runs])
        for threshold in thresholds
    }
    return ConfigTaskScore(
        system=system,
        label=SYSTEM_LABEL.get(system, system),
        runs=runs,
        coverage_by_threshold=coverage_by_threshold,
        tokens_input=_mean_min_max([run.fields.tokens_input for run in runs]),
        tokens_output=_mean_min_max([run.fields.tokens_output for run in runs]),
        cost_usd=_mean_min_max([run.fields.cost_usd for run in runs]),
        wall_clock_s=_mean_min_max([run.fields.wall_clock_s for run in runs]),
    )


SYSTEMS: tuple[str, ...] = ("vanilla_rlm", "mard", "mard_a1", "mard_a1f")


def score_all(
    systems: tuple[str, ...] = SYSTEMS,
    *,
    seeds: tuple[int, ...] = CAMPAIGN_SEEDS,
    thresholds: tuple[float, ...] = THRESHOLDS,
) -> list[ConfigTaskScore]:
    objectives = load_objectives()
    return [
        score_config(system, objectives, seeds=seeds, thresholds=thresholds) for system in systems
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Task A — O3 quality score (docs/34 §2).")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    configs = score_all()
    payload = [config.to_dict() for config in configs]
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
