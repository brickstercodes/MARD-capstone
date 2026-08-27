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
    for chapter in chapters:
        number = chapter.get("number")
        if number is not None and chapter["page_start"] <= page <= chapter["page_end"]:
            return int(number)
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
    """
    objectives: list[LearningObjective] = []
    index = 0
    while index < len(blocks):
        marker = blocks[index]
        if marker.get("role") != "learning_objectives":
            index += 1
            continue

        marker_page = marker["page"]
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

    docs/23-GROUNDTRUTH_SPEC.md §3.2: classify forward or backward by comparing the
    referenced chapter's page range against the citing page. Scored against
    references extracted from the text, never against edges a model emitted — the
    latter would repeat the circularity §1 rejects for concept/prerequisite ground
    truth in a more respectable form.
    """
    by_number = {c["number"]: c for c in chapters if c.get("number") is not None}
    references: list[CrossReference] = []
    current_page: int | None = None

    for raw_line in document_text.splitlines():
        line = raw_line.strip()
        page_match = PAGE_MARKER_PATTERN.match(line)
        if page_match:
            current_page = int(page_match.group(1))
            continue
        if current_page is None or line.startswith("#"):
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
            if current_page < page_start:
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
