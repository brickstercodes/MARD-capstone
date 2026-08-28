"""Tests for Track B — per-chapter learning-objective coverage (docs/37 §3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.chapter_scoring import (
    REAL_CHAPTERS,
    _heading_spans,
    b1_chapter_texts,
    mard_chapter_texts,
    objectives_by_chapter,
    score_all,
    score_run_b1,
    score_run_mard,
)
from eval.ordering import load_chapters
from eval.runs import RUNS_DIR, select_run
from eval.structure import HeadingMatch, load_chapter_descriptors
from eval.task_score import load_objectives
from ingest.groundtruth import LearningObjective

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"


def _objective(chapter: int, text: str) -> LearningObjective:
    return LearningObjective(
        objective_id=f"t.lo.{chapter}",
        chapter_number=chapter,
        page=1,
        text=text,
        source_block_ids=("b",),
    )


# ---- objectives_by_chapter --------------------------------------------------------------


def test_objectives_by_chapter_groups_and_drops_unassigned() -> None:
    objectives = [_objective(1, "a"), _objective(1, "b"), _objective(2, "c")]
    grouped = objectives_by_chapter(objectives)
    assert len(grouped[1]) == 2
    assert len(grouped[2]) == 1
    assert 3 not in grouped


# ---- _heading_spans -----------------------------------------------------------------------


def test_heading_spans_slices_between_consecutive_headings() -> None:
    text = "# Chapter 1\nbody one\n\n# Chapter 2\nbody two\n"
    spans = _heading_spans(text, level=1)
    assert [h for h, _s, _e in spans] == ["Chapter 1", "Chapter 2"]
    first_text = text[spans[0][1] : spans[0][2]]
    assert "body one" in first_text
    assert "body two" not in first_text


def test_heading_spans_last_span_runs_to_end_of_document() -> None:
    text = "# Chapter 1\nonly body\n"
    spans = _heading_spans(text, level=1)
    assert spans[0][2] == len(text)


def test_heading_spans_repeated_heading_text_gets_two_separate_spans() -> None:
    text = "# Chapter 2\nfirst part\n\n# Chapter 3\nother\n\n# Chapter 2\nsecond part\n"
    spans = _heading_spans(text, level=1)
    ch2_spans = [(s, e) for h, s, e in spans if h == "Chapter 2"]
    assert len(ch2_spans) == 2


# ---- b1_chapter_texts ---------------------------------------------------------------------


def test_b1_chapter_texts_concatenates_repeated_headings_into_one_chapter() -> None:
    from eval.structure import B1Structure

    text = "# Chapter 2\nfirst part\n\n# Chapter 2\nsecond part\n"
    structure = B1Structure(
        run_id="r",
        seed=1,
        word_count=10,
        heading_counts={1: 2},
        concept_level=1,
        concept_count=2,
        concept_headings=("Chapter 2", "Chapter 2"),
        chapter_level=1,
        chapter_count=2,
        chapter_headings=("Chapter 2", "Chapter 2"),
    )
    matches = [HeadingMatch("Chapter 2", 2, 1.0, "explicit_number")]

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        (run_dir / "artefacts").mkdir()
        (run_dir / "artefacts" / "vanilla_answer.md").write_text(text, encoding="utf-8")
        result = b1_chapter_texts(run_dir, structure, matches)

    assert "first part" in result[2]
    assert "second part" in result[2]


def test_b1_chapter_texts_empty_when_no_chapter_level() -> None:
    from eval.structure import B1Structure

    structure = B1Structure(
        run_id="r",
        seed=1,
        word_count=1,
        heading_counts={2: 1},
        concept_level=2,
        concept_count=1,
        concept_headings=("only",),
        chapter_level=None,
        chapter_count=0,
        chapter_headings=(),
    )
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        (run_dir / "artefacts").mkdir()
        (run_dir / "artefacts" / "vanilla_answer.md").write_text(
            "## only\nbody\n", encoding="utf-8"
        )
        result = b1_chapter_texts(run_dir, structure, [])
    assert result == {}


# ---- real runs --------------------------------------------------------------------------


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_b1_seed11_maps_all_14_chapters(self) -> None:
        objectives = load_objectives()
        by_chapter = objectives_by_chapter(objectives)
        descriptors = load_chapter_descriptors()
        score = score_run_b1(select_run("vanilla_rlm", 11), objectives, by_chapter, descriptors)
        mappable = [c for c in score.chapters if c.mappable]
        assert len(mappable) == 14

    def test_b1_seed42_leaves_several_chapters_unmappable(self) -> None:
        # docs/37's own assumption was that B1 "cannot be scored at all" for
        # flat-heading runs; seed 42 is the real partial case — some chapters are
        # genuinely unmappable, but not all of them, and not zero.
        objectives = load_objectives()
        by_chapter = objectives_by_chapter(objectives)
        descriptors = load_chapter_descriptors()
        score = score_run_b1(select_run("vanilla_rlm", 42), objectives, by_chapter, descriptors)
        mappable = [c for c in score.chapters if c.mappable]
        assert 0 < len(mappable) < 14

    def test_unmappable_chapters_report_none_fraction_not_zero(self) -> None:
        objectives = load_objectives()
        by_chapter = objectives_by_chapter(objectives)
        descriptors = load_chapter_descriptors()
        score = score_run_b1(select_run("vanilla_rlm", 42), objectives, by_chapter, descriptors)
        unmappable = [c for c in score.chapters if not c.mappable]
        assert unmappable  # seed 42 has at least one
        for chapter in unmappable:
            for stats in chapter.coverage_by_threshold.values():
                assert stats["fraction"] is None

    def test_mard_full_covers_all_14_chapters_in_every_seed(self) -> None:
        # Retraction: an earlier version of this module attributed MARD concepts
        # to chapters via chapter_for_page (page range), under which chapters 10
        # and 13 appeared absent from the compiled plan in nearly every run. That
        # was `eval.ordering.chapter_for_page`'s boundary-overlap bug (every
        # chapter's page_start equals the previous chapter's page_end), not a
        # Pass 1 extraction gap — `docs/35` §2.2's forward-reference finding of
        # the "same" gap was the identical bug, independently. Attributed
        # correctly (by section_id), all 14 chapters are covered in every seed.
        objectives = load_objectives()
        by_chapter = objectives_by_chapter(objectives)
        chapters_ref = load_chapters()
        for seed in (11, 23, 42):
            score = score_run_mard(
                select_run("mard", seed), "mard", objectives, by_chapter, chapters_ref
            )
            mappable_numbers = {c.chapter for c in score.chapters if c.mappable}
            assert mappable_numbers == set(REAL_CHAPTERS)

    def test_mard_chapter_texts_are_attributed_by_verified_citation(self) -> None:
        chapters_ref = load_chapters()
        texts = mard_chapter_texts(select_run("mard", 42), chapters_ref)
        assert set(texts) == set(REAL_CHAPTERS)
        assert len(texts[10]) > 0
        assert len(texts[13]) > 0
        assert 1 in texts and len(texts[1]) > 0

    def test_whole_document_fallback_is_a_separate_field_from_per_chapter_scores(self) -> None:
        # docs/37 §3: "never mix the two in one mean" — structural guarantee that
        # RunChapterScore keeps them in separate fields, never combined by any
        # function in this module.
        objectives = load_objectives()
        by_chapter = objectives_by_chapter(objectives)
        descriptors = load_chapter_descriptors()
        score = score_run_b1(select_run("vanilla_rlm", 23), objectives, by_chapter, descriptors)
        assert hasattr(score, "whole_document_fallback")
        assert hasattr(score, "chapters")

    def test_score_all_covers_every_system_and_seed(self) -> None:
        results = score_all()
        assert len(results) == 4 * 3
        systems = {r.system for r in results}
        assert systems == {"vanilla_rlm", "mard", "mard_a1", "mard_a1f"}
