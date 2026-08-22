"""Pass 1 — enriched exploration, one call per chapter, envelope carried into each.

`CONTEXT.md` line 75: input is "section boundaries + skeleton + parent directive
(~200 tokens/chapter)", output is "core concepts, prerequisites, forward
dependencies", and the envelope is "enriched per call". That last phrase is the whole
mechanism: each chapter's call sees what earlier chapters found, so exploration
confirms a hypothesis rather than discovering blindly (`docs/00-CLAIM.md`).

This is where the A1 comparison becomes meaningful. A vanilla-RLM call sees a raw
slice; a MARD Pass 1 call sees the same slice plus the structural map plus every
prior finding. Both are one call per chapter over the same document, so the delta is
the envelope and nothing else.

**What this module refuses to do.** It does not repair a model's output. An extracted
concept naming a section outside its own chapter, an edge pointing at a concept that
was never declared, a `cross_reference` with no quote — each is dropped and named in
the trace rather than silently corrected. Tier 1 is a language model; a pipeline that
quietly patches its output produces measurements of the patcher.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol

from envelope.envelope import Envelope, Finding
from ingest.chapters import Chapter

PASS1_PROMPT_VERSION = "pass1-concepts-v1"

# Mirrors plan.models.ConceptId. Duplicated deliberately rather than imported: this
# module must run before PR #48 lands, and a pattern that drifts is caught by
# tests/test_pass1.py::test_concept_id_pattern_matches_the_contract.
CONCEPT_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
MAX_CONCEPT_ID_CHARS = 80

VALID_EVIDENCE = frozenset({"cross_reference", "glossary", "inferred"})

# A directive is a Tier 2 builder's entire brief. plan.validation rejects anything
# under 12 characters, so a shorter one is dropped here where the chapter that
# produced it can still be named.
MIN_DIRECTIVE_CHARS = 12

PASS1_PROMPT = """\
You are the Scout, exploring one chapter of a textbook you have already mapped.

{envelope}

## THIS CHAPTER
{chapter_title} (pages {page_start}-{page_end}, {section_count} sections)

Sections available in this chapter, by id:
{section_lines}

## WHAT TO RETURN
JSON only, with exactly these two keys:

{{
  "concepts": [
    {{"id": "lower-kebab-id", "label": "Human Readable Name",
      "section_id": "<one of the ids above>",
      "directive": "What a writer must produce for this concept, one or two sentences."}}
  ],
  "prerequisites": [
    {{"prerequisite": "<concept id>", "dependent": "<concept id>",
      "evidence": "cross_reference" | "glossary" | "inferred",
      "quote": "the document's own words, required for cross_reference, else null"}}
  ]
}}

Rules. Name at most {max_concepts} concepts — the ones a study plan would be built
around, not every term. A prerequisite may point at a concept found in an earlier
chapter; those are listed in the findings above. Use "cross_reference" only when the
chapter itself says so, and then quote it. Do not restate the chapter title as a
concept. Do not invent section ids.
"""

MAX_CONCEPTS_PER_CHAPTER = 6


@dataclass(frozen=True)
class ExtractedConcept:
    """One concept Pass 1 accepted, anchored to a section that really exists."""

    concept_id: str
    label: str
    section_id: str
    directive: str
    chapter_id: str


@dataclass(frozen=True)
class ExtractedEdge:
    prerequisite: str
    dependent: str
    evidence: str
    quote: str | None
    chapter_id: str


@dataclass
class Pass1Result:
    """Everything Pass 1 produced, plus the envelope it grew into."""

    envelope: Envelope
    concepts: list[ExtractedConcept]
    edges: list[ExtractedEdge]
    traces: list[dict[str, Any]]

    @property
    def concept_ids(self) -> set[str]:
        return {concept.concept_id for concept in self.concepts}


class ChapterExplorer(Protocol):
    """Whatever turns a Pass 1 prompt into the JSON object described above."""

    def explore(self, prompt: str, chapter: Chapter) -> dict[str, Any]: ...


class NoOpChapterExplorer:
    """Pass 1 with the scout call switched off.

    Produces an empty exploration, which is a legitimate configuration and not a test
    double: it is what a run looks like when the model contributes nothing, and the
    resulting Master Plan is correctly empty rather than fabricated.
    """

    def explore(self, prompt: str, chapter: Chapter) -> dict[str, Any]:
        return {"concepts": [], "prerequisites": []}


def build_prompt(envelope: Envelope, chapter: Chapter, section_titles: dict[str, str]) -> str:
    lines = "\n".join(
        f"  {section_id} — {section_titles.get(section_id, '(untitled)')}"
        for section_id in chapter.section_ids
    )
    return PASS1_PROMPT.format(
        envelope=envelope.render(),
        chapter_title=chapter.title,
        page_start=chapter.page_start,
        page_end=chapter.page_end,
        section_count=len(chapter.section_ids),
        section_lines=lines,
        max_concepts=MAX_CONCEPTS_PER_CHAPTER,
    )


def _valid_concept_id(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) <= MAX_CONCEPT_ID_CHARS
        and bool(CONCEPT_ID.match(value))
    )


def _accept_concepts(raw: object, chapter: Chapter, rejected: list[str]) -> list[ExtractedConcept]:
    if not isinstance(raw, list):
        rejected.append("concepts was not a list")
        return []

    allowed_sections = set(chapter.section_ids)
    accepted: list[ExtractedConcept] = []
    seen: set[str] = set()

    for item in raw[:MAX_CONCEPTS_PER_CHAPTER]:
        if not isinstance(item, dict):
            rejected.append("concept entry was not an object")
            continue

        concept_id = item.get("id")
        if not _valid_concept_id(concept_id):
            rejected.append(f"concept id {concept_id!r} does not match the contract pattern")
            continue
        assert isinstance(concept_id, str)
        if concept_id in seen:
            rejected.append(f"concept {concept_id!r} declared twice in one chapter")
            continue

        section_id = item.get("section_id")
        if section_id not in allowed_sections:
            rejected.append(
                f"concept {concept_id!r} claims section {section_id!r}, "
                f"which is not in this chapter"
            )
            continue

        label = item.get("label")
        directive = item.get("directive")
        if not isinstance(label, str) or not label.strip():
            rejected.append(f"concept {concept_id!r} has no label")
            continue
        if not isinstance(directive, str) or len(directive.strip()) < MIN_DIRECTIVE_CHARS:
            rejected.append(
                f"concept {concept_id!r} has a directive under "
                f"{MIN_DIRECTIVE_CHARS} characters, which the tier boundary rejects"
            )
            continue

        seen.add(concept_id)
        accepted.append(
            ExtractedConcept(
                concept_id=concept_id,
                label=label.strip(),
                section_id=str(section_id),
                directive=directive.strip(),
                chapter_id=chapter.chapter_id,
            )
        )

    if len(raw) > MAX_CONCEPTS_PER_CHAPTER:
        rejected.append(
            f"{len(raw)} concepts returned, {MAX_CONCEPTS_PER_CHAPTER} kept "
            "— the cap is a budget decision, not a quality judgement"
        )
    return accepted


def _accept_edges(
    raw: object, chapter: Chapter, known_ids: set[str], rejected: list[str]
) -> list[ExtractedEdge]:
    if not isinstance(raw, list):
        rejected.append("prerequisites was not a list")
        return []

    accepted: list[ExtractedEdge] = []
    for item in raw:
        if not isinstance(item, dict):
            rejected.append("prerequisite entry was not an object")
            continue

        prerequisite = item.get("prerequisite")
        dependent = item.get("dependent")
        evidence = item.get("evidence")
        quote = item.get("quote")

        if prerequisite not in known_ids or dependent not in known_ids:
            rejected.append(
                f"edge {prerequisite!r} -> {dependent!r} names a concept that was never declared"
            )
            continue
        if prerequisite == dependent:
            rejected.append(f"concept {prerequisite!r} listed as its own prerequisite")
            continue
        if evidence not in VALID_EVIDENCE:
            rejected.append(f"edge {prerequisite!r} -> {dependent!r} has evidence {evidence!r}")
            continue
        if evidence == "cross_reference" and not (isinstance(quote, str) and quote.strip()):
            # The boundary rejects an unsupported cross-reference. Demoting it to
            # "inferred" here would launder the claim, so the edge is dropped and named.
            rejected.append(
                f"edge {prerequisite!r} -> {dependent!r} claims a cross-reference with no quote"
            )
            continue

        accepted.append(
            ExtractedEdge(
                prerequisite=str(prerequisite),
                dependent=str(dependent),
                evidence=str(evidence),
                quote=quote.strip() if isinstance(quote, str) and quote.strip() else None,
                chapter_id=chapter.chapter_id,
            )
        )
    return accepted


def directive_for(chapter: Chapter) -> str:
    """The parent directive a chapter's call is given. Part of the envelope, not the prompt.

    Deliberately generic: Pass 1's job is uniform across chapters, and a directive that
    varied per chapter would be an untracked prompt variable inside a measured run.
    """
    return (
        f"Identify the concepts a learner must acquire in {chapter.title}, and state "
        "which earlier concepts each one depends on. Prefer dependencies the chapter "
        "itself asserts over ones you infer."
    )


def run_pass1(
    envelope: Envelope,
    chapters: list[Chapter],
    section_titles: dict[str, str],
    explorer: ChapterExplorer | None = None,
) -> Pass1Result:
    """Explore each chapter in book order, growing the envelope as it goes.

    Book order, not plan order: the plan does not exist yet. Chapters are visited in
    the document's own sequence so a later chapter's call can see what earlier ones
    found, which is the accumulation the claim rests on.
    """
    active = explorer or NoOpChapterExplorer()
    concepts: list[ExtractedConcept] = []
    edges: list[ExtractedEdge] = []
    traces: list[dict[str, Any]] = []
    known_ids: set[str] = set()

    for chapter in chapters:
        directive = directive_for(chapter)
        child = envelope.for_child(chapter.chapter_id, directive)
        prompt = build_prompt(child, chapter, section_titles)

        rejected: list[str] = []
        try:
            raw = active.explore(prompt, chapter)
        except Exception as err:  # noqa: BLE001 — a failed chapter is a finding, not a crash
            traces.append(
                {
                    "pass": 1,
                    "chapter_id": chapter.chapter_id,
                    "prompt_version": PASS1_PROMPT_VERSION,
                    "error": f"{type(err).__name__}: {err}",
                    "concepts_accepted": 0,
                    "edges_accepted": 0,
                }
            )
            continue

        if not isinstance(raw, dict):
            rejected.append(f"explorer returned {type(raw).__name__}, expected an object")
            raw = {}

        chapter_concepts = _accept_concepts(raw.get("concepts"), chapter, rejected)
        known_ids |= {concept.concept_id for concept in chapter_concepts}
        chapter_edges = _accept_edges(raw.get("prerequisites"), chapter, known_ids, rejected)

        concepts.extend(chapter_concepts)
        edges.extend(chapter_edges)

        envelope = envelope.with_findings(
            Finding(
                section_id=chapter.chapter_id,
                pass_index=1,
                concepts=tuple(concept.concept_id for concept in chapter_concepts),
                prerequisites=tuple((edge.prerequisite, edge.dependent) for edge in chapter_edges),
                note=f"{chapter.title} (pp.{chapter.page_start}-{chapter.page_end})",
            )
        )

        traces.append(
            {
                "pass": 1,
                "chapter_id": chapter.chapter_id,
                "prompt_version": PASS1_PROMPT_VERSION,
                "prompt_chars": len(prompt),
                "envelope": child.to_dict(),
                "concepts_accepted": len(chapter_concepts),
                "edges_accepted": len(chapter_edges),
                "rejected": rejected,
            }
        )

    return Pass1Result(envelope=envelope, concepts=concepts, edges=edges, traces=traces)
