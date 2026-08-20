"""Tests for the Tier 2 stub and the fork-join contract.

Two properties are worth testing before there is a real builder behind the
interface: that a builder is given its own concept and nothing else, and that
the joined artefact is in Master-Plan order no matter what order the builders
finish in. Both are claims the paper makes; neither is obvious from the code
once a worker pool is in front of them.
"""

from __future__ import annotations

import asyncio

import pytest

from orchestrate import (
    Artefact,
    BuilderBrief,
    BuiltSpan,
    Provenance,
    StubBuilder,
    briefs_for,
    execute_plan_sync,
    join_in_plan_order,
)
from plan import EXAMPLE_PLAN_PATH, MasterPlanError, load_master_plan
from runlog import RunLogger, load_run


@pytest.fixture
def plan():
    return load_master_plan(EXAMPLE_PLAN_PATH)


@pytest.fixture
def logger(tmp_path):
    """Every run is logged, so every test that runs one has to log it too."""
    return RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="ostep",
        seed=11,
        models={"tier2": "stub"},
    )


class ReverseFinishingBuilder:
    """Finishes in reverse plan order, to prove the join does not trust arrival order."""

    name = "reverse"

    def __init__(self, total: int) -> None:
        self._total = total

    async def build(self, brief: BuilderBrief) -> BuiltSpan:
        # Later steps return first. Any join that appends on completion produces
        # a backwards artefact and this test catches it.
        await asyncio.sleep(0.001 * (self._total - brief.position))
        return BuiltSpan(
            concept_id=brief.concept.id,
            position=brief.position,
            text=brief.concept.id,
            provenance=Provenance(
                document_id=brief.document_id,
                section_id=brief.section_id,
                page_start=brief.concept.source.page_start,
                page_end=brief.concept.source.page_end,
                plan_position=brief.position,
                builder=self.name,
            ),
        )


class FailingBuilder:
    name = "failing"

    async def build(self, brief: BuilderBrief) -> BuiltSpan:
        raise RuntimeError(f"builder for {brief.concept.id} died")


def test_the_example_plan_passes_the_boundary(plan):
    assert plan.document_id == "ostep"
    assert len(plan.study_sequence) == 6


def test_one_brief_per_step_in_plan_order(plan):
    briefs = briefs_for(plan)
    assert [b.position for b in briefs] == [1, 2, 3, 4, 5, 6]
    assert tuple(b.concept.id for b in briefs) == plan.ordered_concept_ids


def test_a_builder_sees_its_own_concept_and_directive_and_nothing_else(plan):
    brief = briefs_for(plan)[2]
    fields = set(vars(brief))
    # If this set grows, the two-tier cost model changes with it.
    assert fields == {"document_id", "position", "concept", "directive"}
    assert brief.concept.id == "address-spaces"
    assert brief.directive == plan.study_sequence[2].directive


def test_the_artefact_is_in_plan_order_not_book_order(plan, logger):
    artefact = execute_plan_sync(plan, StubBuilder(), logger)
    assert artefact.concept_order == plan.ordered_concept_ids
    assert artefact.concept_order != plan.book_ordered_concept_ids


def test_completion_order_does_not_change_the_artefact(plan, logger):
    fast = execute_plan_sync(plan, StubBuilder(), logger)
    reversed_finish = execute_plan_sync(
        plan, ReverseFinishingBuilder(len(plan.study_sequence)), logger
    )
    assert reversed_finish.concept_order == fast.concept_order == plan.ordered_concept_ids


def test_every_span_carries_a_provenance_pointer(plan, logger):
    artefact = execute_plan_sync(plan, StubBuilder(), logger)
    for span in artefact.spans:
        concept = plan.concept_graph.concept(span.concept_id)
        assert span.provenance.section_id == concept.source.section_id
        assert span.provenance.page_start == concept.source.page_start
        assert span.provenance.plan_position == span.position
        assert span.provenance.builder == "stub"


def test_the_stub_is_deterministic(plan, logger):
    assert execute_plan_sync(plan, StubBuilder(), logger) == execute_plan_sync(
        plan, StubBuilder(), logger
    )


def test_an_invalid_plan_never_reaches_a_builder(plan, logger):
    broken = plan.model_copy(update={"reordering_rationale": ()})
    with pytest.raises(MasterPlanError):
        execute_plan_sync(broken, StubBuilder(), logger)


def test_a_failing_builder_is_not_silently_swallowed(plan, logger):
    # W1 has no retry policy; taking the run down is the honest behaviour until
    # W2 adds one. This test exists so that adding isolation is a deliberate act.
    with pytest.raises(RuntimeError):
        execute_plan_sync(plan, FailingBuilder(), logger)


def test_join_sorts_spans_that_arrive_shuffled():
    spans = [
        BuiltSpan(concept_id=f"c{i}", position=i, text=str(i), provenance=_p(i)) for i in (3, 1, 2)
    ]
    artefact = join_in_plan_order(spans, "ostep")
    assert isinstance(artefact, Artefact)
    assert artefact.concept_order == ("c1", "c2", "c3")
    assert artefact.text == "1\n\n2\n\n3"


def test_the_run_is_logged_with_the_join_order_and_provenance(plan, logger):
    artefact = execute_plan_sync(plan, StubBuilder(), logger)
    logger.close()

    run = load_run(logger.run_dir)
    joins = [e for e in run["events"] if e["kind"] == "tier2_join"]
    assert len(joins) == 1
    # The join order is the O5 claim; it has to be readable from the log alone.
    assert joins[0]["concept_order"] == list(artefact.concept_order)
    assert {p["section_id"] for p in joins[0]["provenance"]} == {
        c.source.section_id for c in plan.concept_graph.concepts
    }
    assert (logger.run_dir / "artefacts" / "tier2_output.md").exists()


def test_a_run_cannot_be_executed_without_a_logger(plan):
    # Not a style preference: CLAUDE.md admits no unlogged runs, so the omission
    # has to be a type error rather than a habit anyone can fall out of.
    with pytest.raises(TypeError):
        execute_plan_sync(plan, StubBuilder())  # type: ignore[call-arg]


def _p(position: int) -> Provenance:
    return Provenance(
        document_id="ostep",
        section_id="ch01",
        page_start=1,
        page_end=2,
        plan_position=position,
        builder="test",
    )
