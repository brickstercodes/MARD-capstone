"""Track A — structural determinism and fidelity (docs/37 §2).

**A2 (determinism) and A3 (fidelity) both need one thing first: which heading level
in a B1 artefact is "the chapters" and which is "the concepts".** No B1 run declares
this — headings are whatever the self-authored root happened to emit — so it is
inferred the same way `eval.groundedness.extract_concepts` already does: the level
with the most headings is the concept level (the model's finest structural unit,
`vanilla.run._count_concepts`'s own reasoning). The level directly above it, if any
heading exists there at all, is the chapter level. Applied uniformly, with no
per-run special-casing, this recovers exactly the shape each run actually has:
seed 11 has headings at level 1 (20, mostly "Chapter N", several repeated — see
below) and level 2 (156, the concept level, no level 3 at all); seed 23 has level 2
(14, "Chapter 1".."Chapter 14") and level 3 (190); seed 42 has level 2 (16,
self-numbered "1."-"16.") and level 3 (75).

**Seed 11's chapter markers repeat.** `# Chapter 2` appears twice, `# Chapter 4`
twice, `# Chapter 6` twice, `# Chapter 7` three times — 19 chapter markers naming
only 13 distinct numbers, not the flat absence of structure a bare "156 headings,
0 subsections" count suggests on its own. Both facts are reported: the concept
level is genuinely flat (no level-3 nesting under any of the 156 concepts), and the
level above it is not a clean 1-per-chapter list either.

**MARD's joined artefact (`tier2_output.md`) carries no markdown heading structure
at all** — checked directly: 0 lines starting with `#` in 8 of 9 runs, 8 lines in one
(`mard_a1f` seed 42, one Tier 2 builder's own prose choice, not a pipeline behaviour).
MARD's structure lives entirely in `artefacts/master_plan.json`'s typed concept
graph, external to and independently checkable from the prose — not inferred from
headings the way every B1 number in this module is.

**Fidelity matching (A3) is content-overlap, not chapter-number matching, except
where a heading says "Chapter N" outright.** `corpus/introcs/chapters.json`'s own
`title` field is just its first section's title (e.g. chapter 4 is titled "4.1
Models of Computation") — thin signal on its own, so each chapter's descriptor here
is its title plus every one of its section titles
(`corpus/introcs/sections.json`), giving `eval.groundtruth_scoring.score_overlap`
enough vocabulary to work with. A heading that literally starts "Chapter N" (seed
11's level-1 markers, seed 23's level-2 list) is matched by that number directly —
unambiguous, and checked against the chapter set rather than assumed valid.
Everything else (seed 42's self-numbered, self-titled modules — its own numbering is
curriculum order, not the book's chapter order, confirmed by reading the 16 titles
against the 14 real chapters by hand before trusting any automated score) is matched
by content overlap with a stated threshold, greedily, highest score first, so no
chapter or heading is claimed twice. The threshold is deliberately visible in the
report rather than baked into a verdict: short titles make this an approximate
instrument, and `docs/38`'s prose says so plainly rather than presenting the
mechanical count as the final word on what seed 42 invented.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from eval.groundtruth_scoring import score_overlap
from eval.runs import CAMPAIGN_SEEDS, select_run

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"

CONTENT_OVERLAP_THRESHOLD = 0.3
"""Recall threshold for matching an invented heading to a real chapter by content.
Deliberately lower than `eval.groundtruth_scoring.DEFAULT_THRESHOLD` (0.6): that
threshold assumes a short reference against a long candidate document, where high
recall is achievable; here both sides are short (a heading, a chapter descriptor
built from a handful of section titles), so recall saturates lower even for a
genuine match. Reported alongside every match so the threshold's effect is visible,
not asserted."""

_EXPLICIT_CHAPTER_PATTERN = re.compile(r"^chapter\s+(\d+)\b", re.IGNORECASE)

MatchMethod = Literal["explicit_number", "content_overlap", "unmatched"]


# ---- heading parsing -----------------------------------------------------------------


@dataclass(frozen=True)
class HeadingTree:
    by_level: dict[int, tuple[str, ...]]

    def count(self, level: int) -> int:
        return len(self.by_level.get(level, ()))


_HEADING_PATTERNS = {
    level: re.compile(rf"^{'#' * level}\s+(\S.*)$", re.MULTILINE) for level in (1, 2, 3)
}


def parse_markdown_headings(text: str) -> HeadingTree:
    return HeadingTree(
        by_level={
            level: tuple(pattern.findall(text)) for level, pattern in _HEADING_PATTERNS.items()
        }
    )


def concept_level(tree: HeadingTree) -> int | None:
    """The heading level with the most entries — the model's finest structural
    unit, same reasoning as `vanilla.run._count_concepts`. `None` if no heading
    exists at any level."""
    populated = {level: tree.count(level) for level in (1, 2, 3) if tree.count(level)}
    if not populated:
        return None
    return max(populated, key=lambda level: populated[level])


def chapter_level(tree: HeadingTree, concept_lvl: int | None) -> int | None:
    """The most-populated level that isn't the concept level — the grouping/
    chapter level, if the run produced one at all.

    Not "the shallowest populated level": seed 42 has a single level-1 heading
    (the document's own title, "# Study Guide...") *and* 16 level-2 module
    headings. Shallowest-populated would pick the lone title as "the chapter
    level"; most-populated correctly picks the 16 modules. A level with exactly
    one heading is never a grouping structure — nothing to group — so it is
    excluded even when it is the only non-concept level with anything in it.
    """
    candidates = {
        level: tree.count(level)
        for level in (1, 2, 3)
        if level != concept_lvl and tree.count(level) > 1
    }
    if not candidates:
        return None
    return max(candidates, key=lambda level: candidates[level])


# ---- Track A2: B1 structure + determinism ---------------------------------------------


@dataclass(frozen=True)
class B1Structure:
    run_id: str
    seed: int
    word_count: int
    heading_counts: dict[int, int]
    concept_level: int | None
    concept_count: int
    concept_headings: tuple[str, ...]
    chapter_level: int | None
    chapter_count: int
    chapter_headings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "seed": self.seed,
            "word_count": self.word_count,
            "heading_counts": {str(k): v for k, v in self.heading_counts.items()},
            "concept_level": self.concept_level,
            "concept_count": self.concept_count,
            "concept_headings": list(self.concept_headings),
            "chapter_level": self.chapter_level,
            "chapter_count": self.chapter_count,
            "chapter_headings": list(self.chapter_headings),
        }


def parse_b1(run_dir: Path) -> B1Structure:
    with (run_dir / "summary.json").open(encoding="utf-8") as handle:
        summary = json.load(handle)
    text = (run_dir / "artefacts" / "vanilla_answer.md").read_text(encoding="utf-8")
    tree = parse_markdown_headings(text)

    c_level = concept_level(tree)
    ch_level = chapter_level(tree, c_level)

    return B1Structure(
        run_id=summary["run_id"],
        seed=summary["seed"],
        word_count=len(text.split()),
        heading_counts={level: tree.count(level) for level in (1, 2, 3)},
        concept_level=c_level,
        concept_count=tree.count(c_level) if c_level is not None else 0,
        concept_headings=tree.by_level.get(c_level, ()) if c_level is not None else (),
        chapter_level=ch_level,
        chapter_count=tree.count(ch_level) if ch_level is not None else 0,
        chapter_headings=tree.by_level.get(ch_level, ()) if ch_level is not None else (),
    )


# ---- Track A2: MARD structure ----------------------------------------------------------


@dataclass(frozen=True)
class MardStructure:
    run_id: str
    system: str
    seed: int
    concepts: int
    """`concept_graph.concepts` node count from `master_plan.json` — **post-merge**,
    the true number of distinct concepts in the compiled plan. Use this one for
    determinism/CV; see `concepts_pre_merge` for why it isn't always 84."""
    concepts_pre_merge: int
    """`summary.json`'s `result.concepts_accepted` — Pass 1's raw accepted count,
    **before** `compile_plan.py` collapses same-id concepts declared in more than
    one chapter (`docs/28` §3). Uniformly 84 across every logged run, including the
    three where a merge happened — it counts *declarations*, not *distinct
    concepts*, so it cannot see the merge. Reported alongside `concepts` so the
    84-vs-83 discrepancy is visible rather than picked silently.
    """
    edges: int
    cross_chapter_edges: int
    prose_word_count: int
    prose_heading_lines: int
    """Lines starting with `#` in `tier2_output.md`. Expected ~0 — MARD's structure
    lives in the plan, not the prose; see module docstring."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system": self.system,
            "seed": self.seed,
            "concepts": self.concepts,
            "concepts_pre_merge": self.concepts_pre_merge,
            "edges": self.edges,
            "cross_chapter_edges": self.cross_chapter_edges,
            "prose_word_count": self.prose_word_count,
            "prose_heading_lines": self.prose_heading_lines,
        }


def parse_mard(run_dir: Path) -> MardStructure:
    with (run_dir / "summary.json").open(encoding="utf-8") as handle:
        summary = json.load(handle)
    result = summary["result"]
    text = (run_dir / "artefacts" / "tier2_output.md").read_text(encoding="utf-8")
    plan: dict[str, Any] = json.loads(
        (run_dir / "artefacts" / "master_plan.json").read_text(encoding="utf-8")
    )

    return MardStructure(
        run_id=summary["run_id"],
        system=summary["system"],
        seed=summary["seed"],
        concepts=len(plan["concept_graph"]["concepts"]),
        concepts_pre_merge=result["concepts_accepted"],
        edges=result["edges_accepted"],
        cross_chapter_edges=result["cross_chapter_edges"],
        prose_word_count=len(text.split()),
        prose_heading_lines=sum(1 for line in text.splitlines() if line.startswith("#")),
    )


# ---- coefficient of variation ----------------------------------------------------------


def coefficient_of_variation(values: list[float]) -> float | None:
    """Population stdev / mean. `None` for a single value (undefined) or a zero mean."""
    if len(values) < 2:
        return None
    mean = sum(values) / len(values)
    if mean == 0:
        return None
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return float(variance**0.5) / mean


# ---- Track A3: fidelity ------------------------------------------------------------------


def load_chapter_descriptors(corpus_dir: Path = CORPUS_INTROCS) -> dict[int, str]:
    """Chapter number -> title + every section title in it. See module docstring
    for why a chapter's own `title` field alone is too thin to match against."""
    chapters: dict[str, Any] = json.loads(
        (corpus_dir / "chapters.json").read_text(encoding="utf-8")
    )
    sections: dict[str, Any] = json.loads(
        (corpus_dir / "sections.json").read_text(encoding="utf-8")
    )
    section_title = {s["section_id"]: s["title"] for s in sections["sections"]}

    descriptors: dict[int, str] = {}
    for chapter in chapters["chapters"]:
        number = chapter.get("number")
        if number is None:
            continue
        titles = [section_title.get(sid, "") for sid in chapter["section_ids"]]
        descriptors[int(number)] = chapter["title"] + " " + " ".join(titles)
    return descriptors


@dataclass(frozen=True)
class HeadingMatch:
    heading: str
    chapter: int | None
    score: float
    method: MatchMethod

    def to_dict(self) -> dict[str, Any]:
        return {
            "heading": self.heading,
            "chapter": self.chapter,
            "score": self.score,
            "method": self.method,
        }


@dataclass(frozen=True)
class FidelityResult:
    matches: list[HeadingMatch]
    invented: list[str]
    """Headings matched to no real chapter."""
    absent_chapters: list[int]
    """Real chapters no heading matched."""
    threshold: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "matches": [m.to_dict() for m in self.matches],
            "invented": self.invented,
            "absent_chapters": self.absent_chapters,
            "threshold": self.threshold,
        }


def match_headings_to_chapters(
    headings: tuple[str, ...],
    descriptors: dict[int, str],
    *,
    threshold: float = CONTENT_OVERLAP_THRESHOLD,
) -> FidelityResult:
    explicit: dict[str, int] = {}
    remaining: list[str] = []
    for heading in headings:
        explicit_match = _EXPLICIT_CHAPTER_PATTERN.match(heading)
        if explicit_match and int(explicit_match.group(1)) in descriptors:
            explicit[heading] = int(explicit_match.group(1))
        else:
            remaining.append(heading)

    # Greedy content-overlap assignment over whatever explicit matching didn't
    # already claim, highest score first, so no chapter or heading is used twice.
    candidates: list[tuple[float, str, int]] = []
    for heading in remaining:
        for chapter, descriptor in descriptors.items():
            if chapter in explicit.values():
                continue
            score = score_overlap(heading, descriptor, threshold=0.0).overlap
            candidates.append((score, heading, chapter))
    candidates.sort(key=lambda item: -item[0])

    claimed_headings = set(explicit)
    claimed_chapters = set(explicit.values())
    fuzzy: dict[str, tuple[int, float]] = {}
    for score, heading, chapter in candidates:
        if score < threshold:
            break
        if heading in claimed_headings or chapter in claimed_chapters:
            continue
        fuzzy[heading] = (chapter, score)
        claimed_headings.add(heading)
        claimed_chapters.add(chapter)

    matches: list[HeadingMatch] = []
    invented: list[str] = []
    for heading in headings:
        if heading in explicit:
            matches.append(HeadingMatch(heading, explicit[heading], 1.0, "explicit_number"))
        elif heading in fuzzy:
            chapter, score = fuzzy[heading]
            matches.append(HeadingMatch(heading, chapter, score, "content_overlap"))
        else:
            matches.append(HeadingMatch(heading, None, 0.0, "unmatched"))
            invented.append(heading)

    absent = [chapter for chapter in sorted(descriptors) if chapter not in claimed_chapters]
    return FidelityResult(matches, invented, absent, threshold)


# ---- Track A4: provenance ----------------------------------------------------------------

_PAGE_CITATION_PATTERN = re.compile(r"(?i)\b(?:page|pp?\.)\s*\d+")
_SECTION_ID_PATTERN = re.compile(r"\bintrocs\.[a-z0-9][a-z0-9._-]*\b")


def count_b1_citations(text: str, valid_section_ids: set[str]) -> int:
    """Resolvable citations in a B1 artefact: a page-number citation (`page 45`,
    `p. 45`, `pp. 45-50`) or a literal `introcs.<section-id>` string that resolves
    against `corpus/introcs/sections.json`. Neither construct exists anywhere in
    any of the three logged B1 runs when actually searched (verified, not assumed
    from `docs/36`'s hand count — see `docs/38` §... for the discrepancy)."""
    page_citations = len(_PAGE_CITATION_PATTERN.findall(text))
    section_citations = sum(
        1 for match in _SECTION_ID_PATTERN.findall(text) if match in valid_section_ids
    )
    return page_citations + section_citations


def load_valid_section_ids(corpus_dir: Path = CORPUS_INTROCS) -> set[str]:
    payload: dict[str, Any] = json.loads((corpus_dir / "sections.json").read_text(encoding="utf-8"))
    return {section["section_id"] for section in payload["sections"]}


# ---- assembly --------------------------------------------------------------------------

MARD_SYSTEMS: tuple[str, ...] = ("mard", "mard_a1", "mard_a1f")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Track A — structural determinism and fidelity (docs/37)."
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    descriptors = load_chapter_descriptors()
    valid_section_ids = load_valid_section_ids()

    b1_structures = [parse_b1(select_run("vanilla_rlm", seed)) for seed in CAMPAIGN_SEEDS]
    mard_structures = {
        system: [parse_mard(select_run(system, seed)) for seed in CAMPAIGN_SEEDS]
        for system in MARD_SYSTEMS
    }
    b1_fidelity = [
        match_headings_to_chapters(s.chapter_headings or s.concept_headings, descriptors)
        for s in b1_structures
    ]
    b1_citations = [
        count_b1_citations(
            (select_run("vanilla_rlm", s.seed) / "artefacts" / "vanilla_answer.md").read_text(
                encoding="utf-8"
            ),
            valid_section_ids,
        )
        for s in b1_structures
    ]

    payload = {
        "b1": [s.to_dict() for s in b1_structures],
        "b1_fidelity": [f.to_dict() for f in b1_fidelity],
        "b1_citations": dict(zip((s.seed for s in b1_structures), b1_citations, strict=True)),
        "mard": {system: [s.to_dict() for s in runs] for system, runs in mard_structures.items()},
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
