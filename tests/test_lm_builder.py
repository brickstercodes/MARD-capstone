"""Tests for the model-backed Tier 2 builder, driven offline.

The point of these is the seam, not the text: `LmBuilder` is typed against a
structural `LanguageModel` protocol rather than against the RLM library, so the
one thing worth proving is that the library's own client actually satisfies it.
That is what `MockLM` is doing here — it is the RLM library's class, not a double
we wrote to agree with ourselves (TRACK2.md: `LocalREPL` + `MockLM` runs the
whole path with no keys).

These tests do not skip when `import rlm` fails. `.vendor/rlm` is gitignored, so
a clone that has never run `scripts/bootstrap_rlm.sh` legitimately has no library
to test against and skipping is honest. A vendored copy that is present but not
importable is a different thing entirely — that is the editable-install breakage
of 4 Aug, and a skip there deletes the only test of the seam while the suite
still reports green.
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
MOCK_LM_PATH = VENDORED_RLM / "tests" / "mock_lm.py"


def _import_rlm_or_explain() -> None:
    """Make the vendored library importable, or say which of the two cases this is."""
    try:
        import rlm  # noqa: F401
    except ImportError:
        pass
    else:
        return

    if not VENDORED_RLM.exists():
        pytest.skip(
            f"no vendored RLM at {VENDORED_RLM} - run scripts/bootstrap_rlm.sh to test the seam"
        )

    # Present but not importable: the editable install is broken, not absent.
    # Import it from the vendored tree so the seam is still tested; check.sh is
    # what fails on the broken install, loudly, in one place.
    sys.path.insert(0, str(VENDORED_RLM))
    try:
        import rlm  # noqa: F401
    except ImportError as err:  # pragma: no cover - a vendored copy that cannot load at all
        pytest.fail(f"vendored RLM at {VENDORED_RLM} exists but will not import: {err}")


def _mock_lm_class():
    """Load the RLM library's own MockLM, which ships in its tests rather than its package."""
    _import_rlm_or_explain()
    if not MOCK_LM_PATH.exists():
        pytest.fail(f"vendored RLM has no MockLM at {MOCK_LM_PATH}")
    spec = importlib.util.spec_from_file_location("_rlm_mock_lm", MOCK_LM_PATH)
    if spec is None or spec.loader is None:
        pytest.fail(f"could not load MockLM from {MOCK_LM_PATH}")
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
