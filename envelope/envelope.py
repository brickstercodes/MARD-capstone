"""The metadata envelope — the contribution, and its growth semantics.

`docs/01-ENVELOPE_VS_BASE_LIBRARY.md` states the distinction this module has to
implement, and it is worth restating because the code either honours it or the paper
is wrong: **in the base RLM library metadata flows upward and is observational** — a
child is handed a fresh, empty logger (`.vendor/rlm/rlm/core/rlm.py:824`) and
`root_prompt=None`, so nothing a parent learned reaches it. **In MARD the envelope
flows downward and is operative** — skeleton, accumulated findings and a parent
directive enter the child's context before it runs, changing what it can see.

Two design rules follow directly, and both are tested:

1. `for_child()` must carry the parent's findings. If it ever returns something with
   an empty findings set, MARD has silently become vanilla RLM and every O3 number
   measures nothing. `tests/test_envelope.py` pins this.
2. Growth returns a new envelope rather than mutating. An envelope is the input to a
   logged model call; one that can be edited after the fact cannot be reconciled with
   the transcript that `docs/30-MEASUREMENT_PROTOCOL.md` section 7 requires.

The A1 ablation ("envelope removed", `docs/31-ABLATIONS.md`) is expressed here as
`Envelope.stripped()` rather than as a flag threaded through the call sites, so the
vanilla-RLM control is one obvious object and not a scattered condition.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from envelope.skeleton import Skeleton

# How many prior findings a child call is shown. The envelope grows without bound
# across a deep exploration, and the whole cost claim depends on what a child pays to
# read; an unbounded envelope would make MARD lose on tokens for reasons that have
# nothing to do with whether structure-awareness works.
DEFAULT_FINDING_WINDOW = 12


@dataclass(frozen=True)
class Finding:
    """One thing a call learned, attributed to where and when it was learned."""

    section_id: str
    pass_index: int
    concepts: tuple[str, ...] = ()
    prerequisites: tuple[tuple[str, str], ...] = ()
    """(prerequisite, dependent) pairs, in that order. Named-direction pairs, matching
    `plan.models.ConceptEdge`, because an edge whose arrows silently reverse scores as
    confidently wrong rather than failing."""

    note: str = ""

    def render(self) -> str:
        parts = [f"§{self.section_id} (pass {self.pass_index})"]
        if self.concepts:
            parts.append("concepts: " + ", ".join(self.concepts))
        if self.prerequisites:
            edges = ", ".join(f"{a} -> {b}" for a, b in self.prerequisites)
            parts.append("prereqs: " + edges)
        if self.note:
            parts.append(self.note)
        return " | ".join(parts)


@dataclass(frozen=True)
class Envelope:
    """What a MARD call sees before it runs: structure, history, and instruction."""

    document_id: str
    skeleton: Skeleton
    findings: tuple[Finding, ...] = ()
    directive: str | None = None
    target_section_id: str | None = None
    finding_window: int = field(default=DEFAULT_FINDING_WINDOW)

    @classmethod
    def from_skeleton(cls, skeleton: Skeleton) -> Envelope:
        return cls(document_id=skeleton.document_id, skeleton=skeleton)

    def with_findings(self, *findings: Finding) -> Envelope:
        """Accumulate. This is the "growing" in "growing metadata envelope"."""
        return replace(self, findings=self.findings + tuple(findings))

    def for_child(self, section_id: str, directive: str) -> Envelope:
        """The envelope a child call receives — the downward, operative flow.

        Carries the full skeleton and the accumulated findings, plus a directive
        specific to this child. This is the one method that distinguishes MARD from
        the base library; see the module docstring.
        """
        return replace(self, target_section_id=section_id, directive=directive)

    def stripped(self) -> Envelope:
        """Ablation A1: envelope removed, so the call sees raw text only.

        Keeps `document_id` so the run is still identifiable in the log, and keeps the
        target section so the same slice is read — A1 must differ from MARD in exactly
        one respect (`docs/31-ABLATIONS.md`: "What stays fixed: model pair, document,
        seed, Tier 1/Tier 2 split, depth").
        """
        return Envelope(
            document_id=self.document_id,
            skeleton=Skeleton(
                document_id=self.skeleton.document_id,
                provenance=self.skeleton.provenance,
                sections=(),
            ),
            findings=(),
            directive=None,
            target_section_id=self.target_section_id,
            finding_window=self.finding_window,
        )

    @property
    def is_stripped(self) -> bool:
        return self.skeleton.is_empty and not self.findings and self.directive is None

    def render(self) -> str:
        """The envelope as the text that enters a prompt.

        Ordered skeleton, then findings, then directive: the directive goes last
        because it is the instruction the call must act on, and a model reading a long
        context weights the end of it more heavily than the middle.
        """
        if self.is_stripped:
            return ""

        blocks: list[str] = []
        if not self.skeleton.is_empty:
            blocks.append("## STRUCTURAL MAP\n" + self.skeleton.render())

        if self.findings:
            recent = self.findings[-self.finding_window :]
            omitted = len(self.findings) - len(recent)
            header = "## FINDINGS SO FAR"
            if omitted:
                header += f" (most recent {len(recent)} of {len(self.findings)})"
            blocks.append(header + "\n" + "\n".join(f.render() for f in recent))

        if self.target_section_id:
            blocks.append(f"## YOUR TARGET\n§{self.target_section_id}")

        if self.directive:
            blocks.append("## YOUR DIRECTIVE\n" + self.directive)

        return "\n\n".join(blocks)

    def to_dict(self) -> dict[str, Any]:
        """Serialised for the run log, per docs/30-MEASUREMENT_PROTOCOL.md section 7.

        "Every run logged: envelope state" — this is that state, and it includes the
        rendered size because the envelope's own token cost is part of what O6 measures.
        """
        return {
            "document_id": self.document_id,
            "provenance": self.skeleton.provenance,
            "skeleton_sections": len(self.skeleton.sections),
            "findings_total": len(self.findings),
            "findings_shown": min(len(self.findings), self.finding_window),
            "target_section_id": self.target_section_id,
            "has_directive": self.directive is not None,
            "is_stripped": self.is_stripped,
            "rendered_chars": len(self.render()),
        }
