"""Load OOLONG's own scoring functions from the vendored base-paper harness.

`docs/42-HANDOFF_REPRODUCTION_AND_SECOND_DOCUMENT.md` §1.3: "a check scored by a
reimplemented metric tells you nothing about the implementation under test" — so this
module imports `_synth_score`/`_attempt_answer_parse` from
`.vendor/rlm/training/environments/oolong/oolong/env.py` rather than re-deriving them.

That file's own top-level imports pull in `rlm_train`, `verifiers` and `datasets` —
training-framework packages this repo has no other use for and does not install.
Reading the file confirms none of the three is touched by `_synth_score` or
`_attempt_answer_parse`: `rlm_train` and `verifiers` (`vf`) are only referenced inside
`load_environment()`'s body, which this module never calls, and `_score`'s `vf.State`
annotation is never evaluated at import time because the file starts with
`from __future__ import annotations`; `datasets` is only used inside `_build_dataset`,
also never called here. They are stubbed as empty placeholder modules purely so the
`import`/`from ... import` statements at the top of the file succeed — not to fake any
behaviour the scorer depends on. `python-dateutil`, which the scorer's `ANSWER_TYPE.DATE`
branch genuinely calls, is a real dependency and is actually installed, not stubbed.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_ENV_PATH = (
    Path(__file__).resolve().parents[1]
    / ".vendor"
    / "rlm"
    / "training"
    / "environments"
    / "oolong"
    / "oolong"
    / "env.py"
)


def _load_vendored_env_module() -> types.ModuleType:
    for name in ("rlm_train", "verifiers"):
        sys.modules.setdefault(name, types.ModuleType(name))
    if "datasets" not in sys.modules:
        datasets_stub = types.ModuleType("datasets")
        datasets_stub.Dataset = object  # type: ignore[attr-defined] # unused stub attr
        datasets_stub.load_dataset = lambda *a, **k: None  # type: ignore[attr-defined]
        sys.modules["datasets"] = datasets_stub

    spec = importlib.util.spec_from_file_location("_vendored_oolong_env", _ENV_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load vendored OOLONG env module from {_ENV_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_env = _load_vendored_env_module()

synth_score = _env._synth_score
"""`(datapoint: dict, output: str) -> float` — verbatim from the vendored base-paper harness."""

attempt_answer_parse = _env._attempt_answer_parse
"""`(answer: str) -> tuple[str, str]` — verbatim from the vendored base-paper harness."""
