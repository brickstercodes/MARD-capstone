"""Tests for Task B — forward-reference violations, book vs plan order (docs/34 §3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.ordering import (
    SYSTEMS,
    chapter_for_page,
    chapter_plan_positions,
    classify_in_plan_order,
    load_chapters,
    score_all,
    score_run,
)
from eval.runs import RUNS_DIR, select_run
from ingest.groundtruth import CrossReference, extract_cross_references

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"

_CHAPTERS = [
    {"chapter_id": "d.ch01", "number": 1, "page_start": 1, "page_end": 10},
    {"chapter_id": "d.ch02", "number": 2, "page_start": 11, "page_end": 20},
    {"chapter_id": "d.ch03", "number": 3, "page_start": 21, "page_end": 30},
]


def _ref(citing_page: int, referenced_chapter: int, classification: str) -> CrossReference:
    return CrossReference(
        citing_page=citing_page,
        referenced_chapter=referenced_chapter,
        target_page_start=None,
        target_page_end=None,
        classification=classification,
        context="",
    )


def test_chapter_for_page_finds_the_containing_chapter() -> None:
    assert chapter_for_page(_CHAPTERS, 5) == 1
    assert chapter_for_page(_CHAPTERS, 15) == 2
    assert chapter_for_page(_CHAPTERS, 999) is None


def test_classify_in_plan_order_forward_when_citing_chapter_scheduled_earlier() -> None:
    # Chapter 1 cites chapter 3 (its "prerequisite"); the plan puts chapter 1's
    # concepts (position 1) before chapter 3's (position 5) — a violation.
    positions = {1: [1], 3: [5]}
    refs = [_ref(citing_page=5, referenced_chapter=3, classification="forward")]
    result = classify_in_plan_order(refs, _CHAPTERS, positions)
    assert [c.plan_classification for c in result] == ["forward"]


def test_classify_in_plan_order_backward_when_prerequisite_scheduled_earlier() -> None:
    positions = {1: [5], 3: [1]}
    refs = [_ref(citing_page=5, referenced_chapter=3, classification="forward")]
    result = classify_in_plan_order(refs, _CHAPTERS, positions)
    assert [c.plan_classification for c in result] == ["backward"]


def test_classify_in_plan_order_same_chapter_self_reference() -> None:
    positions = {1: [1, 2]}
    refs = [_ref(citing_page=5, referenced_chapter=1, classification="same_chapter")]
    result = classify_in_plan_order(refs, _CHAPTERS, positions)
    assert [c.plan_classification for c in result] == ["same_chapter"]


def test_classify_in_plan_order_unmappable_when_referenced_chapter_has_no_concepts() -> None:
    positions = {1: [1]}  # chapter 3 absent from the plan entirely
    refs = [_ref(citing_page=5, referenced_chapter=3, classification="forward")]
    result = classify_in_plan_order(refs, _CHAPTERS, positions)
    assert [c.plan_classification for c in result] == ["unmappable"]


def test_classify_in_plan_order_unmappable_when_citing_chapter_has_no_concepts() -> None:
    positions = {3: [1]}  # chapter 1 absent from the plan entirely
    refs = [_ref(citing_page=5, referenced_chapter=3, classification="forward")]
    result = classify_in_plan_order(refs, _CHAPTERS, positions)
    assert [c.plan_classification for c in result] == ["unmappable"]


def test_classify_in_plan_order_skips_unresolved_book_order_references() -> None:
    # No target chapter existed in book order either; out of scope for plan order too.
    positions = {1: [1], 3: [2]}
    refs = [_ref(citing_page=5, referenced_chapter=99, classification="unresolved")]
    result = classify_in_plan_order(refs, _CHAPTERS, positions)
    assert result == []


@pytest.mark.skipif(not CORPUS_INTROCS.exists(), reason="corpus/introcs not present")
def test_book_order_reference_count_is_50_with_33_forward() -> None:
    chapters = load_chapters()
    text = (CORPUS_INTROCS / "document.txt").read_text(encoding="utf-8")
    refs = extract_cross_references(text, chapters)
    assert len(refs) == 50
    assert sum(1 for r in refs if r.classification == "forward") == 33


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_mard_full_seed42_covers_all_14_chapters_in_book_order(self) -> None:
        # Attributed by section_id (chapter_for_section), not by page range
        # (chapter_for_page misattributed the majority of concepts near a chapter
        # boundary — see eval.ordering.chapter_for_page's docstring). Corrected:
        # every one of the 14 real chapters has >=1 concept, in strictly
        # increasing chapter-level order — the compiled plan never reorders at
        # chapter granularity in this run, or (see the next test) in any run.
        chapters = load_chapters()
        run_dir = select_run("mard", 42)
        positions = chapter_plan_positions(run_dir, chapters, include_aliases=False)
        chapter_order = sorted(positions, key=lambda ch: min(positions[ch]))
        assert chapter_order == list(range(1, 15))

    def test_mard_full_and_book_order_agree_on_the_mappable_subset(self) -> None:
        # The concrete null result: on the 30 of 50 references both orders can
        # classify, MARD full's plan order produces exactly the same forward count
        # as book order, for every seed.
        chapters = load_chapters()
        text = (CORPUS_INTROCS / "document.txt").read_text(encoding="utf-8")
        refs = extract_cross_references(text, chapters)
        for seed in (11, 23, 42):
            score = score_run(select_run("mard", seed), refs, chapters)
            assert score.plan_order_kept_chapter_only.forward == (
                score.book_order_on_mappable_subset.forward
            )

    def test_no_references_are_unmappable_once_attribution_is_by_section_id(self) -> None:
        # Retraction: an earlier version of this module attributed concepts to
        # chapters by page range and found chapters 10/13 "missing" from the plan
        # in 8 of 9 runs, with 20 of 50 references unmappable as a result. That was
        # a mapping bug (every chapter boundary page is shared with its neighbour;
        # chapter_for_page's first-match resolution silently favoured the earlier
        # chapter), not a Pass 1 extraction gap. Attributed correctly, all 14
        # chapters are covered and nothing is unmappable.
        chapters = load_chapters()
        text = (CORPUS_INTROCS / "document.txt").read_text(encoding="utf-8")
        refs = extract_cross_references(text, chapters)
        for system in SYSTEMS:
            for seed in (11, 23, 42):
                score = score_run(select_run(system, seed), refs, chapters)
                assert score.plan_order_kept_chapter_only.unmappable == 0

    def test_score_all_covers_all_three_ablation_systems_times_three_seeds(self) -> None:
        results = score_all()
        assert len(results) == len(SYSTEMS) * 3
        assert {r.system for r in results} == set(SYSTEMS)
        for system in SYSTEMS:
            seeds = {r.seed for r in results if r.system == system}
            assert seeds == {11, 23, 42}

    def test_alias_data_present_only_for_runs_with_a_concept_id_merge(self) -> None:
        # docs/28 §3 documents one merge (mard seed 23); reading every run's own
        # mard_compile_plan event directly (not assumed from the doc's narrative)
        # shows two more the doc didn't call out: mard_a1 seed 11 and mard_a1f
        # seed 11. plan_order_with_aliases must be non-None for exactly these three
        # and None for the other six.
        chapters = load_chapters()
        text = (CORPUS_INTROCS / "document.txt").read_text(encoding="utf-8")
        refs = extract_cross_references(text, chapters)
        expect_aliases = {("mard", 23), ("mard_a1", 11), ("mard_a1f", 11)}
        for system in SYSTEMS:
            for seed in (11, 23, 42):
                score = score_run(select_run(system, seed), refs, chapters)
                has_aliases = score.plan_order_with_aliases is not None
                assert has_aliases == ((system, seed) in expect_aliases), (system, seed)
