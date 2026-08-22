"""The publisher's own chapter/section tree, read from the PDF bookmark outline.

**This is publisher metadata, not a derived skeleton, and that distinction is load-
bearing for the experiment.** MARD's claim (docs/00-CLAIM.md) is that a metadata
envelope built from reading roughly 3-5% of a document makes exploration structure-
aware. If Pass 0's skeleton were populated from the PDF outline instead, the paper
would be reporting the publisher's table of contents as MARD's output, and a
reviewer would be right to say so.

So this module exists, and its output is written to a separate file with an explicit
provenance field, for three legitimate uses:

1. Ground truth for evaluating how good a *derived* Pass 0 skeleton actually is.
2. Locating chapter boundaries for Track 4's W2 ground-truth extraction.
3. The parse-quality report's coverage check.

Whether Pass 0 may read it is Track 1's call, not this module's, and it is not a
question the parser should answer by accident.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from ingest import pdf


@dataclass(frozen=True)
class OutlineEntry:
    level: int
    title: str
    start_page: int
    end_page: int | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


CONTENT_START_TITLE = re.compile(r"^(chapter|part|unit)\s+\d|^\d+\s+\w", re.I)


def first_content_page(entries: list[OutlineEntry]) -> int:
    """Page where the body begins, i.e. where front matter ends.

    This matters more than it looks. The printed table of contents sits in the front
    matter *as body text*, so a model reading page 7 of this book receives the
    publisher's complete chapter list without having explored anything. That is the
    same confound as reading the PDF outline, but harder to notice because it arrives
    through the ordinary text channel. Marking front matter separately is what makes
    the choice to include or exclude it visible.

    Falls back to page 1 when no numbered chapter entry exists, which means "no front
    matter detected" rather than "there is none".
    """
    for entry in entries:
        if CONTENT_START_TITLE.match(entry.title):
            return entry.start_page
    return 1


def read_outline(path: str) -> list[OutlineEntry]:
    """Read the bookmark outline, resolving each entry's page span.

    End pages are inferred from the next entry at the same or shallower level, which
    is what makes an entry usable as a slice boundary rather than just a pointer.
    """
    doc = pdf.open_document(path)
    raw = doc.get_toc()

    entries: list[OutlineEntry] = []
    for index, (level, title, start_page) in enumerate(raw):
        end_page = None
        for next_level, _next_title, next_start in raw[index + 1 :]:
            if next_level <= level:
                end_page = max(start_page, next_start - 1)
                break
        if end_page is None:
            end_page = pdf.page_count(doc)
        entries.append(
            OutlineEntry(
                level=level,
                title=title.strip(),
                start_page=start_page,
                end_page=end_page,
            )
        )

    return entries
