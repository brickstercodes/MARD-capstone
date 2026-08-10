# 15 — Vertex AI patch for `GeminiClient`

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
            location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
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

## What still needs verifying empirically — do not assume these

1. **Env var names.** `google-genai`'s own docstring says project/location "can be obtained from environment variables" but doesn't name them in the file I read. `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_LOCATION` are Google's usual convention and are what the patch above reads explicitly (so it doesn't rely on the SDK's internal env lookup at all) — but confirm the SDK doesn't also silently read something with different precedence, by running the first real call and checking `client._api_client.project`/`.location`.
2. **The "Gemini 3.x preview models need `location=\"global\"`" rule** that appeared in the earlier REST draft. Our two chosen models (`gemini-3.6-flash`, `gemini-3.1-flash-lite`) are both **GA**, not preview, so this specific rule likely doesn't apply — but the Vertex pricing page (`docs/12-MODEL_PAIR.md`) does distinguish Global vs. non-global endpoint pricing even for GA models (non-global carries a ~10% surcharge, live since 1 Jul 2026). **Test explicitly which `location` value the account's Vertex credits are billed against**, and pass that `location` value rather than defaulting to `us-central1` if global is cheaper or required.
3. **Structured output for the Master Plan.** Tier 1 needs to emit JSON conforming to the Pydantic Master Plan schema (`CONTEXT.md` §1.5, Track 2's `plan/` module). Neither the patch above nor the original `GeminiClient` configures `response_mime_type`/`response_schema` in `GenerateContentConfig`. That's a separate, additional change to `completion`/`acompletion` (or a config passed at call time) — not covered here, and worth raising with Track 2 before W1's stub builder needs it.

## Verification debt this opens

| # | Item | Status |
|---|---|---|
| 1 | Whether `genai.Client`'s ADC fallback works correctly inside the sandboxed/CI environments Track 2 runs in, vs. needing the explicit service-account JSON path every time | [UNVERIFIED] — test on first real Vertex call |
| 2 | Billing location (`global` vs. regional) for the actual Vertex credit account | [UNVERIFIED] — Track 2, before first paid call |
