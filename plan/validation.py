"""The tier boundary — where a malformed Master Plan stops.

CONTEXT.md §1.5 is explicit about why this module exists: a malformed plan must
fail loudly rather than producing N subtly wrong sections that nobody notices
until the results are in. Everything checked here is a rule that cannot be
expressed on a single field, which is why it lives outside `plan.models`.

Two properties matter more than the individual rules:

- **Every violation is collected, not just the first.** Tier 1 is a language
  model; the error message is the repair prompt, and a boundary that reports one
  problem per attempt turns one re-prompt into six.
- **One exception type crosses the boundary.** Callers catch `MasterPlanError`
  whether the plan was malformed JSON, the wrong shape, or internally
  incoherent. Anything that gets past it is safe to fan out to builders.

The one rule deliberately *not* here: whether the plan's prerequisite edges match
the document's own cross-references. That is a measurement (O5,
docs/30-MEASUREMENT_PROTOCOL.md §3), not a validity check. A plan that is wrong
about the document is still a well-formed plan, and rejecting it here would
delete the result Track 3 exists to report.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from plan.models import MasterPlan, ReorderNote

# Text a model emits when it has nothing to say. The schema already rejects an
# empty directive, which catches only the honest version of this failure.
PLACEHOLDERS = frozenset(
    {
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
)

MIN_DIRECTIVE_CHARS = 12
"""A directive has to name a concept and say what to do with it. Below this it
cannot be doing both, and a builder handed it will invent the rest."""

_PLACEHOLDER_PREFIX = re.compile(
    rf"^({'|'.join(re.escape(word) for word in sorted(PLACEHOLDERS))})\b[\s:;,.\-]*",
    re.IGNORECASE,
)
"""`TODO: write this later` is long enough to clear the length floor and is not
an exact match for any placeholder, but it is still a builder brief that briefs
nobody."""


@dataclass(frozen=True)
class PlanViolation:
    """One reason a plan cannot be handed to Tier 2."""

    code: str
    """Stable identifier, so Track 3 can count failure kinds across runs without
    parsing prose."""

    where: str
    """Pointer into the plan: a concept id, an edge, or a field path."""

    message: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.where}: {self.message}"


class MasterPlanError(ValueError):
    """Raised at the Tier 1 to Tier 2 boundary. Carries every violation found."""

    def __init__(self, violations: Sequence[PlanViolation]) -> None:
        self.violations = tuple(violations)
        super().__init__(self._render())

    def _render(self) -> str:
        count = len(self.violations)
        noun = "violation" if count == 1 else "violations"
        listed = "\n".join(f"  {i}. {v}" for i, v in enumerate(self.violations, start=1))
        return f"Master Plan rejected at the tier boundary - {count} {noun}:\n{listed}"


def check_master_plan(plan: MasterPlan) -> tuple[PlanViolation, ...]:
    """Return every coherence violation in a plan that already has the right shape.

    Non-raising on purpose: the ablation runner and the plan-quality report want
    to count violations, not be stopped by them.
    """
    violations: list[PlanViolation] = []
    violations.extend(_check_edge_endpoints(plan))
    violations.extend(_check_edge_evidence(plan))

    cycle = _find_cycle(_adjacency(plan))
    if cycle is not None:
        violations.append(
            PlanViolation(
                code="prerequisite_cycle",
                where=" -> ".join(cycle),
                message="concepts form a prerequisite cycle, so no ordering can satisfy them",
            )
        )

    violations.extend(_check_sequence_covers_graph(plan))
    position_violations = tuple(_check_sequence_positions(plan))
    violations.extend(position_violations)
    violations.extend(_check_directives(plan))

    # Everything below reads a concept's place in the sequence. Two guards, both
    # for the same reason: a check whose input is already known to be broken
    # produces one violation per concept and buries the report that matters.
    #
    #  - a cyclic graph makes every edge in the loop an ordering violation
    #  - a sequence numbered 1, 3, 7 has no meaningful positions at all, so
    #    every rationale disagrees with it and every concept looks moved
    positions_usable = not position_violations
    if cycle is None and positions_usable:
        violations.extend(_check_sequence_respects_edges(plan))
    violations.extend(_check_rationale(plan, positions_usable=positions_usable))
    return tuple(violations)


def validate_master_plan(plan: MasterPlan) -> MasterPlan:
    """Return the plan, or raise `MasterPlanError` listing everything wrong with it."""
    violations = check_master_plan(plan)
    if violations:
        raise MasterPlanError(violations)
    return plan


def parse_master_plan(raw: str | bytes) -> MasterPlan:
    """Parse and validate Tier 1's JSON. The only entry point Tier 2 should use."""
    try:
        plan = MasterPlan.model_validate_json(raw)
    except ValidationError as err:
        raise MasterPlanError(_violations_from_schema_error(err)) from err
    return validate_master_plan(plan)


def load_master_plan(path: Path) -> MasterPlan:
    """Parse and validate a plan from disk - hand-written fixtures included."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as err:
        raise MasterPlanError(
            [PlanViolation(code="unreadable_plan", where=str(path), message=str(err))]
        ) from err
    return parse_master_plan(raw)


def _violations_from_schema_error(err: ValidationError) -> list[PlanViolation]:
    return [
        PlanViolation(
            code=f"schema.{detail['type']}",
            where=".".join(str(part) for part in detail["loc"]) or "<root>",
            message=detail["msg"],
        )
        for detail in err.errors()
    ]


def _check_edge_endpoints(plan: MasterPlan) -> Iterable[PlanViolation]:
    known = plan.concept_graph.concept_ids
    for edge in plan.concept_graph.edges:
        endpoints = (("prerequisite", edge.prerequisite), ("dependent", edge.dependent))
        for role, concept_id in endpoints:
            if concept_id not in known:
                yield PlanViolation(
                    code="unknown_concept",
                    where=f"edge {edge.prerequisite} -> {edge.dependent}",
                    message=f"{role} '{concept_id}' is not a declared concept",
                )


def _check_edge_evidence(plan: MasterPlan) -> Iterable[PlanViolation]:
    # A cross-reference edge claims the document itself says so. Without the
    # quote and its location that claim is unfalsifiable, which is the one thing
    # an edge must not be (CONTEXT.md §1.5).
    for edge in plan.concept_graph.edges:
        if edge.evidence != "cross_reference":
            continue
        missing = [
            name
            for name, value in (("quote", edge.quote), ("located_at", edge.located_at))
            if value is None
        ]
        if missing:
            yield PlanViolation(
                code="unsupported_cross_reference",
                where=f"edge {edge.prerequisite} -> {edge.dependent}",
                message=f"declared as a cross-reference but missing {' and '.join(missing)}",
            )


def _check_sequence_covers_graph(plan: MasterPlan) -> Iterable[PlanViolation]:
    sequenced = [step.concept_id for step in plan.study_sequence]
    known = plan.concept_graph.concept_ids

    for concept_id in sorted({c for c in sequenced if sequenced.count(c) > 1}):
        yield PlanViolation(
            code="duplicate_step",
            where=concept_id,
            message="appears more than once in the study sequence",
        )
    for concept_id in sorted({c for c in sequenced if c not in known}):
        yield PlanViolation(
            code="unknown_concept",
            where=f"study_sequence:{concept_id}",
            message="sequenced concept is not in the concept graph",
        )
    for concept_id in sorted(known - set(sequenced)):
        yield PlanViolation(
            code="orphan_concept",
            where=concept_id,
            message="in the concept graph but never sequenced, so no builder covers it",
        )


def _check_sequence_positions(plan: MasterPlan) -> Iterable[PlanViolation]:
    # Positions are explicit in the schema, so a plan can disagree with itself.
    # Renumbering silently would change the ordering O5 scores.
    positions = sorted(step.position for step in plan.study_sequence)
    expected = list(range(1, len(plan.study_sequence) + 1))
    if positions != expected:
        yield PlanViolation(
            code="sequence_positions",
            where="study_sequence",
            message=(
                f"positions must be 1..{len(plan.study_sequence)} with no gaps or repeats, "
                f"got {positions}"
            ),
        )


def _check_directives(plan: MasterPlan) -> Iterable[PlanViolation]:
    # A builder sees its directive and nothing else, so a placeholder directive
    # does not fail - it produces a confident section about nothing.
    for step in plan.study_sequence:
        yield from _check_instruction(
            text=step.directive,
            code="placeholder_directive",
            where=f"study_sequence[{step.position}]:{step.concept_id}",
            noun="directive",
        )
    for note in plan.reordering_rationale:
        yield from _check_instruction(
            text=note.reason,
            code="placeholder_rationale",
            where=f"reordering_rationale:{note.concept_id}",
            noun="reason",
        )


def _check_instruction(*, text: str, code: str, where: str, noun: str) -> Iterable[PlanViolation]:
    stripped = text.strip().strip(".!?-_ ").lower()
    if stripped in PLACEHOLDERS or _PLACEHOLDER_PREFIX.match(text.strip()):
        yield PlanViolation(
            code=code,
            where=where,
            message=f"{noun} is placeholder text: {text!r}",
        )
    elif len(text.strip()) < MIN_DIRECTIVE_CHARS:
        yield PlanViolation(
            code=code,
            where=where,
            message=(
                f"{noun} is {len(text.strip())} characters, under the "
                f"{MIN_DIRECTIVE_CHARS} needed to brief a builder: {text!r}"
            ),
        )


def _check_sequence_respects_edges(plan: MasterPlan) -> Iterable[PlanViolation]:
    order = {concept_id: i for i, concept_id in enumerate(plan.ordered_concept_ids)}
    for edge in plan.concept_graph.edges:
        before = order.get(edge.prerequisite)
        after = order.get(edge.dependent)
        if before is None or after is None:
            continue  # already reported as an unknown concept
        if before > after:
            yield PlanViolation(
                code="ordering_violation",
                where=f"edge {edge.prerequisite} -> {edge.dependent}",
                message=(
                    f"'{edge.dependent}' is taught at position {after + 1}, before its "
                    f"prerequisite '{edge.prerequisite}' at position {before + 1}"
                ),
            )


def _check_rationale(plan: MasterPlan, *, positions_usable: bool) -> Iterable[PlanViolation]:
    known = plan.concept_graph.concept_ids
    plan_index = {concept_id: i for i, concept_id in enumerate(plan.ordered_concept_ids)}
    book_index = {concept_id: i for i, concept_id in enumerate(plan.book_ordered_concept_ids)}
    explained: set[str] = set()

    for note in plan.reordering_rationale:
        if note.concept_id not in known:
            yield PlanViolation(
                code="unknown_concept",
                where=f"reordering_rationale:{note.concept_id}",
                message="rationale refers to a concept that is not in the graph",
            )
            continue
        if note.concept_id in explained:
            yield PlanViolation(
                code="duplicate_rationale",
                where=note.concept_id,
                message="explained more than once; a concept makes at most one move",
            )
        explained.add(note.concept_id)
        if positions_usable:
            yield from _check_note_agrees_with_plan(plan, note, plan_index)

    # The reordering is the claim (O5). A concept that moved without a stated
    # reason is a result nobody can defend in review, so it is refused here
    # rather than discovered during the write-up.
    if not positions_usable:
        return
    for concept_id, position in plan_index.items():
        if concept_id in explained or concept_id not in book_index:
            continue
        if book_index[concept_id] != position:
            # The move is DETECTED by comparing ranks, but the note that repairs it is
            # VALIDATED against the concept's absolute `source.book_position` (see
            # `_check_note_agrees_with_plan`). Those are different numbers whenever the
            # plan's concepts come from non-consecutive sections, which is the normal
            # case once ingest/ supplies real ordinals. Reporting the rank made this
            # message prompt a note the boundary then rejected with `rationale_mismatch`
            # - and since that rejection is itself the next repair prompt, the loop did
            # not terminate. Quote the number the boundary actually compares.
            concept = plan.concept_graph.concept(concept_id)
            from_book_position = (
                concept.source.book_position if concept is not None else book_index[concept_id]
            )
            yield PlanViolation(
                code="unexplained_move",
                where=concept_id,
                message=(
                    f"moved from book position {from_book_position} to plan position "
                    f"{position + 1} with no entry in reordering_rationale"
                ),
            )


def _check_note_agrees_with_plan(
    plan: MasterPlan,
    note: ReorderNote,
    plan_index: Mapping[str, int],
) -> Iterable[PlanViolation]:
    """A note that disagrees with the sequence it describes is worse than none."""
    concept_id = note.concept_id
    actual_position = plan_index[concept_id] + 1
    if note.to_plan_position != actual_position:
        yield PlanViolation(
            code="rationale_mismatch",
            where=concept_id,
            message=(
                f"rationale claims plan position {note.to_plan_position}, "
                f"the sequence puts it at {actual_position}"
            ),
        )
    concept = plan.concept_graph.concept(concept_id)
    if concept is not None and note.from_book_position != concept.source.book_position:
        yield PlanViolation(
            code="rationale_mismatch",
            where=concept_id,
            message=(
                f"rationale claims book position {note.from_book_position}, "
                f"the concept's section is at {concept.source.book_position}"
            ),
        )


def _adjacency(plan: MasterPlan) -> Mapping[str, tuple[str, ...]]:
    known = plan.concept_graph.concept_ids
    edges: dict[str, list[str]] = {concept_id: [] for concept_id in known}
    for edge in plan.concept_graph.edges:
        if edge.prerequisite in known and edge.dependent in known:
            edges[edge.prerequisite].append(edge.dependent)
    return {node: tuple(sorted(targets)) for node, targets in edges.items()}


def _find_cycle(adjacency: Mapping[str, tuple[str, ...]]) -> tuple[str, ...] | None:
    """Return one cycle as a closed path, or None.

    One cycle rather than all of them: the repair loop is fix-and-revalidate, and
    enumerating every cycle in a cyclic graph is not more actionable.
    """
    visited: set[str] = set()
    on_path: list[str] = []
    in_path: set[str] = set()

    def walk(node: str) -> tuple[str, ...] | None:
        visited.add(node)
        on_path.append(node)
        in_path.add(node)
        for target in adjacency.get(node, ()):
            if target in in_path:
                start = on_path.index(target)
                return (*on_path[start:], target)
            if target not in visited and (found := walk(target)) is not None:
                return found
        on_path.pop()
        in_path.discard(node)
        return None

    for node in sorted(adjacency):
        if node not in visited and (cycle := walk(node)) is not None:
            return cycle
    return None
