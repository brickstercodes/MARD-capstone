"""Text block extraction with page mapping and heading detection.

Blocks carry their page number and bounding box rather than being flattened into a
string, because docs/30-MEASUREMENT_PROTOCOL.md section 1 requires every reported
number to trace back to a logged run, and W7's provenance spot-checks (issue #29
definition-of-done, item 2) need to answer "which page did this claim come from".
A flat string cannot answer that.

Heading detection here is deliberately font-metric based and does NOT read the PDF
bookmark outline. The outline is authoritative but it is publisher metadata, not
something a model derived from reading the document. Keeping the two provenance
paths in separate modules (see ingest/outline.py) means Track 1 has to choose,
explicitly, whether Pass 0 may see publisher metadata — rather than inheriting
that choice silently from how the parser happened to be written.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any

from ingest import pdf

# A heading has to be meaningfully larger than body text, not a rounding artefact.
HEADING_SIZE_RATIO = 1.05

# Long text is a paragraph that happens to be set large, not a heading.
MAX_HEADING_CHARS = 140

# Font sizes vary by fractions of a point within one logical style; bucket them.
SIZE_PRECISION = 1

# Heading levels are assigned by descending size rank among *structural* sizes.
MAX_DETECTED_HEADING_LEVELS = 4

# A size used on only a handful of pages is cover art, a copyright line or a stray
# logo, not a heading level. Filtering on page coverage rather than size alone is
# what stops a 36pt title-page word from being elected "level 1" and burying the
# 13pt section headings that actually structure the book — the exact failure the
# first version of this module shipped with.
MIN_STRUCTURAL_PAGE_FRACTION = 0.01
MIN_STRUCTURAL_PAGES = 5

# Headings in typeset textbooks are set bold. Requiring it keeps large-but-light
# display quotations and pull-outs from being read as structure.
MIN_BOLD_CHAR_FRACTION = 0.5

# Figure and table captions are set in a heading-like style but are not structure.
# Left unmarked they inflate the heading count and, worse, would appear in a derived
# skeleton as if they were sections.
CAPTION_PATTERN = re.compile(r"^(figure|table|example|listing|exhibit)\s+\d", re.I)

# OpenStax books carry the ground-truth signals the measurement protocol scores
# against (section 2: glossary terms, per-chapter learning objectives) inside named
# blocks. Tagging the block that opens each one costs nothing here and saves Track 4's
# W2 ground-truth extraction from re-deriving section boundaries.
ROLE_PATTERNS = {
    "learning_objectives": re.compile(r"^\s*learning objectives?\b", re.I),
    "key_terms": re.compile(r"^\s*key terms\b", re.I),
    "summary": re.compile(r"^\s*(chapter\s+)?(review\s+)?summary\b", re.I),
    "check_understanding": re.compile(r"^\s*(check your understanding|think about it)\b", re.I),
    "review_questions": re.compile(
        r"^\s*(review|conceptual|practice)\s+(questions|problems)\b", re.I
    ),
    "references": re.compile(r"^\s*(references|footnotes|bibliography)\b", re.I),
}


@dataclass(frozen=True)
class Block:
    """One contiguous run of text, with enough provenance to be cited."""

    block_id: str
    page: int
    kind: str
    level: int | None
    role: str | None
    text: str
    bbox: tuple[float, float, float, float]
    font_size: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _dominant_font_size(doc: Any) -> float:
    """Body-text size, weighted by how much text is actually set in it.

    Weighting by character count rather than span count matters: a book has many
    short large-font headings and few long body paragraphs, so counting spans
    would elect a heading size as the body size on some layouts.
    """
    weighted: Counter[float] = Counter()
    for _number, page in pdf.pages(doc):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    size = round(span["size"], SIZE_PRECISION)
                    weighted[size] += len(span["text"])
    return weighted.most_common(1)[0][0] if weighted else 0.0


def _heading_size_levels(doc: Any, body_size: float) -> dict[float, int]:
    """Map each structural font size to a heading level, largest size = level 1.

    A size qualifies as structural only if it is larger than body text, appears on
    enough pages to be a recurring style, and is predominantly bold. See the
    constants above for why each of those three conditions is needed.
    """
    pages_per_size: Counter[float] = Counter()
    chars_per_size: Counter[float] = Counter()
    bold_chars_per_size: Counter[float] = Counter()

    for _number, page in pdf.pages(doc):
        sizes_on_page: set[float] = set()
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    size = round(span["size"], SIZE_PRECISION)
                    sizes_on_page.add(size)
                    chars_per_size[size] += len(span["text"])
                    if "bold" in span["font"].lower():
                        bold_chars_per_size[size] += len(span["text"])
        for size in sizes_on_page:
            pages_per_size[size] += 1

    min_pages = max(MIN_STRUCTURAL_PAGES, int(pdf.page_count(doc) * MIN_STRUCTURAL_PAGE_FRACTION))

    structural = [
        size
        for size in pages_per_size
        if size >= body_size * HEADING_SIZE_RATIO
        and size != body_size
        and pages_per_size[size] >= min_pages
        and bold_chars_per_size[size] >= chars_per_size[size] * MIN_BOLD_CHAR_FRACTION
    ]

    ranked = sorted(structural, reverse=True)[:MAX_DETECTED_HEADING_LEVELS]
    return {size: level for level, size in enumerate(ranked, start=1)}


def _classify_role(text: str) -> str | None:
    for role, pattern in ROLE_PATTERNS.items():
        if pattern.match(text):
            return role
    return None


def extract_blocks(path: str, doc_id: str) -> tuple[list[Block], float]:
    """Parse a PDF into page-mapped blocks. Returns the blocks and the body font size."""
    doc = pdf.open_document(path)
    body_size = _dominant_font_size(doc)
    size_levels = _heading_size_levels(doc, body_size)

    blocks: list[Block] = []
    for page_number, page in pdf.pages(doc):
        for block_index, raw in enumerate(page.get_text("dict")["blocks"]):
            lines = raw.get("lines")
            if not lines:
                continue  # image or drawing block; no text to map

            text = " ".join(span["text"] for line in lines for span in line["spans"]).strip()
            text = re.sub(r"\s+", " ", text)
            if not text:
                continue

            sizes = [
                round(span["size"], SIZE_PRECISION) for line in lines for span in line["spans"]
            ]
            block_size = max(sizes)
            level = size_levels.get(block_size)
            is_caption = bool(CAPTION_PATTERN.match(text))
            is_heading = level is not None and len(text) <= MAX_HEADING_CHARS and not is_caption

            # Role is checked on any short block, not only on detected headings.
            # OpenStax sets "Learning Objectives" and "Key Terms" in a smaller style
            # than chapter titles, and those blocks carry the ground truth the
            # measurement protocol scores against — losing them to a font-size miss
            # would cost more than an occasional false tag.
            role = _classify_role(text) if len(text) <= MAX_HEADING_CHARS else None

            blocks.append(
                Block(
                    block_id=f"{doc_id}:p{page_number:04d}:b{block_index:03d}",
                    page=page_number,
                    kind="heading" if is_heading else ("caption" if is_caption else "body"),
                    level=level if is_heading else None,
                    role=role,
                    text=text,
                    bbox=tuple(round(v, 1) for v in raw["bbox"]),
                    font_size=block_size,
                )
            )

    return blocks, body_size
