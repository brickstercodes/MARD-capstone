"""Tests for docs/23-GROUNDTRUTH_SPEC.md's learning-objective and cross-reference
extraction.

Synthetic blocks and chapters, not the real corpus, for the same reason
tests/test_ingest.py gives: a synthetic fixture asserts on a *known* shape, so a
failure is unambiguous between "the code broke" and "the corpus is unusual". The
one exception is `test_extract_learning_objectives_matches_the_real_corpus_shape`,
which spot-checks against `corpus/introcs/` when it happens to be on disk (it is
gitignored, so CI without it must still pass).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ingest.groundtruth import (
    extract_cross_references,
    extract_learning_objectives,
    summarize_violations,
)

CHAPTERS: list[dict[str, Any]] = [
    {"number": None, "page_start": 1, "page_end": 5},
    {"number": 1, "page_start": 6, "page_end": 20},
    {"number": 2, "page_start": 21, "page_end": 40},
    {"number": 3, "page_start": 41, "page_end": 60},
]


def _block(
    block_id: str, page: int, kind: str, text: str, role: str | None = None
) -> dict[str, Any]:
    return {"block_id": block_id, "page": page, "kind": kind, "role": role, "text": text}


def test_extract_learning_objectives_splits_bullets_across_body_blocks():
    blocks = [
        _block("b0", 6, "heading", "1.1 Computer Science"),
        _block(
            "b1",
            6,
            "heading",
            "Learning Objectives By the end of this section, you will be able to:",
            role="learning_objectives",
        ),
        _block("b2", 6, "body", "• Discuss the history of CS • Define computer science"),
        _block("b3", 6, "body", "• Assess what computer science can do"),
        _block("b4", 7, "body", "The field of computer science is the study of computing."),
        _block("b5", 8, "heading", "The Early History of Computing"),
    ]

    objectives = extract_learning_objectives(blocks, "introcs", CHAPTERS)

    assert [o.text for o in objectives] == [
        "Discuss the history of CS",
        "Define computer science",
        "Assess what computer science can do",
    ]
    assert all(o.chapter_number == 1 for o in objectives)
    assert all(o.page == 6 for o in objectives)
    assert objectives[0].objective_id == "introcs.lo000"
    assert objectives[1].source_block_ids == ("b1", "b2", "b3")


def test_extract_learning_objectives_stops_at_the_next_role_marker_not_only_headings():
    blocks = [
        _block("b0", 21, "heading", "Learning Objectives", role="learning_objectives"),
        _block("b1", 21, "body", "• One objective"),
        _block("b2", 21, "body", "Key Terms", role="key_terms"),
        _block("b3", 21, "body", "algorithm: a sequence of steps"),
    ]

    objectives = extract_learning_objectives(blocks, "introcs", CHAPTERS)

    assert [o.text for o in objectives] == ["One objective"]


def test_extract_learning_objectives_handles_back_to_back_markers():
    blocks = [
        _block("a0", 6, "heading", "Learning Objectives", role="learning_objectives"),
        _block("a1", 6, "body", "• First"),
        _block("b0", 21, "heading", "Learning Objectives", role="learning_objectives"),
        _block("b1", 21, "body", "• Second"),
    ]

    objectives = extract_learning_objectives(blocks, "introcs", CHAPTERS)

    assert [o.text for o in objectives] == ["First", "Second"]
    assert objectives[0].chapter_number == 1
    assert objectives[1].chapter_number == 2


def test_extract_learning_objectives_reports_none_when_page_is_unmapped():
    blocks = [
        _block("z0", 999, "heading", "Learning Objectives", role="learning_objectives"),
        _block("z1", 999, "body", "• Orphan objective"),
    ]

    objectives = extract_learning_objectives(blocks, "introcs", CHAPTERS)

    assert objectives[0].chapter_number is None


DOCUMENT_TEXT = "\n".join(
    [
        "[[page:6]]",
        "# 1.1 Computer Science",
        "As we saw in Chapter 2, this recurs.",
        "[[page:21]]",
        "# 2.1 Computational Thinking",
        "This was discussed in Chapter 1 earlier.",
        "See Chapter 3 for more detail.",
        "Chapter 2 continues to apply here.",
        "[[page:41]]",
        "# 3.1 Data Structures",
        "Refer to Chapter 9 for the missing chapter.",
    ]
)


def test_extract_cross_references_classifies_forward_backward_and_same_chapter():
    references = extract_cross_references(DOCUMENT_TEXT, CHAPTERS)
    by_page_and_target = {
        (r.citing_page, r.referenced_chapter): r.classification for r in references
    }

    assert by_page_and_target[(6, 2)] == "forward"  # chapter 2 starts after page 6
    assert by_page_and_target[(21, 1)] == "backward"  # chapter 1 ended before page 21
    assert by_page_and_target[(21, 3)] == "forward"
    assert by_page_and_target[(21, 2)] == "same_chapter"  # page 21 is inside chapter 2's range
    assert by_page_and_target[(41, 9)] == "unresolved"  # no chapter numbered 9


def test_extract_cross_references_ignores_heading_lines():
    text = "[[page:6]]\n# Chapter 9 Should Not Match As A Heading\nbody text\n"
    assert extract_cross_references(text, CHAPTERS) == []


def test_extract_cross_references_ignores_lines_before_any_page_marker():
    text = "See Chapter 1 before any page marker.\n[[page:6]]\nbody\n"
    assert extract_cross_references(text, CHAPTERS) == []


def test_summarize_violations_counts_each_bucket():
    references = extract_cross_references(DOCUMENT_TEXT, CHAPTERS)
    summary = summarize_violations(references)

    assert summary == {
        "total": 5,
        "forward": 2,
        "backward": 1,
        "same_chapter": 1,
        "unresolved": 1,
    }


CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus" / "introcs"


@pytest.mark.skipif(
    not (CORPUS_DIR / "document.jsonl").exists(), reason="corpus/introcs is gitignored"
)
def test_extract_learning_objectives_matches_the_real_corpus_shape():
    blocks = [json.loads(line) for line in (CORPUS_DIR / "document.jsonl").open(encoding="utf-8")]
    chapters = json.loads((CORPUS_DIR / "chapters.json").read_text(encoding="utf-8"))["chapters"]
    marker_count = sum(1 for b in blocks if b.get("role") == "learning_objectives")

    objectives = extract_learning_objectives(blocks, "introcs", chapters)

    # docs/23-GROUNDTRUTH_SPEC.md §2 records 61 learning_objectives marker blocks;
    # each yields 1+ bullets, so the objective count must be at least the marker count.
    assert marker_count == 61
    assert len(objectives) >= marker_count
    assert all(o.text for o in objectives)
    assert len({o.objective_id for o in objectives}) == len(objectives)
    # A real objective is a short bulleted clause. If collection failed to stop at
    # the first unbulleted body block, a full prose paragraph would leak in here.
    assert all(len(o.text) < 200 for o in objectives)
