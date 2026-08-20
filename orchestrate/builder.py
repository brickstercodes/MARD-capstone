"""Tier 2 execution - what one builder sees, and how the pieces are joined back.

This is the W1 stub of the fork-join described in CONTEXT.md §3.3 Track 2 W2.
It exists before the real orchestrator, and before Track 1 can generate a plan,
because the point of a stub is to fix the contract early: with it in place the
Master Plan has a consumer, and Track 2 is never blocked waiting on the envelope.

Two properties are real here and are not stubbed, because they are the ones the
paper makes claims about:

- **A builder sees one concept and one directive. Nothing else.** No sibling
  output, no full plan, no document. If a builder needed more than its brief,
  the two-tier cost model would be a fiction.
- **The join is in Master-Plan order, not completion order and not book order.**
  Spans are ordered by `position` after every builder returns, so a faster
  builder cannot change the artefact.

Explicitly deferred to W2, and deliberately absent rather than half-built: the
bounded worker pool, per-builder retry, and failure isolation. A builder that
raises here takes the run down, which is the honest behaviour until there is a
retry policy to name.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from plan.models import Concept, MasterPlan
from plan.validation import validate_master_plan
from runlog import RunLogger


@dataclass(frozen=True)
class Provenance:
    """Where a generated span came from - source section, plan slot, and builder.

    On every span rather than on the artefact as a whole because Track 4's
    hallucination-rate spot-checks (CONTEXT.md §3.3 Track 4 W7) sample spans, and
    a span that cannot be traced back to a page is not checkable.
    """

    document_id: str
    section_id: str
    page_start: int
    page_end: int
    plan_position: int
    builder: str


@dataclass(frozen=True)
class BuilderBrief:
    """Everything one Tier 2 builder is given. The narrowness is the point."""

    document_id: str
    position: int
    concept: Concept
    directive: str

    @property
    def section_id(self) -> str:
        return self.concept.source.section_id


@dataclass(frozen=True)
class BuiltSpan:
    """One builder's output, tagged with where it belongs and where it came from."""

    concept_id: str
    position: int
    text: str
    provenance: Provenance


class IncompleteArtefactError(RuntimeError):
    """Raised when the spans do not account for exactly one per Master Plan step.

    W2 adds per-builder retry and failure isolation, and isolation is precisely
    the feature that produces a run with a span missing. Without this the join
    would hand back a short artefact that reads as complete, and the first place
    anyone noticed would be a measurement. Dropping a builder has to be a
    decision someone made and recorded, not something the join absorbs.
    """


@dataclass(frozen=True)
class Artefact:
    """The joined result: spans in Master-Plan order."""

    document_id: str
    spans: tuple[BuiltSpan, ...]

    @property
    def text(self) -> str:
        return "\n\n".join(span.text for span in self.spans)

    @property
    def concept_order(self) -> tuple[str, ...]:
        return tuple(span.concept_id for span in self.spans)


@runtime_checkable
class Builder(Protocol):
    """A Tier 2 worker. Async now so W2 can add the pool without changing callers."""

    name: str

    async def build(self, brief: BuilderBrief) -> BuiltSpan: ...


class StubBuilder:
    """A builder that writes a placeholder instead of calling a model.

    Deterministic and offline: it costs nothing, needs no keys, and gives the
    same artefact every run, so a change in the joined output means the plan or
    the join changed rather than the weather.
    """

    name = "stub"

    async def build(self, brief: BuilderBrief) -> BuiltSpan:
        text = (
            f"## {brief.position}. {brief.concept.label}\n"
            f"{brief.directive}\n"
            f"[stub output - section {brief.section_id}, "
            f"pages {brief.concept.source.page_start}-{brief.concept.source.page_end}]"
        )
        return BuiltSpan(
            concept_id=brief.concept.id,
            position=brief.position,
            text=text,
            provenance=_provenance(brief, self.name),
        )


def _provenance(brief: BuilderBrief, builder: str) -> Provenance:
    source = brief.concept.source
    return Provenance(
        document_id=brief.document_id,
        section_id=source.section_id,
        page_start=source.page_start,
        page_end=source.page_end,
        plan_position=brief.position,
        builder=builder,
    )


def briefs_for(plan: MasterPlan) -> tuple[BuilderBrief, ...]:
    """Fork: one brief per step, each carrying only its own concept and directive."""
    briefs: list[BuilderBrief] = []
    for step in sorted(plan.study_sequence, key=lambda s: s.position):
        concept = plan.concept_graph.concept(step.concept_id)
        if concept is None:  # unreachable after validation; a loud guard, not a fallback
            raise ValueError(f"step {step.position} names unknown concept '{step.concept_id}'")
        briefs.append(
            BuilderBrief(
                document_id=plan.document_id,
                position=step.position,
                concept=concept,
                directive=step.directive,
            )
        )
    return tuple(briefs)


def join_in_plan_order(spans: Sequence[BuiltSpan], plan: MasterPlan) -> Artefact:
    """Join: Master-Plan order, whatever order the builders finished in.

    Takes the plan rather than a document id so the join can check that it was
    handed one span per step. Sorting an incomplete set succeeds quietly, which
    is the wrong failure mode for the thing that produces the measured artefact.
    """
    by_position: dict[int, BuiltSpan] = {}
    duplicates: list[int] = []
    for span in spans:
        if span.position in by_position:
            duplicates.append(span.position)
        by_position[span.position] = span

    expected = {step.position: step.concept_id for step in plan.study_sequence}
    missing = sorted(expected.keys() - by_position.keys())
    unexpected = sorted(by_position.keys() - expected.keys())
    mismatched = sorted(
        position
        for position, span in by_position.items()
        if position in expected and span.concept_id != expected[position]
    )

    if duplicates or missing or unexpected or mismatched:
        raise IncompleteArtefactError(
            _join_failure(plan, sorted(set(duplicates)), missing, unexpected, mismatched)
        )

    ordered = tuple(by_position[position] for position in sorted(by_position))
    return Artefact(document_id=plan.document_id, spans=ordered)


def _join_failure(
    plan: MasterPlan,
    duplicates: Sequence[int],
    missing: Sequence[int],
    unexpected: Sequence[int],
    mismatched: Sequence[int],
) -> str:
    parts = [
        f"cannot join {plan.document_id}: the spans do not match the Master Plan's "
        f"{len(plan.study_sequence)} steps"
    ]
    if missing:
        named = ", ".join(f"{position} ({_concept_at(plan, position)})" for position in missing)
        parts.append(f"  no span for position(s): {named}")
    if duplicates:
        parts.append(f"  more than one span claims position(s): {_numbers(duplicates)}")
    if unexpected:
        parts.append(f"  span(s) at position(s) the plan does not have: {_numbers(unexpected)}")
    if mismatched:
        parts.append(f"  span(s) built the wrong concept for position(s): {_numbers(mismatched)}")
    return "\n".join(parts)


def _numbers(positions: Sequence[int]) -> str:
    return ", ".join(str(position) for position in positions)


def _concept_at(plan: MasterPlan, position: int) -> str:
    for step in plan.study_sequence:
        if step.position == position:
            return step.concept_id
    return "unknown"


async def execute_plan(plan: MasterPlan, builder: Builder, logger: RunLogger) -> Artefact:
    """Validate at the tier boundary, fan out to builders, join in plan order.

    Validation happens here rather than in the caller so there is no path into
    Tier 2 that skips it. The logger is required, not optional: CLAUDE.md admits
    no exceptions, and a stub run that leaves no trace is exactly the run someone
    later cannot tell apart from a real one.
    """
    validate_master_plan(plan)
    briefs = briefs_for(plan)
    logger.log_event(
        "tier2_fork",
        {"document_id": plan.document_id, "builders": len(briefs), "builder": builder.name},
    )

    spans = await asyncio.gather(*(builder.build(brief) for brief in briefs))
    artefact = join_in_plan_order(spans, plan)

    logger.log_event(
        "tier2_join",
        {
            # The join order is the O5 claim, so it is recorded rather than
            # left to be re-derived from the artefact text later.
            "concept_order": list(artefact.concept_order),
            "provenance": [
                {
                    "concept_id": span.concept_id,
                    "position": span.position,
                    "section_id": span.provenance.section_id,
                    "pages": [span.provenance.page_start, span.provenance.page_end],
                    "builder": span.provenance.builder,
                }
                for span in artefact.spans
            ],
        },
    )
    logger.save_artefact("tier2_output.md", artefact.text)
    return artefact


def execute_plan_sync(plan: MasterPlan, builder: Builder, logger: RunLogger) -> Artefact:
    """Blocking entry point for scripts and tests that own no event loop."""
    return asyncio.run(execute_plan(plan, builder, logger))
