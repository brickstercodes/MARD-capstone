"""429/retry visibility for the vanilla arm, via the `openai` SDK's own logger.

`rlm.core.rlm.RLM.__init__`'s `backend_kwargs` always builds a *fresh* `openai.OpenAI`
and `openai.AsyncOpenAI` from the same kwargs dict inside `OpenAIClient.__init__`
(`rlm/clients/openai.py`) — there is no seam to inject a pre-built client the way
`replm`'s `RLMWrapper(client=...)` allowed, and passing a custom `http_client=` through
`backend_kwargs` breaks one of the two constructors outright: `openai.OpenAI` requires
an `httpx.Client`, `openai.AsyncOpenAI` requires an `httpx.AsyncClient`, and both are
built from the identical kwargs, so no single `http_client` value satisfies both
(verified against the installed `openai` SDK's `AsyncAPIClient.__init__`, which raises
`TypeError` on a type mismatch).

The `openai` SDK logs every retry decision through the standard `logging` module
(`openai._base_client`, `log = logging.getLogger("openai")`), independent of which
client instance issues the call. Attaching a handler there is the seam that survives
`get_client()` constructing a new client per sub-call (`rlm/core/rlm.py:234,702` call
`get_client(self.backend, self.backend_kwargs)` fresh each time, so a handle grabbed
once would miss later calls).

Depth/role attribution is deliberately not attempted here: sub-calls with
`max_concurrent_subcalls > 1` run on separate `ThreadPoolExecutor` worker threads
(`rlm/environments/local_repl.py:366`), and a `contextvars.ContextVar` set in the
submitting thread does not propagate into a worker thread unless the library itself
copies the context at submission — it does not. A 429/retry event logged here is
real and timestamped, just not reliably attributable to a specific sub-call.
"""

from __future__ import annotations

import contextlib
import logging
from typing import Any, Protocol


class EventLogger(Protocol):
    def log_event(self, kind: str, payload: dict[str, Any] | None = None) -> None: ...


class _OpenAIRetryBridge(logging.Handler):
    """Watches `openai`'s own DEBUG/INFO records for 429s and retry decisions.

    `record.args` is used instead of parsing the formatted message: the SDK's
    `log.debug('HTTP Response: %s %s "%i %s" %s', method, url, status_code,
    reason_phrase, headers)` and `log.info('Retrying request to %s in %f seconds',
    url, timeout)` calls carry their real values in `args`, not just interpolated
    into `msg` — reading `args` is robust to a message-string wording change,
    reading the formatted string is not.
    """

    def __init__(self, run: EventLogger) -> None:
        super().__init__(level=logging.DEBUG)
        self._run = run

    def emit(self, record: logging.LogRecord) -> None:
        # A logging bridge must never break the run it is observing.
        with contextlib.suppress(Exception):
            self._handle(record)

    def _handle(self, record: logging.LogRecord) -> None:
        msg = record.msg
        args = record.args
        # `record.args` is a tuple for every %-style call this module ever makes
        # (`log.debug(msg, a, b, ...)`); the `Mapping[str, object]` half of its
        # declared type is only reachable via `log.debug(msg, {"k": v})`, which
        # the `openai` SDK's call sites this bridge watches never do.
        if not isinstance(msg, str) or not isinstance(args, tuple) or not args:
            return
        if msg.startswith("HTTP Response:") and record.levelno == logging.DEBUG:
            # args = (method, url, status_code, reason_phrase, headers)
            if len(args) >= 3 and args[2] == 429:
                self._run.log_event(
                    "vanilla_rate_limited",
                    {
                        "method": str(args[0]),
                        "url": str(args[1]),
                        "status_code": 429,
                    },
                )
        elif (
            msg.startswith("Retrying request to")
            and record.levelno == logging.INFO
            and len(args) >= 2
        ):
            # args = (url, timeout_seconds) — timeout already honours Retry-After
            # when the SDK's own retry logic sees that header (openai._base_client
            # ._calculate_retry_timeout reads it before falling back to backoff).
            delay = args[1]
            delay_seconds = float(delay) if isinstance(delay, (int, float, str)) else None
            self._run.log_event(
                "vanilla_retry",
                {"url": str(args[0]), "delay_seconds": delay_seconds},
            )


class rate_limit_visibility:  # noqa: N801 - context manager, lowercase by convention here
    """`with rate_limit_visibility(run): ...` — logs every 429 and retry decision
    the `openai` SDK makes for the duration of the block, across every client the
    vanilla arm's `RLM` instance constructs internally."""

    def __init__(self, run: EventLogger) -> None:
        self._handler = _OpenAIRetryBridge(run)
        self._logger = logging.getLogger("openai")

    def __enter__(self) -> None:
        self._prior_level = self._logger.level
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._handler)

    def __exit__(self, *exc_info: object) -> None:
        self._logger.removeHandler(self._handler)
        self._logger.setLevel(self._prior_level)
