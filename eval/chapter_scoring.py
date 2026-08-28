"""Track B — per-chapter learning-objective coverage (docs/37 §3).

`docs/35` §1.3 already named the problem: whole-document recall saturates at
94-97% for every system, because a short objective's few content words turn up
somewhere in any sufficiently long, same-subject candidate almost regardless of
whether that candidate is organised around the textbook's own chapters. This module
fixes the granularity: each of the 14 numbered chapters' learning objectives are
scored only against the part of a run's output attributed to that chapter, never
against the whole document.

**The attribution step is exact for MARD and approximate-to-impossible for B1, and
that asymmetry is the finding, not a gap in method.** MARD: every concept carries
`source.section_id`/page range verified against the corpus (`docs/35` §3.2, 0 of 677
mis-cited), so a Tier 2 response's chapter is never in question — resolved through
`eval.ordering.chapter_for_section` against its own cited `section_id`, **not**
`chapter_for_page` against its cited page range (an earlier version of this module
used the latter and silently misattributed the majority of concepts near a chapter
boundary — `eval.ordering.chapter_for_page`'s docstring has the full account). B1:
chapter attribution is inferred from `eval.structure`'s heading-tree analysis, which
is only as good as the heading structure a given run happened to emit —

- Seed 23: 14 headings, literally `"Chapter 1"`..`"Chapter 14"`, unambiguous.
- Seed 11: 20 headings at the level above the flat 156-concept list, mostly
  `"Chapter N"` (several repeated — `docs/38`/`eval.structure`), all 14 chapters
  covered. **This revises `docs/37`'s own assumption** that seed 11 "cannot be
  [chapter-]scored at all" — it can, once the level-1 headings `eval.structure`
  found are used rather than assumed absent.
- Seed 42: only the headings `eval.structure.match_headings_to_chapters` could
  confidently attribute (content-overlap, threshold 0.3) are used; several of its
  16 self-numbered modules match no real chapter at that threshold, and several
  real chapters have no module matching them. Those chapters are `unmappable` for
  seed 42, not silently scored against the whole document instead — a fallback
  whole-document score is computed too, kept in its own column, and never averaged
  into the per-chapter numbers.

Same `eval.groundtruth_scoring.score_overlap`, same three thresholds (0.5 / 0.6 /
0.7) as `eval.task_score`; `coverage_at_threshold` is reused directly rather than
re-implemented.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eval.groundedness_mard import parse_tier2_call
from eval.ordering import chapter_for_section, load_chapters, section_to_chapter_map
from eval.runs import CAMPAIGN_SEEDS, select_run
from eval.structure import (
    B1Structure,
    HeadingMatch,
    load_chapter_descriptors,
    match_headings_to_chapters,
    parse_b1,
)
from eval.task_score import (
    ANSWER_FILENAME,
    THRESHOLDS,
    coverage_at_threshold,
    load_objectives,
    score_objectives,
)
from ingest.groundtruth import LearningObjective
from runlog.run import load_run

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"

# Not imported from `eval.structure._HEADING_PATTERNS` (private): a heading-level
# regex is a two-line thing to own directly rather than reach across a module
# boundary for it.
_HEADING_PATTERN_AT_LEVEL = {
    level: re.compile(rf"^{'#' * level}\s+(\S.*)$", re.MULTILINE) for level in (1, 2, 3)
}

REAL_CHAPTERS: tuple[int, ...] = tuple(range(1, 15))


def objectives_by_chapter(
    objectives: list[LearningObjective],
) -> dict[int, list[LearningObjective]]:
    by_chapter: dict[int, list[LearningObjective]] = defaultdict(list)
    for objective in objectives:
        if objective.chapter_number is not None:
            by_chapter[objective.chapter_number].append(objective)
    return by_chapter


# ---- B1 chapter-text attribution --------------------------------------------------------


def _heading_spans(text: str, level: int) -> list[tuple[str, int, int]]:
    """`[(heading text, start of its line, start of the next same-level heading or
    end of document), ...]`, in document order. Two occurrences of the identical
    heading text (seed 11's repeated `"Chapter N"` markers) get two separate spans
    here — both later attributed to the same chapter, so no content is lost."""
    matches = list(_HEADING_PATTERN_AT_LEVEL[level].finditer(text))
    spans = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        spans.append((match.group(1), match.start(), end))
    return spans


def b1_chapter_texts(
    run_dir: Path, structure: B1Structure, matches: list[HeadingMatch]
) -> dict[int, str]:
    """chapter number -> concatenated text attributed to it. Empty dict if this
    run has no chapter-level heading structure at all (none of the three logged
    B1 runs hit this case, but nothing here assumes it can't happen)."""
    if structure.chapter_level is None:
        return {}
    text = (run_dir / "artefacts" / "vanilla_answer.md").read_text(encoding="utf-8")
    spans = _heading_spans(text, structure.chapter_level)
    heading_to_chapter = {
        match.heading: match.chapter for match in matches if match.chapter is not None
    }

    by_chapter: dict[int, list[str]] = defaultdict(list)
    for heading, start, end in spans:
        chapter = heading_to_chapter.get(heading)
        if chapter is not None:
            by_chapter[chapter].append(text[start:end])
    return {chapter: "\n".join(parts) for chapter, parts in by_chapter.items()}


# ---- MARD chapter-text attribution -------------------------------------------------------


def mard_chapter_texts(run_dir: Path, chapters: list[dict[str, Any]]) -> dict[int, str]:
    """chapter number -> concatenated Tier 2 response text for every concept whose
    verified citation (`docs/35` §3.2) places it in that chapter.

    Attributed by `parsed.section_id` through `section_to_chapter_map`, not by
    `parsed.page_start` through `chapter_for_page` — see
    `eval.ordering.chapter_for_page`'s docstring: nearly every chapter boundary
    page is shared with its neighbour, so page-range lookup systematically
    misattributes concepts near a boundary to the earlier chapter. Section-id
    lookup has no such ambiguity. Never approximate either way: a call whose
    prompt doesn't match the known Tier 2 template contributes nothing, same as
    `eval.groundedness_mard`.
    """
    run = load_run(run_dir)
    calls = run["calls"]
    section_to_chapter = section_to_chapter_map(chapters)

    by_chapter: dict[int, list[str]] = defaultdict(list)
    for call in calls:
        if call.get("role") != "tier2":
            continue
        parsed = parse_tier2_call(call)
        if parsed is None or not parsed.matched_known_template:
            continue
        chapter = chapter_for_section(section_to_chapter, parsed.section_id)
        if chapter is not None:
            by_chapter[chapter].append(str(call["response"]))
    return {chapter: "\n".join(parts) for chapter, parts in by_chapter.items()}


# ---- scoring --------------------------------------------------------------------------


@dataclass(frozen=True)
class ChapterCoverage:
    chapter: int
    objective_count: int
    mappable: bool
    coverage_by_threshold: dict[float, dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "objective_count": self.objective_count,
            "mappable": self.mappable,
            "coverage_by_threshold": {str(t): v for t, v in self.coverage_by_threshold.items()},
        }


@dataclass(frozen=True)
class RunChapterScore:
    run_id: str
    system: str
    seed: int
    chapters: list[ChapterCoverage]
    whole_document_fallback: dict[float, dict[str, Any]]
    """Coverage of ALL 243 objectives against the whole document, for comparison
    only — `docs/37` §3: "never mix the two in one mean." Identical in definition
    to `eval.task_score`'s own number; kept here too so a reader of this report
    doesn't have to cross-reference `docs/35` to see both side by side."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system": self.system,
            "seed": self.seed,
            "chapters": [c.to_dict() for c in self.chapters],
            "whole_document_fallback": {str(t): v for t, v in self.whole_document_fallback.items()},
        }


def _score_chapters(
    by_chapter_objectives: dict[int, list[LearningObjective]],
    by_chapter_text: dict[int, str],
    thresholds: tuple[float, ...],
) -> list[ChapterCoverage]:
    results = []
    for chapter in REAL_CHAPTERS:
        objectives = by_chapter_objectives.get(chapter, [])
        text = by_chapter_text.get(chapter)
        mappable = text is not None
        if text is not None:
            scores = score_objectives(objectives, text)
            coverage = {t: coverage_at_threshold(scores, t) for t in thresholds}
        else:
            coverage = {
                t: {"threshold": t, "covered": 0, "total": len(objectives), "fraction": None}
                for t in thresholds
            }
        results.append(ChapterCoverage(chapter, len(objectives), mappable, coverage))
    return results


def score_run_b1(
    run_dir: Path,
    objectives: list[LearningObjective],
    by_chapter_objectives: dict[int, list[LearningObjective]],
    descriptors: dict[int, str],
    thresholds: tuple[float, ...] = THRESHOLDS,
) -> RunChapterScore:
    with (run_dir / "summary.json").open(encoding="utf-8") as handle:
        summary = json.load(handle)
    structure = parse_b1(run_dir)
    fidelity = match_headings_to_chapters(
        structure.chapter_headings or structure.concept_headings, descriptors
    )
    by_chapter_text = b1_chapter_texts(run_dir, structure, fidelity.matches)
    chapters = _score_chapters(by_chapter_objectives, by_chapter_text, thresholds)

    whole_text = (run_dir / "artefacts" / ANSWER_FILENAME["vanilla_rlm"]).read_text(
        encoding="utf-8"
    )
    whole_scores = score_objectives(objectives, whole_text)
    whole_document_fallback = {t: coverage_at_threshold(whole_scores, t) for t in thresholds}

    return RunChapterScore(
        run_id=summary["run_id"],
        system=summary["system"],
        seed=summary["seed"],
        chapters=chapters,
        whole_document_fallback=whole_document_fallback,
    )


def score_run_mard(
    run_dir: Path,
    system: str,
    objectives: list[LearningObjective],
    by_chapter_objectives: dict[int, list[LearningObjective]],
    chapters_ref: list[dict[str, Any]],
    thresholds: tuple[float, ...] = THRESHOLDS,
) -> RunChapterScore:
    with (run_dir / "summary.json").open(encoding="utf-8") as handle:
        summary = json.load(handle)
    by_chapter_text = mard_chapter_texts(run_dir, chapters_ref)
    chapters = _score_chapters(by_chapter_objectives, by_chapter_text, thresholds)

    whole_text = (run_dir / "artefacts" / ANSWER_FILENAME[system]).read_text(encoding="utf-8")
    whole_scores = score_objectives(objectives, whole_text)
    whole_document_fallback = {t: coverage_at_threshold(whole_scores, t) for t in thresholds}

    return RunChapterScore(
        run_id=summary["run_id"],
        system=summary["system"],
        seed=summary["seed"],
        chapters=chapters,
        whole_document_fallback=whole_document_fallback,
    )


SYSTEMS: tuple[str, ...] = ("vanilla_rlm", "mard", "mard_a1", "mard_a1f")


def score_all(
    systems: tuple[str, ...] = SYSTEMS, *, seeds: tuple[int, ...] = CAMPAIGN_SEEDS
) -> list[RunChapterScore]:
    objectives = load_objectives()
    by_chapter_objectives = objectives_by_chapter(objectives)
    descriptors = load_chapter_descriptors()
    chapters_ref = load_chapters()

    results = []
    for system in systems:
        for seed in seeds:
            run_dir = select_run(system, seed)
            if system == "vanilla_rlm":
                results.append(
                    score_run_b1(run_dir, objectives, by_chapter_objectives, descriptors)
                )
            else:
                results.append(
                    score_run_mard(run_dir, system, objectives, by_chapter_objectives, chapters_ref)
                )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Track B — per-chapter learning-objective coverage (docs/37 §3)."
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    payload = [r.to_dict() for r in score_all()]
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
