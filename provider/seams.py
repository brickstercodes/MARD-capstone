"""Real OpenAI clients behind MARD's three existing seams.

`envelope/pass0.py`'s `TopicLabeller`, `envelope/pass1.py`'s `ChapterExplorer` and
`orchestrate/lm_builder.py`'s `LanguageModel` are unchanged — these classes satisfy
those protocols structurally, exactly as `NoOpTopicLabeller`/`NoOpChapterExplorer`/
`MockLM` already do offline.

Two rules carried over verbatim from the modules these seams feed, because
violating either one would mean measuring the adapter instead of the model:

- **No repair, no pre-filtering.** `pass0.run_pass0` and `pass1.run_pass1` already
  validate everything a call returns (`_accept_concepts`, `_accept_edges`, the
  `known_ids` section check) and name what they reject in the trace. An adapter
  that "fixed" a malformed id or dropped an ostensibly-bad entry before that logic
  ever saw it would be reporting its own judgement as the model's output.
- **A parse failure is not swallowed to an empty result.** `pass1.run_pass1` already
  catches an explorer's exception and records it as a trace `"error"` field —
  "a failed chapter is a finding, not a crash" (pass1.py's own docstring).
  `pass0.run_pass0` has no such wrapper, so a `TopicLabeller` failure fails the
  whole run, which is correct for a Pass 0 failure. Catching the parse error here
  and returning `{}` would defeat both of those and hide the failure from the log.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ingest.chapters import Chapter
from provider.openai_client import ThrottledAsyncOpenAI

# Small, capped JSON responses (at most MAX_CONCEPTS_PER_CHAPTER=6 concepts plus
# their prerequisites, or one phrase per section) — generous headroom, not tuned.
DEFAULT_PASS0_MAX_TOKENS = 4096
DEFAULT_PASS1_MAX_TOKENS = 4096
# Tier 2 writes prose, ~1,000 tokens/section per docs/18 §10.3's cost model.
DEFAULT_TIER2_MAX_TOKENS = 2048


def _parse_json_object(text: str) -> dict[str, Any]:
    """Strip an optional ```json fence and parse. Raises on anything else — see
    the module docstring on why this must not degrade to `{}`."""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.split("\n", 1)[1] if "\n" in stripped else ""
        if stripped.endswith("```"):
            stripped = stripped[: -len("```")]
        stripped = stripped.strip()
    parsed = json.loads(stripped)
    if not isinstance(parsed, dict):
        raise ValueError(f"expected a JSON object, got {type(parsed).__name__}: {text!r}")
    return parsed


@dataclass
class OpenAITopicLabeller:
    """Satisfies `envelope.pass0.TopicLabeller`."""

    client: ThrottledAsyncOpenAI
    model: str
    reasoning_effort: str | None = None
    max_tokens: int = DEFAULT_PASS0_MAX_TOKENS

    async def label(self, prompt: str, section_ids: list[str]) -> dict[str, str]:
        with self.client.tagged(role="tier1_pass0"):
            result = await self.client.acomplete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                reasoning_effort=self.reasoning_effort,
            )
        parsed = _parse_json_object(result.content)
        return {str(k): str(v) for k, v in parsed.items()}


@dataclass
class OpenAIChapterExplorer:
    """Satisfies `envelope.pass1.ChapterExplorer`."""

    client: ThrottledAsyncOpenAI
    model: str
    reasoning_effort: str | None = None
    max_tokens: int = DEFAULT_PASS1_MAX_TOKENS

    async def explore(self, prompt: str, chapter: Chapter) -> dict[str, Any]:
        with self.client.tagged(role="tier1_pass1"):
            result = await self.client.acomplete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                reasoning_effort=self.reasoning_effort,
            )
        # Raw parsed JSON, unfiltered — pass1._accept_concepts/_accept_edges are
        # the sole validators, per this module's docstring.
        return _parse_json_object(result.content)


@dataclass
class OpenAILanguageModel:
    """Satisfies `orchestrate.lm_builder.LanguageModel`.

    Tier 2 output is prose, not JSON — `lm_builder.LmBuilder` writes the raw
    response straight into a `BuiltSpan`, so there is nothing to parse here.
    """

    client: ThrottledAsyncOpenAI
    model: str
    reasoning_effort: str | None = None
    max_tokens: int = DEFAULT_TIER2_MAX_TOKENS

    async def acompletion(self, prompt: str) -> str:
        with self.client.tagged(role="tier2"):
            result = await self.client.acomplete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                reasoning_effort=self.reasoning_effort,
            )
        return result.content


__all__ = [
    "OpenAITopicLabeller",
    "OpenAIChapterExplorer",
    "OpenAILanguageModel",
]
