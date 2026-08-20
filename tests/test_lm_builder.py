"""Tests for the model-backed Tier 2 builder, driven offline.

The point of these is the seam, not the text: `LmBuilder` is typed against a
structural `LanguageModel` protocol rather than against the RLM library, so the
one thing worth proving is that the library's own client actually satisfies it.
That is what `MockLM` is doing here — it is the RLM library's class, not a
double we wrote to agree with ourselves (TRACK2.md: `LocalREPL` + `MockLM` runs
the whole path with no keys).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from orchestrate import BuilderBrief, LanguageModel, LmBuilder, execute_plan_sync, prompt_for
from plan import EXAMPLE_PLAN_PATH, load_master_plan
from runlog import RunLogger

VENDORED_RLM = Path(__file__).resolve().parents[1] / ".vendor" / "rlm"


def _mock_lm_class():
    """Load the RLM library's own MockLM, which ships in its tests rather than its package."""
    pytest.importorskip("rlm", reason="the vendored RLM editable install is not importable")
    spec = importlib.util.spec_from_file_location(
        "_rlm_mock_lm", VENDORED_RLM / "tests" / "mock_lm.py"
    )
    if spec is None or spec.loader is None:
        pytest.skip(f"no MockLM at {VENDORED_RLM}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.MockLM


@pytest.fixture
def plan():
    return load_master_plan(EXAMPLE_PLAN_PATH)


@pytest.fixture
def logger(tmp_path):
    return RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="ostep",
        seed=11,
        models={"tier2": "mock-model"},
    )


def test_the_rlm_librarys_client_satisfies_our_protocol():
    # If this breaks, W2's real client will not drop in where the stub sits.
    mock_lm = _mock_lm_class()()
    assert isinstance(mock_lm, LanguageModel)


def test_a_plan_runs_end_to_end_through_a_model_client_with_no_keys(plan, logger):
    responses = [f"section {i}" for i in range(1, len(plan.study_sequence) + 1)]
    builder = LmBuilder(lm=_mock_lm_class()(responses=responses), name="mock")
    artefact = execute_plan_sync(plan, builder, logger)

    assert artefact.concept_order == plan.ordered_concept_ids
    assert all(span.provenance.builder == "mock" for span in artefact.spans)
    assert artefact.text.startswith("section 1")


def test_the_model_is_asked_for_one_section_and_told_not_to_summarise(plan):
    brief = _brief(plan, index=2)
    prompt = prompt_for(brief)

    assert brief.concept.label in prompt
    assert brief.directive in prompt
    assert "Write only this section" in prompt
    # The whole cost argument rests on a builder never seeing the rest of the plan.
    for other in plan.ordered_concept_ids:
        if other != brief.concept.id:
            assert other not in prompt


def _brief(plan, index: int) -> BuilderBrief:
    from orchestrate import briefs_for

    return briefs_for(plan)[index]
