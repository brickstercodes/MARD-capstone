"""Tests for Task A — the O3 quality score (docs/34 §2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.runs import RUNS_DIR
from eval.task_score import (
    ANSWER_FILENAME,
    THRESHOLDS,
    ObjectiveCoverage,
    coverage_at_threshold,
    load_objectives,
    score_all,
    score_config,
    score_objectives,
    score_run,
)
from ingest.groundtruth import LearningObjective

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"


def _objective(text: str, oid: str = "t.lo000") -> LearningObjective:
    return LearningObjective(
        objective_id=oid, chapter_number=1, page=1, text=text, source_block_ids=("b1",)
    )


# ---- score_objectives / coverage_at_threshold --------------------------------------


def test_score_objectives_full_recall_when_all_tokens_present() -> None:
    scores = score_objectives(
        [_objective("Define computer science")], "we define computer science here"
    )
    assert scores[0].overlap == 1.0


def test_score_objectives_partial_recall() -> None:
    scores = score_objectives(
        [_objective("Discuss algorithms and data structures")], "this text only mentions algorithms"
    )
    assert 0.0 < scores[0].overlap < 1.0


def test_coverage_at_threshold_counts_correctly() -> None:
    scores = [
        ObjectiveCoverage("a", 3, 3, 1.0),
        ObjectiveCoverage("b", 3, 1, 1 / 3),
        ObjectiveCoverage("c", 3, 2, 2 / 3),
    ]
    result = coverage_at_threshold(scores, 0.6)
    assert result == {"threshold": 0.6, "covered": 2, "total": 3, "fraction": 2 / 3}


def test_coverage_at_threshold_empty_scores_is_zero_not_a_crash() -> None:
    result = coverage_at_threshold([], 0.6)
    assert result["fraction"] == 0.0


def test_thresholds_are_the_three_docs34_asks_for() -> None:
    assert set(THRESHOLDS) == {0.5, 0.6, 0.7}


def test_answer_filename_covers_all_four_systems() -> None:
    assert set(ANSWER_FILENAME) == {"vanilla_rlm", "mard", "mard_a1", "mard_a1f"}
    assert ANSWER_FILENAME["mard"] == ANSWER_FILENAME["mard_a1"] == ANSWER_FILENAME["mard_a1f"]
    assert ANSWER_FILENAME["vanilla_rlm"] != ANSWER_FILENAME["mard"]


# ---- load_objectives -----------------------------------------------------------------


@pytest.mark.skipif(not CORPUS_INTROCS.exists(), reason="corpus/introcs not present")
def test_load_objectives_count_is_243_not_the_61_marker_block_count() -> None:
    # docs/23 §2's table counts 61 learning_objectives *marker blocks*; each one
    # introduces several bulleted objectives. docs/34's brief carries "61 objectives"
    # forward from that table — the measured, correct count is 243. See module
    # docstring for the full account; this test is what makes 243 a checked number
    # rather than a claim.
    objectives = load_objectives()
    assert len(objectives) == 243


# ---- score_run / score_config against real runs --------------------------------------


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_score_config_b1_matches_known_token_and_cost_figures(self) -> None:
        # docs/24 §1's table: seed 42 spent $1.60 at 3.3M input tokens.
        objectives = load_objectives()
        config = score_config("vanilla_rlm", objectives)
        assert config.tokens_input["max"] == pytest.approx(3315432, rel=1e-6)
        assert config.cost_usd["max"] == pytest.approx(1.6001845, rel=1e-6)

    def test_score_config_mard_matches_known_token_and_cost_figures(self) -> None:
        # docs/34 §2 / docs/28 §4: seed 42 spent $0.577 at 94,660 input tokens;
        # seed 11's cost ($0.590) is actually the campaign's max, not seed 42's —
        # so check each seed's own run rather than assuming "max" lines up across
        # both fields for the same run.
        objectives = load_objectives()
        config = score_config("mard", objectives)
        by_seed = {run.fields.seed: run.fields for run in config.runs}
        assert by_seed[42].tokens_input == 94660
        assert by_seed[42].cost_usd == pytest.approx(0.5767145, rel=1e-6)
        assert by_seed[11].cost_usd == pytest.approx(0.590031, rel=1e-6)
        assert config.cost_usd["max"] == pytest.approx(0.590031, rel=1e-6)

    def test_coverage_fraction_is_between_zero_and_one_for_every_config(self) -> None:
        for config in score_all():
            for threshold, stats in config.coverage_by_threshold.items():
                assert 0.0 <= stats["min"] <= stats["mean"] <= stats["max"] <= 1.0, (
                    config.system,
                    threshold,
                )

    def test_run_ids_are_recorded_for_every_config(self) -> None:
        for config in score_all():
            run_ids = [r.fields.run_id for r in config.runs]
            assert len(run_ids) == 3
            assert len(set(run_ids)) == 3  # three distinct seeds, not one repeated

    def test_score_run_reads_the_right_answer_file_per_system(self) -> None:
        from eval.runs import select_run

        b1 = score_run(select_run("vanilla_rlm", 11), [_objective("computer science")])
        mard = score_run(select_run("mard", 11), [_objective("computer science")])
        assert b1.fields.system == "vanilla_rlm"
        assert mard.fields.system == "mard"
