"""Tests for run selection and field extraction (docs/34, shared by Tasks A-C)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval.runs import RunSelectionError, extract_fields, select_campaign, select_run

RUNS_DIR = Path(__file__).resolve().parents[1] / "runs"


def _write_run(base: Path, run_id: str, *, status: str = "ok") -> Path:
    run_dir = base / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "summary.json").write_text(json.dumps({"status": status}), encoding="utf-8")
    return run_dir


class TestSelectRunSynthetic:
    def test_picks_the_last_completed_run_by_timestamp(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import eval.runs as runs_module

        monkeypatch.setattr(runs_module, "RUNS_DIR", tmp_path)
        _write_run(tmp_path, "20260101T000000__sysX__introcs__s11__aaaaaa")
        expected = _write_run(tmp_path, "20260102T000000__sysX__introcs__s11__bbbbbb")

        assert select_run("sysX", 11) == expected

    def test_skips_a_failed_run_and_picks_the_last_completed_one(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import eval.runs as runs_module

        monkeypatch.setattr(runs_module, "RUNS_DIR", tmp_path)
        _write_run(tmp_path, "20260101T000000__sysX__introcs__s11__aaaaaa")
        _write_run(tmp_path, "20260102T000000__sysX__introcs__s11__bbbbbb", status="failed")
        expected = _write_run(tmp_path, "20260103T000000__sysX__introcs__s11__cccccc")

        assert select_run("sysX", 11) == expected

    def test_run_with_no_summary_json_is_not_completed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import eval.runs as runs_module

        monkeypatch.setattr(runs_module, "RUNS_DIR", tmp_path)
        mid_write = tmp_path / "20260101T000000__sysX__introcs__s11__aaaaaa"
        mid_write.mkdir(parents=True)  # no summary.json yet — a run still in progress
        expected = _write_run(tmp_path, "20260102T000000__sysX__introcs__s11__bbbbbb")

        assert select_run("sysX", 11) == expected

    def test_raises_when_nothing_completed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import eval.runs as runs_module

        monkeypatch.setattr(runs_module, "RUNS_DIR", tmp_path)
        _write_run(tmp_path, "20260101T000000__sysX__introcs__s11__aaaaaa", status="failed")

        with pytest.raises(RunSelectionError):
            select_run("sysX", 11)

    def test_does_not_match_a_different_seed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import eval.runs as runs_module

        monkeypatch.setattr(runs_module, "RUNS_DIR", tmp_path)
        _write_run(tmp_path, "20260101T000000__sysX__introcs__s23__aaaaaa")

        with pytest.raises(RunSelectionError):
            select_run("sysX", 11)


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_mard_full_s11_resolves_to_the_post_fix_run(self) -> None:
        # docs/28 §4: three pre-fix seed-11 attempts exist (one failed outright,
        # two superseded by the merge-policy fix); the last completed one,
        # ...13de68, is the only candidate number.
        run_dir = select_run("mard", 11)
        assert run_dir.name.endswith("13de68")

    def test_mard_a1f_s42_resolves_past_two_rate_limited_attempts(self) -> None:
        # docs/28 §6.3: the first two a1f seed-42 attempts hit a real OpenAI
        # credit-balance error and are recorded status="failed".
        run_dir = select_run("mard_a1f", 42)
        assert run_dir.name.endswith("2f00df")

    def test_select_campaign_returns_all_three_seeds(self) -> None:
        campaign = select_campaign("mard")
        assert set(campaign) == {11, 23, 42}

    def test_extract_fields_vanilla_call_counts_are_not_the_aggregate_two(self) -> None:
        # summary.json's own totals.calls is 2 for every vanilla run (one
        # aggregate row per role) — real per-call counts come from events, and
        # this pins that extract_fields uses those, not the aggregate.
        run_dir = select_run("vanilla_rlm", 42)
        fields = extract_fields(run_dir)
        assert fields.calls_tier1 == 17  # vanilla_root_iteration count
        assert fields.calls_tier2 == 151  # vanilla_subcall_detail count
        assert fields.calls_total == 168

    def test_extract_fields_mard_call_counts_match_summary_totals(self) -> None:
        run_dir = select_run("mard", 42)
        fields = extract_fields(run_dir)
        assert fields.calls_tier1 == 15  # 1 pass0 + 14 pass1
        assert fields.calls_tier2 == 84
        assert fields.calls_total == 99

    def test_extract_fields_config_snapshot_names_the_ablation(self) -> None:
        mard = extract_fields(select_run("mard", 11))
        a1 = extract_fields(select_run("mard_a1", 11))
        assert mard.config_snapshot["params"]["ablation"] is None
        assert a1.config_snapshot["params"]["ablation"] is not None

    def test_extract_fields_builder_wall_clock_max_is_at_most_the_sum(self) -> None:
        for system in ("vanilla_rlm", "mard", "mard_a1", "mard_a1f"):
            for seed in (11, 23, 42):
                fields = extract_fields(select_run(system, seed))
                max_s, sum_s = fields.builder_wall_clock_max_s, fields.builder_wall_clock_sum_s
                if max_s is not None and sum_s is not None:
                    assert max_s <= sum_s
