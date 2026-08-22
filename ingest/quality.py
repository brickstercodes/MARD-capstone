"""The parse-quality report: evidence about how well each document parsed.

ingest/__init__.py states why this is not a build artefact: "the O4 structure-
dependence result depends on knowing which documents parsed cleanly and which did
not, so the quality report this produces is evidence, not a build artefact."

Concretely, the failure this guards against is attributing a measured difference to
MARD when it was really caused by one document parsing worse than another. A run on
a document whose equations were silently dropped is not evidence about recursion
strategies; it is evidence about PDF extraction. This report is what lets that be
distinguished after the fact instead of argued about.

Every metric here is a heuristic and is named as one. A heuristic surfaced with its
limits stated is usable; a heuristic presented as a measurement is not.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

from ingest.blocks import Block
from ingest.outline import OutlineEntry

# Below this, a page carried no usable prose — a plate, a divider, or a scan.
MIN_CHARS_PER_CONTENT_PAGE = 100

# Inline math dropped by text extraction leaves a visible scar: the punctuation that
# followed the formula survives with nothing before it — "we use Equation 3.16, with ."
#
# These rates are computed on RAW page text, not on the joined blocks this package
# produces, so the metric measures the PDF's extraction quality and not an artefact
# of how this code happens to join spans.
#
# Calibrated on the three candidate documents (22 Aug 2026), signal A per 1k lines:
#   Introduction to Computer Science  30   prose, formulas rare
#   Linear Algebra Done Right         87   formula-dense
#   University Physics Volume 1      113   formula-dense
# The threshold below sits between the prose book and the two formula-dense ones.
# It is a calibration against three files, not a validated constant.
MATH_LOSS_WARN_PER_1K_LINES = 50

MATH_LOSS_PATTERNS = {
    "orphan_punctuation": re.compile(r"[^\s]\s+[.,;]\s"),
    "line_ends_in_operator": re.compile(r"[=+\-<>−×]\s*$", re.M),
    "line_ends_in_connective": re.compile(
        r"\b(?:with|about|by|equals|where|gives|is)\s*[.,]\s*$", re.M | re.I
    ),
    "lone_symbol_line": re.compile(r"^\s*[^\w\s]{1,3}\s*$", re.M),
}


@dataclass
class QualityReport:
    doc_id: str
    source_file: str
    page_count: int
    body_font_size: float

    block_counts: dict[str, int] = field(default_factory=dict)
    role_counts: dict[str, int] = field(default_factory=dict)
    heading_level_counts: dict[str, int] = field(default_factory=dict)

    extractable_chars: int = 0
    chars_after_cleaning: int = 0
    boilerplate_chars_removed: int = 0

    low_text_pages: list[int] = field(default_factory=list)
    pages_with_no_heading: int = 0

    raw_text_lines: int = 0
    math_loss_signals: dict[str, int] = field(default_factory=dict)
    math_loss_rate_per_1k_lines: float = 0.0

    content_start_page: int = 1
    front_matter_blocks: int = 0

    outline_entries: int = 0
    outline_max_depth: int = 0
    pages_outside_outline_coverage: int = 0

    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def measure_math_loss(raw_text: str) -> tuple[int, dict[str, int], float]:
    """Rate the extraction scars left by dropped formulae, on raw extracted text."""
    lines = len([line for line in raw_text.split("\n") if line.strip()])
    signals = {name: len(pattern.findall(raw_text)) for name, pattern in MATH_LOSS_PATTERNS.items()}
    rate = 1000 * signals["orphan_punctuation"] / max(lines, 1)
    return lines, signals, round(rate, 1)


def build_report(
    doc_id: str,
    source_file: str,
    page_count: int,
    body_font_size: float,
    blocks: list[Block],
    outline: list[OutlineEntry],
    raw_text: str,
    content_start_page: int = 1,
) -> QualityReport:
    report = QualityReport(
        doc_id=doc_id,
        source_file=source_file,
        page_count=page_count,
        body_font_size=body_font_size,
        content_start_page=content_start_page,
    )

    chars_by_page: dict[int, int] = {}
    pages_with_heading: set[int] = set()

    for block in blocks:
        report.block_counts[block.kind] = report.block_counts.get(block.kind, 0) + 1
        report.extractable_chars += len(block.text)

        if block.kind == "boilerplate":
            report.boilerplate_chars_removed += len(block.text)
            continue

        if block.kind == "front_matter":
            report.front_matter_blocks += 1
            continue

        report.chars_after_cleaning += len(block.text)
        chars_by_page[block.page] = chars_by_page.get(block.page, 0) + len(block.text)

        if block.role:
            report.role_counts[block.role] = report.role_counts.get(block.role, 0) + 1

        if block.kind == "heading":
            pages_with_heading.add(block.page)
            key = f"level_{block.level}"
            report.heading_level_counts[key] = report.heading_level_counts.get(key, 0) + 1

    report.low_text_pages = sorted(
        page
        for page in range(1, page_count + 1)
        if chars_by_page.get(page, 0) < MIN_CHARS_PER_CONTENT_PAGE
    )
    report.pages_with_no_heading = page_count - len(pages_with_heading)

    (
        report.raw_text_lines,
        report.math_loss_signals,
        report.math_loss_rate_per_1k_lines,
    ) = measure_math_loss(raw_text)

    report.outline_entries = len(outline)
    report.outline_max_depth = max((entry.level for entry in outline), default=0)
    covered = {
        page
        for entry in outline
        for page in range(entry.start_page, (entry.end_page or entry.start_page) + 1)
    }
    report.pages_outside_outline_coverage = page_count - len(
        covered & set(range(1, page_count + 1))
    )

    _add_warnings(report, blocks)
    return report


def _add_warnings(report: QualityReport, blocks: list[Block]) -> None:
    """Turn the numbers into statements a person has to actively decide to ignore."""
    if not report.outline_entries:
        report.warnings.append(
            "No PDF bookmark outline. Chapter boundaries must come from detected "
            "headings alone, which is weaker evidence for the W2 ground-truth pass."
        )

    if not report.heading_level_counts:
        report.warnings.append(
            "No heading levels detected at all. Either this document does not use "
            "size or weight to mark structure, or the thresholds in ingest/blocks.py "
            "do not fit its typography. Check before trusting any structural marker."
        )

    if report.math_loss_rate_per_1k_lines > MATH_LOSS_WARN_PER_1K_LINES:
        report.warnings.append(
            f"Orphan-punctuation rate {report.math_loss_rate_per_1k_lines}/1k lines "
            f"exceeds the {MATH_LOSS_WARN_PER_1K_LINES}/1k calibration threshold. "
            "Inline formulae are being dropped by text extraction. Do not use this "
            "document for the primary quality comparison: the loss is content, not "
            "formatting, and it will masquerade as a difference between systems."
        )

    if len(report.low_text_pages) > report.page_count * 0.05:
        report.warnings.append(
            f"{len(report.low_text_pages)} of {report.page_count} pages carry almost no "
            "text. Check whether these are plates and dividers (fine) or scanned pages "
            "(would need OCR, and OCR would corrupt glossary ground truth)."
        )

    if not report.role_counts.get("learning_objectives") and not report.role_counts.get(
        "key_terms"
    ):
        report.warnings.append(
            "No learning-objective or key-terms blocks found. "
            "docs/30-MEASUREMENT_PROTOCOL.md section 2 scores task quality against "
            "document-native ground truth of exactly this kind, so this document cannot "
            "carry the primary task-score measurement."
        )

    if report.content_start_page <= 1:
        report.warnings.append(
            "Front matter not detected, so the printed table of contents (if any) is "
            "still in document.txt. A model reading it receives the publisher's "
            "chapter list without exploring — see ingest/outline.first_content_page."
        )

    if report.pages_outside_outline_coverage > report.page_count * 0.1:
        report.warnings.append(
            f"{report.pages_outside_outline_coverage} pages fall outside any outline "
            "entry's page span. Section slicing by outline will miss them."
        )


def render_markdown(report: QualityReport) -> str:
    """Human-readable form, because a JSON file nobody opens is not evidence."""
    lines = [
        f"# Parse quality — {report.doc_id}",
        "",
        f"Source: `{report.source_file}`",
        f"Pages: {report.page_count} · body font size: {report.body_font_size}pt",
        "",
        "## Extraction",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Extractable characters | {report.extractable_chars:,} |",
        f"| After boilerplate removal | {report.chars_after_cleaning:,} |",
        f"| Removed as running header/footer | {report.boilerplate_chars_removed:,} |",
        f"| Blocks by kind | {report.block_counts} |",
        f"| Body begins on page | {report.content_start_page} "
        f"({report.front_matter_blocks:,} front-matter blocks held back) |",
        f"| Headings by level | {report.heading_level_counts} |",
        f"| Pages with no detected heading | {report.pages_with_no_heading} |",
        f"| Pages with almost no text | {len(report.low_text_pages)} |",
        "",
        "## Dropped-formula scars (measured on raw extraction, not on our blocks)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Raw non-empty lines | {report.raw_text_lines:,} |",
        f"| Orphan-punctuation rate | **{report.math_loss_rate_per_1k_lines}/1k lines** "
        f"(warn above {MATH_LOSS_WARN_PER_1K_LINES}) |",
        f"| Raw signal counts | {report.math_loss_signals} |",
        "",
        "## Structural signals",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| PDF outline entries | {report.outline_entries} |",
        f"| Outline max depth | {report.outline_max_depth} |",
        f"| Pages outside outline coverage | {report.pages_outside_outline_coverage} |",
        f"| Ground-truth blocks tagged | {report.role_counts} |",
        "",
        "## Warnings",
        "",
    ]

    if report.warnings:
        lines.extend(f"- {warning}" for warning in report.warnings)
    else:
        lines.append("None raised by the checks in `ingest/quality.py`.")

    lines.extend(
        [
            "",
            "## What these numbers are not",
            "",
            "Every figure above is a heuristic over PDF text-extraction output. The "
            "orphan-punctuation rate undercounts: a display equation that vanishes without "
            "leaving punctuation behind is invisible to it, and its threshold is calibrated "
            "against three files, not validated. `pages_with_no_heading` counts pages, not "
            "sections, so a long section reads as many headingless pages. Treat all of it as "
            "flags for a human to check, not as measurements to report.",
            "",
        ]
    )
    return "\n".join(lines)
