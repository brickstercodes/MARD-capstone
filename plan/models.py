"""The Master Plan types — the typed JSON contract between Tier 1 and Tier 2.

CONTEXT.md §1.5 defines the Master Plan as concept graph + ordered study
sequence + reordering rationale. This module is only the *shape* of that
contract; the cross-collection rules that decide whether a plan is coherent
enough to hand to N builders live in `plan.validation`, because those are the
rules that have to fail loudly at the tier boundary and they need to report on
the plan as a whole rather than one field at a time.

Three decisions here are load-bearing for measurement, not just for typing:

- **Edge direction is named, never positional.** `ConceptEdge` has
  `prerequisite` and `dependent` rather than source/target. O5 counts
  forward-reference violations (docs/30-MEASUREMENT_PROTOCOL.md §3), so a plan
  whose edges are silently reversed scores as confidently wrong rather than
  malformed — the one failure mode this schema exists to prevent.
- **Every concept carries a `SourceSpan` with a `book_position`.** O5 compares
  book order against Master-Plan order; a plan that cannot be scored without
  re-parsing the document is not self-contained evidence.
- **`extra="forbid"` everywhere.** Tier 1 is a language model emitting JSON. A
  key we did not ask for means the model answered a different question than the
  one the prompt posed, and dropping it quietly is how N builders end up
  producing subtly wrong sections.

Models are frozen: a plan is measured evidence once it is validated, and the
orchestrator must not be able to edit it between the boundary check and the
builders reading it.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

SCHEMA_VERSION: Literal["1"] = "1"
"""Bumped only when the contract changes shape. Frozen for Manuscript A."""

# Tier 1 emits these ids and Tier 2, Track 3's scorers and Track 4's ground-truth
# matcher all key off them. Constraining the alphabet here means an id can be
# compared, sorted and used as a filename without anyone writing a normaliser.
ConceptId = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z0-9][a-z0-9._-]*$", min_length=2, max_length=80),
]

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class _Contract(BaseModel):
    """Shared config for every type in the contract."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)


class SourceSpan(_Contract):
    """Where in the document a concept or directive comes from.

    The boundary shape between Track 4's `ingest/` page map and this contract.
    Track 4 fills it; nothing here parses a PDF.
    """

    section_id: NonEmptyStr
    """Track 4's identifier for the section — stable across re-parses."""

    book_position: int = Field(ge=0)
    """Ordinal of this section in the document's own order. O5's baseline
    ordering is book order, which is a real ordering and not a straw man
    (CONTEXT.md §2.4), so it has to survive into the plan."""

    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)

    @model_validator(mode="after")
    def _pages_run_forwards(self) -> SourceSpan:
        if self.page_end < self.page_start:
            raise ValueError(f"span ends before it starts: pages {self.page_start}-{self.page_end}")
        return self


class Concept(_Contract):
    """One unit of the thing being learned, anchored to where the document says it."""

    id: ConceptId
    label: NonEmptyStr
    source: SourceSpan
    aliases: tuple[NonEmptyStr, ...] = ()
    """Surface forms Track 4's glossary extraction may have used instead of
    `label`. Matching ground truth on one spelling would understate the plan."""


EdgeEvidence = Literal["cross_reference", "glossary", "inferred"]
"""How Tier 1 claims to know an edge exists.

`cross_reference` is the only kind the document itself asserts ("as we saw in
Ch. 3"); `inferred` is the model's own claim. Track 3 needs to be able to score
those separately — an envelope that only recovers edges the document states
outright is a weaker result than one that predicts unstated edges correctly.
"""


class ConceptEdge(_Contract):
    """A prerequisite claim: `dependent` cannot be understood before `prerequisite`.

    CONTEXT.md §1.5 calls this the field that carries the contribution — each
    edge is a falsifiable prediction, scorable against the document's own in-text
    cross-references. `evidence` and `quote` are what make it falsifiable rather
    than merely asserted.
    """

    prerequisite: ConceptId
    dependent: ConceptId
    evidence: EdgeEvidence
    quote: NonEmptyStr | None = None
    """The document's own words, for a `cross_reference` edge. Track 4's
    extraction produces the reference positions this is checked against."""

    located_at: SourceSpan | None = None
    """Where `quote` was found. Required in spirit for `cross_reference` edges;
    enforced at the boundary rather than here, so the failure names the edge."""


class ConceptGraph(_Contract):
    """The concepts and the prerequisite claims between them."""

    concepts: tuple[Concept, ...] = Field(min_length=1)
    edges: tuple[ConceptEdge, ...] = ()

    @field_validator("concepts")
    @classmethod
    def _ids_are_unique(cls, concepts: tuple[Concept, ...]) -> tuple[Concept, ...]:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for concept in concepts:
            if concept.id in seen:
                duplicates.add(concept.id)
            seen.add(concept.id)
        if duplicates:
            raise ValueError(f"duplicate concept ids: {', '.join(sorted(duplicates))}")
        return concepts

    @field_validator("edges")
    @classmethod
    def _edges_are_distinct_and_not_self(
        cls, edges: tuple[ConceptEdge, ...]
    ) -> tuple[ConceptEdge, ...]:
        # A self-edge is a concept that is its own prerequisite, which makes the
        # ordering unsatisfiable; catching it here keeps the cycle report at the
        # boundary about real cycles.
        loops = sorted({e.prerequisite for e in edges if e.prerequisite == e.dependent})
        if loops:
            raise ValueError(f"concepts listed as their own prerequisite: {', '.join(loops)}")
        pairs = [(e.prerequisite, e.dependent) for e in edges]
        repeated = sorted({p for p in pairs if pairs.count(p) > 1})
        if repeated:
            listed = ", ".join(f"{a} -> {b}" for a, b in repeated)
            raise ValueError(f"duplicate edges: {listed}")
        return edges

    @property
    def concept_ids(self) -> frozenset[str]:
        return frozenset(c.id for c in self.concepts)

    def concept(self, concept_id: str) -> Concept | None:
        return next((c for c in self.concepts if c.id == concept_id), None)


class StudyStep(_Contract):
    """One step of the sequence — and one Tier 2 builder's entire brief.

    A builder sees this step and the section its concept points at, nothing
    else (CONTEXT.md §1.4). Whatever a builder needs has to be in `directive`.
    """

    position: int = Field(ge=1)
    """1-based position in Master-Plan order. Explicit rather than implied by
    list index so a plan that disagrees with itself fails instead of being
    silently renumbered on load."""

    concept_id: ConceptId
    directive: NonEmptyStr
    """What Tier 2 must produce for this concept, in Tier 1's words."""


class ReorderNote(_Contract):
    """Why one concept was moved out of book order.

    The rationale is part of the contract because O5's claim is that the
    reordering is dependency-driven; a move nobody can explain is a move nobody
    can defend in review.
    """

    concept_id: ConceptId
    from_book_position: int = Field(ge=0)
    to_plan_position: int = Field(ge=1)
    reason: NonEmptyStr


class MasterPlan(_Contract):
    """The whole contract. Tier 1 emits it; Tier 2 executes it; Track 3 scores it."""

    schema_version: Literal["1"] = SCHEMA_VERSION
    document_id: NonEmptyStr
    concept_graph: ConceptGraph
    study_sequence: tuple[StudyStep, ...] = Field(min_length=1)
    reordering_rationale: tuple[ReorderNote, ...] = ()

    run_id: str | None = None
    """The `runlog` run that produced this plan. Optional only because
    hand-written fixtures have no run behind them."""

    @property
    def ordered_concept_ids(self) -> tuple[str, ...]:
        """Concept ids in Master-Plan order — the sequence O5 scores."""
        return tuple(step.concept_id for step in sorted(self.study_sequence, key=_position))

    @property
    def book_ordered_concept_ids(self) -> tuple[str, ...]:
        """The same concepts in the document's own order — O5's baseline."""
        concepts = sorted(self.concept_graph.concepts, key=_book_position)
        return tuple(c.id for c in concepts)


def _position(step: StudyStep) -> int:
    return step.position


def _book_position(concept: Concept) -> tuple[int, str]:
    # Ties broken by id so book order is total, not merely partial — two
    # concepts drawn from the same section must still compare deterministically
    # or O5's baseline count changes between runs.
    return (concept.source.book_position, concept.id)
