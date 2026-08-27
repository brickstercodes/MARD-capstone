"""Reasoning-model request shaping for MARD's own Tier 1/2 calls.

`Zhang_RLM`'s own `_normalize_sampling_args` (`rlm/clients/openai.py`) does the
`max_tokens` → `max_completion_tokens` rename for the vanilla arm's calls, but does
*not* strip `temperature` for reasoning models the way this module does — so
`vanilla/run.py` never puts one in `sampling_args`/`sub_sampling_args` at all, rather
than relying on the library to ignore it. MARD's own Tier 1/2 calls go through this
module's `.venv`-fresh `openai.AsyncOpenAI` directly rather than through the vendored
RLM library, so the same reasoning-model rule has to exist here too — duplicated
deliberately (`envelope/pass1.py`'s `CONCEPT_ID` regex sets the precedent) rather than
imported from `.vendor/rlm`, which `orchestrate/lm_builder.py`'s own docstring already
warns off importing from (the editable-install trap, TRACK2.md).
"""

from __future__ import annotations

from typing import Any

# Both gpt-5.2 (Tier 1) and gpt-5-mini (Tier 2) match "gpt-5", so this applies
# uniformly to both roles for the current model pair (docs/18 §7 item 1, resolved).
_REASONING_MODEL_PREFIXES = ("o1", "o3", "o4", "gpt-5")


def is_reasoning_model(model: str) -> bool:
    name = model.rsplit("/", 1)[-1]
    return name.startswith(_REASONING_MODEL_PREFIXES)


def completion_kwargs(
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    *,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> dict[str, Any]:
    """Build the `chat.completions.create` kwargs for one call.

    `temperature` is silently omitted for a reasoning model — those endpoints
    reject a custom value outright (docs/18 §5.4). The caller is responsible for
    recording in the run's config snapshot that a configured temperature was not
    applied; this function only controls what actually reaches the wire.
    """
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    if temperature is not None and not is_reasoning_model(model):
        kwargs["temperature"] = temperature
    if reasoning_effort is not None:
        kwargs["extra_body"] = {"reasoning_effort": reasoning_effort}
    return kwargs
