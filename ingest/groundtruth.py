"""Document-native ground truth: learning objectives and cross-references.

docs/23-GROUNDTRUTH_SPEC.md froze the ground-truth *source* as document-native,
extracted programmatically, never expert-annotated (docs/30-MEASUREMENT_PROTOCOL.md
§2 — model-generated ground truth was considered and rejected as circular, see
docs/23 §1). This module implements the two sources costed high-confidence there:

  learning objectives   §3.1 — the task-score reference set for Manuscript A.
  cross-references       §3.2 — feeds the O5 forward-reference-violation metric.

Glossary terms (§3.3) are deferred: extraction depends on an `[UNVERIFIED]` PDF
font-face check that cannot be run until the source PDF is re-fetched. Review
questions (§3.4) are out of scope entirely — docs/30 §2 fixes the evaluated
modality as explanations only.

Cross-references are classified against **book order** (page position) only.
Classifying against Master Plan join order is also specified in docs/30 §3, but
no Master Plan artefact exists for introcs yet (`master_plan_trace.json` records
`compiled: false`) — that reclassification is Track 2/3 follow-up, not invented here.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from ingest.chapters import CHAPTER_OPENER, CHAPTER_PREFIX

BULLET_PATTERN = re.compile(r"•\s*")
PAGE_MARKER_PATTERN = re.compile(r"^\[\[page:(\d+)\]\]$")

# introcs chapter titles are numbered "N.M Title" (see ingest/chapters.py), never
# "Chapter N" — so this pattern only fires on in-text cross-references, not on a
# chapter's own heading. A heading line is still excluded defensively below in case
# another corpus's typography does use "Chapter N" as a heading.
CHAPTER_REF_PATTERN = re.compile(r"\bChapter\s+(\d{1,2})\b")

CONTEXT_CHARS_BEFORE = 40
CONTEXT_CHARS_AFTER = 60


@dataclass(frozen=True)
class LearningObjective:
    """One bulleted objective, attributed back to the chapter and page it came from."""

    objective_id: str
    chapter_number: int | None
    page: int
    text: str
    source_block_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CrossReference:
    """One in-text "Chapter N" mention, classified against book (page) order."""

    citing_page: int
    referenced_chapter: int
    target_page_start: int | None
    target_page_end: int | None
    classification: str
    """"forward" | "backward" | "same_chapter" | "unresolved" (no chapter numbered N)."""
    context: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _chapter_for_page(chapters: list[dict[str, Any]], page: int) -> int | None:
    """Page -> chapter, by range membership. **Fallback only** — every chapter
    boundary in `corpus/introcs/chapters.json` overlaps its neighbour by exactly one
    shared page (chapter N's `page_end` equals chapter N+1's `page_start`, since a
    chapter can begin partway down the page the previous one ends on), so this
    function's first-match resolution silently favours the *earlier* chapter for
    anything on a boundary page — verified directly: block 529 (the "Learning
    Objectives" marker opening chapter 2's first section, on page 50, which chapter
    1 also ends on) resolved to chapter 1 under this function alone. `eval.ordering.
    chapter_for_page` hit the identical bug for MARD concepts (`docs/35` §2.2,
    `docs/38` §5.1); this is the third instance of the same mistake, now fixed at
    its root by preferring `_chapter_for_block`/structural chapter tracking, which
    read the document's own headings instead of doing page arithmetic. Kept only as
    what `_chapter_for_block` falls back to when no numbered heading precedes a
    marker at all (a case that does not occur anywhere in the real corpus — verified,
    zero of 61 markers need it — but a degenerate/synthetic input might still hit it,
    and returning `None` outright there would be a worse regression than an
    occasionally-wrong page guess).
    """
    for chapter in chapters:
        number = chapter.get("number")
        if number is not None and chapter["page_start"] <= page <= chapter["page_end"]:
            return int(number)
    return None


def _chapter_number_from_heading(text: str) -> int | None:
    """A heading's own declared chapter number — "1.1 Computer Science" -> 1,
    "Chapter 4 Processes" -> 4 — via the same patterns `ingest.chapters` uses to
    group sections into chapters, so a heading is read identically wherever this
    project reads one."""
    for pattern in (CHAPTER_PREFIX, CHAPTER_OPENER):
        match = pattern.match(text)
        if match:
            return int(match.group(1))
    return None


def _chapter_for_block(blocks: list[dict[str, Any]], index: int) -> int | None:
    """Walk backward from `blocks[index]` to the nearest heading that declares a
    chapter number, and return it. Structural — document order, not page position —
    so it is immune to the page-boundary-sharing bug `_chapter_for_page` has:
    a marker block on a page two chapters share is still preceded, in block order,
    by exactly one real heading, and that heading is unambiguous about which
    chapter it opens."""
    for position in range(index, -1, -1):
        block = blocks[position]
        if block.get("kind") != "heading":
            continue
        number = _chapter_number_from_heading(block["text"])
        if number is not None:
            return number
    return None


def extract_learning_objectives(
    blocks: list[dict[str, Any]],
    doc_id: str,
    chapters: list[dict[str, Any]],
) -> list[LearningObjective]:
    """Walk forward from each `learning_objectives` marker to the next heading or role.

    docs/23-GROUNDTRUTH_SPEC.md §2: the tagged block is the heading only ("Learning
    Objectives By the end of this section, you will be able to:"); the bullets live in
    the untagged body blocks that follow, split on the `•` delimiter observed in
    corpus/introcs/document.jsonl. Collection stops at the first block that is a
    heading, a role marker, or — critically — a body block with no `•` in it: in the
    real corpus the bulleted blocks are immediately followed by ordinary prose
    (`"The field of computer science (CS) is the study of computing..."`), and that
    prose would `split()` into one bogus, unbulleted "objective" per paragraph if
    collection did not stop the moment the bullets run out.

    `chapter_number` is attributed via `_chapter_for_block` — the nearest preceding
    numbered heading in *document order* — not via the marker's page number. A page
    lookup silently misattributes any marker on a page two chapters share (every
    chapter boundary in this corpus is such a page): block 529, the marker opening
    chapter 2's first section on page 50 — the page chapter 1 also ends on —
    resolved to chapter 1 under a page-range lookup alone. 42 of 243 objectives sit
    on a shared boundary page; 39 of 243 move chapters once attribution is
    structural instead.
    """
    objectives: list[LearningObjective] = []
    index = 0
    while index < len(blocks):
        marker = blocks[index]
        if marker.get("role") != "learning_objectives":
            index += 1
            continue

        marker_page = marker["page"]
        chapter_number = _chapter_for_block(blocks, index)
        if chapter_number is None:
            # No numbered heading precedes this marker at all — does not happen
            # anywhere in the real corpus (verified: 0 of 61 markers), but fall
            # back to the page-range guess rather than giving up outright.
            chapter_number = _chapter_for_page(chapters, marker_page)

        cursor = index + 1
        source_ids = [marker["block_id"]]
        bullets: list[str] = []
        while cursor < len(blocks):
            body = blocks[cursor]
            if body["kind"] == "heading" or body.get("role") or "•" not in body["text"]:
                break
            source_ids.append(body["block_id"])
            bullets.extend(
                part.strip() for part in BULLET_PATTERN.split(body["text"]) if part.strip()
            )
            cursor += 1

        for bullet in bullets:
            objectives.append(
                LearningObjective(
                    objective_id=f"{doc_id}.lo{len(objectives):03d}",
                    chapter_number=chapter_number,
                    page=marker_page,
                    text=bullet,
                    source_block_ids=tuple(source_ids),
                )
            )
        index = cursor if cursor > index else index + 1

    return objectives


def extract_cross_references(
    document_text: str,
    chapters: list[dict[str, Any]],
) -> list[CrossReference]:
    """Regex over `document.txt` for in-text "Chapter N" references.

    docs/23-GROUNDTRUTH_SPEC.md §3.2: classify forward, backward, or same-chapter.
    Scored against references extracted from the text, never against edges a model
    emitted — the latter would repeat the circularity §1 rejects for concept/
    prerequisite ground truth in a more respectable form.

    **Classified by the citing *chapter*, tracked structurally from the document's
    own ATX headings — not by comparing the citing page number against the target
    chapter's page range.** The latter has the identical failure mode
    `_chapter_for_page` has (`extract_learning_objectives`'s docstring): a citing
    line that falls on a page two chapters share cannot be told apart from a page
    arithmetic comparison alone. `current_chapter` is updated every time a `# N.M
    Title` or `# Chapter N` heading is seen, in document order, and classification
    compares chapter numbers directly (`current_chapter` vs the referenced chapter)
    once a heading has been seen at all. Before the first numbered heading in the
    document, `current_chapter` is `None` and classification falls back to the old
    page-range comparison against the target chapter — a page that precedes every
    heading cannot be chapter-boundary-ambiguous in the first place.
    """
    by_number = {c["number"]: c for c in chapters if c.get("number") is not None}
    references: list[CrossReference] = []
    current_page: int | None = None
    current_chapter: int | None = None

    for raw_line in document_text.splitlines():
        line = raw_line.strip()
        page_match = PAGE_MARKER_PATTERN.match(line)
        if page_match:
            current_page = int(page_match.group(1))
            continue
        if line.startswith("#"):
            heading_number = _chapter_number_from_heading(line.lstrip("#").strip())
            if heading_number is not None:
                current_chapter = heading_number
            continue
        if current_page is None:
            continue

        for match in CHAPTER_REF_PATTERN.finditer(raw_line):
            referenced = int(match.group(1))
            start = match.start()
            context = raw_line[
                max(0, start - CONTEXT_CHARS_BEFORE) : start + CONTEXT_CHARS_AFTER
            ].strip()
            target = by_number.get(referenced)

            if target is None:
                references.append(
                    CrossReference(current_page, referenced, None, None, "unresolved", context)
                )
                continue

            page_start, page_end = target["page_start"], target["page_end"]
            if current_chapter is not None:
                if current_chapter == referenced:
                    classification = "same_chapter"
                elif current_chapter < referenced:
                    classification = "forward"
                else:
                    classification = "backward"
            elif current_page < page_start:
                classification = "forward"
            elif current_page > page_end:
                classification = "backward"
            else:
                classification = "same_chapter"

            references.append(
                CrossReference(
                    current_page, referenced, page_start, page_end, classification, context
                )
            )

    return references


def summarize_violations(references: list[CrossReference]) -> dict[str, int]:
    """docs/30-MEASUREMENT_PROTOCOL.md §3's O5 count, plus the other buckets for context."""
    summary = {
        "total": len(references),
        "forward": 0,
        "backward": 0,
        "same_chapter": 0,
        "unresolved": 0,
    }
    for reference in references:
        summary[reference.classification] += 1
    return summary
