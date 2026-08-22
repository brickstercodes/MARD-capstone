"""Sections grouped into chapters — the unit Pass 1 runs at.

Pass 1 runs per chapter, not per section, decided 22 Aug 2026 and recorded in
`docs/17-W1_DECISION_POINTS.md`. `CONTEXT.md` line 75 prices Pass 1 at
"~200 tokens/chapter", and `introcs` has **14** numbered chapters against 120
sections — an 8.6x difference in both call count and the envelope's own token cost,
which is paid on every recursive call. Sections remain the unit Tier 2 dispatches on.

(14, measured here, not the 18 first assumed from the PDF outline's level-1 entry
count. Those 18 include the contents, preface, "About OpenStax" and the back matter.)

**Chapters are derived from the section titles' own numbering, not from the PDF
outline.** "1.1 Computer Science" and "1.2 Computer Science across the Disciplines"
declare their chapter in their own text. Reading the bookmark tree instead would put
publisher metadata into the skeleton, which is the confound `envelope/outline.py`
exists to keep visible rather than silent.

Sections whose titles carry no number ("Chapter Review", "Key Terms") attach to the
chapter in progress. They are real content, and dropping them would lose the blocks
that carry the ground truth the measurement protocol scores against.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from ingest.sections import Section

# "1.1 Title", "12.3 Title", and Axler's "1A Title" / "7F Title".
CHAPTER_PREFIX = re.compile(r"^\s*(\d{1,2})\s*(?:\.\d+|[A-Z])\b")

# A chapter opener numbers itself without a subsection part: "Chapter 4 Processes".
CHAPTER_OPENER = re.compile(r"^\s*(?:chapter|unit)\s+(\d{1,2})\b", re.I)


@dataclass(frozen=True)
class Chapter:
    """A run of consecutive sections that declare the same chapter number."""

    chapter_id: str
    number: int | None
    """None when the chapter could not be numbered from any of its section titles —
    reported rather than guessed, because an unnumbered chapter means the numbering
    heuristic did not fit this document and the caller should know before trusting it."""

    title: str
    book_position: int
    page_start: int
    page_end: int
    char_count: int
    section_ids: tuple[str, ...]

    is_repeat: bool = False
    """This chapter's number was already used by an earlier chapter.

    A textbook numbers its chapters once, so a second run of 1..N is back matter.
    University Physics Volume 1 prints its Answer Key that way — bare "Chapter 1" to
    "Chapter 17" on pp.895-959, after the real chapters end at p.895 — which doubled
    the chapter count and would have doubled Pass 1's call volume on content that is
    answers rather than exposition.

    Marked, not deleted: `content_chapters()` is what excludes them, so the exclusion
    is visible at the call site and the pages are still in the artefact for anyone who
    wants to check the judgement.
    """

    @property
    def page_count(self) -> int:
        return self.page_end - self.page_start + 1

    @property
    def density(self) -> float:
        return round(self.char_count / self.page_count, 1)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["page_count"] = self.page_count
        payload["density"] = self.density
        payload["section_count"] = len(self.section_ids)
        return payload


def _chapter_number(title: str) -> int | None:
    for pattern in (CHAPTER_PREFIX, CHAPTER_OPENER):
        match = pattern.match(title)
        if match:
            return int(match.group(1))
    return None


def group_into_chapters(sections: list[Section], doc_id: str) -> list[Chapter]:
    """Group consecutive sections by the chapter number their titles declare.

    Grouping is on *consecutive* runs rather than on the number alone. If chapter 3's
    number reappears 400 pages later — a numbering restart in an appendix, or a
    misparsed heading — merging the two into one chapter would produce a span covering
    half the book, and every page range derived from it would be wrong.
    """
    chapters: list[Chapter] = []
    current: list[Section] = []
    current_number: int | None = None
    numbers_seen: set[int] = set()

    def flush() -> None:
        if not current:
            return
        pages = [section.page_start for section in current] + [
            section.page_end for section in current
        ]
        numbered = next((s for s in current if _chapter_number(s.title) is not None), None)
        title = numbered.title if numbered is not None else current[0].title
        position = len(chapters)
        chapters.append(
            Chapter(
                chapter_id=f"{doc_id}.ch{current_number:02d}"
                if current_number is not None
                else f"{doc_id}.unnumbered{position:02d}",
                number=current_number,
                title=title,
                book_position=position,
                page_start=min(pages),
                page_end=max(pages),
                char_count=sum(section.char_count for section in current),
                section_ids=tuple(section.section_id for section in current),
                is_repeat=current_number is not None and current_number in numbers_seen,
            )
        )
        if current_number is not None:
            numbers_seen.add(current_number)

    for section in sections:
        number = _chapter_number(section.title)
        if number is not None and number != current_number:
            flush()
            current = [section]
            current_number = number
        elif current:
            current.append(section)
        else:
            # Leading sections before any numbered one: keep them, unnumbered.
            current = [section]

    flush()
    return chapters


def content_chapters(chapters: list[Chapter]) -> list[Chapter]:
    """The chapters Pass 1 should explore: numbered, and not a repeated run.

    Unnumbered chapters are excluded too. In practice they are the leading run before
    the first numbered heading — front matter that survived the front-matter cut, or a
    chapter opener the numbering heuristic did not recognise. Either way, exploring a
    chapter the document did not number would put a unit into the plan that the
    document never declared.
    """
    return [chapter for chapter in chapters if chapter.number is not None and not chapter.is_repeat]
