"""Tests for the vanilla-RLM control arm (`vanilla/run.py`).

Zhang_RLM has no client-injection seam (`RLM.__init__`'s `backend`/`backend_kwargs`
always builds its own `openai` client internally — see `vanilla/run.py`'s and
`vanilla/openai_logging_bridge.py`'s module docstrings), unlike `replm`'s
`RLMWrapper(client=...)` or MARD's own structural `LanguageModel` protocol
(`tests/test_lm_builder.py`). So these tests do not attempt to drive a real `RLM`
completion offline the way `test_lm_builder.py` does with the library's own `MockLM`.
Instead they patch `vanilla.run.RLM` at the boundary and assert *our* wrapper code —
manifest verification, page splitting, the frozen prompt, logging, truncation
detection, 429 visibility — behaves correctly, which is what this module actually
owns. The seam to the real library is exercised by the (unmocked) construction test
below and, later, by the smoke test against a real API key.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from rlm.core.types import ModelUsageSummary, RLMChatCompletion, UsageSummary
from rlm.logger.rlm_logger import RLMLogger
from rlm.utils.exceptions import TokenLimitExceededError

from ingest.manifest import SourceRecord, write_manifest
from runlog import RunLogger
from vanilla.openai_logging_bridge import rate_limit_visibility
from vanilla.run import (
    FROZEN_STUDY_GUIDE_PROMPT,
    _count_concepts,
    _log_root_trajectory,
    _log_subcall_detail,
    _reconcile_usage,
    _walk_subcalls,
    run_vanilla_rlm,
    split_pages,
    zhang_rlm_fork_sha,
)

SOURCE = SourceRecord(
    file_name="book.pdf",
    sha256="0" * 64,
    bytes=1234,
    page_count=3,
    url="https://example.invalid/book.pdf",
    retrieved_on="2026-08-27",
)


def _corpus(tmp_path: Path, *, document_text: str, with_manifest: bool = True) -> Path:
    root = tmp_path / "corpus"
    target = root / "introcs"
    target.mkdir(parents=True)
    (target / "document.txt").write_text(document_text, encoding="utf-8")
    (target / "document.jsonl").write_text('{"block_id": "b1"}\n', encoding="utf-8")
    (target / "outline.json").write_text('{"entries": []}', encoding="utf-8")
    (target / "sections.json").write_text("[]", encoding="utf-8")
    (target / "chapters.json").write_text("[]", encoding="utf-8")
    (target / "parse_quality.json").write_text("{}", encoding="utf-8")
    if with_manifest:
        write_manifest(target, "introcs", SOURCE)
    return root


def _fake_completion(*, root_model: str, sub_model: str, answer: str = "study guide") -> Any:
    return RLMChatCompletion(
        root_model=root_model,
        prompt=["p1", "p2"],
        response=answer,
        usage_summary=UsageSummary(
            model_usage_summaries={
                root_model: ModelUsageSummary(
                    total_calls=3, total_input_tokens=1000, total_output_tokens=200, total_cost=0.05
                ),
                sub_model: ModelUsageSummary(
                    total_calls=7, total_input_tokens=3000, total_output_tokens=900, total_cost=0.02
                ),
            }
        ),
        execution_time=12.5,
        metadata=None,
    )


@pytest.fixture
def logger(tmp_path):
    with RunLogger.start(
        runs_root=tmp_path / "runs",
        system="vanilla_rlm",
        document_id="introcs",
        seed=11,
        models={"root": "gpt-5.2", "sub": "gpt-5-mini"},
    ) as run:
        yield run


# --------------------------------------------------------------------- split_pages


def test_split_pages_rejects_a_single_chunk() -> None:
    with pytest.raises(ValueError, match="multiple"):
        split_pages("no markers here at all")


def test_split_pages_rejects_a_lone_marker() -> None:
    with pytest.raises(ValueError):
        split_pages("[[page:1]]only one chunk")


def test_split_pages_returns_the_non_empty_chunks_in_order() -> None:
    pages = split_pages("[[page:1]]first[[page:2]]second[[page:3]]  ")
    assert pages == ["first", "second"]


# ------------------------------------------------------------------------- fork sha


def test_zhang_rlm_fork_sha_reads_a_fixture_repo(tmp_path: Path) -> None:
    repo = tmp_path / "fixture_rlm"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    (repo / "f.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "f.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=repo, check=True)
    expected = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert zhang_rlm_fork_sha(repo) == expected


def test_zhang_rlm_fork_sha_returns_none_for_a_non_git_dir(tmp_path: Path) -> None:
    assert zhang_rlm_fork_sha(tmp_path) is None


# --------------------------------------------------------------------- frozen prompt


def test_frozen_prompt_matches_docs21_verbatim() -> None:
    # Regression guard: this string is paper content (docs/21 §3.1) and must never
    # drift from what was signed off, even by an "obvious" wording cleanup.
    assert FROZEN_STUDY_GUIDE_PROMPT == (
        "Using the textbook available in `context`, write a study guide for a learner "
        "meeting this material for the first time. Identify the concepts the textbook "
        "teaches and, for each one, write an explanation the learner can study from. "
        "Order the guide so that a concept is explained only after anything it depends "
        "on has been explained. Output the study guide itself, with no commentary about "
        "your process."
    )


# ----------------------------------------------------------- run_vanilla_rlm wiring


def test_manifest_is_verified_before_the_library_is_ever_touched(
    tmp_path: Path, logger: RunLogger, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_dir = _corpus(tmp_path, document_text="[[page:1]]a[[page:2]]b", with_manifest=False)
    never_called = MagicMock(side_effect=AssertionError("RLM must not be constructed"))
    monkeypatch.setattr("vanilla.run.RLM", never_called)

    with pytest.raises(FileNotFoundError, match="manifest"):
        run_vanilla_rlm(
            corpus_dir, "introcs", root_model="gpt-5.2", sub_model="gpt-5-mini", logger=logger
        )
    never_called.assert_not_called()


def test_a_single_page_document_is_refused_before_the_library_is_touched(
    tmp_path: Path, logger: RunLogger, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_dir = _corpus(tmp_path, document_text="just one chunk, no markers")
    never_called = MagicMock(side_effect=AssertionError("RLM must not be constructed"))
    monkeypatch.setattr("vanilla.run.RLM", never_called)

    with pytest.raises(ValueError, match="multiple"):
        run_vanilla_rlm(
            corpus_dir, "introcs", root_model="gpt-5.2", sub_model="gpt-5-mini", logger=logger
        )
    never_called.assert_not_called()


def test_the_task_is_passed_as_root_prompt_never_folded_into_the_pages(
    tmp_path: Path, logger: RunLogger, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The vanilla arm's own version of tests/test_envelope.py's guard: the frozen
    task string rides in `root_prompt`, and nothing envelope-shaped ever does."""
    corpus_dir = _corpus(tmp_path, document_text="[[page:1]]alpha[[page:2]]beta[[page:3]]gamma")
    fake_rlm_instance = MagicMock()
    fake_rlm_instance.completion.return_value = _fake_completion(
        root_model="gpt-5.2", sub_model="gpt-5-mini"
    )
    fake_rlm_class = MagicMock(return_value=fake_rlm_instance)
    monkeypatch.setattr("vanilla.run.RLM", fake_rlm_class)

    run_vanilla_rlm(
        corpus_dir, "introcs", root_model="gpt-5.2", sub_model="gpt-5-mini", logger=logger
    )

    _, call_kwargs = fake_rlm_instance.completion.call_args
    assert call_kwargs["root_prompt"] == FROZEN_STUDY_GUIDE_PROMPT
    assert call_kwargs["prompt"] == ["alpha", "beta", "gamma"]
    # The construction kwargs are the other half of the boundary: max_depth fixed,
    # sub-call model routed through other_backends, never through root's own kwargs.
    _, construct_kwargs = fake_rlm_class.call_args
    assert construct_kwargs["max_depth"] == 1
    assert construct_kwargs["other_backend_kwargs"][0]["model_name"] == "gpt-5-mini"
    assert construct_kwargs["backend_kwargs"]["model_name"] == "gpt-5.2"


def test_a_limit_exceeded_error_is_logged_and_the_run_is_recorded_failed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_dir = _corpus(tmp_path, document_text="[[page:1]]a[[page:2]]b")
    fake_rlm_instance = MagicMock()
    fake_rlm_instance.completion.side_effect = TokenLimitExceededError(
        tokens_used=999_999, token_limit=500_000
    )
    monkeypatch.setattr("vanilla.run.RLM", MagicMock(return_value=fake_rlm_instance))

    runs_root = tmp_path / "runs"
    with (
        pytest.raises(TokenLimitExceededError),
        RunLogger.start(
            runs_root=runs_root,
            system="vanilla_rlm",
            document_id="introcs",
            seed=11,
            models={"root": "gpt-5.2", "sub": "gpt-5-mini"},
        ) as run,
    ):
        run_vanilla_rlm(
            corpus_dir, "introcs", root_model="gpt-5.2", sub_model="gpt-5-mini", logger=run
        )

    fake_rlm_instance.close.assert_called_once()
    run_dir = next(runs_root.iterdir())
    summary = __import__("json").loads((run_dir / "summary.json").read_text())
    assert summary["status"] == "failed"
    assert "TokenLimitExceededError" in summary["error"]["traceback"]
    events = [
        __import__("json").loads(line)
        for line in (run_dir / "events.jsonl").read_text().splitlines()
    ]
    assert any(e["kind"] == "vanilla_limit_exceeded" for e in events)


def test_usage_is_logged_per_model_and_the_answer_is_saved(
    tmp_path: Path, logger: RunLogger, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus_dir = _corpus(tmp_path, document_text="[[page:1]]a[[page:2]]b")
    fake_rlm_instance = MagicMock()
    fake_rlm_instance.completion.return_value = _fake_completion(
        root_model="gpt-5.2", sub_model="gpt-5-mini", answer="the study guide text"
    )
    monkeypatch.setattr("vanilla.run.RLM", MagicMock(return_value=fake_rlm_instance))

    response = run_vanilla_rlm(
        corpus_dir, "introcs", root_model="gpt-5.2", sub_model="gpt-5-mini", logger=logger
    )
    assert response.response == "the study guide text"

    totals = logger.totals()
    assert totals["calls"] == 2  # one aggregate log_call per model
    assert totals["input_tokens"] == 1000 + 3000
    assert totals["output_tokens"] == 200 + 900

    answer_path = logger.run_dir / "artefacts" / "vanilla_answer.md"
    assert answer_path.read_text(encoding="utf-8") == "the study guide text"


# --------------------------------------------------------------- truncation flagging


class _FakeRunLogger:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def log_event(self, kind: str, payload: dict[str, Any] | None = None) -> None:
        self.events.append((kind, payload or {}))


def test_truncation_is_flagged_when_max_iterations_is_hit_without_a_final_answer() -> None:
    trajectory_logger = RLMLogger()
    from rlm.core.types import RLMMetadata

    trajectory_logger.log_metadata(
        RLMMetadata(
            root_model="gpt-5.2",
            max_depth=1,
            max_iterations=2,
            backend="openai",
            backend_kwargs={},
            environment_type="local",
            environment_kwargs={},
        )
    )
    from rlm.core.types import RLMIteration

    for _ in range(2):
        trajectory_logger.log(
            RLMIteration(prompt="p", response="still working", code_blocks=[], final_answer=None)
        )

    fake_logger = _FakeRunLogger()
    _log_root_trajectory(fake_logger, trajectory_logger, max_iterations=2)  # type: ignore[arg-type]

    assert any(kind == "vanilla_truncated" for kind, _ in fake_logger.events)


def test_no_truncation_flag_when_a_final_answer_is_reached_early() -> None:
    trajectory_logger = RLMLogger()
    from rlm.core.types import RLMIteration, RLMMetadata

    trajectory_logger.log_metadata(
        RLMMetadata(
            root_model="gpt-5.2",
            max_depth=1,
            max_iterations=30,
            backend="openai",
            backend_kwargs={},
            environment_type="local",
            environment_kwargs={},
        )
    )
    trajectory_logger.log(
        RLMIteration(prompt="p", response="done", code_blocks=[], final_answer="the answer")
    )

    fake_logger = _FakeRunLogger()
    _log_root_trajectory(fake_logger, trajectory_logger, max_iterations=30)  # type: ignore[arg-type]

    assert not any(kind == "vanilla_truncated" for kind, _ in fake_logger.events)


# --------------------------------------------------------------- 429/retry visibility


def test_a_429_response_log_record_is_captured() -> None:
    fake_logger = _FakeRunLogger()
    openai_logger = logging.getLogger("openai")
    with rate_limit_visibility(fake_logger):
        openai_logger.debug(
            'HTTP Response: %s %s "%i %s" %s',
            "POST",
            "https://api.openai.com/v1/chat/completions",
            429,
            "Too Many Requests",
            {},
        )

    kinds = [kind for kind, _ in fake_logger.events]
    assert "vanilla_rate_limited" in kinds
    payload = next(p for k, p in fake_logger.events if k == "vanilla_rate_limited")
    assert payload["status_code"] == 429


def test_a_retry_decision_log_record_is_captured() -> None:
    fake_logger = _FakeRunLogger()
    openai_logger = logging.getLogger("openai")
    with rate_limit_visibility(fake_logger):
        openai_logger.info(
            "Retrying request to %s in %f seconds",
            "https://api.openai.com/v1/chat/completions",
            1.5,
        )

    payload = next(p for k, p in fake_logger.events if k == "vanilla_retry")
    assert payload["delay_seconds"] == 1.5


def test_a_200_response_is_not_logged_as_a_rate_limit() -> None:
    fake_logger = _FakeRunLogger()
    openai_logger = logging.getLogger("openai")
    with rate_limit_visibility(fake_logger):
        openai_logger.debug(
            'HTTP Response: %s %s "%i %s" %s',
            "POST",
            "https://api.openai.com/v1/chat/completions",
            200,
            "OK",
            {},
        )
    assert not fake_logger.events


# ------------------------------------------------------------- construction sanity


def test_the_wrapper_constructs_a_real_rlm_instance_with_no_network_call() -> None:
    """Not mocked: proves the exact kwargs vanilla/run.py passes are accepted by the
    real vendored RLM constructor. RLM.__init__ does not touch the network or
    require an API key (client construction is deferred to call time), so this is
    safe to run without keys."""
    from rlm.core.rlm import RLM

    instance = RLM(
        backend="openai",
        backend_kwargs={"model_name": "gpt-5.2", "max_retries": 5},
        other_backends=["openai"],
        other_backend_kwargs=[{"model_name": "gpt-5-mini", "max_retries": 5}],
        max_depth=1,
        max_iterations=30,
        max_concurrent_subcalls=4,
        sampling_args=None,
        sub_sampling_args=None,
        on_subcall_start=lambda depth, model, preview: None,
        on_subcall_complete=lambda depth, model, duration, error: None,
        logger=RLMLogger(),
        verbose=False,
    )
    instance.close()


# -------------------------------------------------------- subcall trajectory walk


def _fake_subcall(
    *,
    model: str,
    prompt: str,
    response: str,
    execution_time: float,
    input_tokens: int,
    output_tokens: int,
) -> RLMChatCompletion:
    return RLMChatCompletion(
        root_model=model,
        prompt=prompt,
        response=response,
        usage_summary=UsageSummary(
            model_usage_summaries={
                model: ModelUsageSummary(
                    total_calls=1,
                    total_input_tokens=input_tokens,
                    total_output_tokens=output_tokens,
                )
            }
        ),
        execution_time=execution_time,
    )


def _trajectory_with_subcalls(subcalls: list[RLMChatCompletion]) -> dict[str, Any]:
    from rlm.core.types import CodeBlock, REPLResult, RLMIteration

    result = REPLResult(stdout="", stderr="", locals={}, execution_time=1.0, rlm_calls=subcalls)
    block = CodeBlock(code="rlm_query(...)", result=result)
    iteration = RLMIteration(
        prompt="p", response="r", code_blocks=[block], final_answer="done", iteration_time=1.0
    )
    return {"run_metadata": {}, "iterations": [iteration.to_dict()]}


def test_walk_subcalls_flattens_across_iterations_and_code_blocks() -> None:
    a = _fake_subcall(
        model="gpt-5-mini",
        prompt="p1",
        response="r1",
        execution_time=2.0,
        input_tokens=100,
        output_tokens=20,
    )
    b = _fake_subcall(
        model="gpt-5-mini",
        prompt="p2",
        response="r2",
        execution_time=5.0,
        input_tokens=300,
        output_tokens=40,
    )
    trajectory = _trajectory_with_subcalls([a, b])
    calls = _walk_subcalls(trajectory)
    assert len(calls) == 2
    assert {c["prompt"] for c in calls} == {"p1", "p2"}


def test_walk_subcalls_handles_no_trajectory() -> None:
    assert _walk_subcalls(None) == []
    assert _walk_subcalls({"iterations": []}) == []


def test_log_subcall_detail_computes_real_max_and_sum_wall_clock(tmp_path: Path) -> None:
    a = _fake_subcall(
        model="gpt-5-mini",
        prompt="p1",
        response="r1",
        execution_time=2.0,
        input_tokens=100,
        output_tokens=20,
    )
    b = _fake_subcall(
        model="gpt-5-mini",
        prompt="p2",
        response="r2",
        execution_time=5.0,
        input_tokens=300,
        output_tokens=40,
    )
    trajectory = _trajectory_with_subcalls([a, b])

    with RunLogger.start(
        runs_root=tmp_path,
        system="vanilla_rlm",
        document_id="introcs",
        seed=11,
        models={"root": "gpt-5.2", "sub": "gpt-5-mini"},
    ) as run:
        detail = _log_subcall_detail(run, trajectory)

    assert detail["subcall_count"] == 2
    assert detail["subcall_wall_clock_max_s"] == 5.0
    assert detail["subcall_wall_clock_sum_s"] == 7.0
    assert detail["granular_totals"]["gpt-5-mini"] == {
        "input_tokens": 400,
        "output_tokens": 60,
        "calls": 2,
    }
    events = [
        __import__("json").loads(line)
        for line in (run.run_dir / "events.jsonl").read_text().splitlines()
    ]
    detail_events = [e for e in events if e["kind"] == "vanilla_subcall_detail"]
    assert len(detail_events) == 2
    assert {e["prompt_preview"] for e in detail_events} == {"p1", "p2"}


def test_reconcile_usage_logs_nothing_when_totals_match(tmp_path: Path) -> None:
    completion = _fake_completion(root_model="gpt-5.2", sub_model="gpt-5-mini")
    # completion's usage_summary has gpt-5-mini: in=3000, out=900 (see _fake_completion)
    subcall_detail = {
        "granular_totals": {"gpt-5-mini": {"input_tokens": 3000, "output_tokens": 900, "calls": 7}}
    }
    with RunLogger.start(
        runs_root=tmp_path,
        system="vanilla_rlm",
        document_id="introcs",
        seed=11,
        models={"root": "gpt-5.2", "sub": "gpt-5-mini"},
    ) as run:
        _reconcile_usage(run, completion, subcall_detail)
    events_path = run.run_dir / "events.jsonl"
    # A clean reconciliation logs nothing at all, so the file may not exist yet.
    events = (
        [__import__("json").loads(line) for line in events_path.read_text().splitlines()]
        if events_path.exists()
        else []
    )
    assert not any(e["kind"] == "vanilla_usage_reconciliation_mismatch" for e in events)


def test_reconcile_usage_flags_a_real_mismatch(tmp_path: Path) -> None:
    completion = _fake_completion(root_model="gpt-5.2", sub_model="gpt-5-mini")
    subcall_detail = {
        "granular_totals": {"gpt-5-mini": {"input_tokens": 1, "output_tokens": 1, "calls": 1}}
    }
    with RunLogger.start(
        runs_root=tmp_path,
        system="vanilla_rlm",
        document_id="introcs",
        seed=11,
        models={"root": "gpt-5.2", "sub": "gpt-5-mini"},
    ) as run:
        _reconcile_usage(run, completion, subcall_detail)
    events = [
        __import__("json").loads(line)
        for line in (run.run_dir / "events.jsonl").read_text().splitlines()
    ]
    mismatches = [e for e in events if e["kind"] == "vanilla_usage_reconciliation_mismatch"]
    assert len(mismatches) == 1
    assert mismatches[0]["model"] == "gpt-5-mini"


# ----------------------------------------------------------------- concept count


def test_count_concepts_counts_numbered_level2_headings() -> None:
    md = "# Study Guide\n\n## 1. First concept\nbody\n\n## 2. Second concept\nbody\n"
    assert _count_concepts(md) == 2


def test_count_concepts_falls_back_to_any_level2_heading_when_unnumbered() -> None:
    md = "# Study Guide\n\n## First concept\nbody\n\n## Second concept\nbody\n"
    assert _count_concepts(md) == 2


def test_count_concepts_returns_zero_for_no_headings() -> None:
    assert _count_concepts("just prose, no structure at all") == 0


def test_count_concepts_prefers_nested_level3_headings_over_chapter_wrappers() -> None:
    # Regression guard for the real seed-23 case: 14 "## Chapter N" wrappers each
    # holding several "### Concept" entries. A ##-only count would report 14 (the
    # wrapper count) — the wrong, and opposite-direction, answer.
    md = (
        "# Study Guide\n\n"
        "## Chapter 1\n### Algorithm\nbody\n### Computer Science\nbody\n\n"
        "## Chapter 2\n### Computational Thinking\nbody\n"
    )
    assert _count_concepts(md) == 3
