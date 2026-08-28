"""Tests for Track A — structural determinism and fidelity (docs/37 §2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from eval.runs import RUNS_DIR, select_run
from eval.structure import (
    CONTENT_OVERLAP_THRESHOLD,
    HeadingTree,
    chapter_level,
    coefficient_of_variation,
    concept_level,
    count_b1_citations,
    load_chapter_descriptors,
    match_headings_to_chapters,
    parse_b1,
    parse_mard,
    parse_markdown_headings,
)

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"


# ---- heading parsing / level inference ------------------------------------------------


def test_parse_markdown_headings_counts_each_level_separately() -> None:
    text = "# Title\n\n## A\n\n## B\n\n### x\n\n### y\n\n### z\n"
    tree = parse_markdown_headings(text)
    assert tree.by_level[1] == ("Title",)
    assert tree.by_level[2] == ("A", "B")
    assert tree.by_level[3] == ("x", "y", "z")


def test_concept_level_is_the_most_populated_level() -> None:
    tree = HeadingTree({1: ("t",), 2: ("a", "b"), 3: ("x", "y", "z")})
    assert concept_level(tree) == 3


def test_concept_level_none_when_no_headings_at_all() -> None:
    assert concept_level(HeadingTree({})) is None


def test_chapter_level_skips_a_lone_title_heading() -> None:
    # The seed-42 shape: one level-1 title, sixteen level-2 modules, no level-3.
    # Level 2 is the concept level here, so there is no separate chapter level —
    # and critically, the lone level-1 title must NOT be picked as one; a single
    # heading is not a grouping structure.
    tree = HeadingTree({1: ("Study Guide",), 2: tuple(f"Module {i}" for i in range(16))})
    assert concept_level(tree) == 2
    assert chapter_level(tree, concept_lvl=2) is None


def test_chapter_level_picks_the_most_populated_non_concept_level() -> None:
    # The seed-11 shape: 20 level-1 headings, 156 level-2, nothing at level 3.
    tree = HeadingTree(
        {1: tuple(f"Chapter {i}" for i in range(20)), 2: tuple(f"c{i}" for i in range(156))}
    )
    assert concept_level(tree) == 2
    assert chapter_level(tree, concept_lvl=2) == 1


def test_chapter_level_none_when_only_one_level_is_populated() -> None:
    tree = HeadingTree({2: ("a", "b", "c")})
    assert chapter_level(tree, concept_lvl=2) is None


# ---- coefficient_of_variation -----------------------------------------------------------


def test_coefficient_of_variation_zero_for_identical_values() -> None:
    assert coefficient_of_variation([84.0, 84.0, 84.0]) == 0.0


def test_coefficient_of_variation_positive_for_varying_values() -> None:
    cv = coefficient_of_variation([124.0, 128.0, 133.0])
    assert cv is not None
    assert cv > 0.0


def test_coefficient_of_variation_none_for_a_single_value() -> None:
    assert coefficient_of_variation([84.0]) is None


def test_coefficient_of_variation_none_for_a_zero_mean() -> None:
    assert coefficient_of_variation([0.0, 0.0]) is None


# ---- match_headings_to_chapters ----------------------------------------------------------


def test_explicit_chapter_number_is_matched_directly() -> None:
    descriptors = {1: "algorithms and problem solving", 2: "data structures and abstract types"}
    result = match_headings_to_chapters(("Chapter 1", "Chapter 2"), descriptors)
    assert {m.heading: m.chapter for m in result.matches} == {"Chapter 1": 1, "Chapter 2": 2}
    assert all(m.method == "explicit_number" for m in result.matches)
    assert result.invented == []
    assert result.absent_chapters == []


def test_explicit_chapter_number_out_of_range_is_unmatched_not_assumed() -> None:
    descriptors = {1: "algorithms"}
    result = match_headings_to_chapters(("Chapter 99",), descriptors)
    assert result.matches[0].chapter is None
    assert result.matches[0].method == "unmatched"
    assert result.invented == ["Chapter 99"]


def test_content_overlap_matches_a_heading_with_no_explicit_number() -> None:
    descriptors = {1: "operating systems process scheduling memory management"}
    result = match_headings_to_chapters(
        ("Operating Systems Deep Dive",), descriptors, threshold=0.2
    )
    assert result.matches[0].chapter == 1
    assert result.matches[0].method == "content_overlap"


def test_content_overlap_below_threshold_is_invented() -> None:
    descriptors = {1: "operating systems process scheduling"}
    result = match_headings_to_chapters(("Bicycle Repair Techniques",), descriptors, threshold=0.5)
    assert result.matches[0].chapter is None
    assert result.invented == ["Bicycle Repair Techniques"]


def test_greedy_assignment_never_claims_one_chapter_twice() -> None:
    descriptors = {1: "networking protocols internet routing"}
    headings = ("Networking Basics", "Introduction to the Internet")
    result = match_headings_to_chapters(headings, descriptors, threshold=0.1)
    matched_chapters = [m.chapter for m in result.matches if m.chapter is not None]
    assert len(matched_chapters) == len(set(matched_chapters))


def test_absent_chapters_are_those_no_heading_claimed() -> None:
    descriptors = {1: "algorithms", 2: "networking protocols"}
    result = match_headings_to_chapters(("Chapter 1",), descriptors)
    assert result.absent_chapters == [2]


# ---- count_b1_citations -------------------------------------------------------------------


def test_count_b1_citations_finds_page_references() -> None:
    text = "As discussed on page 45 and pp. 100-102, algorithms matter."
    assert count_b1_citations(text, valid_section_ids=set()) == 2


def test_count_b1_citations_finds_resolvable_section_ids() -> None:
    text = "See introcs.1-1-computer-science for background."
    assert count_b1_citations(text, valid_section_ids={"introcs.1-1-computer-science"}) == 1


def test_count_b1_citations_ignores_unresolvable_section_id_lookalikes() -> None:
    text = "See introcs.made-up-section for background."
    assert count_b1_citations(text, valid_section_ids={"introcs.1-1-computer-science"}) == 0


def test_count_b1_citations_zero_for_page_table_prose() -> None:
    # The real false-positive risk: "page table", "page fault" are OS vocabulary,
    # not citations, and must not be counted as such.
    text = "The OS maintains page tables; a page fault triggers a handler."
    assert count_b1_citations(text, valid_section_ids=set()) == 0


# ---- real runs --------------------------------------------------------------------------


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_b1_seed11_is_flat_at_the_concept_level(self) -> None:
        structure = parse_b1(select_run("vanilla_rlm", 11))
        assert structure.concept_level == 2
        assert structure.concept_count == 156
        assert structure.chapter_level == 1
        assert structure.chapter_count == 20

    def test_b1_seed23_has_a_clean_14_chapter_list(self) -> None:
        structure = parse_b1(select_run("vanilla_rlm", 23))
        assert structure.chapter_count == 14
        assert structure.concept_count == 190

    def test_b1_seed42_emits_16_modules_against_14_real_chapters(self) -> None:
        structure = parse_b1(select_run("vanilla_rlm", 42))
        assert structure.chapter_count == 16
        assert structure.concept_count == 75

    def test_b1_word_counts_match_docs36(self) -> None:
        # docs/36 §2's own table — corroborated independently.
        assert parse_b1(select_run("vanilla_rlm", 11)).word_count == 21410
        assert parse_b1(select_run("vanilla_rlm", 23)).word_count == 14552
        assert parse_b1(select_run("vanilla_rlm", 42)).word_count == 17645

    def test_no_b1_run_has_any_resolvable_citation(self) -> None:
        # docs/36 §2 hand-counted "0, 1, 0" — re-derived here and found to be
        # 0, 0, 0. Every "page"/"p." occurrence in all three runs turns out to be
        # OS vocabulary ("page table", "page fault"), not a citation.
        from eval.structure import load_valid_section_ids

        valid_ids = load_valid_section_ids()
        for seed in (11, 23, 42):
            text = (select_run("vanilla_rlm", seed) / "artefacts" / "vanilla_answer.md").read_text(
                encoding="utf-8"
            )
            assert count_b1_citations(text, valid_ids) == 0

    def test_mard_full_concept_count_is_83_or_84_never_uniformly_84(self) -> None:
        # concepts_pre_merge (summary.json's concepts_accepted) IS uniformly 84 —
        # it counts Pass 1 declarations, before compile_plan.py collapses a
        # same-id concept declared in two chapters (docs/28 §3) into one node.
        # `.concepts` (concept_graph's real node count) is the corrected figure,
        # and seed 23 has exactly one merge, giving 83.
        structures = [parse_mard(select_run("mard", seed)) for seed in (11, 23, 42)]
        assert [s.concepts_pre_merge for s in structures] == [84, 84, 84]
        assert [s.concepts for s in structures] == [84, 83, 84]

    def test_mard_edge_count_varies_across_seeds(self) -> None:
        edges = [parse_mard(select_run("mard", seed)).edges for seed in (11, 23, 42)]
        assert edges == [124, 128, 133]
        assert len(set(edges)) == 3  # genuinely different, not coincidentally equal

    def test_mard_prose_has_essentially_no_heading_structure(self) -> None:
        for system in ("mard", "mard_a1"):
            for seed in (11, 23, 42):
                structure = parse_mard(select_run(system, seed))
                assert structure.prose_heading_lines == 0

    def test_b1_seed23_fidelity_maps_all_14_chapters_cleanly(self) -> None:
        descriptors = load_chapter_descriptors()
        structure = parse_b1(select_run("vanilla_rlm", 23))
        result = match_headings_to_chapters(structure.chapter_headings, descriptors)
        matched = {m.chapter for m in result.matches if m.chapter is not None}
        assert matched == set(range(1, 15))
        assert result.invented == []
        assert result.absent_chapters == []

    def test_b1_seed42_fidelity_is_not_a_clean_14_plus_2(self) -> None:
        # The mechanical threshold-based count does NOT resolve to "14 matched, 2
        # invented" the way a naive 16-vs-14 comparison might suggest — several
        # real chapters go unmatched at this threshold too. Pinned so a future
        # change to the matcher or the threshold is a visible, deliberate choice,
        # not a silent drift. See docs/38 for the hand-verified reading.
        descriptors = load_chapter_descriptors()
        structure = parse_b1(select_run("vanilla_rlm", 42))
        result = match_headings_to_chapters(
            structure.chapter_headings, descriptors, threshold=CONTENT_OVERLAP_THRESHOLD
        )
        assert len(result.invented) > 2
        assert len(result.absent_chapters) > 0
