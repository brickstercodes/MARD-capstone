"""Run the MARD pipeline end to end: Pass 0, Pass 1, Master Plan compile, Tier 2
fork-join, all under one `RunLogger` — mirroring `vanilla/run.py`'s shape for the
other arm `docs/25-HANDOFF_MARD_ARM.md` hands off.

Real spend, real per-call logging: Tier 1 and Tier 2 both go through one shared
`ThrottledAsyncOpenAI` (`provider/openai_client.py`), which logs every call to the
`RunLogger` directly via `CallLogger.log_call`. Unlike the vanilla arm there is no
separate usage-summary reconciliation step here, because MARD's own seams
(`provider/seams.py`) are this pipeline's only path to the model — nothing else
could report tokens that per-call logging missed.

Tier 1's two call sites (`envelope.pass0.TopicLabeller.label`,
`envelope.pass1.ChapterExplorer.explore`) are synchronous — `provider/sync_seams.py`
bridges them to the async OpenAI seams; see that module's docstring for why a
plain `asyncio.run()` per call is correct here, given Tier 1 is inherently
sequential (`envelope.pass1.run_pass1`'s own docstring). Tier 2's fork-join keeps
its own async event loop via `orchestrate.execute_plan_sync`, entered only after
Tier 1's loops have each already closed.

A1 (`docs/31-ABLATIONS.md`, `docs/25` §T5) was originally one substitution —
`envelope.stripped()` in place of `envelope` before Pass 1 runs. The first real
runs (28 Aug 2026, `docs/28` §6) showed that cut only removes the skeleton:
`pass1.run_pass1`'s frozen `with_findings` accumulation keeps growing regardless,
and `Envelope.render()`'s findings block was never gated on the stripped state, so
cross-chapter structure survived the ablation nearly unchanged. Per Anugrah's
call (`docs/28` §7), the single ablation is now two single-variable cuts: `"a1s"`
(skeleton removed, findings kept — what the first runs actually measured,
relabelled rather than discarded) and `"a1f"` (findings removed via
`Envelope.findings_suppressed()`, skeleton kept — the cut that actually tests the
findings-channel hypothesis). Same models, same document, same throttle for both.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from envelope.compile_plan import UnsequenceablePlanError, compile_master_plan
from envelope.envelope import Envelope
from envelope.pass0 import run_pass0
from envelope.pass1 import Pass1Result, run_pass1
from ingest.blocks import Block
from ingest.chapters import content_chapters, group_into_chapters
from ingest.manifest import verify_or_raise
from ingest.sections import build_sections
from orchestrate import Artefact, LmBuilder, execute_plan_sync
from plan import MasterPlan, parse_master_plan
from provider.openai_client import ThrottledAsyncOpenAI
from provider.seams import OpenAIChapterExplorer, OpenAILanguageModel, OpenAITopicLabeller
from provider.sync_seams import SyncChapterExplorer, SyncTopicLabeller
from provider.throttle import Throttle, ThrottleConfig
from runlog import RunLogger

Ablation = Literal["a1s", "a1f"] | None

# `provider/seams.py`'s `DEFAULT_TIER2_MAX_TOKENS=2048` was sized against docs/18
# §10.3's "~1,000 tokens/section" prose estimate, which predates measuring this
# pair's actual behaviour. A first real run (seed 11, 28 Aug 2026) showed why that
# estimate is not enough: `gpt-5-mini` is a reasoning model
# (`provider.reasoning.is_reasoning_model`), and reasoning tokens are drawn from
# the same `max_completion_tokens` budget as the visible answer. 15 of 84 Tier 2
# calls exhausted the full 2048-token budget on hidden reasoning and returned
# `content=""` — confirmed directly from that run's `calls.jsonl`
# (`output_tokens == 2048` on every empty response), not inferred. The 69 calls
# that *did* produce output used 608-1993 tokens (median 1510) — already close to
# the old cap even when they succeeded. `join_in_plan_order` correctly refused to
# silently join a short artefact (`docs/25` trap #3), so this surfaced as a loud
# `IncompleteArtefactError` rather than a quietly truncated one.
# `TIER2_REASONING_EFFORT="low"` targets the actual cause — Tier 2's task is
# writing one already-scoped prose section from a given directive, not open-ended
# problem-solving, so it should not need heavy reasoning — and `TIER2_MAX_TOKENS`
# adds headroom on top as a second line of defence. Both are overridable per call;
# neither touches `provider/seams.py`'s shared defaults, which other call sites may
# still depend on.
TIER2_MAX_TOKENS = 4096
TIER2_REASONING_EFFORT = "low"

# Tier 1 stays at the provider's own default effort — its task (per-chapter
# concept/prerequisite extraction over a growing envelope) is closer to the
# open-ended reasoning `TIER2_REASONING_EFFORT` deliberately avoids for Tier 2,
# and the seed-11 smoke/full runs produced non-zero concepts with no coroutine or
# token-budget failures at this setting. `None` here is a recorded decision, not
# an oversight — every run logs it explicitly (`params["tier1_reasoning_effort"]`)
# rather than leaving "not overridden" implicit.
TIER1_REASONING_EFFORT = None


@dataclass
class MardResult:
    """Everything a driver script needs to report, plus enough to audit later."""

    document_id: str
    ablation: Ablation
    skeleton_sections: int
    chapters_explored: int
    chapters_total: int
    concepts_accepted: int
    edges_accepted: int
    cross_chapter_edges: int
    never_declared_rejections: int
    compiled: bool
    plan: MasterPlan | None
    artefact: Artefact | None
    pass1_traces: tuple[dict[str, Any], ...]


def _load_blocks(document_dir: Path) -> list[Block]:
    """Same shape as `envelope.cli`'s private loader — `document.jsonl`'s `bbox`
    field is a JSON list and `Block` wants a tuple."""
    blocks: list[Block] = []
    with (document_dir / "document.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            payload["bbox"] = tuple(payload["bbox"])
            blocks.append(Block(**payload))
    return blocks


def _cross_chapter_edge_count(result: Pass1Result) -> int:
    """Prerequisite and dependent declared in different chapters — the headline
    cross-chapter measurement `docs/25` §T3 asks for. The only channel carrying an
    earlier chapter's concept ids into a later chapter's call is the envelope's
    `FINDINGS SO FAR` block, so this count is a direct read on whether that channel
    did anything.

    First-occurrence-wins when a concept id was independently declared by more
    than one chapter, matching `envelope.compile_plan._merge_concepts`'s policy —
    a plain dict comprehension over `result.concepts` would keep the *last*
    chapter instead, silently disagreeing with which chapter the compiled plan
    actually attributes the merged concept to.
    """
    chapter_of: dict[str, str] = {}
    for concept in result.concepts:
        chapter_of.setdefault(concept.concept_id, concept.chapter_id)
    return sum(
        1
        for edge in result.edges
        if chapter_of.get(edge.prerequisite) != chapter_of.get(edge.dependent)
    )


def _never_declared_count(result: Pass1Result) -> int:
    """A chapter whose `explore()` call raised is recorded with an `"error"` key
    and no `"rejected"` key at all (`envelope.pass1.run_pass1`'s except branch) —
    `.get(..., [])` rather than `trace["rejected"]`, or a chapter-level explorer
    failure crashes this count instead of just being absent from it."""
    return sum(
        1
        for trace in result.traces
        for rejection in trace.get("rejected", [])
        if "was never declared" in rejection
    )


def run_mard(
    corpus_dir: Path,
    document_id: str,
    *,
    tier1_model: str,
    tier2_model: str,
    logger: RunLogger,
    ablation: Ablation = None,
    max_chapters: int | None = None,
    throttle_config: ThrottleConfig | None = None,
    client: ThrottledAsyncOpenAI | None = None,
    tier1_reasoning_effort: str | None = TIER1_REASONING_EFFORT,
    tier2_max_tokens: int = TIER2_MAX_TOKENS,
    tier2_reasoning_effort: str | None = TIER2_REASONING_EFFORT,
) -> MardResult:
    """Run Pass 0 -> Pass 1 -> compile -> Tier 2 -> join, fully logged under `logger`.

    `ablation="a1s"` strips the skeleton (`Envelope.stripped()`); `ablation="a1f"`
    suppresses findings rendering (`Envelope.findings_suppressed()`) — see the
    module docstring. `max_chapters` restricts Pass 1 to the document's
    first N chapters, for a cheap smoke run (`docs/25` §T2); leave it `None` for a
    measured run. `client` is injectable for tests, same reasoning as
    `ThrottledAsyncOpenAI.raw_client` — a measured run omits it and gets a real one.

    `envelope.compile_plan.UnsequenceablePlanError` is deliberately not caught here
    beyond the point already logged before compiling — a genuine cycle is a finding
    (`docs/25` §T3), reported via `MardResult.compiled=False`, never hand-edited.
    `orchestrate.IncompleteArtefactError` is not caught at all: a truncated
    artefact must fail the run, not score low (`docs/25` trap #3).
    """
    document_dir = corpus_dir / document_id
    verify_or_raise(document_dir)
    blocks = _load_blocks(document_dir)
    sections = build_sections(blocks, document_id)
    all_chapters = group_into_chapters(sections, document_id)
    chapters = content_chapters(all_chapters)
    if max_chapters is not None:
        chapters = chapters[:max_chapters]
    section_titles = {section.section_id: section.title for section in sections}

    client = client or ThrottledAsyncOpenAI(Throttle(throttle_config), logger=logger)

    logger.log_event("mard_tier1_config", {"reasoning_effort": tier1_reasoning_effort})
    labeller = SyncTopicLabeller(
        inner=OpenAITopicLabeller(
            client=client, model=tier1_model, reasoning_effort=tier1_reasoning_effort
        )
    )
    skeleton, pass0_trace = run_pass0(document_id, sections, labeller=labeller)
    logger.log_event("mard_pass0", pass0_trace)

    envelope = Envelope.from_skeleton(skeleton)
    logger.log_envelope(0, envelope, label="initial")
    if ablation == "a1s":
        envelope = envelope.stripped()
        logger.log_event(
            "mard_ablation",
            {
                "ablation": "a1s",
                "note": "skeleton removed before Pass 1, findings kept — docs/28 §6/§7",
            },
        )
    elif ablation == "a1f":
        envelope = envelope.findings_suppressed()
        logger.log_event(
            "mard_ablation",
            {
                "ablation": "a1f",
                "note": "findings never rendered before Pass 1, skeleton kept — docs/28 §6/§7",
            },
        )

    explorer = SyncChapterExplorer(
        inner=OpenAIChapterExplorer(
            client=client, model=tier1_model, reasoning_effort=tier1_reasoning_effort
        )
    )
    pass1_result = run_pass1(envelope, chapters, section_titles, explorer=explorer)
    logger.log_envelope(1, pass1_result.envelope, label="final")
    # Saved as an artefact, not just an aggregate event: a per-chapter failure
    # (explorer raised, caught by run_pass1's own try/except) only shows up here —
    # a run that then crashes elsewhere would otherwise leave no record of which
    # chapter or why.
    logger.save_artefact("pass1_trace.json", json.dumps(pass1_result.traces, indent=2))

    logger.log_event(
        "mard_pass1",
        {
            "chapters_explored": len(pass1_result.traces),
            "chapters_total": len(all_chapters),
            "concepts_accepted": len(pass1_result.concepts),
            "edges_accepted": len(pass1_result.edges),
        },
    )

    cross_chapter = _cross_chapter_edge_count(pass1_result)
    never_declared = _never_declared_count(pass1_result)
    logger.log_event(
        "mard_cross_chapter_edges",
        {
            "cross_chapter_edges": cross_chapter,
            "total_edges": len(pass1_result.edges),
            "never_declared_rejections": never_declared,
        },
    )

    if not pass1_result.concepts:
        logger.log_event(
            "mard_no_plan", {"reason": "Pass 1 accepted no concepts; nothing to compile."}
        )
        return MardResult(
            document_id=document_id,
            ablation=ablation,
            skeleton_sections=len(skeleton.sections),
            chapters_explored=len(pass1_result.traces),
            chapters_total=len(all_chapters),
            concepts_accepted=0,
            edges_accepted=len(pass1_result.edges),
            cross_chapter_edges=cross_chapter,
            never_declared_rejections=never_declared,
            compiled=False,
            plan=None,
            artefact=None,
            pass1_traces=tuple(pass1_result.traces),
        )

    try:
        compiled = compile_master_plan(
            document_id, pass1_result.concepts, pass1_result.edges, sections
        )
    except UnsequenceablePlanError as err:
        # A finding about the concept graph, not a harness fault — docs/25 §T3.
        logger.log_event("mard_unsequenceable_plan", {"error": str(err)})
        return MardResult(
            document_id=document_id,
            ablation=ablation,
            skeleton_sections=len(skeleton.sections),
            chapters_explored=len(pass1_result.traces),
            chapters_total=len(all_chapters),
            concepts_accepted=len(pass1_result.concepts),
            edges_accepted=len(pass1_result.edges),
            cross_chapter_edges=cross_chapter,
            never_declared_rejections=never_declared,
            compiled=False,
            plan=None,
            artefact=None,
            pass1_traces=tuple(pass1_result.traces),
        )

    logger.save_artefact("master_plan.json", json.dumps(compiled.plan, indent=2))
    logger.log_event("mard_compile_plan", {"compiled": True, **compiled.trace})

    plan = parse_master_plan(json.dumps({**compiled.plan, "run_id": logger.run_id}))

    logger.log_event(
        "mard_tier2_config",
        {"max_tokens": tier2_max_tokens, "reasoning_effort": tier2_reasoning_effort},
    )
    lm = OpenAILanguageModel(
        client=client,
        model=tier2_model,
        reasoning_effort=tier2_reasoning_effort,
        max_tokens=tier2_max_tokens,
    )
    builder = LmBuilder(lm=lm, name="mard_tier2")
    artefact = execute_plan_sync(plan, builder, logger)

    return MardResult(
        document_id=document_id,
        ablation=ablation,
        skeleton_sections=len(skeleton.sections),
        chapters_explored=len(pass1_result.traces),
        chapters_total=len(all_chapters),
        concepts_accepted=len(pass1_result.concepts),
        edges_accepted=len(pass1_result.edges),
        cross_chapter_edges=cross_chapter,
        never_declared_rejections=never_declared,
        compiled=True,
        plan=plan,
        artefact=artefact,
        pass1_traces=tuple(pass1_result.traces),
    )
