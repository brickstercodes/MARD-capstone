"""Synchronous adapters over `provider/seams.py`'s async OpenAI seams.

`envelope/pass0.py`'s `TopicLabeller` and `envelope/pass1.py`'s `ChapterExplorer`
protocols are synchronous (`def label(...)`, `def explore(...)`), and both frozen
modules call them without `await` — `pass0.py:107`'s `raw_topics = active.label(...)`
and `pass1.py:307`'s `raw = active.explore(...)`. `provider/seams.py`'s
`OpenAITopicLabeller`/`OpenAIChapterExplorer` are `async def`, so handed to
`run_pass0`/`run_pass1` directly they return an unawaited coroutine object.
`run_pass1`'s own `isinstance(raw, dict)` check then fails for every chapter, and
each one is silently recorded as `"explorer returned coroutine, expected an
object"` — zero concepts, no exception (`docs/25` §2).

This module closes that gap without touching either frozen protocol.

**Why a fresh `asyncio.run()` per call, not a persistent background loop.** Pass 1
is inherently sequential (`run_pass1`'s own docstring: a later chapter's call must
see what earlier ones found), so there is no concurrency at Tier 1 for a persistent
loop to preserve — opening and closing one loop per call costs nothing that matters.
It is also safe to alternate with Tier 2's own separate event loop
(`orchestrate.builder.execute_plan_sync`, its own `asyncio.run()` after Tier 1
finishes) even when both share one `Throttle` instance: on this project's Python
(3.10+), `asyncio.Semaphore` no longer binds to a loop at construction — it grabs
the running loop lazily, via `get_running_loop()`, on first `acquire()` — and Tier 1
and Tier 2 never hold that semaphore concurrently against two different loops, only
sequentially. A persistent loop would only earn its complexity if that assumption
ever changed.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from ingest.chapters import Chapter
from provider.seams import OpenAIChapterExplorer, OpenAITopicLabeller


@dataclass
class SyncTopicLabeller:
    """Satisfies `envelope.pass0.TopicLabeller` by blocking on `OpenAITopicLabeller.label`."""

    inner: OpenAITopicLabeller

    def label(self, prompt: str, section_ids: list[str]) -> dict[str, str]:
        return asyncio.run(self.inner.label(prompt, section_ids))


@dataclass
class SyncChapterExplorer:
    """Satisfies `envelope.pass1.ChapterExplorer` by blocking on `OpenAIChapterExplorer.explore`."""

    inner: OpenAIChapterExplorer

    def explore(self, prompt: str, chapter: Chapter) -> dict[str, Any]:
        return asyncio.run(self.inner.explore(prompt, chapter))


__all__ = ["SyncTopicLabeller", "SyncChapterExplorer"]
