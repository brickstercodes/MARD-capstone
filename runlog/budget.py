"""Spend ceiling enforcement across a measurement campaign.

Risk #5 in CONTEXT.md §3.7 is API cost or rate limits throttling W6, and the
stated response is a spend cap set in W0 and checked weekly. W6 runs 4 documents
x 5 systems x 3 seeds plus an ablation grid and a depth sweep, concurrently — by
the time a bill is noticed, the money is gone.

The ceiling itself is Anugrah's decision (§4.2 open item 3), not this module's.
So the design is: refuse to run without an explicit number rather than pick a
"sensible default". A default here would be exactly the kind of invented
decision §0.3 rule 3 warns about, and it would fail silently — the worst shape
for a budget control.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SPEND_CAP_ENV = "MARD_SPEND_CAP_USD"
LEDGER_FILE = "_ledger.json"

# Warn well before the wall. W6 is the expensive week and a warning that fires at
# 95% arrives after the decision to cut scope would have had to be made.
WARN_FRACTION = 0.75


class UnsetSpendCapError(RuntimeError):
    """Raised when a campaign is started without an explicit ceiling."""


class BudgetExceededError(RuntimeError):
    """Raised before a run starts that would take cumulative spend over the cap."""


@dataclass(frozen=True)
class SpendCap:
    """An explicit ceiling, in USD, with the person who set it on record."""

    ceiling_usd: float
    set_by: str
    set_on: str
    note: str = ""

    @classmethod
    def from_env(cls) -> SpendCap:
        """Read the cap from the environment, or refuse.

        Kept out of a config file on purpose: the cap changes when Anugrah says
        it changes, and an env var makes that an explicit act rather than a diff
        that can ride along in an unrelated commit.
        """
        raw = os.environ.get(SPEND_CAP_ENV)
        if not raw:
            raise UnsetSpendCapError(
                f"{SPEND_CAP_ENV} is not set. The compute/API budget ceiling is "
                f"Anugrah's decision (CONTEXT.md §4.2 open item 3, issue #46) and has "
                f"no default. Set it once the number exists:\n"
                f"    export {SPEND_CAP_ENV}=250.00"
            )
        try:
            ceiling = float(raw)
        except ValueError as err:
            raise UnsetSpendCapError(f"{SPEND_CAP_ENV}={raw!r} is not a number.") from err
        if ceiling <= 0:
            raise UnsetSpendCapError(f"{SPEND_CAP_ENV}={ceiling} must be positive.")
        return cls(
            ceiling_usd=ceiling,
            set_by=os.environ.get("MARD_SPEND_CAP_SET_BY", "unrecorded"),
            set_on=os.environ.get("MARD_SPEND_CAP_SET_ON", "unrecorded"),
            note=os.environ.get("MARD_SPEND_CAP_NOTE", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "ceiling_usd": self.ceiling_usd,
            "set_by": self.set_by,
            "set_on": self.set_on,
            "note": self.note,
        }


class SpendLedger:
    """Cumulative spend across every run in a campaign.

    Lives beside the runs rather than in a service because it has to survive a
    laptop reboot mid-matrix and be readable by a human at the Friday gate review.
    """

    def __init__(self, runs_root: Path | str, cap: SpendCap) -> None:
        self.runs_root = Path(runs_root)
        self.cap = cap
        self.path = self.runs_root / LEDGER_FILE
        self._lock = threading.Lock()
        self.runs_root.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(
                {
                    "cap": cap.to_dict(),
                    "spent_usd": 0.0,
                    "uncounted_runs": [],
                    "entries": [],
                }
            )

    # ------------------------------------------------------------------- state

    def _read(self) -> dict[str, Any]:
        state: dict[str, Any] = json.loads(self.path.read_text(encoding="utf-8"))
        return state

    def _write(self, state: dict[str, Any]) -> None:
        """Write via a temp file and rename.

        A plain write truncates before it fills. Under the W6 concurrent matrix a
        second thread reading at that moment gets an empty file and a JSON decode
        error — a crash in the one component whose job is to stop crashes from
        costing money. os.replace is atomic on POSIX, so a reader sees either the
        old ledger or the new one, never a half-written one.
        """
        tmp = self.path.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)

    @property
    def spent(self) -> float:
        return float(self._read()["spent_usd"])

    @property
    def remaining(self) -> float:
        return self.cap.ceiling_usd - self.spent

    def uncounted_runs(self) -> list[str]:
        """Runs whose cost could not be computed because a model had no rate.

        These are surfaced rather than treated as zero. A ledger that reads
        "$40 spent" while ten unpriced runs sit outside it is worse than no
        ledger, because it will be believed.
        """
        return list(self._read()["uncounted_runs"])

    # ------------------------------------------------------------------ checks

    def check_before_run(self, estimated_usd: float) -> None:
        """Refuse a run that would breach the ceiling. Call before spending, not after."""
        if estimated_usd < 0:
            raise ValueError("Estimated cost cannot be negative.")
        projected = self.spent + estimated_usd
        if projected > self.cap.ceiling_usd:
            raise BudgetExceededError(
                f"Run would take cumulative spend to ${projected:.2f}, over the "
                f"${self.cap.ceiling_usd:.2f} ceiling set by {self.cap.set_by}. "
                f"${self.remaining:.2f} remains. Cut scope or escalate to Anugrah — "
                f"do not raise the cap unilaterally."
            )

    def record(self, summary: dict[str, Any]) -> dict[str, Any]:
        """Add a finished run's cost to the ledger. Takes a `summary.json` payload.

        Returns the ledger state so a caller can act on a warning without a
        second read.
        """
        run_id = summary.get("run_id", "unknown")
        totals = summary.get("totals", {})
        cost = totals.get("cost")

        with self._lock:
            state = self._read()
            if cost is None:
                if run_id not in state["uncounted_runs"]:
                    state["uncounted_runs"].append(run_id)
            else:
                state["spent_usd"] = round(float(state["spent_usd"]) + float(cost), 6)
                state["entries"].append(
                    {
                        "run_id": run_id,
                        "system": summary.get("system"),
                        "document_id": summary.get("document_id"),
                        "seed": summary.get("seed"),
                        "cost_usd": cost,
                        "at": datetime.now(timezone.utc).isoformat(),
                    }
                )
            self._write(state)

        return self.status()

    def status(self) -> dict[str, Any]:
        state = self._read()
        spent = float(state["spent_usd"])
        fraction = spent / self.cap.ceiling_usd if self.cap.ceiling_usd else 0.0
        return {
            "ceiling_usd": self.cap.ceiling_usd,
            "spent_usd": round(spent, 4),
            "remaining_usd": round(self.cap.ceiling_usd - spent, 4),
            "fraction_used": round(fraction, 4),
            "warn": fraction >= WARN_FRACTION,
            "uncounted_runs": state["uncounted_runs"],
            "runs_counted": len(state["entries"]),
        }
