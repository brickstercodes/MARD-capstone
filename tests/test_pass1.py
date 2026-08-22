"""Tests for chapter grouping and Pass 1.

The test that matters most here is `test_a_later_chapters_prompt_contains_an_earlier
_chapters_findings`. Accumulation across calls is the mechanism the whole claim rests
on (`docs/00-CLAIM.md`); without it Pass 1 is N independent calls, which is vanilla
RLM with extra steps, and every O3 number would be measuring nothing.

The rest are the rejection paths. Pass 1 refuses to repair a model's output, so each
refusal needs a test proving the bad value is dropped *and* named in the trace —
silently dropping it would be the same failure with better manners.
"""

from __future__ import annotations

from typing import Any

from envelope.envelope import Envelope
from envelope.pass1 import (
    CONCEPT_ID,
    MAX_CONCEPT_ID_CHARS,
    MAX_CONCEPTS_PER_CHAPTER,
    build_prompt,
    run_pass1,
)
from envelope.skeleton import Skeleton
from ingest.blocks import Block
from ingest.chapters import Chapter, content_chapters, group_into_chapters
from ingest.sections import Section, build_sections


def _section(index: int, title: str, page: int) -> Section:
    return Section(
        section_id=f"doc.s{index}",
        title=title,
        book_position=index,
        page_start=page,
        page_end=page + 4,
        char_count=5000,
        block_ids=(f"doc:p{page:04d}:b000",),
    )


def _three_chapters() -> tuple[list[Section], list[Chapter]]:
    sections = [
        _section(0, "1.1 Processes", 10),
        _section(1, "1.2 Process API", 20),
        _section(2, "2.1 Scheduling", 30),
        _section(3, "3.1 Address Spaces", 40),
    ]
    return sections, group_into_chapters(sections, "doc")


def _envelope(sections: list[Section]) -> Envelope:
    return Envelope.from_skeleton(Skeleton.from_sections("doc", sections))


def _titles(sections: list[Section]) -> dict[str, str]:
    return {section.section_id: section.title for section in sections}


class Recorder:
    """Captures every prompt it is given, and returns a scripted reply per chapter."""

    def __init__(self, replies: dict[str, dict[str, Any]]) -> None:
        self.replies = replies
        self.prompts: dict[str, str] = {}

    def explore(self, prompt: str, chapter) -> dict[str, Any]:
        self.prompts[chapter.chapter_id] = prompt
        return self.replies.get(chapter.chapter_id, {"concepts": [], "prerequisites": []})


def _reply(section_id: str, concept_id: str, prerequisites=()) -> dict[str, Any]:
    return {
        "concepts": [
            {
                "id": concept_id,
                "label": concept_id.replace("-", " ").title(),
                "section_id": section_id,
                "directive": f"Explain {concept_id} and how it is used.",
            }
        ],
        "prerequisites": [
            {
                "prerequisite": prerequisite,
                "dependent": concept_id,
                "evidence": "inferred",
                "quote": None,
            }
            for prerequisite in prerequisites
        ],
    }


# --- chapter grouping -------------------------------------------------------------


def test_sections_group_into_chapters_by_their_own_numbering():
    _sections, chapters = _three_chapters()
    assert [chapter.number for chapter in chapters] == [1, 2, 3]
    assert chapters[0].section_ids == ("doc.s0", "doc.s1")
    assert chapters[0].page_start == 10
    assert chapters[0].page_end == 24


def test_unnumbered_sections_attach_to_the_chapter_in_progress():
    sections = [
        _section(0, "1.1 Processes", 10),
        _section(1, "Key Terms", 20),
        _section(2, "2.1 Scheduling", 30),
    ]
    chapters = group_into_chapters(sections, "doc")
    assert len(chapters) == 2
    assert chapters[0].section_ids == ("doc.s0", "doc.s1")


def test_a_repeated_chapter_number_far_later_is_not_merged_backwards():
    """Regression guard: merging non-consecutive runs would span half the book."""
    sections = [
        _section(0, "1.1 Processes", 10),
        _section(1, "2.1 Scheduling", 20),
        _section(2, "1.1 Appendix Restart", 400),
    ]
    chapters = group_into_chapters(sections, "doc")
    assert len(chapters) == 3
    assert chapters[2].page_start == 400


def test_axler_style_letter_numbering_is_recognised():
    sections = [_section(0, "1A Rn and Cn", 10), _section(1, "1B Definition", 20)]
    chapters = group_into_chapters(sections, "doc")
    assert len(chapters) == 1
    assert chapters[0].number == 1


def test_a_second_run_of_the_same_numbers_is_marked_as_a_repeat():
    """University Physics prints its Answer Key as a bare second "Chapter 1..17".

    Found on the real document: 34 chapters where the book has 17, the extra run
    sitting on pp.895-959 with a tenth of the density. Left unmarked it would double
    Pass 1's call volume on answers rather than exposition.
    """
    sections = [
        _section(0, "1.1 Real Content", 10),
        _section(1, "2.1 More Real Content", 30),
        _section(2, "Chapter 1", 900),
        _section(3, "Chapter 2", 910),
    ]
    chapters = group_into_chapters(sections, "doc")

    assert [chapter.is_repeat for chapter in chapters] == [False, False, True, True]
    explored = content_chapters(chapters)
    assert [chapter.page_start for chapter in explored] == [10, 30]


def test_content_chapters_also_excludes_the_unnumbered_leading_run():
    sections = [_section(0, "Chapter Outline", 1), _section(1, "1.1 Real", 10)]
    chapters = group_into_chapters(sections, "doc")
    assert len(chapters) == 2
    assert [chapter.number for chapter in content_chapters(chapters)] == [1]


def test_a_chapter_that_cannot_be_numbered_says_so_rather_than_guessing():
    sections = [_section(0, "Preface", 1), _section(1, "Acknowledgements", 3)]
    chapters = group_into_chapters(sections, "doc")
    assert chapters[0].number is None
    assert "unnumbered" in chapters[0].chapter_id


def test_chapters_come_from_real_blocks_end_to_end():
    blocks = [
        Block(
            block_id=f"doc:p{page:04d}:h",
            page=page,
            kind="heading",
            level=1,
            role=None,
            text=title,
            bbox=(72.0, 100.0, 400.0, 120.0),
            font_size=15.6,
        )
        for page, title in ((5, "1.1 First"), (15, "1.2 Second"), (25, "2.1 Third"))
    ]
    blocks += [
        Block(
            block_id=f"doc:p{page:04d}:b",
            page=page,
            kind="body",
            level=None,
            role=None,
            text="prose " * 100,
            bbox=(72.0, 200.0, 400.0, 600.0),
            font_size=9.0,
        )
        for page in range(5, 30)
    ]
    sections = build_sections(
        sorted(blocks, key=lambda b: (b.page, b.kind != "heading")), "doc", level=1
    )
    chapters = group_into_chapters(sections, "doc")
    assert [chapter.number for chapter in chapters] == [1, 2]


# --- the mechanism ----------------------------------------------------------------


def test_a_later_chapters_prompt_contains_an_earlier_chapters_findings():
    """Accumulation across calls. If this fails, Pass 1 is N independent calls.

    Chapter 1 finds `processes`; chapter 3's prompt must show it. That is the
    downward, operative flow docs/01-ENVELOPE_VS_BASE_LIBRARY.md distinguishes MARD by.
    """
    sections, chapters = _three_chapters()
    recorder = Recorder({"doc.ch01": _reply("doc.s0", "processes")})

    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    third = recorder.prompts["doc.ch03"]
    assert "FINDINGS SO FAR" in third
    assert "processes" in third
    assert len(result.envelope.findings) == 3


def test_the_first_chapters_prompt_has_the_map_but_no_findings_yet():
    sections, chapters = _three_chapters()
    recorder = Recorder({})
    run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    first = recorder.prompts["doc.ch01"]
    assert "STRUCTURAL MAP" in first
    assert "FINDINGS SO FAR" not in first
    assert "YOUR DIRECTIVE" in first


def test_a_prerequisite_may_point_at_a_concept_from_an_earlier_chapter():
    sections, chapters = _three_chapters()
    recorder = Recorder(
        {
            "doc.ch01": _reply("doc.s0", "processes"),
            "doc.ch02": _reply("doc.s2", "scheduling", prerequisites=("processes",)),
        }
    )
    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    assert [(e.prerequisite, e.dependent) for e in result.edges] == [("processes", "scheduling")]


def test_the_section_ids_offered_are_only_this_chapters():
    sections, chapters = _three_chapters()
    prompt = build_prompt(_envelope(sections), chapters[0], _titles(sections))
    assert "doc.s0" in prompt and "doc.s1" in prompt
    assert "doc.s2" not in prompt


# --- rejection paths --------------------------------------------------------------


def test_a_concept_claiming_another_chapters_section_is_dropped_and_named():
    sections, chapters = _three_chapters()
    recorder = Recorder({"doc.ch01": _reply("doc.s3", "address-spaces")})

    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    assert result.concepts == []
    assert any("not in this chapter" in reason for reason in result.traces[0]["rejected"])


def test_a_malformed_concept_id_is_dropped_and_named():
    sections, chapters = _three_chapters()
    recorder = Recorder({"doc.ch01": _reply("doc.s0", "Not A Valid Id")})

    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    assert result.concepts == []
    assert any("contract pattern" in reason for reason in result.traces[0]["rejected"])


def test_a_cross_reference_without_a_quote_is_dropped_not_demoted_to_inferred():
    """Demoting it would launder an unsupported claim into a plausible one."""
    sections, chapters = _three_chapters()
    reply = _reply("doc.s0", "processes")
    reply["concepts"].append(
        {
            "id": "process-api",
            "label": "Process API",
            "section_id": "doc.s1",
            "directive": "Explain fork, exec and wait in detail.",
        }
    )
    reply["prerequisites"] = [
        {
            "prerequisite": "processes",
            "dependent": "process-api",
            "evidence": "cross_reference",
            "quote": None,
        }
    ]
    recorder = Recorder({"doc.ch01": reply})

    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    assert result.edges == []
    assert any("no quote" in reason for reason in result.traces[0]["rejected"])


def test_a_short_directive_is_dropped_because_the_boundary_would_reject_it():
    sections, chapters = _three_chapters()
    reply = _reply("doc.s0", "processes")
    reply["concepts"][0]["directive"] = "Explain."
    recorder = Recorder({"doc.ch01": reply})

    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    assert result.concepts == []
    assert any("characters" in reason for reason in result.traces[0]["rejected"])


def test_more_concepts_than_the_cap_are_truncated_and_the_truncation_is_recorded():
    sections, chapters = _three_chapters()
    reply = {
        "concepts": [
            {
                "id": f"concept-{n}",
                "label": f"Concept {n}",
                "section_id": "doc.s0",
                "directive": "Explain this concept thoroughly.",
            }
            for n in range(MAX_CONCEPTS_PER_CHAPTER + 3)
        ],
        "prerequisites": [],
    }
    recorder = Recorder({"doc.ch01": reply})

    result = run_pass1(_envelope(sections), chapters, _titles(sections), recorder)

    assert len(result.concepts) == MAX_CONCEPTS_PER_CHAPTER
    assert any("kept" in reason for reason in result.traces[0]["rejected"])


def test_an_explorer_that_raises_costs_one_chapter_not_the_run():
    sections, chapters = _three_chapters()

    class Exploding:
        def __init__(self) -> None:
            self.calls = 0

        def explore(self, prompt, chapter):
            self.calls += 1
            if chapter.chapter_id == "doc.ch02":
                raise RuntimeError("safety block")
            return _reply(chapter.section_ids[0], f"c{chapter.number}")

    explorer = Exploding()
    result = run_pass1(_envelope(sections), chapters, _titles(sections), explorer)

    assert explorer.calls == 3
    assert len(result.concepts) == 2
    failed = [trace for trace in result.traces if "error" in trace]
    assert len(failed) == 1
    assert "safety block" in failed[0]["error"]


def test_no_explorer_produces_an_empty_exploration_rather_than_a_crash():
    sections, chapters = _three_chapters()
    result = run_pass1(_envelope(sections), chapters, _titles(sections))
    assert result.concepts == []
    assert len(result.traces) == 3


def test_concept_id_pattern_matches_the_contract():
    """`CONCEPT_ID` restates `plan.models.ConceptId`; this is the guard against drift.

    Restated rather than imported because `plan/` arrives with PR #48 and this module
    has to run before it lands. Replace both sides with an import from `plan.models`
    once it does — a duplicated pattern is a liability, and this test only detects the
    drift, it cannot prevent it.
    """
    contract_pattern = r"^[a-z0-9][a-z0-9._-]*$"
    assert CONCEPT_ID.pattern == contract_pattern
    assert MAX_CONCEPT_ID_CHARS == 80

    for good in ("processes", "process-api", "a1", "limited.direct_execution"):
        assert CONCEPT_ID.match(good), good
    for bad in ("Processes", "-leading", "has space", "_leading"):
        assert not CONCEPT_ID.match(bad), bad


def test_the_full_w1_pipeline_produces_a_plan_the_boundary_accepts(tmp_path):
    """Pass 0, Pass 1 and the compiler end to end, over blocks rather than fixtures."""
    from envelope.compile_plan import compile_master_plan
    from envelope.pass0 import run_pass0

    sections, chapters = _three_chapters()
    skeleton, pass0_trace = run_pass0("doc", sections)
    assert not skeleton.is_empty
    assert pass0_trace["degenerate"] is False

    recorder = Recorder(
        {
            "doc.ch01": _reply("doc.s0", "processes"),
            "doc.ch02": _reply("doc.s2", "scheduling", prerequisites=("processes",)),
            "doc.ch03": _reply("doc.s3", "address-spaces", prerequisites=("processes",)),
        }
    )
    pass1 = run_pass1(Envelope.from_skeleton(skeleton), chapters, _titles(sections), recorder)
    compiled = compile_master_plan("doc", pass1.concepts, pass1.edges, sections)

    from tests.test_compile_plan import _assert_boundary_rules

    _assert_boundary_rules(compiled.plan)
    assert compiled.trace["plan_order"] == ["processes", "scheduling", "address-spaces"]
    assert compiled.trace["moves"] == 0  # book order already satisfies both edges
