"""`ThrottledAsyncOpenAI` — the client MARD's own Tier 1/2 calls go through.

Historical design note: this class exposes an async `.chat.completions.create(...)`
surface because `replm`'s own `wrap_if_needed` auto-wrapped exactly that shape when
passed as `RLMWrapper(client=...)`, so the vanilla arm and MARD's own calls could
share one `Throttle`. `Zhang_RLM` (the control since `docs/18` §4.2 addendum, 28 Aug
2026) has no equivalent client-injection point — `rlm.core.rlm.RLM.__init__` always
builds its own `openai` client internally — so this class now serves **only** MARD's
own Tier 1/2 seam adapters (`provider/seams.py`, via the lower-level `acomplete()`
helper below). The vanilla arm's throttling/logging design lives in
`vanilla/openai_logging_bridge.py` instead.

Role/depth tagging for the log uses a `contextvars.ContextVar` rather than a call
argument, because `acomplete`'s call sites are spread across `provider/seams.py`'s
several adapters and a positional/keyword parameter would have to thread through all
of them. Setting the tag via `tagged()` immediately before a call, from within the
same coroutine that makes the call, is safe under `asyncio.gather`-concurrent
sub-calls: each gathered coroutine is its own `asyncio.Task` with its own copied
context, so one sub-call's tag can never leak into a sibling's.
"""

from __future__ import annotations

import contextvars
import json
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Protocol

import openai

from provider.reasoning import completion_kwargs
from provider.throttle import Throttle


@dataclass(frozen=True)
class _CallTag:
    role: str
    depth: int


_DEFAULT_TAG = _CallTag(role="untagged", depth=0)
_CALL_TAG: contextvars.ContextVar[_CallTag] = contextvars.ContextVar(
    "mard_call_tag", default=_DEFAULT_TAG
)


@dataclass(frozen=True)
class CompletionResult:
    """The shape `provider/seams.py`'s adapters need back from a chat completion."""

    content: str
    input_tokens: int
    output_tokens: int


class CallLogger(Protocol):
    """The one method this module needs from `runlog.RunLogger` — kept structural
    so `provider/` does not have to import `runlog` just to type a parameter."""

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
    ) -> str: ...


def _extract(response: Any) -> CompletionResult:
    content: str = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    return CompletionResult(
        content=content,
        input_tokens=getattr(usage, "prompt_tokens", 0) if usage else 0,
        output_tokens=getattr(usage, "completion_tokens", 0) if usage else 0,
    )


class _Completions:
    def __init__(self, owner: ThrottledAsyncOpenAI) -> None:
        self._owner = owner

    async def create(self, **kwargs: Any) -> Any:
        return await self._owner._create(**kwargs)


class _Chat:
    def __init__(self, owner: ThrottledAsyncOpenAI) -> None:
        self.completions = _Completions(owner)


class ThrottledAsyncOpenAI:
    """Wraps a real `openai.AsyncOpenAI`, gated by one shared `Throttle`.

    `raw_client` is injectable for tests; a real run constructs this with no
    argument and the SDK reads `OPENAI_API_KEY` from the environment itself.
    `logger` is optional so unit tests can exercise this with no `RunLogger`.
    """

    def __init__(
        self,
        throttle: Throttle,
        *,
        raw_client: openai.AsyncOpenAI | None = None,
        logger: CallLogger | None = None,
    ) -> None:
        self._throttle = throttle
        self._raw = raw_client if raw_client is not None else openai.AsyncOpenAI()
        self._logger = logger
        self.chat = _Chat(self)

    @contextmanager
    def tagged(self, role: str, depth: int = 0) -> Iterator[None]:
        """Attribute every call made inside this context to `role`/`depth` in the log."""
        token = _CALL_TAG.set(_CallTag(role=role, depth=depth))
        try:
            yield
        finally:
            _CALL_TAG.reset(token)

    async def _create(self, **kwargs: Any) -> Any:
        tag = _CALL_TAG.get()
        label = f"{tag.role}(depth={tag.depth})"
        start = time.monotonic()
        response = await self._throttle.run(
            lambda: self._raw.chat.completions.create(**kwargs), label=label
        )
        latency = time.monotonic() - start
        if self._logger is not None:
            result = _extract(response)
            self._logger.log_call(
                role=tag.role,
                model=kwargs.get("model", "unknown"),
                prompt=json.dumps(kwargs.get("messages", [])),
                response=result.content,
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                depth=tag.depth,
                latency_s=latency,
            )
        return response

    async def acomplete(
        self,
        model: str,
        messages: list[dict[str, str]],
        max_tokens: int,
        *,
        temperature: float | None = None,
        reasoning_effort: str | None = None,
    ) -> CompletionResult:
        """Direct completion helper for MARD's own Tier 1/2 seam adapters.

        Goes through the same `chat.completions.create` path as the vanilla arm
        (via `wrap_if_needed`/`OpenAIAdapter`), so throttling, retries and per-call
        logging are identical for both arms.
        """
        kwargs = completion_kwargs(
            model, messages, max_tokens, temperature=temperature, reasoning_effort=reasoning_effort
        )
        response = await self.chat.completions.create(**kwargs)
        return _extract(response)
