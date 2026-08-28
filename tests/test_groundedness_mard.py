"""Tests for Task C — groundedness over the MARD arm (docs/34 §4)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval.groundedness_mard import (
    SYSTEMS,
    attribution_correct,
    load_sections_by_id,
    parse_tier2_call,
    score_all,
    score_run,
    text_grounded,
)
from eval.runs import RUNS_DIR, select_run

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"


def _tier2_call(prompt_content: str, input_tokens: int = 100) -> dict[str, object]:
    return {
        "role": "tier2",
        "prompt": json.dumps([{"role": "user", "content": prompt_content}]),
        "input_tokens": input_tokens,
    }


_REAL_SHAPED_PROMPT = (
    "You are writing one section of a study guide for 'introcs'.\n"
    "Concept: Foo\n"
    "Source: section introcs.1-1-computer-science, pages 20-30\n"
    "Position in the study sequence: 1\n\n"
    "Do the thing.\n\n"
    "Write only this section. Do not summarise what comes before or after it."
)


# ---- parse_tier2_call ---------------------------------------------------------------


def test_parse_tier2_call_matches_the_known_template() -> None:
    parsed = parse_tier2_call(_tier2_call(_REAL_SHAPED_PROMPT))
    assert parsed is not None
    assert parsed.matched_known_template is True
    assert parsed.concept_label == "Foo"
    assert parsed.section_id == "introcs.1-1-computer-science"
    assert parsed.page_start == 20
    assert parsed.page_end == 30
    assert parsed.position == 1


def test_parse_tier2_call_flags_deviation_when_shape_differs() -> None:
    weird = "Concept: Foo\nSome extra unexpected field: bar\n\nHere is real prose."
    parsed = parse_tier2_call(_tier2_call(weird))
    assert parsed is not None
    assert parsed.matched_known_template is False
    assert parsed.concept_label == "Foo"


def test_parse_tier2_call_returns_none_when_not_a_tier2_prompt_at_all() -> None:
    parsed = parse_tier2_call(_tier2_call("This has no Concept: line whatsoever."))
    assert parsed is None


# ---- text_grounded / attribution_correct ---------------------------------------------


def test_text_grounded_is_always_false_for_a_matched_template() -> None:
    parsed = parse_tier2_call(_tier2_call(_REAL_SHAPED_PROMPT))
    assert parsed is not None
    assert text_grounded(parsed) is False


def test_attribution_correct_true_when_citation_matches_the_corpus() -> None:
    parsed = parse_tier2_call(_tier2_call(_REAL_SHAPED_PROMPT))
    assert parsed is not None
    sections_by_id = {
        "introcs.1-1-computer-science": {"page_start": 20, "page_end": 30},
    }
    assert attribution_correct(parsed, sections_by_id) is True


def test_attribution_correct_false_when_pages_dont_match() -> None:
    parsed = parse_tier2_call(_tier2_call(_REAL_SHAPED_PROMPT))
    assert parsed is not None
    sections_by_id = {
        "introcs.1-1-computer-science": {"page_start": 20, "page_end": 999},  # wrong end page
    }
    assert attribution_correct(parsed, sections_by_id) is False


def test_attribution_correct_false_when_section_id_unknown() -> None:
    parsed = parse_tier2_call(_tier2_call(_REAL_SHAPED_PROMPT))
    assert parsed is not None
    assert attribution_correct(parsed, {}) is False


def test_attribution_correct_none_when_template_did_not_match() -> None:
    weird = "Concept: Foo\nunexpected shape"
    parsed = parse_tier2_call(_tier2_call(weird))
    assert parsed is not None
    assert attribution_correct(parsed, {}) is None


# ---- score_run against real MARD runs -------------------------------------------------


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_every_run_is_100_percent_ungrounded_by_construction(self) -> None:
        # The central finding: orchestrate.lm_builder.prompt_for never embeds
        # document prose, at any tier, in any of the nine logged runs — confirmed
        # against every real Tier 2 call, not assumed from reading the code alone.
        sections_by_id = load_sections_by_id()
        for system in SYSTEMS:
            for seed in (11, 23, 42):
                report = score_run(select_run(system, seed), sections_by_id)
                assert report.grounded == 0
                assert report.ungrounded == report.total_concepts
                assert report.template_deviations == 0

    def test_every_run_has_zero_attribution_errors(self) -> None:
        sections_by_id = load_sections_by_id()
        for system in SYSTEMS:
            for seed in (11, 23, 42):
                report = score_run(select_run(system, seed), sections_by_id)
                assert report.attribution_incorrect == 0
                assert report.attribution_correct == report.total_concepts

    def test_tier1_is_also_never_text_grounded(self) -> None:
        sections_by_id = load_sections_by_id()
        for system in SYSTEMS:
            for seed in (11, 23, 42):
                report = score_run(select_run(system, seed), sections_by_id)
                assert report.tier1_text_grounded is False

    def test_total_concepts_is_84_or_83_matching_the_compiled_plan(self) -> None:
        # 83 exactly when a same-label-different-id pair or a compiler merge
        # reduced the study sequence by one; never anything else.
        sections_by_id = load_sections_by_id()
        for system in SYSTEMS:
            for seed in (11, 23, 42):
                report = score_run(select_run(system, seed), sections_by_id)
                assert report.total_concepts in (83, 84)

    def test_same_label_different_id_concepts_are_not_double_counted_as_regenerated(
        self,
    ) -> None:
        # mard_a1 seed 42: two distinct concept ids ("abstraction-and-models" and
        # "abstraction-and-modeling") share the label "Abstraction and Modeling".
        # Keying by plan position (not label) must resolve this as two concepts,
        # not one concept regenerated once.
        sections_by_id = load_sections_by_id()
        report = score_run(select_run("mard_a1", 42), sections_by_id)
        assert report.total_concepts == 84
        assert report.regenerated == 0

    def test_score_all_covers_every_ablation_times_three_seeds(self) -> None:
        reports = score_all()
        assert len(reports) == len(SYSTEMS) * 3
        for system in SYSTEMS:
            seeds = {r.seed for r in reports if r.system == system}
            assert seeds == {11, 23, 42}
