"""Tests for the envelope-to-Master-Plan compilation.

These assert the rules `plan/validation.py` enforces, restated locally rather than
imported. That is deliberate and temporary: `plan/` arrives with PR #48, and a test
that skipped until then would be the `importorskip` pattern that hid the broken RLM
seam for sixteen days (TRACK2.md). `test_the_compiled_plan_satisfies_the_boundarys
_rules` is the one to replace with a real `validate_master_plan` call the day #48
lands.

The rule worth its own test is the reorder note's two different numbers. The boundary
detects a move by comparing *ranks* but validates the note against the concept's
*absolute* `book_position`. A note carrying the rank passes the move check and fails
the agreement check, and because the rejection message is Tier 1's repair prompt, that
is an infinite loop rather than an error.
"""

from __future__ import annotations

from typing import Any

import pytest

from envelope.compile_plan import UnsequenceablePlanError, compile_master_plan
from envelope.pass1 import ExtractedConcept, ExtractedEdge
from ingest.sections import Section

MIN_DIRECTIVE_CHARS = 12
PLACEHOLDERS = {
    "-",
    "...",
    "fixme",
    "n/a",
    "na",
    "none",
    "placeholder",
    "tba",
    "tbd",
    "todo",
    "xxx",
}


def _section(book_position: int, page: int) -> Section:
    return Section(
        section_id=f"doc.s{book_position}",
        title=f"Section {book_position}",
        book_position=book_position,
        page_start=page,
        page_end=page + 4,
        char_count=5000,
        block_ids=(f"doc:p{page:04d}:b000",),
    )


def _concept(concept_id: str, section: Section) -> ExtractedConcept:
    return ExtractedConcept(
        concept_id=concept_id,
        label=concept_id.replace("-", " ").title(),
        section_id=section.section_id,
        directive=f"Explain {concept_id} and how a learner should use it.",
        chapter_id="doc.ch01",
    )


def _edge(prerequisite: str, dependent: str, evidence: str = "inferred", quote=None):
    return ExtractedEdge(
        prerequisite=prerequisite,
        dependent=dependent,
        evidence=evidence,
        quote=quote,
        chapter_id="doc.ch01",
    )


def _sparse_sections() -> list[Section]:
    """Non-consecutive book positions, which is what a real parse produces."""
    return [_section(0, 10), _section(3, 40), _section(7, 80), _section(12, 130)]


def _assert_boundary_rules(plan: dict[str, Any]) -> None:
    """The cross-collection rules plan/validation.py enforces. Replace with the real one."""
    concepts = plan["concept_graph"]["concepts"]
    edges = plan["concept_graph"]["edges"]
    sequence = plan["study_sequence"]
    rationale = plan["reordering_rationale"]

    ids = [concept["id"] for concept in concepts]
    assert len(ids) == len(set(ids)), "duplicate concept ids"

    for edge in edges:
        assert edge["prerequisite"] in ids and edge["dependent"] in ids
        assert edge["prerequisite"] != edge["dependent"]
        if edge["evidence"] == "cross_reference":
            assert edge["quote"] and edge["located_at"], "unsupported cross-reference"
    pairs = [(edge["prerequisite"], edge["dependent"]) for edge in edges]
    assert len(pairs) == len(set(pairs)), "duplicate edges"

    positions = sorted(step["position"] for step in sequence)
    assert positions == list(range(1, len(sequence) + 1)), "positions are not 1..n"
    sequenced = [step["concept_id"] for step in sequence]
    assert sorted(sequenced) == sorted(ids), "sequence is not a permutation of the graph"

    for step in sequence:
        directive = step["directive"].strip()
        assert len(directive) >= MIN_DIRECTIVE_CHARS
        assert directive.lower().strip(".!?-_ ") not in PLACEHOLDERS

    order = {step["concept_id"]: step["position"] for step in sequence}
    for edge in edges:
        assert order[edge["prerequisite"]] < order[edge["dependent"]], "ordering violation"

    by_id = {concept["id"]: concept for concept in concepts}
    book_rank = {
        concept["id"]: rank
        for rank, concept in enumerate(
            sorted(concepts, key=lambda c: (c["source"]["book_position"], c["id"]))
        )
    }
    explained = {note["concept_id"] for note in rationale}
    assert len(explained) == len(rationale), "duplicate rationale"

    for concept_id, position in order.items():
        moved = book_rank[concept_id] != position - 1
        assert moved == (concept_id in explained), f"note/move mismatch for {concept_id}"

    for note in rationale:
        assert note["to_plan_position"] == order[note["concept_id"]]
        # The boundary compares this against the ABSOLUTE book_position, not the rank.
        assert note["from_book_position"] == by_id[note["concept_id"]]["source"]["book_position"]
        assert len(note["reason"].strip()) >= MIN_DIRECTIVE_CHARS
        assert note["reason"].lower().strip(".!?-_ ") not in PLACEHOLDERS


# --- ordering ---------------------------------------------------------------------


def test_with_no_edges_the_plan_is_book_order():
    """Every difference from book order must be forced by a dependency, not incidental."""
    sections = _sparse_sections()
    concepts = [_concept(f"c{n}", section) for n, section in enumerate(sections)]

    compiled = compile_master_plan("doc", concepts, [], sections)

    assert compiled.trace["plan_order"] == ["c0", "c1", "c2", "c3"]
    assert compiled.trace["moves"] == 0
    assert compiled.plan["reordering_rationale"] == []
    _assert_boundary_rules(compiled.plan)


def test_an_edge_that_contradicts_book_order_forces_a_move():
    sections = _sparse_sections()
    concepts = [_concept(f"c{n}", section) for n, section in enumerate(sections)]
    # c3 is last in the book but is a prerequisite of c1.
    compiled = compile_master_plan("doc", concepts, [_edge("c3", "c1")], sections)

    order = compiled.trace["plan_order"]
    assert order.index("c3") < order.index("c1")
    assert compiled.trace["moves"] > 0
    _assert_boundary_rules(compiled.plan)


def test_the_tie_break_keeps_the_sequence_as_close_to_book_order_as_possible():
    sections = _sparse_sections()
    concepts = [_concept(f"c{n}", section) for n, section in enumerate(sections)]
    # Only c0 -> c1 is constrained; c2 and c3 are free and must stay in book order.
    compiled = compile_master_plan("doc", concepts, [_edge("c0", "c1")], sections)

    assert compiled.trace["plan_order"] == ["c0", "c1", "c2", "c3"]
    assert compiled.trace["moves"] == 0


def test_a_prerequisite_cycle_is_refused_rather_than_broken():
    sections = _sparse_sections()[:2]
    concepts = [_concept("a", sections[0]), _concept("b", sections[1])]

    with pytest.raises(UnsequenceablePlanError) as err:
        compile_master_plan("doc", concepts, [_edge("a", "b"), _edge("b", "a")], sections)

    assert "cycle" in str(err.value)
    assert "a" in str(err.value) and "b" in str(err.value)


def test_a_diamond_dependency_sequences_cleanly():
    """The normal shape of a prerequisite graph, and the shape a naive cycle check breaks on."""
    sections = _sparse_sections()
    concepts = [_concept(name, section) for name, section in zip("abcd", sections, strict=True)]
    edges = [_edge("a", "b"), _edge("a", "c"), _edge("b", "d"), _edge("c", "d")]

    compiled = compile_master_plan("doc", concepts, edges, sections)

    assert compiled.trace["plan_order"] == ["a", "b", "c", "d"]
    _assert_boundary_rules(compiled.plan)


# --- the reorder note's two numbers -----------------------------------------------


def test_a_reorder_note_carries_the_absolute_book_position_not_the_rank():
    """The bug this guards is a repair loop, not a rejection.

    Ranks here are 0,1,2,3 while absolute book positions are 0,3,7,12. A note carrying
    the rank would satisfy the move check and fail `_check_note_agrees_with_plan`.
    """
    sections = _sparse_sections()
    concepts = [_concept(f"c{n}", section) for n, section in enumerate(sections)]
    compiled = compile_master_plan("doc", concepts, [_edge("c3", "c0")], sections)

    notes = {note["concept_id"]: note for note in compiled.plan["reordering_rationale"]}
    assert notes, "expected at least one move"
    # c3 must precede c0, so the order is c1, c2, c3, c0 - c3 lands at position 3.
    assert notes["c3"]["from_book_position"] == 12  # absolute, not rank 3
    assert notes["c3"]["to_plan_position"] == 3
    assert notes["c0"]["from_book_position"] == 0
    assert notes["c0"]["to_plan_position"] == 4
    _assert_boundary_rules(compiled.plan)


def test_an_unmoved_concept_gets_no_note():
    """The boundary rejects a note for a concept that did not move, as well as the reverse."""
    sections = _sparse_sections()
    concepts = [_concept(f"c{n}", section) for n, section in enumerate(sections)]
    compiled = compile_master_plan("doc", concepts, [_edge("c3", "c2")], sections)

    explained = {note["concept_id"] for note in compiled.plan["reordering_rationale"]}
    assert "c0" not in explained and "c1" not in explained


def test_the_reason_distinguishes_a_forced_move_from_a_displacement():
    sections = _sparse_sections()
    concepts = [_concept(f"c{n}", section) for n, section in enumerate(sections)]
    compiled = compile_master_plan("doc", concepts, [_edge("c3", "c1")], sections)

    reasons = {n["concept_id"]: n["reason"] for n in compiled.plan["reordering_rationale"]}
    assert "depends on" in reasons["c3"] or "Displaced" in reasons["c3"]
    displaced = [reason for cid, reason in reasons.items() if cid != "c3"]
    assert all("Displaced" in reason or "depends on" in reason for reason in displaced)


# --- edges ------------------------------------------------------------------------


def test_the_same_edge_from_two_chapters_is_deduplicated():
    """plan.models rejects a duplicate pair, and two chapters can assert one edge."""
    sections = _sparse_sections()[:2]
    concepts = [_concept("a", sections[0]), _concept("b", sections[1])]
    duplicate = [_edge("a", "b"), _edge("a", "b")]

    compiled = compile_master_plan("doc", concepts, duplicate, sections)

    assert len(compiled.plan["concept_graph"]["edges"]) == 1
    assert any("duplicate" in dropped for dropped in compiled.trace["edges_dropped"])
    _assert_boundary_rules(compiled.plan)


def test_a_cross_reference_edge_gets_a_located_at_span():
    sections = _sparse_sections()[:2]
    concepts = [_concept("a", sections[0]), _concept("b", sections[1])]
    edges = [_edge("a", "b", evidence="cross_reference", quote="as we saw in chapter 1")]

    compiled = compile_master_plan("doc", concepts, edges, sections)

    edge = compiled.plan["concept_graph"]["edges"][0]
    # The quote sits in the dependent's own text - the later chapter pointing back.
    assert edge["located_at"]["section_id"] == "doc.s3"
    _assert_boundary_rules(compiled.plan)


def test_an_inferred_edge_has_no_located_at():
    sections = _sparse_sections()[:2]
    concepts = [_concept("a", sections[0]), _concept("b", sections[1])]

    compiled = compile_master_plan("doc", concepts, [_edge("a", "b")], sections)

    assert compiled.plan["concept_graph"]["edges"][0]["located_at"] is None


def test_a_concept_pointing_at_a_section_that_is_not_in_the_parse_is_refused():
    sections = _sparse_sections()[:1]
    orphan = ExtractedConcept(
        concept_id="ghost",
        label="Ghost",
        section_id="doc.does-not-exist",
        directive="Explain the thing that is not there.",
        chapter_id="doc.ch01",
    )

    with pytest.raises(UnsequenceablePlanError) as err:
        compile_master_plan("doc", [orphan], [], sections)

    assert "SourceSpan" in str(err.value)


# --- the whole thing --------------------------------------------------------------


def test_the_compiled_plan_satisfies_the_boundarys_rules():
    """Replace the local restatement with `plan.validate_master_plan` once #48 lands."""
    sections = _sparse_sections()
    concepts = [_concept(name, section) for name, section in zip("abcd", sections, strict=True)]
    edges = [
        _edge("d", "a", evidence="cross_reference", quote="see the later chapter"),
        _edge("a", "c"),
        _edge("b", "c"),
    ]

    compiled = compile_master_plan("doc", concepts, edges, sections)

    _assert_boundary_rules(compiled.plan)
    assert compiled.plan["schema_version"] == "1"
    assert compiled.plan["document_id"] == "doc"
    assert compiled.plan["run_id"] is None
