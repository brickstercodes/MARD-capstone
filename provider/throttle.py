"""One semaphore, one retry policy, for MARD's own Tier 1/2 calls.

`replm` had no concurrency cap at all (docs/18 §4.2, historical: bare
`asyncio.gather`, no semaphore anywhere in its `src/`), which is why this module was
built. It now serves only MARD's own Tier 1/2 calls (via `provider/seams.py`) — the
vanilla arm runs on `Zhang_RLM` since `docs/18` §4.2 addendum (28 Aug 2026), which has
no client-injection seam to thread this `Throttle` through and relies on its own
`max_concurrent_subcalls` instead (`vanilla/run.py`).

Design points that are requirements, not preferences (docs/18-W3_PROVIDER_SWITCH.md
§4.2):

- One `Throttle` instance is shared across Tier 1 and Tier 2, so total in-flight
  requests are capped regardless of which tier is calling.
- A 429 is data: every rate-limit response is reported through `on_rate_limited`
  with its timestamp and `Retry-After`, never silently retried away.
- Backoff without `Retry-After` uses full jitter (`random.uniform(0, cap)`), not a
  fixed exponential curve — without jitter, N builders that fork together (Tier 2's
  120-way burst) get throttled together and retry together, reproducing the burst.
- Bounded attempts, then `RetryExhaustedError` — the run fails loudly rather than
  hanging, and `RunLogger`'s context manager turns that into `status: "failed"`
  with a traceback (runlog/run.py's `__exit__`).

`max_concurrency`'s default is a labelled placeholder, not a measured ceiling:
`RATE_LIMIT_BUDGET.md` §2/§6's OpenAI RPM number was never filled in (the doc's own
"before W3" deadline for that passed). Track 2 or whoever reads the OpenAI dashboard
next should override `MARD_MAX_CONCURRENCY` with `0.7 * measured_rpm`-derived value,
per that document's own "run at ≤70% of the measured ceiling" policy — this module
cannot invent the 70% arithmetic against a number nobody has read yet.
"""

from __future__ import annotations

import asyncio
import os
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, TypeVar

import openai

T = TypeVar("T")

MAX_CONCURRENCY_ENV = "MARD_MAX_CONCURRENCY"

# Placeholder, not a measurement — see module docstring.
DEFAULT_MAX_CONCURRENCY = 6

DEFAULT_MAX_ATTEMPTS = 5
DEFAULT_BASE_BACKOFF_S = 1.0
DEFAULT_MAX_BACKOFF_S = 60.0

# Historical: matched the now-retired replm-based vanilla arm's own
# `sub_call_max_input_chars` default (`RLMConfig`), so MARD's own Tier 1/2 calls
# used one number instead of two that could drift apart. Zhang_RLM has no
# equivalent parameter; kept here for MARD's own calls only.
DEFAULT_SUB_CALL_MAX_INPUT_CHARS = 500_000

# Retryable beyond a 429: transient connection/timeout/5xx. Anything else (bad
# request, auth, not-found) is a real error and must not be retried away.
_RETRYABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
    openai.APIConnectionError,
    openai.APITimeoutError,
    openai.InternalServerError,
)


@dataclass(frozen=True)
class ThrottleConfig:
    """Every field here is config, not a literal — and every field lands in the
    run's manifest via `to_dict()`, per docs/30 §1's "config snapshot" requirement.
    """

    max_concurrency: int = DEFAULT_MAX_CONCURRENCY
    max_attempts: int = DEFAULT_MAX_ATTEMPTS
    base_backoff_s: float = DEFAULT_BASE_BACKOFF_S
    max_backoff_s: float = DEFAULT_MAX_BACKOFF_S
    sub_call_max_input_chars: int = DEFAULT_SUB_CALL_MAX_INPUT_CHARS

    @classmethod
    def from_env(cls) -> ThrottleConfig:
        raw = os.environ.get(MAX_CONCURRENCY_ENV)
        return cls(max_concurrency=int(raw) if raw else DEFAULT_MAX_CONCURRENCY)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_concurrency": self.max_concurrency,
            "max_attempts": self.max_attempts,
            "base_backoff_s": self.base_backoff_s,
            "max_backoff_s": self.max_backoff_s,
            "sub_call_max_input_chars": self.sub_call_max_input_chars,
            "max_concurrency_is_measured": False,
            "max_concurrency_source": (
                "placeholder pending RATE_LIMIT_BUDGET.md §2/§6 OpenAI RPM reading"
            ),
        }


class RetryExhaustedError(RuntimeError):
    """All `max_attempts` attempts failed with a retryable error."""


@dataclass(frozen=True)
class RateLimitEvent:
    """One logged 429 — never swallowed, per docs/18 §4.2 / RATE_LIMIT_BUDGET.md §3."""

    at: str
    label: str
    attempt: int
    retry_after_s: float | None
    message: str


def _retry_after_seconds(err: openai.RateLimitError) -> float | None:
    response = getattr(err, "response", None)
    header = response.headers.get("retry-after") if response is not None else None
    if header is None:
        return None
    try:
        return float(header)
    except ValueError:
        return None


class Throttle:
    """Gate every OpenAI call through one semaphore and one retry policy."""

    def __init__(
        self,
        config: ThrottleConfig | None = None,
        *,
        on_rate_limited: Callable[[RateLimitEvent], None] | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        rand: random.Random | None = None,
    ) -> None:
        self.config = config or ThrottleConfig.from_env()
        self._semaphore = asyncio.Semaphore(self.config.max_concurrency)
        self._on_rate_limited = on_rate_limited
        self._sleep = sleep
        self._rand = rand or random.Random()

    def _backoff_delay(self, attempt: int) -> float:
        """Full jitter: uniform(0, min(cap, base * 2**(attempt-1)))."""
        cap = min(self.config.max_backoff_s, self.config.base_backoff_s * (2 ** (attempt - 1)))
        return self._rand.uniform(0, cap)

    async def run(self, call: Callable[[], Awaitable[T]], *, label: str = "") -> T:
        """Run `call` under the shared semaphore, retrying transient failures.

        Backoff sleeps happen *outside* the semaphore, so a builder waiting out a
        429 does not also hold a concurrency slot idle.
        """
        attempt = 0
        while True:
            attempt += 1
            delay: float | None = None
            async with self._semaphore:
                try:
                    return await call()
                except openai.RateLimitError as err:
                    retry_after = _retry_after_seconds(err)
                    if self._on_rate_limited is not None:
                        self._on_rate_limited(
                            RateLimitEvent(
                                at=datetime.now(timezone.utc).isoformat(),
                                label=label,
                                attempt=attempt,
                                retry_after_s=retry_after,
                                message=str(err),
                            )
                        )
                    if attempt >= self.config.max_attempts:
                        raise RetryExhaustedError(
                            f"{label or 'call'}: exhausted {attempt} attempts, "
                            f"last response was a 429"
                        ) from err
                    delay = retry_after if retry_after is not None else self._backoff_delay(attempt)
                except _RETRYABLE_EXCEPTIONS as err:
                    if attempt >= self.config.max_attempts:
                        raise RetryExhaustedError(
                            f"{label or 'call'}: exhausted {attempt} attempts, "
                            f"last error was {type(err).__name__}: {err}"
                        ) from err
                    delay = self._backoff_delay(attempt)
            # Semaphore released above; sleep outside it.
            await self._sleep(delay)
