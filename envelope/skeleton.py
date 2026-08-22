"""The Pass 0 skeleton: the structural map, and where each part of it came from.

`CONTEXT.md` line 74 specifies Pass 0 exactly — input "Headings, TOC, index
(~500 tokens)", output "Structural map: titles, topic per section, page ranges,
density estimate". Three of those four are arithmetic over Track 4's parse and need
no model call; only `topic` requires Tier 1. Splitting them is not an optimisation,
it is what makes the skeleton partly reproducible: a re-run changes the topics and
nothing else, so a difference in results can be attributed.

**Provenance is a field, not a comment.** A skeleton derived from the document's own
headings and a skeleton copied from the PDF bookmark tree are different evidence,
and `docs/16-PRIMARY_DOCUMENT.md` leaves open which one Pass 0 is allowed to use.
Recording it on the object means a run log can answer the question later, and means
the two can be compared rather than argued about (see `envelope.fidelity`).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any, Literal

from ingest.sections import Section

Provenance = Literal["derived_from_text", "pdf_outline"]

# Roughly four characters per token for English prose. Used only to report the
# skeleton's rendered size against Pass 0's ~500-token budget, never to bill anything.
CHARS_PER_TOKEN_ESTIMATE = 4


@dataclass(frozen=True)
class SkeletonSection:
    section_id: str
    title: str
    book_position: int
    page_start: int
    page_end: int
    density: float
    topic: str | None = None
    """Tier 1's one-line summary of what the section is about. None until the scout
    has labelled it — an unlabelled skeleton is still a usable structural map, which
    is why this is optional rather than required."""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Skeleton:
    document_id: str
    provenance: Provenance
    sections: tuple[SkeletonSection, ...]

    @classmethod
    def from_sections(cls, document_id: str, sections: list[Section]) -> Skeleton:
        """Build the deterministic half of the map from Track 4's parse."""
        return cls(
            document_id=document_id,
            provenance="derived_from_text",
            sections=tuple(
                SkeletonSection(
                    section_id=section.section_id,
                    title=section.title,
                    book_position=section.book_position,
                    page_start=section.page_start,
                    page_end=section.page_end,
                    density=section.density,
                )
                for section in sections
            ),
        )

    def with_topics(self, topics: dict[str, str]) -> Skeleton:
        """Return a new skeleton with Tier 1's topic labels applied.

        Returns a copy rather than mutating, for the same reason `plan.models` freezes
        the Master Plan: once a skeleton has been used to make a call, it is evidence,
        and evidence that can be edited in place cannot be reconciled with a log.
        """
        return replace(
            self,
            sections=tuple(
                replace(section, topic=topics.get(section.section_id, section.topic))
                for section in self.sections
            ),
        )

    @property
    def is_empty(self) -> bool:
        """True when the document offered no exploitable structure.

        This is the O4 boundary made checkable rather than asserted. `CONTEXT.md`
        line 92: "On documents with no headings or hierarchy, Pass 0 yields an empty
        skeleton and MARD degenerates to vanilla RLM." A caller that sees this should
        report degeneration, not fabricate a structure.
        """
        return not self.sections

    @property
    def labelled_fraction(self) -> float:
        if not self.sections:
            return 0.0
        labelled = sum(1 for section in self.sections if section.topic)
        return round(labelled / len(self.sections), 3)

    def render(self) -> str:
        """The skeleton as the text a child call actually receives.

        One line per section, deliberately terse: this text is paid for on every
        recursive call, so its size is a running cost and not a formatting choice.
        """
        lines = [f"DOCUMENT {self.document_id} — {len(self.sections)} sections"]
        for section in self.sections:
            topic = f" — {section.topic}" if section.topic else ""
            lines.append(
                f"[{section.book_position}] {section.title} "
                f"(pp.{section.page_start}-{section.page_end}, "
                f"{section.density:.0f} chars/page){topic}"
            )
        return "\n".join(lines)

    @property
    def estimated_render_tokens(self) -> int:
        return len(self.render()) // CHARS_PER_TOKEN_ESTIMATE

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "provenance": self.provenance,
            "section_count": len(self.sections),
            "labelled_fraction": self.labelled_fraction,
            "estimated_render_tokens": self.estimated_render_tokens,
            "sections": [section.to_dict() for section in self.sections],
        }
