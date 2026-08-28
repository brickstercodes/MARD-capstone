# 15 — Vertex AI patch for `GeminiClient`

> ### ⛔ SUPERSEDED IN FULL — 26 Aug 2026
>
> This document patches a **Vertex AI** code path the project no longer uses. The project
> moved to **OpenAI** on 26 Aug — see
> [`18-W3_PROVIDER_SWITCH.md`](18-W3_PROVIDER_SWITCH.md).
>
> Retained for the record. **Not maintained. Do not build against it.**

**Status:** Ready for Track 2, 9 Aug 2026 · Owner: Track 1 (Anugrah), to be applied by Track 2 · Target: `.vendor/rlm/rlm/clients/gemini.py` (gitignored, so this patch lives here as the source of truth rather than in a diff against a file this repo doesn't track)

## Why this, and not a new REST client

`google-genai` (already a core dependency, `>=1.56.0`) supports Vertex AI natively via `genai.Client(vertexai=True, project=..., location=..., credentials=...)` — confirmed by reading the SDK's own `Client.__init__` source. `GeminiClient.__init__` just never exposes that path; it hardcodes the direct API-key constructor call. Everything else in the class — `completion`, `acompletion`, `_prepare_contents` (OpenAI-style message → Gemini `Content` conversion), `_track_cost`, `get_usage_summary` — is backend-agnostic and needs no changes. So the fix is a constructor patch, not a new client.

An earlier draft considered here was a hand-rolled REST client (raw `requests` calls against `aiplatform.googleapis.com`). Rejected: it has no async path (breaks Tier 2's fork-join concurrency, which needs `acompletion`), no retry/backoff (Track 2's own `docs/RATE_LIMIT_BUDGET.md` §3 policy — honour `Retry-After`, jittered exponential backoff, log 429s as data — would need reimplementing from scratch), and returns a bare tuple instead of the `UsageSummary`/`ModelUsageSummary` shape `runlog` already consumes. One reference detail from that draft is worth keeping — see "credential loading" below.

## The patch

```python
import json
import os
from collections import defaultdict
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from rlm.clients.base_lm import BaseLM
from rlm.core.types import ModelUsageSummary, UsageSummary

load_dotenv()

DEFAULT_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class GeminiClient(BaseLM):
    """
    LM Client for running models with the Google Gemini API.
    Uses the official google-genai SDK.

    Supports two backends, chosen by `use_vertex`:
      - Direct Gemini API (default) — requires GEMINI_API_KEY.
      - Vertex AI — requires GOOGLE_CLOUD_PROJECT (or `project` kwarg) and
        Application Default Credentials, or a service-account JSON via
        GOOGLE_APPLICATION_CREDENTIALS_JSON.

    MARD runs Vertex-only (docs/12-MODEL_PAIR.md) — credits are redeemable
    via Vertex only, not the direct API. Direct-API support is left in
    place because it's what upstream ships and other users of this vendored
    copy may still want it.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = "gemini-2.5-flash",
        use_vertex: bool = False,
        project: str | None = None,
        location: str | None = None,
        **kwargs,
    ):
        super().__init__(model_name=model_name, **kwargs)

        http_options = types.HttpOptions(timeout=int(self.timeout * 1000))  # milliseconds

        if use_vertex:
            project = project or os.environ.get("GOOGLE_CLOUD_PROJECT")
            location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
            if not project:
                raise ValueError(
                    "Vertex AI requires a project. Set GOOGLE_CLOUD_PROJECT env "
                    "var or pass project=."
                )

            credentials = self._load_vertex_credentials()

            self.client = genai.Client(
                vertexai=True,
                project=project,
                location=location,
                credentials=credentials,
                http_options=http_options,
            )
        else:
            if api_key is None:
                api_key = DEFAULT_GEMINI_API_KEY
            if api_key is None:
                raise ValueError(
                    "Gemini API key is required. Set GEMINI_API_KEY env var or pass api_key."
                )
            self.client = genai.Client(api_key=api_key, http_options=http_options)

        self.model_name = model_name
        self.use_vertex = use_vertex

        # Per-model usage tracking -- unchanged from upstream
        self.model_call_counts: dict[str, int] = defaultdict(int)
        self.model_input_tokens: dict[str, int] = defaultdict(int)
        self.model_output_tokens: dict[str, int] = defaultdict(int)
        self.model_total_tokens: dict[str, int] = defaultdict(int)
        self.last_prompt_tokens = 0
        self.last_completion_tokens = 0

    @staticmethod
    def _load_vertex_credentials():
        """Service-account JSON from env, falling back to ADC.

        Kept as an explicit method (rather than relying on genai.Client's
        own ADC fallback silently) because a silent auth fallback is exactly
        what CLAUDE.md's "security defaults are loud failures" rule (Part
        1.9) exists to prevent -- if the service-account path is meant to be
        used and the JSON is malformed, we want that to fail loudly here,
        not surface three calls later as an opaque 401 from Vertex.
        """
        cred_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        if cred_json:
            from google.oauth2 import service_account

            info = json.loads(cred_json)
            return service_account.Credentials.from_service_account_info(
                info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        # Falls through to ADC inside genai.Client if credentials=None.
        return None

    # completion(), acompletion(), _prepare_contents(), _track_cost(),
    # get_usage_summary(), get_last_usage() -- all unchanged from upstream.
    # They call self.client.models.generate_content / self.client.aio.models.generate_content,
    # which work identically whether self.client was constructed for the
    # direct API or for Vertex -- the backend switch lives entirely in
    # __init__.
```

**What to actually copy:** everything above `# completion(), acompletion(), ...` replaces the top of the existing file down through `__init__`. Everything below that comment — `completion`, `acompletion`, `_prepare_contents`, `_track_cost`, `get_usage_summary`, `get_last_usage` — is copied unchanged from the current vendored file. Nothing in those methods references `api_key` or the direct-API constructor path, so they don't need touching.

**Call site change, wherever `GeminiClient` gets instantiated for MARD:**

```python
tier1_client = GeminiClient(model_name="gemini-3.6-flash", use_vertex=True)
tier2_client = GeminiClient(model_name="gemini-3.1-flash-lite", use_vertex=True)
```

## Second patch: `None` response crashes the RLM regex, not just the Tier 2 join

**Status:** Applied, 22 Aug 2026 · Found by Parth (Track 2), documented in `TRACK2.md`, folded in here because `.vendor/` is gitignored and this doc is the only thing that survives a `bootstrap_rlm.sh` — that gap is exactly why it regressed the first time: Parth's fix lived only on his machine and never travelled.

`.vendor/rlm/rlm/utils/parsing.py:18` does `re.finditer(pattern, text, re.DOTALL)` against whatever `GeminiClient.completion`/`acompletion` return. The Google SDK sets `response.text` to `None` — not `""` — when the model emits no text part: a safety block, a `MAX_TOKENS` finish with nothing produced, or a function-call-only candidate. The two return sites in the patch above (`return response.text`, in both `completion` and `acompletion`) pass that `None` straight through, and the regex raises `TypeError: expected string or bytes-like object, got 'NoneType'`. This is the same failure class as the empty-span bug closed in #48 (PR review, `orchestrate/builder.py`): a model returns nothing and downstream code assumes content. There it was silent (the join accepted `""` as a valid span); here it's loud (RLM crashes outright), which is the better failure mode but still needs handling so one empty call in a few hundred doesn't take down a whole run.

Add this function once, at module scope (not inside the class):

```python
def _text_or_empty(response: object) -> str:
    """The SDK sets .text to None when the model emits no text part.

    A safety block, a MAX_TOKENS finish with nothing produced, or a function-call-only
    candidate all land here. Upstream never sees it because the OpenAI client returns ""
    in the same situation, so this is specific to the Vertex path. Returning "" lets RLM
    find no code blocks and iterate again, which is the right behaviour when one call in
    a few hundred comes back empty during W6. The finish reason is printed rather than
    swallowed: an empty response is a fact about the run, not noise.
    """
    text = getattr(response, "text", None)
    if text is None:
        candidates = getattr(response, "candidates", None) or []
        reason = getattr(candidates[0], "finish_reason", "unknown") if candidates else "unknown"
        print(f"[GeminiClient] empty response, finish_reason={reason}")
        return ""
    return str(text)
```

Then route both existing return sites through it: replace `return response.text` at the end of `completion` and at the end of `acompletion` with `return _text_or_empty(response)`. Nothing else in either method changes.

**Both patches on this page are required, and both are lost on every `bootstrap_rlm.sh`** — the constructor branch from the first section and this guard. Re-apply both, in this order, every time `.vendor/rlm` is re-bootstrapped, before running anything that makes a real Vertex call.

## What still needs verifying empirically — do not assume these

1. **Env var names.** `google-genai`'s own docstring says project/location "can be obtained from environment variables" but doesn't name them in the file I read. `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_LOCATION` are Google's usual convention and are what the patch above reads explicitly (so it doesn't rely on the SDK's internal env lookup at all) — but confirm the SDK doesn't also silently read something with different precedence, by running the first real call and checking `client._api_client.project`/`.location`.
2. ~~**The "Gemini 3.x preview models need `location="global"`" rule**~~ — **Resolved, 22 Aug 2026.** `gemini-3.6-flash` 404s on `us-central1` for this project (issue #11); `location=global` is what actually works and is billed against. The constructor's default above has been changed from `us-central1` to `global` accordingly. `GOOGLE_CLOUD_LOCATION=global` is still set explicitly in `.env` and should stay that way — the default is a safety net for anyone who forgets it, not a reason to drop the explicit env var.
3. **Structured output for the Master Plan.** Tier 1 needs to emit JSON conforming to the Pydantic Master Plan schema (`CONTEXT.md` §1.5, Track 2's `plan/` module). Neither the patch above nor the original `GeminiClient` configures `response_mime_type`/`response_schema` in `GenerateContentConfig`. That's a separate, additional change to `completion`/`acompletion` (or a config passed at call time) — not covered here, and worth raising with Track 2 before W1's stub builder needs it.

## Verification debt this opens

| # | Item | Status |
|---|---|---|
| 1 | Whether `genai.Client`'s ADC fallback works correctly inside the sandboxed/CI environments Track 2 runs in, vs. needing the explicit service-account JSON path every time | [UNVERIFIED] — test on first real Vertex call |
| 2 | Billing location (`global` vs. regional) for the actual Vertex credit account | [UNVERIFIED] — Track 2, before first paid call |
