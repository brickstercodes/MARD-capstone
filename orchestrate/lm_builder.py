"""A Tier 2 builder backed by a real language-model client.

The stub proves the fork-join; this proves the seam. `LmBuilder` is the shape a
real builder has, and it satisfies the same `Builder` protocol, so W2's worker
pool has something to put under load before there is a Vertex bill attached.

Tier 2 is a plain completion, not a recursive call. The scout (Tier 1) is the
RLM; the swarm reads one section and writes one span (CONTEXT.md §1.4). Modelling
Tier 2 as recursion would inflate the cheap tier's cost and quietly undo the
two-tier claim.

`LanguageModel` is declared structurally rather than imported from the RLM
library on purpose. `rlm.clients.base_lm.BaseLM` satisfies it — the tests prove
that against the library's own `MockLM` — but importing it here would make every
module in this package depend on an editable install that has already broken
once on this machine (TRACK2.md, "the editable-install trap").
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from orchestrate.builder import BuilderBrief, BuiltSpan, Provenance


@runtime_checkable
class LanguageModel(Protocol):
    """The one method Tier 2 needs. `rlm`'s `BaseLM` satisfies this."""

    async def acompletion(self, prompt: str) -> str: ...


@dataclass
class LmBuilder:
    """Turns one brief into one span by asking a model.

    Deliberately not logging per-call token counts yet. The only client this can
    be driven with offline is the RLM library's `MockLM`, whose usage numbers are
    invented (ten tokens a call); writing those into `runs/` would put fabricated
    figures where Track 3 reads real ones. Call logging lands in W2 alongside the
    Vertex client that reports true usage.
    """

    lm: LanguageModel
    name: str = "tier2"

    async def build(self, brief: BuilderBrief) -> BuiltSpan:
        response = await self.lm.acompletion(prompt_for(brief))
        source = brief.concept.source
        return BuiltSpan(
            concept_id=brief.concept.id,
            position=brief.position,
            text=response,
            provenance=Provenance(
                document_id=brief.document_id,
                section_id=source.section_id,
                page_start=source.page_start,
                page_end=source.page_end,
                plan_position=brief.position,
                builder=self.name,
            ),
        )


def prompt_for(brief: BuilderBrief) -> str:
    """Render a brief as a prompt.

    Kept as a function so the wording is one visible, diffable thing rather than
    scattered f-strings. The wording itself is not tuned — Tier 2 prompt work is
    W2, and CONTEXT.md §3.4 makes any change after Feature freeze A a re-run of
    the whole matrix.
    """
    concept = brief.concept
    return (
        f"You are writing one section of a study guide for '{brief.document_id}'.\n"
        f"Concept: {concept.label}\n"
        f"Source: section {concept.source.section_id}, "
        f"pages {concept.source.page_start}-{concept.source.page_end}\n"
        f"Position in the study sequence: {brief.position}\n\n"
        f"{brief.directive}\n\n"
        "Write only this section. Do not summarise what comes before or after it."
    )
