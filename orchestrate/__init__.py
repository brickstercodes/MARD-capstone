"""Tier 2 fork-join execution. Owned by Track 2.

Bounded asyncio worker pool, per-builder retry, failure isolation, and a join
that respects Master Plan order rather than book order. Wall-clock is
max(builder), not the sum — that property is a measured claim, so the
orchestrator has to be honest about where time actually goes.
"""

from orchestrate.builder import (
    Artefact,
    Builder,
    BuilderBrief,
    BuiltSpan,
    Provenance,
    StubBuilder,
    briefs_for,
    execute_plan,
    execute_plan_sync,
    join_in_plan_order,
)
from orchestrate.lm_builder import LanguageModel, LmBuilder, prompt_for

__all__ = [
    "Artefact",
    "Builder",
    "BuilderBrief",
    "BuiltSpan",
    "LanguageModel",
    "LmBuilder",
    "Provenance",
    "StubBuilder",
    "briefs_for",
    "execute_plan",
    "execute_plan_sync",
    "join_in_plan_order",
    "prompt_for",
]
