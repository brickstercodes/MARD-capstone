"""Task B — forward-reference violations, book order vs Master Plan order.

`docs/34` §3, implementing `docs/30-MEASUREMENT_PROTOCOL.md` §3's O5 metric. The
"before" half already existed: `ingest.groundtruth.extract_cross_references` finds
every in-text `Chapter N` mention and classifies it `forward` (the citing page comes
before chapter N's own page range — the book cites something not yet reached, a book-
order violation), `backward` (citing page is after — fine, already covered), or
`same_chapter`. `summarize_violations`'s `forward` count is the O5 "before" number,
unchanged here (`docs/23` §7's blocked note: this half predates any Master Plan).

**The "after" half, new here.** For the same set of references, ask the identical
question against Master Plan order instead of page order: does the plan place the
citing chapter's concepts before the referenced (prerequisite) chapter's concepts?

**Chapter granularity, on both sides of the comparison, and that is a real, named
simplification, not free.** A cross-reference is extracted at chapter granularity (it
names "Chapter N", not a specific concept), and `docs/30` §3 itself operationalizes
book order the same way — comparing one page position against a chapter's whole
`[page_start, page_end]` span. The Master Plan side mirrors that exactly: each
chapter's "position" in the plan is `min(plan position of every concept whose source
page falls in that chapter)` — the plan-order analogue of a chapter's `page_start`. A
concept-level version of this metric is not implementable from what a cross-reference
records; this is the finest grain the ground truth itself supports.

**Retracted: chapters 10 and 13 are not, in fact, missing from the study sequence.**
An earlier version of this module attributed a concept to a chapter via
`chapter_for_page` — page-range membership against `concept_graph.concepts[i].source
.page_start` — and found chapters 10 and 13 absent in 8 of 9 runs, 20 of 50 references
`unmappable` as a result. That was `chapter_for_page`'s own bug, not a Pass 1
extraction gap: nearly every chapter boundary in `chapters.json` overlaps its
neighbour by exactly one page (chapter N's `page_end` equals chapter N+1's
`page_start`), and `chapter_for_page` returns the *first* range match, which for a
boundary page is always the earlier chapter — checked directly against one run's
concepts, this misattributed 66 of 84 (79%). Fixed by attributing through
`chapter_for_section` against the concept's own `source.section_id`
(`section_to_chapter_map`, built from `chapters.json`'s `section_ids` lists) instead
— exact, no page arithmetic, no boundary ambiguity. **Every one of the 9 MARD-family
runs now covers all 14 chapters; nothing is `unmappable`.** `unmappable` is kept as a
reported category regardless (a run that genuinely omitted a chapter would still be
named, not silently folded into an average), it is simply empty for every run
actually logged so far.

**The concept-alias/merge question `docs/34` §3 asks about, resolved.** Three
concepts, across all nine runs — `mard` seed 23's `microservices-and-service-
decomposition` (`docs/28` §3), `mard_a1` seed 11's `abstraction-and-modeling`, and
`mard_a1f` seed 11's `microservices-architecture` (the latter two found by reading
each run's own `mard_compile_plan` event directly, not covered by `docs/28`'s prose,
which only discusses the first) — were merged from two chapters. The primary mapping
here uses only the *kept* chapter (`concept_graph.concepts[i].source`, which every
concept has) — the simplest rule and the only one that needs no extra per-run event
parsing. A secondary mapping additionally attributes a merged concept's plan position
to every chapter in its `concepts_merged[].occurrences` (from the `mard_compile_plan`
event), and both are reported for the three runs this affects, per `docs/34` §3's "report
the count both ways if the choice moves the number."
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from eval.runs import CAMPAIGN_SEEDS, select_run
from ingest.groundtruth import CrossReference, extract_cross_references

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"

Classification = Literal["forward", "backward", "same_chapter", "unmappable"]


def load_chapters(corpus_dir: Path = CORPUS_INTROCS) -> list[dict[str, Any]]:
    payload: dict[str, Any] = json.loads((corpus_dir / "chapters.json").read_text(encoding="utf-8"))
    chapters: list[dict[str, Any]] = payload["chapters"]
    return chapters


def load_document_text(corpus_dir: Path = CORPUS_INTROCS) -> str:
    return (corpus_dir / "document.txt").read_text(encoding="utf-8")


def chapter_for_page(chapters: list[dict[str, Any]], page: int) -> int | None:
    """Page -> chapter, by range membership. **Only for pages with no section id to
    look up directly** (book-order cross-references, extracted from raw
    `[[page:N]]`-marked text with no section attached) — every chapter boundary in
    `chapters.json` overlaps its neighbour by exactly one page (chapter N's
    `page_end` equals chapter N+1's `page_start`, since a chapter can begin partway
    down the page the previous one ends on), so this function's first-match
    resolution is a real, systematic bias toward the *earlier* chapter on every
    boundary page, not a rare edge case. `chapter_for_section` is exact and has no
    such bias; use it whenever a section id is available, which for every MARD
    concept it always is."""
    for chapter in chapters:
        number = chapter.get("number")
        if number is not None and chapter["page_start"] <= page <= chapter["page_end"]:
            return int(number)
    return None


def section_to_chapter_map(chapters: list[dict[str, Any]]) -> dict[str, int]:
    """`section_id -> chapter number`, built from `chapters.json`'s own
    `section_ids` lists — exact, no page-boundary ambiguity. This is the mapping
    every MARD concept should be attributed through, since `concept_graph.concepts
    [i].source.section_id` is always present and always correct
    (`docs/35` §3.2: 0 of 677 mis-cited)."""
    mapping: dict[str, int] = {}
    for chapter in chapters:
        number = chapter.get("number")
        if number is None:
            continue
        for section_id in chapter["section_ids"]:
            mapping[section_id] = int(number)
    return mapping


def chapter_for_section(section_to_chapter: dict[str, int], section_id: str) -> int | None:
    return section_to_chapter.get(section_id)


def book_order_references(
    chapters: list[dict[str, Any]] | None = None,
    document_text: str | None = None,
) -> list[CrossReference]:
    """The O5 "before" half — unchanged from `ingest.groundtruth`, loaded once so
    every run scores against the identical reference set."""
    chapters = chapters if chapters is not None else load_chapters()
    document_text = document_text if document_text is not None else load_document_text()
    return extract_cross_references(document_text, chapters)


def _load_master_plan(run_dir: Path) -> dict[str, Any]:
    plan: dict[str, Any] = json.loads(
        (run_dir / "artefacts" / "master_plan.json").read_text(encoding="utf-8")
    )
    return plan


def _load_merge_occurrences(run_dir: Path) -> dict[str, list[str]]:
    """concept_id -> every chapter_id it occurred in, from the `mard_compile_plan`
    event's `concepts_merged`. Empty for a run with no merges (all nine runs but one)."""
    events_path = run_dir / "events.jsonl"
    if not events_path.exists():
        return {}
    occurrences: dict[str, list[str]] = {}
    with events_path.open(encoding="utf-8") as handle:
        for line in handle:
            event = json.loads(line)
            if event.get("kind") != "mard_compile_plan":
                continue
            for merged in event.get("concepts_merged", []):
                occurrences[merged["concept_id"]] = [
                    occ["chapter_id"] for occ in merged["occurrences"]
                ]
    return occurrences


def _chapter_number_from_id(chapters: list[dict[str, Any]], chapter_id: str) -> int | None:
    for chapter in chapters:
        if chapter["chapter_id"] == chapter_id and chapter.get("number") is not None:
            return int(chapter["number"])
    return None


def chapter_plan_positions(
    run_dir: Path,
    chapters: list[dict[str, Any]],
    *,
    include_aliases: bool,
) -> dict[int, list[int]]:
    """chapter number -> every plan position of a concept attributed to it.

    Attributed by `concept_graph.concepts[i].source.section_id` through
    `section_to_chapter_map` — exact, not by page range
    (`chapter_for_page`'s docstring explains why page range is the wrong tool
    here: it was used in an earlier version of this function and silently
    misattributed 66 of 84 concepts in one spot-checked run, because almost every
    chapter boundary page is shared with its neighbour).

    `include_aliases=False` (primary): each concept counts only for its kept
    chapter. `include_aliases=True` (secondary): a merged concept additionally
    counts for every chapter its pre-merge occurrences came from (see module
    docstring).
    """
    plan = _load_master_plan(run_dir)
    concepts = {c["id"]: c for c in plan["concept_graph"]["concepts"]}
    merge_occurrences = _load_merge_occurrences(run_dir) if include_aliases else {}
    section_to_chapter = section_to_chapter_map(chapters)

    positions: dict[int, list[int]] = {}
    for entry in plan["study_sequence"]:
        concept = concepts[entry["concept_id"]]
        position = entry["position"]

        kept_chapter = chapter_for_section(section_to_chapter, concept["source"]["section_id"])
        if kept_chapter is not None:
            positions.setdefault(kept_chapter, []).append(position)

        for chapter_id in merge_occurrences.get(entry["concept_id"], []):
            alias_chapter = _chapter_number_from_id(chapters, chapter_id)
            if alias_chapter is not None and alias_chapter != kept_chapter:
                positions.setdefault(alias_chapter, []).append(position)

    return positions


@dataclass(frozen=True)
class OrderingResult:
    total: int
    forward: int
    """Violations: the citing chapter's material is scheduled before its declared
    prerequisite's."""
    backward: int
    same_chapter: int
    unmappable: int
    """Excluded from forward/backward: the citing or referenced chapter has no
    concept in this run's plan at all (see module docstring)."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "forward": self.forward,
            "backward": self.backward,
            "same_chapter": self.same_chapter,
            "unmappable": self.unmappable,
        }


@dataclass(frozen=True)
class ReferenceClassification:
    reference: CrossReference
    plan_classification: Classification


def classify_in_plan_order(
    references: list[CrossReference],
    chapters: list[dict[str, Any]],
    positions_by_chapter: dict[int, list[int]],
) -> list[ReferenceClassification]:
    """Per-reference plan-order classification — kept per-reference, not just
    tallied, so a caller can recover exactly which references were `unmappable`
    and restrict a book-order comparison to the same subset (`_summarize` for the
    aggregate; `score_run` for the matched-subset book-order comparison)."""
    results: list[ReferenceClassification] = []
    for reference in references:
        if reference.classification == "unresolved":
            continue  # no target chapter at all — out of scope in book order too
        citing_chapter = chapter_for_page(chapters, reference.citing_page)
        referenced_chapter = reference.referenced_chapter

        if citing_chapter == referenced_chapter:
            results.append(ReferenceClassification(reference, "same_chapter"))
            continue

        citing_positions = positions_by_chapter.get(citing_chapter) if citing_chapter else None
        referenced_positions = positions_by_chapter.get(referenced_chapter)
        if not citing_positions or not referenced_positions:
            results.append(ReferenceClassification(reference, "unmappable"))
            continue

        if min(citing_positions) < min(referenced_positions):
            results.append(ReferenceClassification(reference, "forward"))
        else:
            results.append(ReferenceClassification(reference, "backward"))
    return results


def _summarize(classifications: list[ReferenceClassification]) -> OrderingResult:
    forward = sum(1 for c in classifications if c.plan_classification == "forward")
    backward = sum(1 for c in classifications if c.plan_classification == "backward")
    same_chapter = sum(1 for c in classifications if c.plan_classification == "same_chapter")
    unmappable = sum(1 for c in classifications if c.plan_classification == "unmappable")
    return OrderingResult(len(classifications), forward, backward, same_chapter, unmappable)


@dataclass(frozen=True)
class RunOrderingScore:
    run_id: str
    system: str
    seed: int
    book_order: OrderingResult
    """All 50 extracted references, classified by page order — invariant across
    every run (a property of the document, not the plan)."""
    book_order_on_mappable_subset: OrderingResult
    """The same book-order classification, restricted to exactly the references
    `plan_order_kept_chapter_only` could also classify — the fair "before" number
    to compare `plan_order_kept_chapter_only` against, since comparing it to
    `book_order`'s full 50 would be comparing different denominators."""
    plan_order_kept_chapter_only: OrderingResult
    plan_order_with_aliases: OrderingResult | None
    """`None` unless this run has >=1 merged concept — see module docstring."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system": self.system,
            "seed": self.seed,
            "book_order": self.book_order.to_dict(),
            "book_order_on_mappable_subset": self.book_order_on_mappable_subset.to_dict(),
            "plan_order_kept_chapter_only": self.plan_order_kept_chapter_only.to_dict(),
            "plan_order_with_aliases": (
                self.plan_order_with_aliases.to_dict()
                if self.plan_order_with_aliases is not None
                else None
            ),
        }


def score_run(
    run_dir: Path,
    references: list[CrossReference],
    chapters: list[dict[str, Any]],
) -> RunOrderingScore:
    with (run_dir / "summary.json").open(encoding="utf-8") as handle:
        summary = json.load(handle)

    # Book order is page order, already classified by extract_cross_references
    # itself — no "positions" concept to feed through classify_in_plan_order, so
    # it is tallied directly against those existing classifications instead.
    book = _book_order_result(references)

    merge_occurrences = _load_merge_occurrences(run_dir)
    kept_only = chapter_plan_positions(run_dir, chapters, include_aliases=False)
    kept_only_classifications = classify_in_plan_order(references, chapters, kept_only)
    plan_kept_only = _summarize(kept_only_classifications)

    mappable_references = [
        c.reference for c in kept_only_classifications if c.plan_classification != "unmappable"
    ]
    book_on_mappable = _book_order_result(mappable_references)

    plan_with_aliases = None
    if merge_occurrences:
        with_aliases = chapter_plan_positions(run_dir, chapters, include_aliases=True)
        plan_with_aliases = _summarize(classify_in_plan_order(references, chapters, with_aliases))

    return RunOrderingScore(
        run_id=summary["run_id"],
        system=summary["system"],
        seed=summary["seed"],
        book_order=book,
        book_order_on_mappable_subset=book_on_mappable,
        plan_order_kept_chapter_only=plan_kept_only,
        plan_order_with_aliases=plan_with_aliases,
    )


def _book_order_result(references: list[CrossReference]) -> OrderingResult:
    forward = sum(1 for r in references if r.classification == "forward")
    backward = sum(1 for r in references if r.classification == "backward")
    same_chapter = sum(1 for r in references if r.classification == "same_chapter")
    unresolved = sum(1 for r in references if r.classification == "unresolved")
    total = len(references)
    # "unresolved" (no chapter numbered N exists) is folded into "unmappable" here for
    # a uniform report shape — book order and plan order then both report the same
    # four buckets, with "unmappable" meaning "could not be classified at all" in
    # each order's own sense.
    return OrderingResult(total, forward, backward, same_chapter, unresolved)


SYSTEMS: tuple[str, ...] = ("mard", "mard_a1", "mard_a1f")


def score_all(
    systems: tuple[str, ...] = SYSTEMS, *, seeds: tuple[int, ...] = CAMPAIGN_SEEDS
) -> list[RunOrderingScore]:
    chapters = load_chapters()
    references = book_order_references(chapters)
    results = []
    for system in systems:
        for seed in seeds:
            run_dir = select_run(system, seed)
            results.append(score_run(run_dir, references, chapters))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Task B — forward-reference violations, book vs plan order (docs/34 §3)."
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    results = score_all()
    payload = [result.to_dict() for result in results]
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
