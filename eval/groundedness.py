"""The groundedness detector — the seed-42 trajectory trace, made repeatable.

`docs/24` §1 hand-traced one concept ("Trees and balanced trees") through a vanilla-RLM
run and found the version published in the study guide was written from the model's
parametric knowledge alone — the generating call's prompt carried no document text at
all, 88 input tokens, no exception raised. This module turns that one hand-traced
concept into a check run over every concept in a run's final artefact, from data
already on disk: no new runs, no scorer with an API key, no spend.

Validated (28 Aug 2026, Anugrah): reproducing the seed-42 hand-trace was the real gate,
and it passed — see `test_seed_42_reproduces_the_docs_24_hand_trace`.

**What "the generating call" means here, and the four statuses this module reports.**
`docs/24` §5 specifies three concept classes plus a call-history flag — grounded /
ungrounded / regenerated / mis-sourced — assuming every concept in the final artefact
traces back to an inspectable per-concept call. Reading all three vanilla runs'
`events.jsonl` by hand before writing this showed that assumption holds for exactly one
of them:

- Seed 42: all 75 concepts are individually delegated to a sub-call carrying that
  concept's name in its prompt (`## {concept}` or `Concept: {concept}`), so each one
  resolves to a real generating call, classified `grounded` or `ungrounded` directly.
- Seeds 11 and 23: the root delegates only at chapter granularity (14 and 29 calls
  respectively — one extraction call per chapter, plus JSON-repair and a final editing
  pass for seed 23) and then writes every individual explanation itself, inside its own
  iteration code. Zero of 156 (seed 11) and zero of 190 (seed 23) concepts match any
  sub-call's prompt — not because the detector missed them, but because no per-concept
  generating call exists in the trajectory to find.

The second case is `root_authored`, not `ungrounded` and not silently folded into
`grounded`: the root wrote these itself, but at one remove from real source text — its
own per-chapter extraction calls, which it had already run and which the same
`_classify_call` heuristic classifies `grounded` for every single one of them in both
runs (14/14 background calls in seed 11, 29/29 in seed 23; see `score_run`'s
`root_authored_context` field, computed and reported per run rather than assumed).
"Grounded at one remove" is therefore an evidence-backed reading of these two runs
specifically, not a guess dressed as a class name — and if a future run's background
calls come back *ungrounded*, `root_authored_context` will say so and the write-up must
follow the evidence, not this module's docstring.

`unresolved` is kept only for the case `root_authored` cannot cover: a run with no
sub-calls in its trajectory at all, so there is no digest — grounded or otherwise — to
attribute the root's writing to. None of the three logged runs hit this case; it exists
for whatever shows up next, MARD included.

`groundedness_rate` is computed over directly-resolved concepts only
(`grounded / (grounded + ungrounded)`) — see `GroundednessReport` for why
`root_authored` and `unresolved` both stay out of that denominator, and why an empty
resolved count must not be misread as a rate of 0.0 or 1.0.

**41/75 and `missing_outline`'s "≥41" are the same signal, not two independent
routes to it — verified, not assumed.** `docs/24` §4 flagged "≥41 of 75" as
`[UNVERIFIED]`, sourced from a `missing_outline` counter printed to console at
iteration 15 and never captured in any logged artefact (`events.jsonl` records the
*code* that computes and prints it, at `runs/.../s42.../events.jsonl` iteration 15-16,
but not its stdout). Reading that code shows *why* it cannot be independent: every name
in `missing_outline` is immediately re-generated with `gen_no_source_prompt` — the exact
zero-source template this module's `_classify_call` calls `ungrounded` — and the result
unconditionally overwrites `explanations[name]`, with no further regeneration round
after. So `missing_outline`'s members and this module's `ungrounded` concepts are the
same set by construction, not two measurements that happen to agree. Confirmed
directly against the seed-42 trajectory: exactly 41 sub-calls match the zero-source
template (no `SOURCE:` marker, `input_tokens < 500`), they name exactly 41 distinct
concepts, and **every one of those 41 calls is the last call in the trajectory for its
concept** (0 of 41 superseded by a later attempt) — the precise shape a
`missing_outline`-driven, never-revisited fill-in pass would produce. The number 41
should be read as *the `[UNVERIFIED]` figure now confirmed reproducible from committed
artefacts*, not as two independent detectors landing on the same value by chance.

**mis-sourced: not implemented.** `docs/24` §5 already flags this as possibly
unreachable. For the vanilla arm specifically it is unreachable for two independent
reasons: classifying a sourced concept as drawn from the wrong chapter needs the
concept's *expected* chapter span, which nothing in the vanilla arm's trajectory
records anywhere; and it needs the source text's *actual* chapter of origin, which
`prompt_preview`'s hard 500-character truncation (`vanilla/run.py`
`_log_subcall_detail`) usually cuts before the source text says enough to place it.
Approximating either would be exactly the kind of heuristic `docs/23` §3.3 already
rejected once for a different extraction. Shipped: the first three.

**Only the vanilla arm's trajectory shape is supported here.** MARD's calls.jsonl is
granular per real call rather than aggregated, its prompts are fully logged rather
than truncated, and (the actual finding, once MARD runs existed to check) its Tier 2
prompts never carry a `SOURCE:`-style field at all — a shared `score_run` covering
both shapes would be a false abstraction over two measurements that share nothing but
a name. `eval/groundedness_mard.py` is the MARD-arm scorer `docs/26` §3 asked be
measured "whatever it is" once those runs landed; this module's `score_run` is
unchanged and still vanilla-only, kept re-runnable rather than folded into the new one
(`docs/34` §4).

**See also `docs/32-GROUNDEDNESS_RESULTS_AND_ARCHITECTURAL_INSTABILITY.md`**, which
also records the per-run call-count/delegation-granularity finding this module's data
made visible: three repeats of the same baseline produced three structurally different
self-authored generation strategies, not just three different outputs.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

ConceptStatus = Literal["grounded", "ungrounded", "root_authored", "unresolved"]

# A generating call that embeds real source text is, in every subcall inspected across
# all three logged runs, in the thousands of input tokens (chunk text dominates the
# prompt). A call built with no source at all is a few dozen to a few hundred tokens of
# metadata (concept name, prereqs, module label). The observed gap was 88 tokens
# (no source) versus 21,056+ tokens (source present) — three orders of magnitude, not a
# tuned cutoff with a close margin.
UNGROUNDED_TOKEN_THRESHOLD = 500

_NUMBERED_H2 = re.compile(r"^##\s+\d+\.\s*(\S.*)$", re.MULTILINE)
_PLAIN_H2 = re.compile(r"^##\s+(\S.*)$", re.MULTILINE)
_H3 = re.compile(r"^###\s+(\S.*)$", re.MULTILINE)

# What a generating call's prompt names the concept it is writing, across the two
# templates observed in practice: "## {concept}\nPrereqs: ..." and
# "Concept: {concept}\nModule: ...". Checked in this order; first match wins.
_PROMPT_CONCEPT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^##\s+(.+)$", re.MULTILINE),
    re.compile(r"^Concept:\s*(.+)$", re.MULTILINE),
)

_SOURCE_MARKER = re.compile(r"SOURCE:\s*\n*(.*)", re.DOTALL)


def extract_concepts(answer_markdown: str) -> list[str]:
    """Concept titles at whichever heading level the study guide actually used.

    Deliberately re-derives `vanilla.run._count_concepts`'s level-selection logic
    (numbered `##`, plain `##`, or `###` — whichever is most numerous) rather than
    importing that private helper: it returns a count and this needs titles, and
    that function's docstring explains why the level is not fixed across runs (a
    real run nested concepts one level deeper than another). Four lines of
    duplicated regex is cheaper than reshaping a frozen module's contract for a
    second, differently-shaped caller.
    """
    numbered_h2 = [m.strip() for m in _NUMBERED_H2.findall(answer_markdown)]
    plain_h2 = [m.strip() for m in _PLAIN_H2.findall(answer_markdown)]
    h3 = [m.strip() for m in _H3.findall(answer_markdown)]
    return max((numbered_h2, plain_h2, h3), key=len)


def _concept_in_prompt(prompt_preview: str) -> str | None:
    for pattern in _PROMPT_CONCEPT_PATTERNS:
        match = pattern.search(prompt_preview)
        if match:
            return match.group(1).strip()
    return None


def _classify_call(call: dict[str, Any]) -> Literal["grounded", "ungrounded"]:
    """grounded/ungrounded for one already-resolved generating call.

    Two independent signals, because `prompt_preview` is a hard 500-character
    truncation of the real prompt: a `SOURCE:` marker near the truncation boundary
    can read as empty in the preview while real source text follows past character
    500. `input_tokens` is never truncated, so where the text signal says "empty"
    but the token count is far above what a source-free prompt costs, the token
    count wins — it is the signal immune to truncation.
    """
    match = _SOURCE_MARKER.search(call["prompt_preview"])
    if match and match.group(1).strip():
        return "grounded"
    return "ungrounded" if call["input_tokens"] < UNGROUNDED_TOKEN_THRESHOLD else "grounded"


@dataclass(frozen=True)
class ConceptResult:
    concept: str
    status: ConceptStatus
    regenerated: bool
    """True when >=1 prior attempt for this concept was discarded before the one
    classified — i.e. more than one sub-call in the trajectory named this concept."""
    attempt_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "concept": self.concept,
            "status": self.status,
            "regenerated": self.regenerated,
            "attempt_count": self.attempt_count,
        }


def classify_concepts(concepts: list[str], subcalls: list[dict[str, Any]]) -> list[ConceptResult]:
    """Resolve each concept to its generating call (the last sub-call naming it, in
    trajectory order — `docs/24` §1's "attempt 3 is the version in the published
    guide") and classify it.

    A concept with no matching sub-call is `root_authored` whenever the run had *any*
    sub-calls at all — the root wrote it directly, but from a digest it built out of
    calls that did happen and can themselves be checked (`score_run`'s
    `root_authored_context`). Only a run with zero sub-calls in its whole trajectory —
    nothing to attribute the root's writing to, grounded or otherwise — falls back to
    `unresolved`. See the module docstring for why this is not a guessed
    grounded/ungrounded.
    """
    by_concept: dict[str, list[dict[str, Any]]] = {}
    for call in subcalls:
        name = _concept_in_prompt(call["prompt_preview"])
        if name is not None:
            by_concept.setdefault(name, []).append(call)

    fallback_status: ConceptStatus = "root_authored" if subcalls else "unresolved"

    results = []
    for concept in concepts:
        attempts = by_concept.get(concept, [])
        if not attempts:
            results.append(ConceptResult(concept, fallback_status, False, 0))
            continue
        status = _classify_call(attempts[-1])
        results.append(ConceptResult(concept, status, len(attempts) > 1, len(attempts)))
    return results


def _background_groundedness(subcalls: list[dict[str, Any]]) -> dict[str, int] | None:
    """Classify the sub-calls that don't name any concept — the material a
    `root_authored` concept's explanation was, at best, digested from.

    `None` when there is nothing to classify: either the run has no sub-calls at all
    (concepts fall back to `unresolved`, not `root_authored`), or every sub-call named
    a concept (nothing was left over to attribute `root_authored` writing to, because
    there is no `root_authored` writing in that run). This is the evidence behind the
    module docstring's "grounded at one remove" claim — computed per run, not assumed:
    for seeds 11 and 23 it comes back `{"grounded": 14, "ungrounded": 0}` and
    `{"grounded": 29, "ungrounded": 0}` respectively.
    """
    background = [call for call in subcalls if _concept_in_prompt(call["prompt_preview"]) is None]
    if not background:
        return None
    counts = Counter(_classify_call(call) for call in background)
    return {"grounded": counts["grounded"], "ungrounded": counts["ungrounded"]}


@dataclass(frozen=True)
class GroundednessReport:
    run_id: str
    total_concepts: int
    resolved: int
    """Concepts with >=1 matching per-concept generating call — `grounded` plus
    `ungrounded`. Deliberately excludes `root_authored`: that status has evidence
    (`root_authored_context`) but not a per-concept generating call, so folding it in
    here would blur two different strengths of evidence into one number.
    `groundedness_rate` is relative to this, not to `total_concepts`."""
    root_authored: int
    """Concepts with no per-concept generating call, written by the root itself from
    its own digest of the document. See `root_authored_context` for whether that
    digest was itself grounded, per run."""
    root_authored_context: dict[str, int] | None
    """`{"grounded": n, "ungrounded": m}` over this run's sub-calls that named no
    concept — the material any `root_authored` concept was written from, at one
    remove. `None` when nothing in the run supports or undermines that claim (no such
    sub-calls exist). Always check this before reading `root_authored` as "grounded";
    it is only as strong as this field says it is, run by run."""
    unresolved: int
    """Concepts with no per-concept call AND no sub-calls anywhere in the run to
    attribute root-authored writing to. Kept separate from `root_authored` for
    exactly this reason — see the module docstring."""
    grounded: int
    ungrounded: int
    regenerated: int
    groundedness_rate: float | None
    """`grounded / resolved`. `None` when `resolved == 0` — an empty denominator is
    not a rate of zero, and reporting one would assert every concept in the run was
    ungrounded when in fact none of them could be checked at all."""
    mis_sourced: None = None
    """Always `None`. Not implemented — see the module docstring's "mis-sourced: not
    implemented" section for why, reported as a field rather than an omission so a
    reader of the JSON sees the gap rather than inferring a zero."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "total_concepts": self.total_concepts,
            "resolved": self.resolved,
            "root_authored": self.root_authored,
            "root_authored_context": self.root_authored_context,
            "unresolved": self.unresolved,
            "grounded": self.grounded,
            "ungrounded": self.ungrounded,
            "regenerated": self.regenerated,
            "groundedness_rate": self.groundedness_rate,
            "mis_sourced": self.mis_sourced,
        }


def load_events(run_dir: Path) -> list[dict[str, Any]]:
    with (run_dir / "events.jsonl").open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def score_run(run_dir: Path) -> GroundednessReport:
    """Score one vanilla-RLM run directory. See module docstring for scope — this
    does not yet handle a MARD-arm run directory."""
    events = load_events(run_dir)
    subcalls = [event for event in events if event.get("kind") == "vanilla_subcall_detail"]
    answer = (run_dir / "artefacts" / "vanilla_answer.md").read_text(encoding="utf-8")
    concepts = extract_concepts(answer)

    results = classify_concepts(concepts, subcalls)
    counts = Counter(result.status for result in results)
    resolved = counts["grounded"] + counts["ungrounded"]
    regenerated = sum(1 for result in results if result.regenerated)

    return GroundednessReport(
        run_id=run_dir.name,
        total_concepts=len(concepts),
        resolved=resolved,
        root_authored=counts["root_authored"],
        root_authored_context=_background_groundedness(subcalls),
        unresolved=counts["unresolved"],
        grounded=counts["grounded"],
        ungrounded=counts["ungrounded"],
        regenerated=regenerated,
        groundedness_rate=(counts["grounded"] / resolved) if resolved else None,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score groundedness for one or more logged runs (docs/26 Task B)."
    )
    parser.add_argument("run_dirs", nargs="+", type=Path)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write the combined report as JSON here (default: stdout only).",
    )
    args = parser.parse_args()

    reports = [score_run(run_dir).to_dict() for run_dir in args.run_dirs]
    payload = json.dumps(reports, ensure_ascii=False, indent=2)
    print(payload)
    if args.out is not None:
        args.out.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
