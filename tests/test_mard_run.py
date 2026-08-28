"""Offline tests for `mard/run.py`'s wiring: Pass 0 -> Pass 1 -> compile -> Tier 2
-> join, driven by a fake OpenAI raw client so nothing here touches the network.

Also the empirical check for a question `docs/25-HANDOFF_MARD_ARM.md` §T5 raises
but does not settle: whether `ablation="a1s"` (`Envelope.stripped()` substituted
once, before Pass 1 starts) keeps every chapter's rendered envelope empty, or
whether `envelope.pass1.run_pass1`'s own (frozen) `with_findings` accumulation lets
findings leak back in from chapter 2 onward regardless. See
`test_a1s_ablation_strips_chapter_one_but_findings_reaccumulate_from_chapter_two`.
That question is what motivated splitting the original single-substitution "A1"
into two cuts, `"a1s"` and `"a1f"` (`docs/28` §6/§7) — see
`test_a1f_ablation_never_renders_findings_even_after_they_accumulate`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from envelope.envelope import Envelope
from envelope.pass1 import ExtractedConcept, ExtractedEdge, Pass1Result
from envelope.skeleton import Skeleton
from ingest.manifest import SourceRecord, write_manifest
from mard.run import _cross_chapter_edge_count, _never_declared_count, run_mard
from provider.openai_client import ThrottledAsyncOpenAI
from provider.throttle import Throttle
from runlog import RunLogger

SOURCE = SourceRecord(file_name="book.pdf", sha256="0" * 64, bytes=100, page_count=8)


def _block(
    block_id: str, page: int, kind: str, text: str, level: int | None = None
) -> dict[str, Any]:
    return {
        "block_id": block_id,
        "page": page,
        "kind": kind,
        "level": level,
        "role": None,
        "text": text,
        "bbox": [0.0, 0.0, 1.0, 1.0],
        "font_size": 10.0,
    }


def _write_corpus(corpus_dir: Path, document_id: str) -> None:
    """Two chapters, one section each, spread over 8 pages so `choose_section_level`
    settles on level 1 (`MIN_PAGES_PER_SECTION=3 <= 4 <= MAX_PAGES_PER_SECTION=40`)."""
    target = corpus_dir / document_id
    target.mkdir(parents=True)

    blocks = [
        _block("b1", 1, "heading", "Chapter 1 Introduction", level=1),
        _block("b2", 1, "body", "Some introductory material."),
        _block("b3", 4, "body", "More introductory material."),
        _block("b4", 5, "heading", "Chapter 2 Advanced Topics", level=1),
        _block("b5", 5, "body", "Some advanced material."),
        _block("b6", 8, "body", "More advanced material."),
    ]
    with (target / "document.jsonl").open("w", encoding="utf-8") as handle:
        for block in blocks:
            handle.write(json.dumps(block) + "\n")
    (target / "document.txt").write_text("Chapter 1 Introduction\nChapter 2 Advanced Topics\n")

    write_manifest(target, document_id, SOURCE)


@dataclass
class _FakeMessage:
    content: str


@dataclass
class _FakeChoice:
    message: _FakeMessage


@dataclass
class _FakeUsage:
    prompt_tokens: int
    completion_tokens: int


@dataclass
class _FakeResponse:
    choices: list[_FakeChoice]
    usage: _FakeUsage


def _response(content: str) -> _FakeResponse:
    return _FakeResponse(
        choices=[_FakeChoice(message=_FakeMessage(content=content))],
        usage=_FakeUsage(prompt_tokens=10, completion_tokens=5),
    )


def _first_section_id(prompt: str) -> str:
    match = re.search(r"Sections available in this chapter, by id:\n\s*(\S+)", prompt)
    assert match, f"no section id block found in prompt: {prompt!r}"
    return match.group(1)


def _this_chapter_title(prompt: str) -> str:
    """The chapter this prompt is actually exploring — not a substring match
    against the whole prompt, which (for MARD's un-ablated envelope) can also
    contain an earlier chapter's title inside its "FINDINGS SO FAR" block."""
    match = re.search(r"## THIS CHAPTER\n(.+?) \(pages", prompt)
    assert match, f"no '## THIS CHAPTER' marker found in prompt: {prompt!r}"
    return match.group(1)


class _FakeMardClient:
    """Dispatches by prompt content, not by call order — Tier 2's builders run
    concurrently (`asyncio.gather`), so order is not guaranteed."""

    def __init__(self) -> None:
        self.chat = self

    @property
    def completions(self):
        return self

    async def create(self, **kwargs: object) -> _FakeResponse:
        messages = kwargs["messages"]
        content = messages[0]["content"]  # type: ignore[index]

        if "## THIS CHAPTER" in content:
            return _response(self._pass1_response(content))
        if "Section ids, in order" in content:
            return _response(json.dumps({}))  # empty topic labelling; not load-bearing here
        return _response(self._tier2_response(content))

    def _pass1_response(self, content: str) -> str:
        section_id = _first_section_id(content)
        payload: dict[str, Any]
        if _this_chapter_title(content).startswith("Chapter 1"):
            payload = {
                "concepts": [
                    {
                        "id": "doc.c1",
                        "section_id": section_id,
                        "label": "Concept One",
                        "directive": "Explain concept one in full detail for a learner.",
                    }
                ],
                "prerequisites": [],
            }
        else:
            payload = {
                "concepts": [
                    {
                        "id": "doc.c2",
                        "section_id": section_id,
                        "label": "Concept Two",
                        "directive": "Explain concept two in full detail for a learner.",
                    }
                ],
                "prerequisites": [
                    {
                        "prerequisite": "doc.c1",
                        "dependent": "doc.c2",
                        "evidence": "inferred",
                        "quote": None,
                    }
                ],
            }
        return json.dumps(payload)

    def _tier2_response(self, content: str) -> str:
        match = re.search(r"Concept: (.+)", content)
        label = match.group(1) if match else "unknown"
        return f"Explanation text for {label}."


def _client(logger: RunLogger) -> ThrottledAsyncOpenAI:
    return ThrottledAsyncOpenAI(Throttle(), raw_client=_FakeMardClient(), logger=logger)  # type: ignore[arg-type]


def _logger(tmp_path: Path, system: str) -> RunLogger:
    return RunLogger.start(
        runs_root=tmp_path / "runs",
        system=system,
        document_id="doc",
        seed=11,
        models={"tier1": "fake-tier1", "tier2": "fake-tier2"},
    )


def test_cross_chapter_edge_count_attributes_a_merged_concept_to_its_first_chapter():
    """Matches `envelope.compile_plan._merge_concepts`'s policy: when a concept id
    is independently declared by two chapters, the compiled plan keeps the first
    (book-order) declaration. This count must agree, or it silently disagrees with
    the plan it is meant to describe. Discriminating case: "dup" is declared in
    chapter 1 and again in chapter 3; "x" is declared only in chapter 3. Under
    first-wins, "dup" is attributed to chapter 1, so "dup" -> "x" is cross-chapter.
    A plain dict comprehension over `result.concepts` (last-wins) would instead
    attribute "dup" to chapter 3 — the same chapter as "x" — and wrongly count it
    as not cross-chapter."""
    skeleton = Skeleton.from_sections("doc", [])
    envelope = Envelope.from_skeleton(skeleton)
    concepts = [
        ExtractedConcept(
            concept_id="dup",
            label="First",
            section_id="doc.s0",
            directive="Explain the first chapter's version.",
            chapter_id="doc.ch01",
        ),
        ExtractedConcept(
            concept_id="x",
            label="X",
            section_id="doc.s2",
            directive="Explain x.",
            chapter_id="doc.ch03",
        ),
        ExtractedConcept(
            concept_id="dup",
            label="Second",
            section_id="doc.s2",
            directive="Explain the second chapter's version.",
            chapter_id="doc.ch03",
        ),
    ]
    edges = [
        ExtractedEdge(
            prerequisite="dup",
            dependent="x",
            evidence="inferred",
            quote=None,
            chapter_id="doc.ch03",
        )
    ]
    result = Pass1Result(envelope=envelope, concepts=concepts, edges=edges, traces=[])

    assert _cross_chapter_edge_count(result) == 1


def test_never_declared_count_tolerates_a_chapter_that_raised():
    """A chapter whose `explore()` call raises is recorded by `run_pass1`'s own
    except branch with an `"error"` key and no `"rejected"` key at all — confirmed
    the hard way (A1f seed 42, 28 Aug 2026: `KeyError: 'rejected'` crashed a real,
    paid run after Pass 1 had already completed cleanly). This must not crash;
    a chapter that errored out contributes zero to the count, not an exception."""
    skeleton = Skeleton.from_sections("doc", [])
    envelope = Envelope.from_skeleton(skeleton)
    traces = [
        {"pass": 1, "chapter_id": "doc.ch01", "error": "ValueError: boom"},
        {
            "pass": 1,
            "chapter_id": "doc.ch02",
            "rejected": ["'x' -> 'y' names a concept that was never declared"],
        },
    ]
    result = Pass1Result(envelope=envelope, concepts=[], edges=[], traces=traces)

    assert _never_declared_count(result) == 1


def test_run_mard_wires_pass0_through_tier2_join(tmp_path):
    _write_corpus(tmp_path, "doc")
    logger = _logger(tmp_path, "mard")

    with logger:
        result = run_mard(
            tmp_path,
            "doc",
            tier1_model="fake-tier1",
            tier2_model="fake-tier2",
            logger=logger,
            client=_client(logger),
        )

    assert result.compiled
    assert result.concepts_accepted == 2
    assert result.edges_accepted == 1
    assert result.cross_chapter_edges == 1  # doc.c1 (chapter 1) -> doc.c2 (chapter 2)
    assert result.never_declared_rejections == 0
    assert result.artefact is not None
    assert result.artefact.concept_order == ("doc.c1", "doc.c2")
    assert "Explanation text for Concept One." in result.artefact.text
    assert "Explanation text for Concept Two." in result.artefact.text

    totals = logger.totals()
    assert totals["calls"] == 5  # 1 pass0 + 2 pass1 chapters + 2 tier2 builders


def test_run_mard_reports_an_unsequenceable_plan_as_a_finding_not_a_crash(tmp_path):
    """A prerequisite cycle must surface as `compiled=False`, never propagate as an
    exception that the run log would record as `status="failed"` — docs/25 §T3:
    "that is a finding — report the cycle, do not hand-edit the graph to remove it."
    """
    _write_corpus(tmp_path, "doc")
    logger = _logger(tmp_path, "mard")

    class _CyclicClient(_FakeMardClient):
        def _pass1_response(self, content: str) -> str:
            section_id = _first_section_id(content)
            if _this_chapter_title(content).startswith("Chapter 1"):
                # Nothing declared yet — a cycle needs both endpoints already
                # known (`_accept_edges`'s `known_ids` check), so it can only be
                # constructed within one chapter's own concepts, not across two.
                return json.dumps({"concepts": [], "prerequisites": []})
            payload = {
                "concepts": [
                    {
                        "id": "doc.c1",
                        "section_id": section_id,
                        "label": "Concept One",
                        "directive": "Explain concept one in full detail for a learner.",
                    },
                    {
                        "id": "doc.c2",
                        "section_id": section_id,
                        "label": "Concept Two",
                        "directive": "Explain concept two in full detail for a learner.",
                    },
                ],
                "prerequisites": [
                    {
                        "prerequisite": "doc.c1",
                        "dependent": "doc.c2",
                        "evidence": "inferred",
                        "quote": None,
                    },
                    {
                        "prerequisite": "doc.c2",
                        "dependent": "doc.c1",
                        "evidence": "inferred",
                        "quote": None,
                    },
                ],
            }
            return json.dumps(payload)

    with logger:
        result = run_mard(
            tmp_path,
            "doc",
            tier1_model="fake-tier1",
            tier2_model="fake-tier2",
            logger=logger,
            client=ThrottledAsyncOpenAI(Throttle(), raw_client=_CyclicClient()),  # type: ignore[arg-type]
        )

    assert result.compiled is False
    assert result.artefact is None
    assert result.concepts_accepted == 2  # Pass 1 itself still succeeded


def test_a1s_ablation_strips_chapter_one_but_findings_reaccumulate_from_chapter_two(tmp_path):
    """Empirical check, not an assumption. `Envelope.stripped()`'s `is_stripped`
    requires `directive is None` (`envelope/envelope.py`), but `run_pass1`'s frozen
    loop always sets a directive via `for_child` before the very first render — so
    `is_stripped` is false from chapter 1 onward, and `render()` falls through to
    its per-field branches rather than short-circuiting to `""`. Chapter 1 still
    gets a genuinely structure-free prompt (no skeleton, no findings yet — there is
    nothing to have accumulated), but by chapter 2, `with_findings` (called at the
    end of chapter 1's iteration) has put a real finding on the envelope, and
    nothing re-strips it before chapter 2's `render()` runs. Confirmed here rather
    than assumed, per `docs/25`'s own instruction not to carry an inferred number
    forward without checking a real trace. This is exactly why "a1s" isolates the
    skeleton, not the whole envelope (`docs/28` §6/§7) — see the "a1f" test below
    for the cut that actually removes findings.
    """
    _write_corpus(tmp_path, "doc")
    logger = _logger(tmp_path, "mard_a1s")

    with logger:
        result = run_mard(
            tmp_path,
            "doc",
            tier1_model="fake-tier1",
            tier2_model="fake-tier2",
            logger=logger,
            ablation="a1s",
            client=_client(logger),
        )

    assert result.compiled
    chapter_one, chapter_two = result.pass1_traces
    assert chapter_one["envelope"]["skeleton_sections"] == 0
    assert chapter_one["envelope"]["findings_total"] == 0
    assert chapter_one["envelope"]["rendered_chars"] > 0  # target + directive blocks still render

    # The actual finding: chapter 2's envelope is not stripped either, and it now
    # carries the "accumulated finding" a1s does not remove.
    assert chapter_two["envelope"]["skeleton_sections"] == 0
    assert chapter_two["envelope"]["findings_total"] == 1


def test_a1f_ablation_never_renders_findings_even_after_they_accumulate(tmp_path):
    """The other half of the split (`docs/28` §6/§7): skeleton stays, findings
    accumulate exactly as in MARD full (`findings_total` grows), but the rendered
    envelope never shows a `FINDINGS SO FAR` block at any chapter — the actual cut
    the "cross-chapter edges should collapse" hypothesis needs to be tested
    against."""
    _write_corpus(tmp_path, "doc")
    logger = _logger(tmp_path, "mard_a1f")

    with logger:
        result = run_mard(
            tmp_path,
            "doc",
            tier1_model="fake-tier1",
            tier2_model="fake-tier2",
            logger=logger,
            ablation="a1f",
            client=_client(logger),
        )

    assert result.compiled
    chapter_one, chapter_two = result.pass1_traces
    assert chapter_one["envelope"]["skeleton_sections"] == 2  # skeleton kept
    assert chapter_two["envelope"]["findings_total"] == 1  # still accumulates
    assert chapter_two["envelope"]["findings_shown"] == 0  # never rendered
    assert chapter_two["envelope"]["suppress_findings"] is True
