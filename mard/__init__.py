"""The MARD arm: Pass 0 -> Pass 1 -> Master Plan compile -> Tier 2 fork-join.

A thin package on purpose (global `CLAUDE.md` Part 4). The pipeline stages
themselves live in `envelope/`, `plan/` and `orchestrate/`, which are frozen and
shared with the offline W1 CLI (`envelope/cli.py`); this package's own job is only
to wire real OpenAI seams (`provider/seams.py`, `provider/sync_seams.py`) through
those stages under one `runlog.RunLogger`, for both the MARD-full and A1
(envelope-stripped) configurations (`docs/25-HANDOFF_MARD_ARM.md`).
"""

from mard.run import MardResult, run_mard

__all__ = ["MardResult", "run_mard"]
