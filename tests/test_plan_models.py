"""Tests for the Master Plan types.

The cases that matter are the ones where a malformed plan could reach a builder
looking well-formed: a reversed or duplicated prerequisite edge, a concept id
that appears twice, an unexpected key from Tier 1 that gets dropped instead of
raised, or a plan that survives a JSON round-trip as something slightly
different from what Tier 1 emitted.
"""

from __future__ import annotations

import pathlib

import pytest
from pydantic import ValidationError

import plan as plan_package
from plan import Concept, ConceptEdge, ConceptGraph, MasterPlan, ReorderNote, SourceSpan, StudyStep


def _span(book_position: int = 0, page: int = 1) -> SourceSpan:
    return SourceSpan(
        section_id=f"ch{book_position + 1}",
        book_position=book_position,
        page_start=page,
        page_end=page + 4,
    )


def _concept(concept_id: str, book_position: int = 0) -> Concept:
    return Concept(id=concept_id, label=concept_id.title(), source=_span(book_position))


def _plan() -> MasterPlan:
    graph = ConceptGraph(
        concepts=(_concept("processes", 0), _concept("scheduling", 1)),
        edges=(
            ConceptEdge(
                prerequisite="processes",
                dependent="scheduling",
                evidence="cross_reference",
                quote="as we saw in Chapter 1",
                located_at=_span(1, 20),
            ),
        ),
    )
    return MasterPlan(
        document_id="ostep",
        concept_graph=graph,
        study_sequence=(
            StudyStep(position=1, concept_id="processes", directive="Explain what a process is."),
            StudyStep(position=2, concept_id="scheduling", directive="Explain the scheduler."),
        ),
        reordering_rationale=(
            ReorderNote(
                concept_id="scheduling",
                from_book_position=1,
                to_plan_position=2,
                reason="Depends on processes, which the book already introduces first.",
            ),
        ),
    )


def test_the_worked_example_ships_with_the_package():
    # It ships only in an editable install unless pyproject declares it as
    # package data, and `EXAMPLE_PLAN_PATH` is what the reproducibility artefact
    # resolves — the one context where nobody has the repo.
    from plan import EXAMPLE_PLAN_PATH

    assert EXAMPLE_PLAN_PATH.exists()
    assert EXAMPLE_PLAN_PATH.parent == pathlib.Path(plan_package.__file__).parent


def test_plan_survives_a_json_round_trip_unchanged():
    plan = _plan()
    assert MasterPlan.model_validate_json(plan.model_dump_json()) == plan


def test_unexpected_tier1_keys_are_rejected_not_dropped():
    payload = _plan().model_dump()
    payload["confidence"] = 0.9
    with pytest.raises(ValidationError) as err:
        MasterPlan.model_validate(payload)
    assert "confidence" in str(err.value)


def test_a_plan_cannot_be_edited_after_validation():
    plan = _plan()
    with pytest.raises(ValidationError):
        plan.document_id = "axler"


@pytest.mark.parametrize("bad_id", ["", "a", "Processes", "process ids", "-leading"])
def test_malformed_concept_ids_are_rejected(bad_id):
    with pytest.raises(ValidationError):
        Concept(id=bad_id, label="x", source=_span())


def test_duplicate_concept_ids_are_named_in_the_error():
    with pytest.raises(ValidationError) as err:
        ConceptGraph(concepts=(_concept("processes"), _concept("processes", 3)))
    assert "processes" in str(err.value)


def test_a_concept_cannot_be_its_own_prerequisite():
    with pytest.raises(ValidationError) as err:
        ConceptGraph(
            concepts=(_concept("processes"),),
            edges=(
                ConceptEdge(prerequisite="processes", dependent="processes", evidence="inferred"),
            ),
        )
    assert "own prerequisite" in str(err.value)


def test_the_same_edge_twice_is_rejected():
    edge = ConceptEdge(prerequisite="processes", dependent="scheduling", evidence="inferred")
    with pytest.raises(ValidationError) as err:
        ConceptGraph(
            concepts=(_concept("processes", 0), _concept("scheduling", 1)),
            edges=(edge, edge),
        )
    assert "processes -> scheduling" in str(err.value)


def test_a_span_cannot_end_before_it_starts():
    with pytest.raises(ValidationError):
        SourceSpan(section_id="ch1", book_position=0, page_start=30, page_end=12)


def test_edge_direction_is_named_so_it_cannot_be_swapped_positionally():
    with pytest.raises(TypeError):
        ConceptEdge("processes", "scheduling", "inferred")  # type: ignore[call-arg]


def test_plan_order_and_book_order_are_both_recoverable():
    graph = ConceptGraph(concepts=(_concept("scheduling", 1), _concept("processes", 0)))
    plan = MasterPlan(
        document_id="ostep",
        concept_graph=graph,
        study_sequence=(
            StudyStep(position=2, concept_id="processes", directive="second"),
            StudyStep(position=1, concept_id="scheduling", directive="first"),
        ),
    )
    # Master-Plan order follows `position`, not the order the steps were listed.
    assert plan.ordered_concept_ids == ("scheduling", "processes")
    assert plan.book_ordered_concept_ids == ("processes", "scheduling")
