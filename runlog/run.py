"""The run logger every measured number in both manuscripts must pass through.

Track 3 is blocked on this existing in W0 (CONTEXT.md §3.6), and §3.4 fixes what
it has to capture: envelope state, transcripts, token counts, config snapshot,
seed. Three design choices follow from how this project actually fails:

1. Append-only JSONL, flushed per line. W3 and W6 runs die from rate limits and
   timeouts mid-flight. A partially written run must still be readable, because
   the alternative is discovering on measurement day that a 40-minute run left
   nothing behind.
2. Failure is recorded, not raised away. A crashed run writes a summary with
   status="failed" and its traceback, so a hole in the matrix has an explanation
   attached rather than being silently absent.
3. Cost is None when unpriced. See `pricing` — an unpriced run must not look free.
"""

from __future__ import annotations

import json
import threading
import time
import traceback
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType
from typing import Any, Literal

from runlog.config import ConfigSnapshot
from runlog.pricing import RateCard, StaleRateError
from runlog.seeds import seed_everything

MANIFEST_FILE = "manifest.json"
CALLS_FILE = "calls.jsonl"
EVENTS_FILE = "events.jsonl"
SUMMARY_FILE = "summary.json"
ENVELOPE_DIR = "envelope"
ARTEFACT_DIR = "artefacts"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_run_id(system: str, document_id: str, seed: int) -> str:
    """Human-sortable and human-readable, because these get read in a terminal.

    The uuid suffix is what keeps two runs launched in the same second from
    colliding during the W6 concurrent matrix.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"{stamp}__{system}__{document_id}__s{seed}__{uuid.uuid4().hex[:6]}"


class RunLogger:
    """One directory per run, written as the run happens.

    Use via `RunLogger.start(...)` as a context manager. Direct construction is
    possible but skips seeding and manifest capture.
    """

    def __init__(self, run_dir: Path, snapshot: ConfigSnapshot, rate_card: RateCard) -> None:
        self.run_dir = run_dir
        self.snapshot = snapshot
        self.rate_card = rate_card
        self.run_id = snapshot.run_id

        # Builders run concurrently in the Tier 2 fork-join, so every append has
        # to be serialised or lines interleave and the file stops being parseable.
        self._lock = threading.Lock()
        self._started_at = time.monotonic()
        self._calls = 0
        self._input_tokens: defaultdict[str, int] = defaultdict(int)
        self._output_tokens: defaultdict[str, int] = defaultdict(int)
        self._result: dict[str, Any] | None = None
        self._closed = False

    # ---------------------------------------------------------------- lifecycle

    @classmethod
    def start(
        cls,
        *,
        runs_root: Path | str,
        system: str,
        document_id: str,
        seed: int,
        models: dict[str, str],
        params: dict[str, Any] | None = None,
        rate_card: RateCard | None = None,
    ) -> RunLogger:
        run_id = _new_run_id(system, document_id, seed)
        run_dir = Path(runs_root) / run_id
        (run_dir / ENVELOPE_DIR).mkdir(parents=True, exist_ok=True)
        (run_dir / ARTEFACT_DIR).mkdir(parents=True, exist_ok=True)

        seeding = seed_everything(seed)
        snapshot = ConfigSnapshot.capture(
            run_id=run_id,
            system=system,
            document_id=document_id,
            seed=seed,
            models=models,
            params=params,
        )
        logger = cls(run_dir, snapshot, rate_card or RateCard.empty())
        manifest = {
            "config": snapshot.to_dict(),
            "seeding": seeding,
            "rate_card": logger.rate_card.to_dict(),
            "started_at": _utc_now(),
        }
        (run_dir / MANIFEST_FILE).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return logger

    def __enter__(self) -> RunLogger:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        # Literal[False] rather than bool: a bool return type tells mypy this
        # context manager might swallow exceptions, and it must never do that.
        # The caller decides whether a failed run is fatal to the campaign; this
        # class only guarantees the failure was recorded before re-raising.
        if exc is not None:
            self.close(
                status="failed",
                error={
                    "type": exc_type.__name__ if exc_type else "Unknown",
                    "message": str(exc),
                    "traceback": "".join(traceback.format_exception(exc_type, exc, tb)),
                },
            )
        else:
            self.close(status="ok")
        return False

    # ----------------------------------------------------------------- writing

    def _append(self, filename: str, record: dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False, default=str)
        with self._lock, (self.run_dir / filename).open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            # Flushed per record so a killed process still leaves a usable file.
            handle.flush()

    def log_call(
        self,
        *,
        role: str,
        model: str,
        prompt: str,
        response: str,
        input_tokens: int,
        output_tokens: int,
        depth: int = 0,
        parent_call_id: str | None = None,
        latency_s: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Record one model call, transcript included. Returns its call id.

        `depth` and `parent_call_id` are what make the recursion reconstructable
        after the fact — without them a transcript is a flat pile of calls and
        the depth sweep ablation has nothing to read.
        """
        call_id = uuid.uuid4().hex[:12]
        with self._lock:
            self._calls += 1
            self._input_tokens[model] += input_tokens
            self._output_tokens[model] += output_tokens
        self._append(
            CALLS_FILE,
            {
                "call_id": call_id,
                "parent_call_id": parent_call_id,
                "at": _utc_now(),
                "role": role,
                "model": model,
                "depth": depth,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_s": latency_s,
                "prompt": prompt,
                "response": response,
                "metadata": metadata or {},
            },
        )
        return call_id

    def log_envelope(self, pass_index: int, envelope: Any, *, label: str | None = None) -> Path:
        """Snapshot envelope state after a pass.

        The envelope is the contribution (§1.5). "The envelope grew" is not a
        result; the states it grew through are, and the ablation that removes it
        needs something concrete to be compared against.
        """
        name = f"pass_{pass_index}" + (f"_{label}" if label else "") + ".json"
        path = self.run_dir / ENVELOPE_DIR / name
        payload = envelope if isinstance(envelope, (dict, list)) else _as_jsonable(envelope)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
        )
        self.log_event("envelope_snapshot", {"pass": pass_index, "path": str(path.name)})
        return path

    def log_event(self, kind: str, payload: dict[str, Any] | None = None) -> None:
        """Anything that is not a model call: retries, validation failures, joins."""
        self._append(EVENTS_FILE, {"at": _utc_now(), "kind": kind, **(payload or {})})

    def save_artefact(self, name: str, content: str) -> Path:
        """Persist a produced output — a Master Plan, a joined document, a scorer input."""
        path = self.run_dir / ARTEFACT_DIR / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def set_result(self, result: dict[str, Any]) -> None:
        """Attach the scored outcome so summary.json is self-contained."""
        self._result = result

    # ----------------------------------------------------------------- closing

    def totals(self) -> dict[str, Any]:
        with self._lock:
            # Annotated because a cost is written into these dicts below, and the
            # inferred int-valued type would make that a type error.
            per_model: dict[str, dict[str, Any]] = {
                model: {
                    "input_tokens": self._input_tokens[model],
                    "output_tokens": self._output_tokens[model],
                }
                for model in set(self._input_tokens) | set(self._output_tokens)
            }
            calls = self._calls

        cost = 0.0
        unpriced: list[str] = []
        stale: list[str] = []
        for model, counts in per_model.items():
            try:
                model_cost = self.rate_card.cost_for(
                    model, counts["input_tokens"], counts["output_tokens"]
                )
            except StaleRateError as err:
                stale.append(str(err))
                model_cost = None
            if model_cost is None:
                unpriced.append(model)
            else:
                cost += model_cost
            counts["cost"] = model_cost

        return {
            "calls": calls,
            "input_tokens": sum(c["input_tokens"] for c in per_model.values()),
            "output_tokens": sum(c["output_tokens"] for c in per_model.values()),
            "per_model": per_model,
            # None, not 0.0 — a run with any unpriced model has no total cost.
            "cost": None if unpriced else cost,
            "unpriced_models": unpriced,
            "stale_rates": stale,
        }

    def close(self, *, status: str = "ok", error: dict[str, Any] | None = None) -> Path:
        if self._closed:
            return self.run_dir / SUMMARY_FILE
        self._closed = True
        summary = {
            "run_id": self.run_id,
            "status": status,
            "system": self.snapshot.system,
            "document_id": self.snapshot.document_id,
            "seed": self.snapshot.seed,
            "wall_clock_s": round(time.monotonic() - self._started_at, 3),
            "totals": self.totals(),
            "result": self._result,
            "error": error,
            "finished_at": _utc_now(),
        }
        path = self.run_dir / SUMMARY_FILE
        path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
        return path


def _as_jsonable(obj: Any) -> Any:
    """Best-effort conversion for envelope objects that are not plain containers."""
    for attr in ("model_dump", "to_dict", "_asdict"):
        method = getattr(obj, attr, None)
        if callable(method):
            return method()
    if hasattr(obj, "__dict__"):
        return vars(obj)
    return obj


def load_run(run_dir: Path | str) -> dict[str, Any]:
    """Read a completed run back. This is the half that makes logging worth doing.

    Track 3's per-number audit (issues #23, #27) needs every reported figure to
    trace to a logged run, so reading has to be as easy as writing.
    """
    run_dir = Path(run_dir)
    manifest = json.loads((run_dir / MANIFEST_FILE).read_text(encoding="utf-8"))
    summary_path = run_dir / SUMMARY_FILE
    summary = (
        json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else None
    )
    calls = _read_jsonl(run_dir / CALLS_FILE)
    events = _read_jsonl(run_dir / EVENTS_FILE)
    envelopes = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((run_dir / ENVELOPE_DIR).glob("*.json"))
    }
    return {
        "run_dir": str(run_dir),
        "manifest": manifest,
        "summary": summary,
        "calls": calls,
        "events": events,
        "envelopes": envelopes,
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            # A truncated final line means the process was killed mid-write.
            # Everything before it is still valid data and is worth more than
            # an exception raised during an audit.
            continue
    return records
