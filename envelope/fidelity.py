"""How good is the derived skeleton? Scored against the publisher's bookmark tree.

`docs/16-PRIMARY_DOCUMENT.md` leaves open whether Pass 0 may read `outline.json`.
This module is the cheap way to answer it: rather than making the outline a second
input and adding a condition to a four-day measurement week, treat it as **ground
truth for grading the derived skeleton**. No model calls, no extra matrix cells, and
the paper gets to report skeleton fidelity instead of assuming it.

What the numbers mean, stated so nobody over-reads them:

- **Recall** — the share of outline entries a derived section matches. Low recall
  means Pass 0 is missing structure the document declares.
- **Spurious rate** — derived sections matching no outline entry. Some of these are
  real (a heading the publisher left out of the bookmarks); the metric cannot tell
  the difference, so it is a flag, not a verdict.
- **Boundary error** — mean absolute difference in start page across matched pairs.
  Zero would mean the derived cut points agree with the publisher's exactly.

Titles are matched on a normalised form, not fuzzily. A near-miss threshold would
need tuning, and a tuned threshold on one book is how a metric starts flattering the
thing it measures.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from envelope.skeleton import Skeleton, SkeletonSection

# Section numbers are dropped before matching. The PDF outline writes
# "Chapter 1 Introduction to Computer Science" while the page writes
# "1.1 Computer Science", so the digits are noise for identity purposes.
LEADING_LABEL = re.compile(r"^(chapter|part|unit|section|appendix)?\s*[\d.]*\s*", re.I)
NON_WORD = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class FidelityReport:
    document_id: str
    outline_entries: int
    derived_sections: int
    matched: int
    recall: float
    spurious: int
    spurious_rate: float
    mean_start_page_error: float
    worst_start_page_error: int
    unmatched_outline_titles: tuple[str, ...]
    spurious_derived_titles: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalise(title: str) -> str:
    without_label = LEADING_LABEL.sub("", title.strip())
    return NON_WORD.sub("", without_label.lower())


def score_fidelity(
    skeleton: Skeleton,
    outline_entries: list[dict[str, Any]],
    outline_levels: tuple[int, ...] = (1, 2),
) -> FidelityReport:
    """Compare a derived skeleton against PDF outline entries at the given levels.

    Only levels 1 and 2 by default: those are the chapter and section granularity the
    Master Plan's concepts point at. Including every level would score the skeleton
    against structure it was never asked to find.
    """
    relevant = [entry for entry in outline_entries if entry.get("level") in outline_levels]

    derived_by_key: dict[str, list[SkeletonSection]] = {}
    for section in skeleton.sections:
        derived_by_key.setdefault(_normalise(section.title), []).append(section)

    matched_keys: set[str] = set()
    start_errors: list[int] = []
    unmatched: list[str] = []

    for entry in relevant:
        key = _normalise(entry["title"])
        candidates = derived_by_key.get(key)
        if not candidates:
            unmatched.append(entry["title"])
            continue
        matched_keys.add(key)
        # Nearest start page among same-titled candidates, so a repeated title does
        # not count as a boundary error just because the first copy was picked.
        best = min(candidates, key=lambda s: abs(s.page_start - entry["start_page"]))
        start_errors.append(abs(best.page_start - entry["start_page"]))

    spurious_titles = tuple(
        section.title
        for section in skeleton.sections
        if _normalise(section.title) not in matched_keys
    )

    derived_count = len(skeleton.sections)
    return FidelityReport(
        document_id=skeleton.document_id,
        outline_entries=len(relevant),
        derived_sections=derived_count,
        matched=len(start_errors),
        recall=round(len(start_errors) / len(relevant), 3) if relevant else 0.0,
        spurious=len(spurious_titles),
        spurious_rate=round(len(spurious_titles) / derived_count, 3) if derived_count else 0.0,
        mean_start_page_error=round(sum(start_errors) / len(start_errors), 2)
        if start_errors
        else 0.0,
        worst_start_page_error=max(start_errors) if start_errors else 0,
        unmatched_outline_titles=tuple(unmatched[:20]),
        spurious_derived_titles=spurious_titles[:20],
    )


def render_markdown(report: FidelityReport) -> str:
    lines = [
        f"# Pass 0 skeleton fidelity — {report.document_id}",
        "",
        "Derived skeleton (from the document's own headings) scored against the PDF "
        "bookmark outline at levels 1-2. No model calls involved.",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Outline entries (levels 1-2) | {report.outline_entries} |",
        f"| Derived sections | {report.derived_sections} |",
        f"| Matched | {report.matched} |",
        f"| **Recall** | **{report.recall:.1%}** |",
        f"| Spurious derived sections | {report.spurious} ({report.spurious_rate:.1%}) |",
        f"| Mean start-page error | {report.mean_start_page_error} pages |",
        f"| Worst start-page error | {report.worst_start_page_error} pages |",
        "",
    ]
    if report.unmatched_outline_titles:
        lines += ["## Outline entries with no derived match", ""]
        lines += [f"- {title}" for title in report.unmatched_outline_titles]
        lines.append("")
    if report.spurious_derived_titles:
        lines += [
            "## Derived sections matching no outline entry",
            "",
            "Some of these are real headings the publisher omitted from the bookmarks. "
            "This metric cannot tell those from false positives.",
            "",
        ]
        lines += [f"- {title}" for title in report.spurious_derived_titles]
        lines.append("")
    return "\n".join(lines)
