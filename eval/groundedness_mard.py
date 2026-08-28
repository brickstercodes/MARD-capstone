"""Task C — groundedness over the MARD arm (docs/34 §4).

`docs/24` §5 predicted MARD's groundedness rate would be "near 1.0, because
`orchestrate.briefs_for` constructs each brief from the plan's recorded source span
rather than matching text at generation time" — explicitly a prediction, not a
result, with the instruction to report whatever the measurement actually shows.

**The measurement shows the prediction was right about attribution and wrong about
text-grounding, and the two are not the same claim.** Reading the frozen prompt-
construction code directly — `orchestrate.lm_builder.prompt_for` (Tier 2),
`envelope.pass1.build_prompt` (Tier 1) — and confirming it against every real call in
`calls.jsonl` (which, unlike `vanilla/run.py`'s 500-character `prompt_preview`, stores
the complete, untruncated prompt): **no MARD prompt at any tier, in any of the nine
logged runs, embeds the underlying document's prose.** Tier 2 gets a concept label, a
*citation* (`Source: section {id}, pages {start}-{end}`), a plan position, and Tier
1's synthesised directive — never the section's actual text. Tier 1 gets section ids
and titles, never chapter text. Token counts corroborate this independent of the code
reading: MARD Tier 2 prompts run 98-143 input tokens (a citation and a two-sentence
directive), where an embedded multi-page excerpt would run into the thousands, as
vanilla's `SOURCE:`-bearing prompts actually do.

**So under vanilla's literal criterion — does the generating call's prompt carry
non-empty source *text* — every MARD Tier 2 call is `ungrounded`, always, by
architecture.** This is reported as `text_grounded` below, to keep it distinct from
the second, independent thing MARD's construction *does* guarantee and vanilla's
does not: **`attribution_correct`** — the cited `section_id`/page range is exactly
the source span `plan.models.SourceSpan` recorded for that concept, verified here
against `corpus/introcs/sections.json` directly rather than trusted from the plan's
own self-report. Vanilla's seed-42 failure (`docs/24` §1) was a *mismapped* citation
mixed with missing text; MARD separates those into "never has the text" (uniform,
architectural) and "the citation is real" (also uniform, verified) — two claims
`docs/23`'s original prediction collapsed into one "near 1.0" number.

**No `root_authored` case, and no s42 anomaly.** `eval.groundedness`'s `root_authored`
status exists because vanilla's self-authored code sometimes has no per-concept call
to inspect at all. MARD's Tier 2 fork always issues exactly one call per plan
concept — 84 (or 83, when a merge lands) per run, matching `study_sequence` exactly,
confirmed against every one of the nine runs — so every concept resolves. And MARD's
per-run cost/wall-clock/call-shape is close to identical across all three seeds
(`docs/28` §4's own table: $0.568-0.590, 437-448s) precisely because MARD's pipeline
(Pass 0 -> Pass 1 -> compile -> Tier 2 fork/join) is fixed by construction, not
self-authored the way vanilla's root loop is — there is no room left for one seed to
invent a different architecture the way vanilla's seed 42 did (`docs/32` §4). That
absence is itself the answer to "does the s42 anomaly reappear": it cannot, because
the mechanism that produced it (a root writing its own exploration code, differently
each run) does not exist on this arm.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from eval.runs import CAMPAIGN_SEEDS, select_run
from runlog.run import load_run

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"

ConceptStatus = Literal["grounded", "ungrounded", "unresolved"]

# Mirrors orchestrate.lm_builder.prompt_for exactly. A prompt that does NOT match
# this in full has deviated from the known, frozen template — flagged as
# `template_deviation` rather than assumed grounded or not, since the whole point
# of this module is not to assume.
_TIER2_PROMPT_PATTERN = re.compile(
    r"^You are writing one section of a study guide for '(?P<document_id>[^']+)'\.\n"
    r"Concept: (?P<concept_label>.+)\n"
    r"Source: section (?P<section_id>\S+), pages (?P<page_start>\d+)-(?P<page_end>\d+)\n"
    r"Position in the study sequence: (?P<position>\d+)\n\n"
    r"(?P<directive>.+?)\n\n"
    r"Write only this section\. Do not summarise what comes before or after it\.$",
    re.DOTALL,
)


def _message_content(raw_prompt: str) -> str:
    """`calls.jsonl`'s `prompt` field is a JSON-encoded `[{"role": ..., "content": ...}]`
    string, not a plain string — unlike vanilla's truncated preview, this is the
    complete prompt actually sent."""
    messages: list[dict[str, Any]] = json.loads(raw_prompt)
    return str(messages[0]["content"])


@dataclass(frozen=True)
class TierTwoCallParse:
    concept_label: str
    section_id: str
    page_start: int
    page_end: int
    position: int
    directive: str
    matched_known_template: bool
    """False means the prompt deviated from `orchestrate.lm_builder.prompt_for`'s
    known shape — everything else on this object is best-effort in that case."""


def parse_tier2_call(call: dict[str, Any]) -> TierTwoCallParse | None:
    """Parse one Tier 2 call's prompt against the known template. `None` if the
    prompt doesn't even contain a `Concept:` line — not a Tier 2 concept-writing
    call at all."""
    content = _message_content(call["prompt"])
    match = _TIER2_PROMPT_PATTERN.match(content)
    if match:
        return TierTwoCallParse(
            concept_label=match.group("concept_label"),
            section_id=match.group("section_id"),
            page_start=int(match.group("page_start")),
            page_end=int(match.group("page_end")),
            position=int(match.group("position")),
            directive=match.group("directive"),
            matched_known_template=True,
        )
    label_match = re.search(r"^Concept: (.+)$", content, re.MULTILINE)
    if label_match is None:
        return None
    return TierTwoCallParse(
        concept_label=label_match.group(1),
        section_id="",
        page_start=-1,
        page_end=-1,
        position=-1,
        directive="",
        matched_known_template=False,
    )


def text_grounded(parsed: TierTwoCallParse) -> bool:
    """Does this call's prompt carry the document's own prose, not just a citation?

    Defined structurally, not by a token-count heuristic (unlike
    `eval.groundedness._classify_call`, which needs one because vanilla's prompts
    are self-authored and untruncated data isn't available): MARD's Tier 2 prompt
    template is fixed and known, so a full match against it (`matched_known_template`)
    *is* the proof nothing beyond a citation and a short directive is present — a
    matched call is never `text_grounded`. Only called by `score_run` when
    `matched_known_template` is `True`; a prompt that deviates from the known
    template is counted separately as `template_deviations` and never reaches
    here, precisely because deviation means this function can no longer prove
    anything either way.
    """
    assert parsed.matched_known_template
    return False


def attribution_correct(
    parsed: TierTwoCallParse, sections_by_id: dict[str, dict[str, Any]]
) -> bool | None:
    """Does the cited `section_id`/page range match `corpus/introcs/sections.json`'s
    own record for that section — checked against the corpus, not trusted from the
    plan's self-report. `None` when the call didn't match the known template at all
    (nothing to check)."""
    if not parsed.matched_known_template:
        return None
    section = sections_by_id.get(parsed.section_id)
    if section is None:
        return False
    return bool(
        section["page_start"] == parsed.page_start and section["page_end"] == parsed.page_end
    )


def load_sections_by_id(corpus_dir: Path = CORPUS_INTROCS) -> dict[str, dict[str, Any]]:
    payload: dict[str, Any] = json.loads((corpus_dir / "sections.json").read_text(encoding="utf-8"))
    return {section["section_id"]: section for section in payload["sections"]}


@dataclass(frozen=True)
class ConceptResult:
    concept_label: str
    status: ConceptStatus
    attribution_correct: bool | None
    regenerated: bool
    attempt_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "concept_label": self.concept_label,
            "status": self.status,
            "attribution_correct": self.attribution_correct,
            "regenerated": self.regenerated,
            "attempt_count": self.attempt_count,
        }


@dataclass(frozen=True)
class GroundednessReportMard:
    run_id: str
    system: str
    seed: int
    total_concepts: int
    grounded: int
    ungrounded: int
    template_deviations: int
    """Calls whose prompt did not match the known Tier 2 template — reported, not
    silently classified either way. Zero across all nine logged runs."""
    attribution_correct: int
    attribution_incorrect: int
    regenerated: int
    tier1_text_grounded: bool
    """Whether ANY Tier 1 (pass0/pass1) call in this run embedded document prose —
    checked the same way as Tier 2, by input-token magnitude against what the known
    prompt templates could contain without an excerpt (envelope render + section
    titles is at most a few thousand tokens; a chapter's own prose is far larger)."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system": self.system,
            "seed": self.seed,
            "total_concepts": self.total_concepts,
            "grounded": self.grounded,
            "ungrounded": self.ungrounded,
            "template_deviations": self.template_deviations,
            "attribution_correct": self.attribution_correct,
            "attribution_incorrect": self.attribution_incorrect,
            "regenerated": self.regenerated,
            "tier1_text_grounded": self.tier1_text_grounded,
        }


# A Tier 1 pass1 prompt embeds a growing "FINDINGS SO FAR" block plus section
# titles — a few thousand tokens at most (observed: 4,522-7,074 across all nine
# runs). An actual chapter's prose (6-40 pages) would run tens of thousands of
# tokens if it were ever included. This is a coarse, documented backstop, not the
# primary evidence — the primary evidence is `envelope.pass1.build_prompt`'s source
# itself, which contains no chapter-text field at all.
_TIER1_TEXT_GROUNDED_TOKEN_FLOOR = 20_000


def score_run(run_dir: Path, sections_by_id: dict[str, dict[str, Any]]) -> GroundednessReportMard:
    run = load_run(run_dir)
    summary = run["summary"]
    calls = run["calls"]

    tier2_calls = [call for call in calls if call.get("role") == "tier2"]
    by_position: dict[int, list[dict[str, Any]]] = {}
    for call in tier2_calls:
        parsed = parse_tier2_call(call)
        if parsed is None:
            continue
        # Keyed by plan `position`, not `concept_label`: two distinct concept ids
        # can carry the identical human-readable label (observed in two real runs
        # — e.g. "abstraction-and-models" vs "abstraction-and-modeling", both
        # labelled "Abstraction and Modeling") without being merged by the
        # compiler's exact-id-match dedup (docs/28 §3). `position` is unique per
        # `study_sequence` entry and is parsed straight from the prompt, so it
        # cannot conflate two concepts the way the label did in an earlier version
        # of this module.
        by_position.setdefault(parsed.position, []).append(call)

    grounded = ungrounded = template_deviations = 0
    attr_correct = attr_incorrect = 0
    regenerated = 0
    for _position, attempts in by_position.items():
        if len(attempts) > 1:
            regenerated += 1
        last = attempts[-1]
        parsed = parse_tier2_call(last)
        assert parsed is not None  # guaranteed: this call built the key above
        if not parsed.matched_known_template:
            template_deviations += 1
            continue
        if text_grounded(parsed):
            grounded += 1
        else:
            ungrounded += 1
        correct = attribution_correct(parsed, sections_by_id)
        if correct is True:
            attr_correct += 1
        elif correct is False:
            attr_incorrect += 1

    tier1_calls = [call for call in calls if str(call.get("role", "")).startswith("tier1")]
    tier1_grounded = any(
        call.get("input_tokens", 0) >= _TIER1_TEXT_GROUNDED_TOKEN_FLOOR for call in tier1_calls
    )

    return GroundednessReportMard(
        run_id=summary["run_id"],
        system=summary["system"],
        seed=summary["seed"],
        total_concepts=len(by_position),
        grounded=grounded,
        ungrounded=ungrounded,
        template_deviations=template_deviations,
        attribution_correct=attr_correct,
        attribution_incorrect=attr_incorrect,
        regenerated=regenerated,
        tier1_text_grounded=tier1_grounded,
    )


SYSTEMS: tuple[str, ...] = ("mard", "mard_a1", "mard_a1f")


def score_all(
    systems: tuple[str, ...] = SYSTEMS, *, seeds: tuple[int, ...] = CAMPAIGN_SEEDS
) -> list[GroundednessReportMard]:
    sections_by_id = load_sections_by_id()
    results = []
    for system in systems:
        for seed in seeds:
            results.append(score_run(select_run(system, seed), sections_by_id))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Task C — groundedness over the MARD arm (docs/34 §4)."
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    reports = [report.to_dict() for report in score_all()]
    text = json.dumps(reports, ensure_ascii=False, indent=2)
    print(text)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
