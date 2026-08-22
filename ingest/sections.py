"""Blocks grouped into sections, in the shape the Master Plan contract requires.

`plan.models.SourceSpan` (PR #48) is the agreed boundary between this package and
Track 2's contract, and it asks for four fields: `section_id`, `book_position`,
`page_start`, `page_end`. Blocks alone cannot supply them — a block is a paragraph,
not a unit of the document's own structure — so this module is what makes the parse
addressable by the rest of the pipeline.

It is also the unit Pass 0 reasons over. `CONTEXT.md` line 74 specifies Pass 0's
output as "titles, topic per section, page ranges, density estimate": three of those
four are computable here, with no model call at all.

**On `section_id` stability.** The contract requires an id "stable across re-parses".
The id is derived from a slug of the section title rather than from its ordinal
position, because a title is the most stable thing about a section — re-running the
parser with different thresholds can shift positions and page counts, but the words
in the heading do not move. Collisions get a numeric suffix, which means a document
with two identically titled sections has one id that is position-dependent. That is
recorded here rather than hidden: it is a real, narrow instability.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from ingest.blocks import Block

# The heading level that marks a section boundary is chosen per document, not fixed.
#
# Fixing it at level 1 was wrong and the numbers said so: it gives 120 sections in
# Introduction to Computer Science (7.8 pages each — right) but 9 in University
# Physics (106 pages each — one "section" per chapter), because the two books map
# their typography onto structure differently.
#
# The rule below is deliberately document-intrinsic: it picks the shallowest detected
# level whose sections come out a plausible length. It does NOT consult the PDF
# outline, even though the outline would pick better — the outline is what
# `envelope.fidelity` scores this against, and tuning the thing being measured against
# its own yardstick would make the recall number meaningless.
MIN_PAGES_PER_SECTION = 3
MAX_PAGES_PER_SECTION = 40
CANDIDATE_HEADING_LEVELS = (1, 2, 3, 4)

MAX_SLUG_CHARS = 60

# Kinds that carry no content and must not extend a section's page span.
NON_CONTENT_KINDS = frozenset({"boilerplate", "front_matter"})


@dataclass(frozen=True)
class Section:
    """One addressable unit of the document, ready to become a SourceSpan."""

    section_id: str
    title: str
    book_position: int
    page_start: int
    page_end: int
    char_count: int
    block_ids: tuple[str, ...]

    @property
    def page_count(self) -> int:
        return self.page_end - self.page_start + 1

    @property
    def density(self) -> float:
        """Characters per page — Pass 0's "density estimate", computed not guessed.

        This is what tells the scout where the content actually is: a 40-page section
        at 300 chars/page is mostly figures, and a targeted deep dive spent there buys
        less than the same call spent on a dense one.
        """
        return round(self.char_count / self.page_count, 1)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["page_count"] = self.page_count
        payload["density"] = self.density
        return payload

    def to_source_span(self) -> dict[str, Any]:
        """The four fields `plan.models.SourceSpan` requires, and nothing else."""
        return {
            "section_id": self.section_id,
            "book_position": self.book_position,
            "page_start": self.page_start,
            "page_end": self.page_end,
        }


def _slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:MAX_SLUG_CHARS].strip("-") or "untitled"


def _unique_id(doc_id: str, title: str, taken: set[str]) -> str:
    base = f"{doc_id}.{_slug(title)}"
    if base not in taken:
        taken.add(base)
        return base

    suffix = 2
    while f"{base}-{suffix}" in taken:
        suffix += 1
    candidate = f"{base}-{suffix}"
    taken.add(candidate)
    return candidate


def choose_section_level(blocks: list[Block]) -> int:
    """Pick the heading level to cut sections at, from the document's own shape.

    Returns the shallowest candidate level whose resulting sections average a
    plausible number of pages. Falls back to the level with the most headings when no
    level qualifies, so a document with unusual typography still yields sections and
    the fidelity score reports how badly rather than the pipeline yielding nothing.
    """
    total_pages = max((block.page for block in blocks), default=1)
    counts = {
        level: sum(1 for b in blocks if b.kind == "heading" and b.level == level)
        for level in CANDIDATE_HEADING_LEVELS
    }

    for level in CANDIDATE_HEADING_LEVELS:
        if not counts[level]:
            continue
        pages_each = total_pages / counts[level]
        if MIN_PAGES_PER_SECTION <= pages_each <= MAX_PAGES_PER_SECTION:
            return level

    return max(counts, key=lambda level: counts[level])


def build_sections(blocks: list[Block], doc_id: str, level: int | None = None) -> list[Section]:
    """Group blocks into sections cut at heading level `level`.

    Content appearing before the first qualifying heading is dropped rather than
    filed under a synthetic "preamble" section. A section that no heading declares is
    not part of the document's own structure, and inventing one would put text into
    the skeleton that the document never said was a unit.
    """
    section_level = level if level is not None else choose_section_level(blocks)

    sections: list[Section] = []
    taken_ids: set[str] = set()

    current_title: str | None = None
    current_blocks: list[Block] = []

    def flush() -> None:
        if current_title is None:
            return
        content = [block for block in current_blocks if block.kind not in NON_CONTENT_KINDS]
        if not content:
            return
        pages = [block.page for block in content]
        sections.append(
            Section(
                section_id=_unique_id(doc_id, current_title, taken_ids),
                title=current_title,
                book_position=len(sections),
                page_start=min(pages),
                page_end=max(pages),
                char_count=sum(len(block.text) for block in content),
                block_ids=tuple(block.block_id for block in content),
            )
        )

    for block in blocks:
        starts_section = block.kind == "heading" and block.level == section_level
        if starts_section:
            flush()
            current_title = block.text
            current_blocks = [block]
        elif current_title is not None:
            current_blocks.append(block)

    flush()
    return sections
