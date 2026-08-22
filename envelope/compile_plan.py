"""Envelope to Master Plan — the compilation Tier 2's contract is fed from.

Everything here exists to satisfy `plan/validation.py` at the tier boundary, and the
ordering of concerns is deliberate: this module produces a plan that either passes
that boundary or fails loudly here, where the chapter that caused it can still be
named. A plan repaired quietly would make N builders produce subtly wrong sections.

Two decisions are load-bearing.

**The sequence is a topological order, tie-broken by book order.** Many orderings
satisfy the same edges; taking the earliest book-order concept that is legal at each
step makes the choice deterministic and makes every reordering *forced* by a
prerequisite rather than incidental. With no edges at all the output is exactly book
order, which is the property that matters: a sequence that shuffled freely would
inflate the very number O5 is measured by.

Stated precisely, because O5 counts moves and the distinction is scoreable: this
produces the **lexicographically smallest** topological order under book rank. It does
*not* minimise total displacement. On a graph whose one edge points backwards across
the whole document, the greedy order shifts every concept by one rather than moving the
single offender to the front — both are valid, both cost the same number of moves here,
but on other shapes a displacement-minimising order would report fewer. If the
forward-reference-violation count ever turns on that difference, this is the line to
revisit, and the choice should be stated in the paper rather than left implicit.

**A `ReorderNote` is emitted for exactly the concepts the boundary demands one for,
and it carries the numbers the boundary compares against.** `plan/validation.py`
detects a move by comparing *ranks* — position within the plan's own concepts — but
`_check_note_agrees_with_plan` requires `from_book_position` to equal the concept's
*absolute* `source.book_position`. Those are different numbers whenever the plan's
concepts are drawn from non-consecutive sections, which is always. Getting this wrong
produces a note the boundary rejects, and since the rejection message is Tier 1's
repair prompt, it loops.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from envelope.pass1 import ExtractedConcept, ExtractedEdge
from ingest.sections import Section

SCHEMA_VERSION = "1"


class UnsequenceablePlanError(RuntimeError):
    """The concept graph has a prerequisite cycle, so no ordering can satisfy it.

    Raised rather than broken by dropping an edge. Which edge to drop is a judgement
    about the document, and making it silently would put a fabricated dependency claim
    into the artefact O5 is scored on.
    """


@dataclass(frozen=True)
class CompiledPlan:
    plan: dict[str, Any]
    trace: dict[str, Any]


def _book_rank(concepts: list[ExtractedConcept], spans: dict[str, Section]) -> dict[str, int]:
    """Rank concepts in the document's own order, matching the boundary's tie-break.

    `plan.models.book_ordered_concept_ids` sorts by `(book_position, id)`. The same
    tie-break is used here so a rank computed on this side agrees with the rank the
    boundary computes on the other.
    """
    ordered = sorted(
        concepts,
        key=lambda concept: (
            spans[concept.section_id].book_position,
            concept.concept_id,
        ),
    )
    return {concept.concept_id: rank for rank, concept in enumerate(ordered)}


def _topological_order(
    concepts: list[ExtractedConcept],
    edges: list[ExtractedEdge],
    book_rank: dict[str, int],
) -> list[str]:
    """Kahn's algorithm, always taking the earliest available concept in book order.

    The tie-break is what keeps the output honest: with no dependency forcing a move,
    the plan is book order, and every difference between the two is a move some edge
    required. This is the lexicographically smallest topological order under book rank,
    not the minimum-displacement one — see the module docstring for why that matters to
    O5's move count.
    """
    concept_ids = [concept.concept_id for concept in concepts]
    dependents: dict[str, list[str]] = {concept_id: [] for concept_id in concept_ids}
    indegree: dict[str, int] = {concept_id: 0 for concept_id in concept_ids}

    for edge in edges:
        dependents[edge.prerequisite].append(edge.dependent)
        indegree[edge.dependent] += 1

    available = sorted(
        (concept_id for concept_id, degree in indegree.items() if degree == 0),
        key=lambda concept_id: (book_rank[concept_id], concept_id),
    )
    ordered: list[str] = []

    while available:
        current = available.pop(0)
        ordered.append(current)
        for dependent in dependents[current]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                available.append(dependent)
        available.sort(key=lambda concept_id: (book_rank[concept_id], concept_id))

    if len(ordered) != len(concept_ids):
        stuck = sorted(set(concept_ids) - set(ordered))
        raise UnsequenceablePlanError(
            "prerequisite cycle among these concepts, so no study sequence can satisfy "
            f"them: {', '.join(stuck)}"
        )
    return ordered


def _reason_for_move(
    concept_id: str,
    edges: list[ExtractedEdge],
    book_rank: dict[str, int],
) -> str:
    """State why a concept moved, from the edges that actually forced it.

    Two cases, and the distinction matters for review: a concept that moved because one
    of its own prerequisites sits later in the book is direct evidence for O5; a concept
    that merely got pushed along is not, and saying so keeps the rationale from
    overstating what the reordering demonstrates.
    """
    late_prerequisites = sorted(
        edge.prerequisite
        for edge in edges
        if edge.dependent == concept_id
        and book_rank.get(edge.prerequisite, -1) > book_rank[concept_id]
    )
    if late_prerequisites:
        named = ", ".join(f"'{prerequisite}'" for prerequisite in late_prerequisites)
        return (
            f"Book order teaches this before {named}, which it depends on. Moved after "
            "its prerequisites so the sequence never asks the reader to use a concept "
            "before meeting it."
        )
    return (
        "Displaced by concepts that had to move ahead of it to satisfy their own "
        "prerequisites. Its own prerequisites still precede it, so its position is a "
        "consequence of another move rather than a claim about this concept."
    )


def compile_master_plan(
    document_id: str,
    concepts: list[ExtractedConcept],
    edges: list[ExtractedEdge],
    sections: list[Section],
) -> CompiledPlan:
    """Turn Pass 1's findings into a Master Plan the tier boundary will accept."""
    spans = {section.section_id: section for section in sections}

    unanchored = [c.concept_id for c in concepts if c.section_id not in spans]
    if unanchored:
        raise UnsequenceablePlanError(
            "concepts point at sections that are not in the parse, so no SourceSpan "
            f"can be built for them: {', '.join(sorted(unanchored))}"
        )

    edges, dropped_edges = _clean_edges(edges, {c.concept_id for c in concepts})

    book_rank = _book_rank(concepts, spans)
    order = _topological_order(concepts, edges, book_rank)
    plan_position = {concept_id: index + 1 for index, concept_id in enumerate(order)}
    by_id = {concept.concept_id: concept for concept in concepts}

    concept_payload = [
        {
            "id": concept.concept_id,
            "label": concept.label,
            "source": _span_payload(spans[concept.section_id]),
            "aliases": [],
        }
        for concept in sorted(concepts, key=lambda c: book_rank[c.concept_id])
    ]

    edge_payload = []
    for edge in edges:
        located_at = None
        if edge.evidence == "cross_reference":
            # The quote sits in the dependent's own text — a cross-reference is the
            # later chapter pointing back, so that is where it was found.
            located_at = _span_payload(spans[by_id[edge.dependent].section_id])
        edge_payload.append(
            {
                "prerequisite": edge.prerequisite,
                "dependent": edge.dependent,
                "evidence": edge.evidence,
                "quote": edge.quote,
                "located_at": located_at,
            }
        )

    sequence_payload = [
        {
            "position": plan_position[concept_id],
            "concept_id": concept_id,
            "directive": by_id[concept_id].directive,
        }
        for concept_id in order
    ]

    rationale_payload = []
    for concept_id in order:
        if book_rank[concept_id] == plan_position[concept_id] - 1:
            continue  # rank unchanged; the boundary demands no note and forbids none
        rationale_payload.append(
            {
                "concept_id": concept_id,
                # Absolute section ordinal, NOT the rank — see the module docstring.
                "from_book_position": spans[by_id[concept_id].section_id].book_position,
                "to_plan_position": plan_position[concept_id],
                "reason": _reason_for_move(concept_id, edges, book_rank),
            }
        )

    plan = {
        "schema_version": SCHEMA_VERSION,
        "document_id": document_id,
        "concept_graph": {"concepts": concept_payload, "edges": edge_payload},
        "study_sequence": sequence_payload,
        "reordering_rationale": rationale_payload,
        "run_id": None,
    }

    trace = {
        "concepts": len(concept_payload),
        "edges": len(edge_payload),
        "edges_by_evidence": _count_by(edges),
        "edges_dropped": dropped_edges,
        "moves": len(rationale_payload),
        "moved_concepts": [note["concept_id"] for note in rationale_payload],
        "book_order": sorted(book_rank, key=lambda cid: book_rank[cid]),
        "plan_order": order,
    }
    return CompiledPlan(plan=plan, trace=trace)


def _clean_edges(
    edges: list[ExtractedEdge], known: set[str]
) -> tuple[list[ExtractedEdge], list[str]]:
    """Drop edges the contract would reject at the field level, and say which.

    Two cases, both of which Pass 1 can produce legitimately and neither of which is a
    model error. The same prerequisite can be asserted by two different chapters, and
    `plan.models.ConceptGraph` rejects a duplicate `(prerequisite, dependent)` pair —
    so the second copy is dropped, keeping the first, which is the one with the earlier
    chapter's evidence. An endpoint outside the accepted concept set can survive if a
    chapter's concepts were rejected after its edges were read.
    """
    seen: set[tuple[str, str]] = set()
    kept: list[ExtractedEdge] = []
    dropped: list[str] = []

    for edge in edges:
        pair = (edge.prerequisite, edge.dependent)
        if edge.prerequisite not in known or edge.dependent not in known:
            dropped.append(f"{edge.prerequisite} -> {edge.dependent} (endpoint not a concept)")
            continue
        if pair in seen:
            dropped.append(f"{edge.prerequisite} -> {edge.dependent} (duplicate)")
            continue
        seen.add(pair)
        kept.append(edge)

    return kept, dropped


def _span_payload(section: Section) -> dict[str, Any]:
    return {
        "section_id": section.section_id,
        "book_position": section.book_position,
        "page_start": section.page_start,
        "page_end": section.page_end,
    }


def _count_by(edges: list[ExtractedEdge]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for edge in edges:
        counts[edge.evidence] = counts.get(edge.evidence, 0) + 1
    return counts
