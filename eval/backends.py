"""Which provider the measurement campaign talks to, resolved in exactly one place.

Until 25 Aug 2026 the backend was not a choice: `eval/run_vanilla_rlm.py`
imported `GeminiClient` directly and hardcoded `backend="gemini"` with
`use_vertex=True`. That was fine while there was one provider and one model
pair (`docs/12-MODEL_PAIR.md`), and it stopped being fine the moment a second
provider entered the picture -- a hardcoded client name reaches into
`live_call_logging`, the rate card, the ledger and the campaign runner, so
"switch provider" turned into a diff across four files that each had to agree.

This module is that agreement, written down once. Everything provider-shaped
lives in a `BackendProfile`; every consumer asks for the active profile and
reads what it needs off it.

**Why the Gemini profile is still here rather than deleted.** 122 runs in
`runs/` and every finding in `docs/16-VANILLA_RLM_GEMINI_FIXES.md` were
measured on Vertex. A result you cannot re-derive is not a result
(`CONTEXT.md` §3.4, "a number you cannot reproduce on 29 Sep is not a
number"), and §4.3 rule 5 says surface what you cannot verify rather than
quietly dropping it. Deleting the Gemini path would silently retire that whole
body of evidence to save about twenty lines. It stays, opt-in and never the
default, so those runs remain reproducible.

Selection is by `MARD_BACKEND`, defaulting to OpenAI. Nothing reaches Vertex
unless someone sets that variable on purpose.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from runlog import sampling_params_for

BACKEND_ENV = "MARD_BACKEND"
DEFAULT_BACKEND = "openai"


@dataclass(frozen=True)
class BackendProfile:
    """Everything that changes when the provider changes, and nothing else."""

    name: str
    """The string `RLM(backend=...)` and `rlm.clients.get_client` dispatch on."""

    tier1_model: str
    """The Scout. Also the model the single-backend vanilla control runs on."""

    tier2_model: str
    """The Swarm. Unused by the vanilla control (A1 is single-backend by
    definition -- see eval/run_vanilla_rlm.py's docstring); recorded here so
    Track 1/Track 2 read the pair from the same place Track 3 does."""

    client_module: str
    client_class_name: str
    """Named as strings, not imported at module scope, so that selecting the
    OpenAI profile never imports `google-genai` and vice versa. `live_call_logging`
    patches the *class* to catch recursive child clients the library builds
    internally, so it needs the real type -- see `client_class()`."""

    runs_root: str = "runs"
    """Where this backend's runs and spend ledger live.

    Per-backend rather than global because `runs/_ledger.json` is not just a
    directory of files, it is a spend ledger with a ceiling baked in -- and that
    ceiling was INR75,000 of *Vertex credit*, converted at 95.13. OpenAI spend
    is cash from a different account against a different cap. Accumulating both
    in one ledger would produce a total that means nothing and a cap that guards
    nothing.

    Deriving it from the profile rather than reading a separate environment
    variable removes the failure where someone switches backend and forgets to
    switch ledger, silently billing OpenAI cash against the Vertex credit cap.
    """

    extra_backend_kwargs: dict[str, Any] = field(default_factory=dict)
    """Provider-specific constructor arguments (e.g. Vertex's `use_vertex`)."""

    supports_temperature: bool = True
    """GPT-5-family reasoning models reject any `temperature` other than the
    default; the Gemini path accepted `temperature=0.0` happily. See
    `sampling_params` for what this costs us."""

    reasoning_effort: str | None = None
    """Passed straight through `sampling_args` to `chat.completions.create`.
    Pinned rather than left to the provider's default because an unpinned
    reasoning budget is an unrecorded experimental variable -- it moves cost
    and quality together, and `CONTEXT.md` §3.4 requires a config snapshot
    that actually determines the run."""

    def client_class(self) -> type:
        """Import and return the client type, at call time.

        Deferred on purpose: importing this module must not require every
        provider SDK to be installed.
        """
        module = __import__(self.client_module, fromlist=[self.client_class_name])
        return getattr(module, self.client_class_name)  # type: ignore[no-any-return]

    def backend_kwargs(self, model: str | None = None) -> dict[str, Any]:
        return {"model_name": model or self.tier1_model, **self.extra_backend_kwargs}

    def sampling_params(self, seed: int) -> dict[str, Any]:
        """Seeded provider-facing sampling settings, adapted to this backend.

        Deliberately built *on top of* `runlog.sampling_params_for` rather than
        replacing it. `runlog/seeds.py` is Track 2's module and its docstring
        makes the load-bearing point that seeding has to be a single call that
        cannot be half-applied; forking that logic here would be exactly the
        half-application it warns about. So the canonical call still happens,
        and this method only removes what the provider will reject and adds
        what it needs.

        `temperature` dropping out for OpenAI is a real loss of control, not a
        formality: it removes one of the two levers `runlog/seeds.py` names for
        hosted determinism, leaving only the best-effort `seed`. That is an
        argument for the 3-seed variance policy, not against this backend --
        `docs/16` §2 already demonstrated Vertex returning different outcomes
        for an identical prompt at identical seed *with* temperature pinned to
        0.0, so the lever was not buying determinism there either.
        """
        params = sampling_params_for(seed)
        if not self.supports_temperature:
            params.pop("temperature", None)
        if self.reasoning_effort is not None:
            params["reasoning_effort"] = self.reasoning_effort
        return params


# Model IDs and the rationale for this pair: docs/17-OPENAI_PIVOT.md.
# Rates live in eval/rates.py, which is the only place a price may be written.
OPENAI = BackendProfile(
    name="openai",
    tier1_model="gpt-5.6-terra",
    tier2_model="gpt-5.6-luna",
    client_module="rlm.clients.openai",
    client_class_name="OpenAIClient",
    runs_root="runs-openai",
    # [UNVERIFIED as of 25 Aug 2026] Assumed rejected, on the GPT-5-generation
    # precedent, because the failure mode is a hard 400 on the first call rather
    # than a silent degradation. scripts/verify_rlm_openai.py probes this
    # directly for about two cents and settles it -- flip to True if it passes.
    supports_temperature=False,
    reasoning_effort="medium",
)

# Retained for reproducing the 122 Vertex runs already in runs/ and every
# experiment in docs/16. Never the default; requires MARD_BACKEND=gemini.
GEMINI_VERTEX = BackendProfile(
    name="gemini",
    tier1_model="gemini-3.6-flash",
    tier2_model="gemini-3.1-flash-lite",
    client_module="rlm.clients.gemini",
    client_class_name="GeminiClient",
    runs_root="runs",
    extra_backend_kwargs={"use_vertex": True},
    supports_temperature=True,
)

PROFILES = {"openai": OPENAI, "gemini": GEMINI_VERTEX}


def active_profile() -> BackendProfile:
    """The backend this process runs against.

    Reads the environment rather than taking a parameter because the choice has
    to be identical across `run_vanilla_rlm`, the campaign runner and the rate
    card within one run; threading it through three call sites is three chances
    for them to disagree, and a run priced against the wrong provider is the
    silent-wrong-number failure `runlog/pricing.py` was written to prevent.
    """
    name = os.environ.get(BACKEND_ENV, DEFAULT_BACKEND).strip().lower()
    try:
        return PROFILES[name]
    except KeyError:
        raise ValueError(
            f"{BACKEND_ENV}={name!r} is not a known backend. Choose one of: {sorted(PROFILES)}."
        ) from None
