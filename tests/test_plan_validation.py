"""Tests for the tier boundary.

Every case here is a plan that is well-typed and still cannot be executed: the
class of failure that would otherwise reach N builders and come back as N subtly
wrong sections. The boundary's job is to name all of them at once, so most of
these assert on the violation codes rather than on the fact that something raised.
"""

from __future__ import annotations

import pytest

from plan import (
    Concept,
    ConceptEdge,
    ConceptGraph,
    MasterPlan,
    MasterPlanError,
    ReorderNote,
    SourceSpan,
    StudyStep,
    check_master_plan,
    load_master_plan,
    parse_master_plan,
    validate_master_plan,
)


def _span(book_position: int) -> SourceSpan:
    return SourceSpan(
        section_id=f"ch{book_position + 1}",
        book_position=book_position,
        page_start=book_position * 10 + 1,
        page_end=book_position * 10 + 9,
    )


def _concept(concept_id: str, book_position: int) -> Concept:
    return Concept(id=concept_id, label=concept_id.title(), source=_span(book_position))


def _edge(prerequisite: str, dependent: str) -> ConceptEdge:
    return ConceptEdge(prerequisite=prerequisite, dependent=dependent, evidence="inferred")


def _plan(
    *,
    concepts: tuple[Concept, ...] | None = None,
    edges: tuple[ConceptEdge, ...] = (),
    sequence: tuple[StudyStep, ...] | None = None,
    rationale: tuple[ReorderNote, ...] = (),
) -> MasterPlan:
    """A plan that is valid unless a test deliberately breaks one part of it."""
    concepts = concepts or (_concept("processes", 0), _concept("scheduling", 1))
    sequence = sequence or tuple(
        StudyStep(position=i, concept_id=c.id, directive=f"Explain {c.label}.")
        for i, c in enumerate(concepts, start=1)
    )
    return MasterPlan(
        document_id="ostep",
        concept_graph=ConceptGraph(concepts=concepts, edges=edges),
        study_sequence=sequence,
        reordering_rationale=rationale,
    )


def _codes(plan: MasterPlan) -> set[str]:
    return {violation.code for violation in check_master_plan(plan)}


def test_a_coherent_plan_passes_and_is_returned_unchanged():
    plan = _plan(edges=(_edge("processes", "scheduling"),))
    assert check_master_plan(plan) == ()
    assert validate_master_plan(plan) is plan


def test_an_edge_pointing_at_an_undeclared_concept_is_rejected():
    plan = _plan(edges=(_edge("processes", "virtual-memory"),))
    assert "unknown_concept" in _codes(plan)


def test_a_prerequisite_cycle_is_reported_as_a_path():
    plan = _plan(edges=(_edge("processes", "scheduling"), _edge("scheduling", "processes")))
    cycle = [v for v in check_master_plan(plan) if v.code == "prerequisite_cycle"]
    assert len(cycle) == 1
    # The path has to name the loop, or nobody can act on the message.
    assert cycle[0].where.count("->") == 2
    assert "processes" in cycle[0].where and "scheduling" in cycle[0].where


def test_a_cycle_suppresses_the_ordering_noise_it_would_cause():
    plan = _plan(edges=(_edge("processes", "scheduling"), _edge("scheduling", "processes")))
    # One unsatisfiable graph, one violation - not one per edge in the loop.
    assert "ordering_violation" not in _codes(plan)


def test_a_concept_taught_before_its_prerequisite_is_rejected():
    concepts = (_concept("processes", 0), _concept("scheduling", 1))
    sequence = (
        StudyStep(position=1, concept_id="scheduling", directive="first"),
        StudyStep(position=2, concept_id="processes", directive="second"),
    )
    rationale = (
        ReorderNote(
            concept_id="scheduling",
            from_book_position=1,
            to_plan_position=1,
            reason="deliberately wrong, to isolate the ordering check",
        ),
        ReorderNote(
            concept_id="processes",
            from_book_position=0,
            to_plan_position=2,
            reason="deliberately wrong, to isolate the ordering check",
        ),
    )
    plan = _plan(
        concepts=concepts,
        edges=(_edge("processes", "scheduling"),),
        sequence=sequence,
        rationale=rationale,
    )
    violations = [v for v in check_master_plan(plan) if v.code == "ordering_violation"]
    assert len(violations) == 1
    assert "position 1" in violations[0].message and "position 2" in violations[0].message


def test_a_concept_nobody_builds_is_rejected():
    concepts = (_concept("processes", 0), _concept("scheduling", 1))
    sequence = (StudyStep(position=1, concept_id="processes", directive="only one"),)
    plan = _plan(concepts=concepts, sequence=sequence)
    assert "orphan_concept" in _codes(plan)


def test_a_sequenced_concept_that_is_not_in_the_graph_is_rejected():
    concepts = (_concept("processes", 0),)
    sequence = (
        StudyStep(position=1, concept_id="processes", directive="a"),
        StudyStep(position=2, concept_id="virtual-memory", directive="b"),
    )
    assert "unknown_concept" in _codes(_plan(concepts=concepts, sequence=sequence))


def test_the_same_concept_sequenced_twice_is_rejected():
    concepts = (_concept("processes", 0),)
    sequence = (
        StudyStep(position=1, concept_id="processes", directive="a"),
        StudyStep(position=2, concept_id="processes", directive="b"),
    )
    assert "duplicate_step" in _codes(_plan(concepts=concepts, sequence=sequence))


@pytest.mark.parametrize("positions", [(1, 3), (2, 3), (1, 1)])
def test_positions_with_gaps_or_repeats_are_rejected(positions):
    concepts = (_concept("processes", 0), _concept("scheduling", 1))
    sequence = tuple(
        StudyStep(position=p, concept_id=c.id, directive="x")
        for p, c in zip(positions, concepts, strict=True)
    )
    assert "sequence_positions" in _codes(_plan(concepts=concepts, sequence=sequence))


@pytest.mark.parametrize("directive", ["TODO", "tbd", "...", "N/A", "-", "Explain."])
def test_a_placeholder_directive_is_rejected(directive):
    # A builder sees its directive and nothing else, so "TODO" does not fail
    # loudly downstream - it produces a confident section about nothing.
    concepts = (_concept("processes", 0),)
    sequence = (StudyStep(position=1, concept_id="processes", directive=directive),)
    assert "placeholder_directive" in _codes(_plan(concepts=concepts, sequence=sequence))


def test_a_real_directive_passes():
    concepts = (_concept("processes", 0),)
    sequence = (
        StudyStep(
            position=1,
            concept_id="processes",
            directive="Define a process and cover its state transitions.",
        ),
    )
    assert _codes(_plan(concepts=concepts, sequence=sequence)) == set()


@pytest.mark.parametrize(
    "directive",
    ["TODO: write this later", "TBD - fill in from chapter 4", "FIXME add detail here"],
)
def test_placeholder_text_with_an_excuse_attached_is_still_placeholder(directive):
    # Long enough to clear the length floor and not an exact match for any
    # placeholder, but still a brief that briefs nobody.
    concepts = (_concept("processes", 0),)
    sequence = (StudyStep(position=1, concept_id="processes", directive=directive),)
    assert "placeholder_directive" in _codes(_plan(concepts=concepts, sequence=sequence))


def test_broken_positions_do_not_cascade_into_every_concept():
    # Positions 1, 3, 5 make every concept look moved and every rationale look
    # wrong. One report about the numbering beats six about its consequences.
    concepts = tuple(_concept(f"concept-{n}", n) for n in range(3))
    sequence = tuple(
        StudyStep(position=1 + 2 * n, concept_id=f"concept-{n}", directive="Explain it fully.")
        for n in range(3)
    )
    violations = check_master_plan(_plan(concepts=concepts, sequence=sequence))
    assert [v.code for v in violations] == ["sequence_positions"]


def test_a_placeholder_reordering_reason_is_rejected():
    rationale = (
        ReorderNote(
            concept_id="scheduling", from_book_position=1, to_plan_position=2, reason="TODO"
        ),
    )
    assert "placeholder_rationale" in _codes(_plan(rationale=rationale))


def test_a_cross_reference_edge_without_its_quote_is_rejected():
    # The evidence is what makes the edge falsifiable; an unsupported claim of
    # document evidence is worse than an honest "inferred".
    edge = ConceptEdge(prerequisite="processes", dependent="scheduling", evidence="cross_reference")
    violations = [v for v in check_master_plan(_plan(edges=(edge,))) if v.code.startswith("unsup")]
    assert len(violations) == 1
    assert "quote" in violations[0].message and "located_at" in violations[0].message


def test_an_inferred_edge_needs_no_quote():
    assert _codes(_plan(edges=(_edge("processes", "scheduling"),))) == set()


def test_a_move_with_no_stated_reason_is_rejected():
    concepts = (_concept("processes", 0), _concept("scheduling", 1))
    sequence = (
        StudyStep(position=1, concept_id="scheduling", directive="moved, unexplained"),
        StudyStep(position=2, concept_id="processes", directive="also moved"),
    )
    violations = [
        v
        for v in check_master_plan(_plan(concepts=concepts, sequence=sequence))
        if v.code == "unexplained_move"
    ]
    assert {v.where for v in violations} == {"processes", "scheduling"}


def test_a_rationale_that_disagrees_with_the_sequence_is_rejected():
    rationale = (
        ReorderNote(
            concept_id="scheduling",
            from_book_position=1,
            to_plan_position=7,
            reason="claims a position the sequence does not have",
        ),
    )
    violations = [
        v for v in check_master_plan(_plan(rationale=rationale)) if v.code == "rationale_mismatch"
    ]
    assert len(violations) == 1
    assert "position 7" in violations[0].message


def test_a_rationale_that_misstates_book_position_is_rejected():
    rationale = (
        ReorderNote(
            concept_id="scheduling",
            from_book_position=5,
            to_plan_position=2,
            reason="wrong book position",
        ),
    )
    assert "rationale_mismatch" in _codes(_plan(rationale=rationale))


def test_every_violation_is_reported_not_just_the_first():
    concepts = (_concept("processes", 0), _concept("scheduling", 1))
    sequence = (
        StudyStep(position=4, concept_id="scheduling", directive="wrong position, and moved"),
        StudyStep(position=9, concept_id="virtual-memory", directive="not a declared concept"),
    )
    plan = _plan(
        concepts=concepts,
        edges=(_edge("processes", "paging"),),
        sequence=sequence,
    )
    assert _codes(plan) >= {
        "unknown_concept",
        "orphan_concept",
        "sequence_positions",
    }


def test_the_error_message_lists_and_numbers_the_violations():
    plan = _plan(edges=(_edge("processes", "paging"),))
    with pytest.raises(MasterPlanError) as err:
        validate_master_plan(plan)
    assert err.value.violations
    assert "1." in str(err.value)
    assert "unknown_concept" in str(err.value)


def test_malformed_json_fails_as_a_plan_error_not_a_json_error():
    with pytest.raises(MasterPlanError) as err:
        parse_master_plan("{not json")
    assert err.value.violations


def test_a_wrong_shaped_plan_names_the_offending_field():
    payload = _plan().model_dump_json()
    broken = payload.replace('"document_id":"ostep"', '"document_id":""')
    with pytest.raises(MasterPlanError) as err:
        parse_master_plan(broken)
    assert any("document_id" in v.where for v in err.value.violations)


def test_a_valid_plan_round_trips_through_the_boundary(tmp_path):
    plan = _plan(edges=(_edge("processes", "scheduling"),))
    path = tmp_path / "plan.json"
    path.write_text(plan.model_dump_json(), encoding="utf-8")
    assert load_master_plan(path) == plan


def test_a_missing_plan_file_fails_at_the_boundary_too(tmp_path):
    with pytest.raises(MasterPlanError) as err:
        load_master_plan(tmp_path / "nope.json")
    assert err.value.violations[0].code == "unreadable_plan"
