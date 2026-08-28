"""Tests for the groundedness detector (docs/26 Task B).

Synthetic-call tests pin the classification rules in isolation. The real-run tests
are the ones that matter most: `docs/26` §3 requires the detector to reproduce
`docs/24` §1's hand-traced finding on the real seed-42 run before it can be trusted
on anything nobody has read by hand, and to be honest about what it finds on seeds 11
and 23 rather than forcing a comparison the trajectories don't support.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from eval.groundedness import (
    UNGROUNDED_TOKEN_THRESHOLD,
    _concept_in_prompt,
    classify_concepts,
    extract_concepts,
    load_events,
    score_run,
)

RUNS_DIR = Path(__file__).resolve().parents[1] / "runs"


def _call(prompt_preview: str, input_tokens: int) -> dict[str, Any]:
    return {"prompt_preview": prompt_preview, "input_tokens": input_tokens}


def _run_dir(seed_marker: str) -> Path | None:
    matches = sorted(RUNS_DIR.glob(f"*__vanilla_rlm__introcs__{seed_marker}__*"))
    return matches[0] if matches else None


# ---- extract_concepts -------------------------------------------------------------


def test_extract_concepts_picks_h3_when_it_outnumbers_h2() -> None:
    markdown = (
        "## Chapter 1\n\n### Alpha\nbody\n\n### Beta\nbody\n\n## Chapter 2\n\n### Gamma\nbody\n"
    )
    assert extract_concepts(markdown) == ["Alpha", "Beta", "Gamma"]


def test_extract_concepts_picks_plain_h2_when_no_h3_exists() -> None:
    markdown = "## Alpha\nbody\n\n## Beta\nbody\n\n## Gamma\nbody\n"
    assert extract_concepts(markdown) == ["Alpha", "Beta", "Gamma"]


def test_extract_concepts_prefers_numbered_h2_titles_on_a_tie_with_plain_h2() -> None:
    # Every numbered-h2 line also matches the plain-h2 pattern, so the two counts can
    # only ever tie (when all plain h2s are numbered) or have plain_h2 win, never the
    # reverse. On a tie, `max` (stable, first-wins) returns numbered_h2 because it
    # comes first in the tuple — the cleaner titles, without the "N. " prefix.
    markdown = "## 1. Alpha\nbody\n\n## 2. Beta\nbody\n"
    assert extract_concepts(markdown) == ["Alpha", "Beta"]


# ---- classify_concepts -------------------------------------------------------------


def test_grounded_when_source_marker_has_content() -> None:
    prompt = "## Foo\nPrereqs: None.\n\nSOURCE:\n\nReal chunk text about foo goes here."
    results = classify_concepts(["Foo"], [_call(prompt, 12000)])
    assert results[0].status == "grounded"


def test_ungrounded_when_source_marker_is_empty_and_tokens_are_low() -> None:
    prompt = "## Foo\nPrereqs: None.\n\nSOURCE:\n\n"
    results = classify_concepts(["Foo"], [_call(prompt, 90)])
    assert results[0].status == "ungrounded"


def test_ungrounded_when_no_source_marker_at_all() -> None:
    prompt = "Concept: Foo\nModule: 1. Intro\n\nWrite: ..."
    results = classify_concepts(["Foo"], [_call(prompt, 88)])
    assert results[0].status == "ungrounded"


def test_grounded_when_no_source_marker_but_tokens_are_high() -> None:
    # No labelled SOURCE field at all, but the token count implies real chunk text
    # elsewhere in the (truncated-in-preview) prompt — the seed-42 "Related
    # extracted subtopics" template, 21k+ tokens with no SOURCE: label.
    prompt = "Concept: Foo\nModule: 1. Intro\nRelated extracted subtopics: [...]"
    results = classify_concepts(["Foo"], [_call(prompt, 21000)])
    assert results[0].status == "grounded"


def test_empty_source_but_high_tokens_trusts_token_count_over_truncated_preview() -> None:
    # SOURCE: appears empty within the 500-char preview, but a large token count
    # means real source text exists past the truncation point.
    prompt = "## Foo\nPrereqs: None.\n\nSOURCE:\n\n"
    results = classify_concepts(["Foo"], [_call(prompt, UNGROUNDED_TOKEN_THRESHOLD + 1)])
    assert results[0].status == "grounded"


def test_root_authored_when_no_call_names_the_concept_but_the_run_had_subcalls() -> None:
    # A subcall happened in this run (for "Bar"), just not for "Foo" — the root wrote
    # "Foo" itself, from whatever digest those other calls built. That is
    # `root_authored`, not `unresolved`: there is *something* to check it against.
    results = classify_concepts(["Foo"], [_call("Concept: Bar\n", 50)])
    assert results[0].status == "root_authored"
    assert results[0].attempt_count == 0


def test_unresolved_when_the_run_had_no_subcalls_at_all() -> None:
    # Nothing happened in this run's trajectory to attribute the writing to, grounded
    # or otherwise — the only case that stays `unresolved`.
    results = classify_concepts(["Foo"], [])
    assert results[0].status == "unresolved"
    assert results[0].attempt_count == 0


def test_regenerated_true_with_multiple_attempts_classified_by_the_last() -> None:
    attempt_1 = _call("## Foo\nSOURCE:\n\nreal source text here", 15000)
    attempt_2 = _call("Concept: Foo\nModule: 1\n", 90)  # discarded, then...
    calls = [attempt_1, attempt_2]
    results = classify_concepts(["Foo"], calls)
    assert results[0].regenerated is True
    assert results[0].attempt_count == 2
    assert results[0].status == "ungrounded"  # classified by the LAST attempt


def test_single_attempt_is_not_regenerated() -> None:
    results = classify_concepts(["Foo"], [_call("Concept: Foo\n", 90)])
    assert results[0].regenerated is False
    assert results[0].attempt_count == 1


# ---- score_run against the real logged runs ----------------------------------------


@pytest.mark.skipif(not RUNS_DIR.exists(), reason="runs/ not present")
class TestRealRuns:
    def test_seed_42_reproduces_the_docs_24_hand_trace(self) -> None:
        """docs/24 §1: seed 42's 'Trees and balanced trees' was published ungrounded,
        and docs/24 §4 flags '>=41 of 75' as UNVERIFIED, sourced from an intermediate
        counter, not a count of the final artefact. This is that count, computed for
        real. It should reproduce ungroundedness generally (not just for the one
        hand-verified concept) and resolve every concept, since seed 42 delegates
        concept-writing per concept unlike seeds 11/23 (see module docstring)."""
        run_dir = _run_dir("s42")
        assert run_dir is not None, "seed 42 run not found under runs/"
        report = score_run(run_dir)

        assert report.total_concepts == 75
        assert report.resolved == 75  # every concept in this run has a per-concept call
        assert report.unresolved == 0
        assert report.ungrounded > 0
        assert report.groundedness_rate is not None
        assert report.groundedness_rate < 1.0

        events = load_events(run_dir)
        subcalls = [e for e in events if e.get("kind") == "vanilla_subcall_detail"]
        tree_calls = [
            c
            for c in subcalls
            if "Trees and balanced trees" in c["prompt_preview"]
            and c["input_tokens"] < UNGROUNDED_TOKEN_THRESHOLD
        ]
        assert tree_calls, "the hand-traced ungrounded attempt should be in this run's trajectory"

    def test_ungrounded_count_is_exactly_the_missing_outline_batch(self) -> None:
        """`docs/24` §4's '>=41 of 75' came from a `missing_outline` counter printed
        to console at iteration 15 and never captured in any logged artefact — only
        the *code* that computes and prints it survives, in this run's
        `vanilla_root_iteration` events. That code (a) builds `missing_outline` from
        concepts with no successfully-parsed explanation, then (b) immediately
        regenerates every one of them with the zero-source template and overwrites
        `explanations` unconditionally, with no further round after. So this
        detector's `ungrounded` count is not a second, independent route to '41' — it
        is the same batch, found a different way. Verified structurally rather than
        assumed: every zero-source-template call is the *last* trajectory entry for
        its concept (none get superseded by a later, better-sourced attempt), which
        is exactly the shape a never-revisited fill-in batch produces.
        """
        run_dir = _run_dir("s42")
        assert run_dir is not None, "seed 42 run not found under runs/"
        events = load_events(run_dir)
        subcalls = [e for e in events if e.get("kind") == "vanilla_subcall_detail"]

        zero_source_calls = [
            (i, name)
            for i, call in enumerate(subcalls)
            if (name := _concept_in_prompt(call["prompt_preview"])) is not None
            and "SOURCE:" not in call["prompt_preview"]
            and call["input_tokens"] < UNGROUNDED_TOKEN_THRESHOLD
        ]
        assert len(zero_source_calls) == 41
        assert len({name for _, name in zero_source_calls}) == 41  # one call per concept

        last_index_by_concept: dict[str, int] = {}
        for i, call in enumerate(subcalls):
            name = _concept_in_prompt(call["prompt_preview"])
            if name is not None:
                last_index_by_concept[name] = i
        superseded = [name for i, name in zero_source_calls if last_index_by_concept[name] != i]
        assert superseded == []

        report = score_run(run_dir)
        assert report.ungrounded == 41

    def test_seeds_11_and_23_are_root_authored_from_a_grounded_digest(self) -> None:
        """The real finding, not a detector defect: seeds 11 and 23 delegate concept
        writing at chapter granularity only (14/29 chapter-level sub-calls for
        156/190 concepts respectively) and the root writes every explanation itself.
        Nothing in their trajectories names an individual concept in a sub-call
        prompt, so every concept is `root_authored` — reported with the evidence for
        "grounded at one remove" attached (`root_authored_context`), not folded into
        `grounded` or `ungrounded` outright. Confirmed by manually reading every
        sub-call's prompt_preview in both runs before writing this assertion.
        """
        for marker, expected_total in (("s11", 156), ("s23", 190)):
            run_dir = _run_dir(marker)
            assert run_dir is not None, f"seed {marker} run not found under runs/"
            report = score_run(run_dir)
            assert report.total_concepts == expected_total
            assert report.root_authored == expected_total
            assert report.unresolved == 0
            assert report.resolved == 0
            assert report.groundedness_rate is None
            assert report.root_authored_context is not None
            assert report.root_authored_context["ungrounded"] == 0
            assert report.root_authored_context["grounded"] > 0

    def test_groundedness_rate_is_not_naively_comparable_across_these_three_seeds(self) -> None:
        """Documents, rather than asserts past, the literal reading of docs/26 §3's
        validation gate ('seed 42 should show a markedly lower rate than 11 and
        23'): that comparison presumes all three runs have a resolvable rate. They
        do not — seeds 11 and 23 resolve zero concepts each (previous test), so
        their rate is `None`, not a number seed 42's rate could be lower than. This
        is a structural fact about how each run's own generated code chose to
        delegate work, verified by hand across all three trajectories, not a
        detector bug to be tuned away."""
        run_42, run_11, run_23 = _run_dir("s42"), _run_dir("s11"), _run_dir("s23")
        assert run_42 is not None and run_11 is not None and run_23 is not None
        s42 = score_run(run_42)
        s11 = score_run(run_11)
        s23 = score_run(run_23)
        assert s42.groundedness_rate is not None
        assert s11.groundedness_rate is None
        assert s23.groundedness_rate is None
