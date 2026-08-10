"""Tests for the run logger.

These are deliberately about failure modes rather than happy paths. The harness
is trusted by three other tracks; the cases that matter are the ones where a run
dies halfway, a rate is stale, or nobody recorded a price.
"""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from runlog import ModelRate, RateCard, RunLogger, StaleRateError, load_run, seed_everything
from runlog.run import CALLS_FILE


def _rate(retrieved_on: date) -> ModelRate:
    return ModelRate(
        model="test-frontier",
        input_per_million=1.25,
        output_per_million=10.0,
        currency="USD",
        retrieved_on=retrieved_on,
        source_url="https://example.invalid/pricing",
    )


def test_manifest_records_config_and_seed(tmp_path):
    with RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="ostep",
        seed=42,
        models={"tier1": "test-frontier", "tier2": "test-budget"},
        params={"depth": 2},
    ) as run:
        run_dir = run.run_dir

    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["config"]["seed"] == 42
    assert manifest["config"]["system"] == "mard"
    assert manifest["config"]["params"]["depth"] == 2
    assert manifest["seeding"]["python_random"] is True
    # Environment capture is what makes a run explainable months later.
    assert manifest["config"]["environment"]["python"]


def test_calls_and_envelopes_are_recorded(tmp_path):
    with RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="axler",
        seed=11,
        models={"tier1": "test-frontier"},
    ) as run:
        root_id = run.log_call(
            role="tier1",
            model="test-frontier",
            prompt="skeleton please",
            response="{...}",
            input_tokens=500,
            output_tokens=120,
            depth=0,
        )
        run.log_call(
            role="tier2",
            model="test-frontier",
            prompt="section 3",
            response="text",
            input_tokens=200,
            output_tokens=800,
            depth=1,
            parent_call_id=root_id,
        )
        run.log_envelope(0, {"sections": [{"title": "Vector Spaces", "pages": [1, 30]}]})
        run.set_result({"task_score": 0.71})

    loaded = load_run(run.run_dir)
    assert len(loaded["calls"]) == 2
    assert loaded["calls"][1]["parent_call_id"] == root_id
    assert loaded["envelopes"]["pass_0"]["sections"][0]["title"] == "Vector Spaces"
    assert loaded["summary"]["status"] == "ok"
    assert loaded["summary"]["totals"]["input_tokens"] == 700
    assert loaded["summary"]["totals"]["output_tokens"] == 920
    assert loaded["summary"]["result"]["task_score"] == 0.71


def test_unpriced_run_reports_none_not_zero(tmp_path):
    with RunLogger.start(
        runs_root=tmp_path,
        system="vanilla_rlm",
        document_id="openstax",
        seed=23,
        models={"tier1": "test-frontier"},
    ) as run:
        run.log_call(
            role="tier1",
            model="test-frontier",
            prompt="p",
            response="r",
            input_tokens=1_000_000,
            output_tokens=0,
        )

    summary = json.loads((run.run_dir / "summary.json").read_text())
    assert summary["totals"]["cost"] is None
    assert summary["totals"]["unpriced_models"] == ["test-frontier"]


def test_priced_run_computes_cost(tmp_path):
    card = RateCard.empty().with_rate(_rate(date.today()))
    with RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="openstax",
        seed=23,
        models={"tier1": "test-frontier"},
        rate_card=card,
    ) as run:
        run.log_call(
            role="tier1",
            model="test-frontier",
            prompt="p",
            response="r",
            input_tokens=1_000_000,
            output_tokens=100_000,
        )

    summary = json.loads((run.run_dir / "summary.json").read_text())
    assert summary["totals"]["cost"] == pytest.approx(1.25 + 1.0)


def test_stale_rate_is_refused(tmp_path):
    card = RateCard.empty().with_rate(_rate(date.today() - timedelta(days=90)))
    with pytest.raises(StaleRateError):
        card.cost_for("test-frontier", 1000, 1000)


def test_failed_run_is_recorded_with_traceback(tmp_path):
    class BoomError(RuntimeError):
        pass

    with (
        pytest.raises(BoomError),
        RunLogger.start(
            runs_root=tmp_path,
            system="mard",
            document_id="pilot",
            seed=11,
            models={"tier1": "test-frontier"},
        ) as run,
    ):
        run.log_call(
            role="tier1",
            model="test-frontier",
            prompt="p",
            response="r",
            input_tokens=10,
            output_tokens=10,
        )
        raise BoomError("rate limit")

    summary = json.loads((run.run_dir / "summary.json").read_text())
    assert summary["status"] == "failed"
    assert summary["error"]["type"] == "BoomError"
    assert "rate limit" in summary["error"]["message"]
    # The work done before the failure must survive it.
    assert summary["totals"]["calls"] == 1


def test_truncated_jsonl_is_still_readable(tmp_path):
    """A killed process leaves a half-written line. The audit must not crash."""
    with RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="pilot",
        seed=11,
        models={"tier1": "test-frontier"},
    ) as run:
        for _ in range(3):
            run.log_call(
                role="tier2",
                model="test-frontier",
                prompt="p",
                response="r",
                input_tokens=1,
                output_tokens=1,
            )

    calls_path = run.run_dir / CALLS_FILE
    with calls_path.open("a", encoding="utf-8") as handle:
        handle.write('{"call_id": "truncated", "pro')

    loaded = load_run(run.run_dir)
    assert len(loaded["calls"]) == 3


def test_concurrent_writes_do_not_interleave(tmp_path):
    import threading

    with RunLogger.start(
        runs_root=tmp_path,
        system="mard",
        document_id="pilot",
        seed=11,
        models={"tier2": "test-budget"},
    ) as run:

        def worker(index: int) -> None:
            run.log_call(
                role="tier2",
                model="test-budget",
                prompt=f"section {index}",
                response="x" * 500,
                input_tokens=10,
                output_tokens=10,
            )

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(32)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    loaded = load_run(run.run_dir)
    assert len(loaded["calls"]) == 32
    assert loaded["summary"]["totals"]["calls"] == 32


def test_seeding_is_reproducible():
    import random

    seed_everything(42)
    first = [random.random() for _ in range(5)]
    seed_everything(42)
    assert [random.random() for _ in range(5)] == first
