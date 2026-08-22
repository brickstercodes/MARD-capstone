"""Tests for the spend ledger.

The cases that matter are the ones where the ledger could lie: an unset cap that
silently defaults, an unpriced run counted as free, or a breach detected after
the money is spent rather than before.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from runlog import BudgetExceededError, SpendCap, SpendLedger, UnsetSpendCapError
from runlog.budget import SPEND_CAP_ENV


def _cap(ceiling: float = 100.0) -> SpendCap:
    return SpendCap(ceiling_usd=ceiling, set_by="anugrah", set_on="2026-08-05")


def _summary(run_id: str, cost: float | None, unpriced: list[str] | None = None) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "system": "mard",
        "document_id": "ostep",
        "seed": 11,
        "totals": {"cost": cost, "unpriced_models": unpriced or []},
    }


def test_unset_cap_refuses_rather_than_defaulting(monkeypatch):
    monkeypatch.delenv(SPEND_CAP_ENV, raising=False)
    with pytest.raises(UnsetSpendCapError) as err:
        SpendCap.from_env()
    # The message has to point at the owner, or someone will invent a number.
    assert "Anugrah" in str(err.value)


@pytest.mark.parametrize("raw", ["", "not-a-number", "0", "-50"])
def test_invalid_caps_are_rejected(monkeypatch, raw):
    monkeypatch.setenv(SPEND_CAP_ENV, raw)
    with pytest.raises(UnsetSpendCapError):
        SpendCap.from_env()


def test_cap_is_read_with_provenance(monkeypatch):
    monkeypatch.setenv(SPEND_CAP_ENV, "250.00")
    monkeypatch.setenv("MARD_SPEND_CAP_SET_BY", "anugrah")
    monkeypatch.setenv("MARD_SPEND_CAP_SET_ON", "2026-08-05")
    cap = SpendCap.from_env()
    assert cap.ceiling_usd == 250.0
    assert cap.set_by == "anugrah"


def test_spend_accumulates_and_breach_is_caught_before_the_run(tmp_path):
    ledger = SpendLedger(tmp_path, _cap(100.0))
    ledger.record(_summary("r1", 40.0))
    ledger.record(_summary("r2", 35.0))
    assert ledger.spent == pytest.approx(75.0)
    assert ledger.remaining == pytest.approx(25.0)

    ledger.check_before_run(20.0)  # fits
    with pytest.raises(BudgetExceededError) as err:
        ledger.check_before_run(30.0)
    assert "do not raise the cap unilaterally" in str(err.value)


def test_unpriced_run_is_surfaced_not_counted_as_free(tmp_path):
    ledger = SpendLedger(tmp_path, _cap(100.0))
    ledger.record(_summary("r1", 10.0))
    ledger.record(_summary("unpriced-run", None, ["some-model"]))
    status = ledger.status()
    assert status["spent_usd"] == pytest.approx(10.0)
    # The danger is a ledger that reads plausibly while runs sit outside it.
    assert status["uncounted_runs"] == ["unpriced-run"]
    assert status["runs_counted"] == 1


def test_warning_fires_before_the_wall(tmp_path):
    ledger = SpendLedger(tmp_path, _cap(100.0))
    ledger.record(_summary("r1", 50.0))
    assert ledger.status()["warn"] is False
    ledger.record(_summary("r2", 26.0))
    assert ledger.status()["warn"] is True


def test_ledger_survives_a_restart(tmp_path):
    SpendLedger(tmp_path, _cap(100.0)).record(_summary("r1", 12.5))
    reopened = SpendLedger(tmp_path, _cap(100.0))
    assert reopened.spent == pytest.approx(12.5)
    state = json.loads((tmp_path / "_ledger.json").read_text())
    assert state["entries"][0]["run_id"] == "r1"


def test_concurrent_records_do_not_lose_spend(tmp_path):
    import threading

    ledger = SpendLedger(tmp_path, _cap(1000.0))

    def worker(index: int) -> None:
        ledger.record(_summary(f"r{index}", 1.0))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(25)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert ledger.spent == pytest.approx(25.0)
