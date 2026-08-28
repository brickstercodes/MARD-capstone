"""Run the vanilla-RLM control on Zhang_RLM's own root-REPL-loop architecture.

`docs/18-W3_PROVIDER_SWITCH.md` §4.2 (reversed 27 Aug 2026, on Anugrah's direct
instruction — the prior CLOSED decision named `replm` instead; both are recorded,
not erased): both arms run on `FalseAdvertising/Zhang_RLM @ 62acf7b`, vendored at
`.vendor/rlm`. The vanilla-RLM control is Zhang's own `rlm.core.rlm.RLM`, not
MARD's own pipeline with `Envelope.stripped()`.

Fixed at `max_depth=1` — Zhang's own default and the base paper's primary reported
condition (root RLM + flat sub-calls). Not exposed as a sweep knob: this is the
control's specification, not a depth-ablation parameter.

Root/sub-call model split uses Zhang's `other_backends`/`other_backend_kwargs`
(`rlm/core/rlm.py` `_subcall`) — the library's supported way to give sub-calls a
different default model than the root. There is no separate `sub_model` constructor
parameter; a per-call `model=` override inside the REPL's own `rlm_query(...)` calls
would take precedence if the root chose to use it, but nothing in this wrapper
prompts it to.

Reads `corpus/<document_id>/document.txt` only — never a PDF, never
`document.jsonl`, never `outline.json` (`docs/16` verification-debt item 2, CLOSED).
Splits on `[[page:N]]` markers using the same regex Zhang_RLM's own bundled
`run_file.py` example uses, and asserts more than one chunk results — a silent
collapse to `[text]` would turn this arm into an unlabelled full-context baseline.

**`on_subcall_start`/`on_subcall_complete` never fire at `max_depth=1`, confirmed by
a real run's empty `events.jsonl` (28 Aug 2026), not by reading the source alone.**
`_subcall()` (`rlm/core/rlm.py`) takes an early-return branch whenever
`next_depth >= max_depth` — true for every sub-call the root issues at our fixed
depth, since `next_depth` is always `1` — and that branch calls the client directly
and returns before reaching either callback later in the function. They are still
wired here in case a future depth sweep needs them; at `max_depth=1` they are dead
weight, not a bug in this wrapper.

**This does not cost the measurement, only the callback.** `_llm_query`,
`_llm_query_batched`, `_rlm_query` and `_rlm_query_batched`
(`rlm/environments/local_repl.py`) all append the real `RLMChatCompletion` they get
back — real prompt, real response, its own `usage_summary`, its own
`execution_time` — to `self._pending_llm_calls`, which surfaces as
`REPLResult.rlm_calls` on every code block, nested inside the `RLMLogger` trajectory
this wrapper already attaches. `_walk_subcalls`/`_log_subcall_detail` below read that
instead of listening for the dead callbacks, which is where `docs/30` §1's "both max
and Σ over sub-calls" actually comes from — real per-call timing, not a placeholder.
Cost/token totals still come from `usage_summary` alone (see `_log_usage`), never
from this granular walk, so a gap in trajectory capture can never silently
under-count real spend.
"""

from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

from rlm.core.rlm import RLM
from rlm.core.types import RLMChatCompletion
from rlm.logger.rlm_logger import RLMLogger
from rlm.utils.exceptions import (
    BudgetExceededError,
    CancellationError,
    ErrorThresholdExceededError,
    TimeoutExceededError,
    TokenLimitExceededError,
)

from ingest.manifest import verify_or_raise
from runlog import RunLogger
from vanilla.openai_logging_bridge import rate_limit_visibility

# The base paper's primary reported condition — see module docstring.
VANILLA_MAX_DEPTH = 1

_VENDOR_RLM_DIR = Path(__file__).resolve().parents[1] / ".vendor" / "rlm"

# Matches ingest/cli.py's PAGE_MARKER = "[[page:{page}]]", and the identical regex
# in Zhang_RLM's own vendored .vendor/rlm/run_file.py (PAGE_MARKER_RE) — reused
# rather than re-derived, per the brief's "do not re-invent chunking" instruction.
_PAGE_MARKER_RE = re.compile(r"\[\[page:\d+\]\]")

# Frozen 27 Aug 2026 (docs/21-HANDOFF_CLOSE_VANILLA_ARM.md §3.1, Anugrah's decision).
# This string is paper content. Do not paraphrase it, and do not change it outside a
# decision to re-run the whole matrix (CONTEXT.md §3.4) — every word here is
# load-bearing, per docs/21 §3.1's own annotation of which three phrases matter.
FROZEN_STUDY_GUIDE_PROMPT = (
    "Using the textbook available in `context`, write a study guide for a learner "
    "meeting this material for the first time. Identify the concepts the textbook "
    "teaches and, for each one, write an explanation the learner can study from. "
    "Order the guide so that a concept is explained only after anything it depends "
    "on has been explained. Output the study guide itself, with no commentary about "
    "your process."
)

_LIMIT_EXCEEDED_ERRORS = (
    BudgetExceededError,
    TimeoutExceededError,
    TokenLimitExceededError,
    ErrorThresholdExceededError,
    CancellationError,
)


def zhang_rlm_fork_sha(vendor_dir: Path = _VENDOR_RLM_DIR) -> str | None:
    """The fork's own commit, not the outer MARD repo's — `ConfigSnapshot.capture()`'s
    `git_commit` field runs `git rev-parse HEAD` in the MARD repo and would silently
    describe the wrong commit for this (docs/18 §5.3's requirement, carried over)."""
    try:
        result = subprocess.run(
            ["git", "-C", str(vendor_dir), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def split_pages(document_text: str) -> list[str]:
    """Split on `[[page:N]]` markers into the per-page chunks Zhang_RLM's `RLM.completion`
    accepts as `prompt=list[str]`. Raises if fewer than two non-empty chunks result —
    trap #3: a silent single-chunk fallback makes this arm a full-context baseline
    wearing an RLM label, and that must fail loudly, not degrade quietly."""
    pages = [p for p in _PAGE_MARKER_RE.split(document_text) if p.strip()]
    if len(pages) <= 1:
        raise ValueError(
            f"Expected multiple [[page:N]]-delimited chunks, got {len(pages)}. "
            "This document was not ingested through ingest/cli.py, or its page "
            "markers were stripped — refusing to silently run as a full-context "
            "baseline."
        )
    return pages


def run_vanilla_rlm(
    corpus_dir: Path,
    document_id: str,
    *,
    root_model: str,
    sub_model: str,
    logger: RunLogger,
    task_prompt: str = FROZEN_STUDY_GUIDE_PROMPT,
    max_iterations: int = 30,
    max_concurrent_subcalls: int = 4,
    max_retries: int = 5,
    sampling_args: dict[str, Any] | None = None,
    sub_sampling_args: dict[str, Any] | None = None,
    verbose: bool = False,
) -> RLMChatCompletion:
    """Run one vanilla-RLM generation and log it under `logger`.

    `task_prompt` defaults to the frozen `FROZEN_STUDY_GUIDE_PROMPT`; a measured run
    must never override it (the override exists only so tests can exercise this
    function without needing the full corpus). Passed as Zhang's `root_prompt`, never
    folded into the page content — the same root_prompt-is-a-small-fixed-string
    boundary MARD's own envelope must never cross (`docs/21` trap #2).

    Never sets `temperature` in `sampling_args`/`sub_sampling_args`: Zhang's
    `_normalize_sampling_args` (`rlm/clients/openai.py`) does not strip it for
    reasoning-model families the way `replm`'s adapter did, so it is this caller's
    job to never put one there, not the library's job to ignore one.

    `verbose` only toggles Zhang's own `VerbosePrinter` console output
    (`rlm/core/rlm.py`: `self.verbose = VerbosePrinter(enabled=verbose)`, read
    directly to confirm it drives printing only, nothing else) — it has no effect
    on what gets logged, computed, or spent. Safe to leave on for a real run without
    touching measurement fidelity.
    """
    verify_or_raise(corpus_dir / document_id)
    document_text = (corpus_dir / document_id / "document.txt").read_text(encoding="utf-8")
    pages = split_pages(document_text)

    return _run_vanilla_rlm_pages(
        pages,
        task_prompt,
        document_id=document_id,
        task_prompt_is_frozen=task_prompt == FROZEN_STUDY_GUIDE_PROMPT,
        root_model=root_model,
        sub_model=sub_model,
        logger=logger,
        max_iterations=max_iterations,
        max_concurrent_subcalls=max_concurrent_subcalls,
        max_retries=max_retries,
        sampling_args=sampling_args,
        sub_sampling_args=sub_sampling_args,
        verbose=verbose,
    )


def run_vanilla_rlm_oolong_task(
    context_lines: list[str],
    task: dict[str, Any],
    *,
    root_model: str,
    sub_model: str,
    logger: RunLogger,
    max_iterations: int = 30,
    max_concurrent_subcalls: int = 4,
    max_retries: int = 5,
    sampling_args: dict[str, Any] | None = None,
    sub_sampling_args: dict[str, Any] | None = None,
    verbose: bool = False,
) -> RLMChatCompletion:
    """Run one vanilla-RLM generation over an OOLONG benchmark task — the harness-check
    exception `docs/42` §1.4 calls for, not a bypass of the study-guide freeze above.

    `run_vanilla_rlm` refuses to run without going through `ingest/manifest.py`'s
    provenance check and defaults `task_prompt` to the frozen study-guide instruction
    because, for that measured run, the prompt is part of what is being measured
    (`docs/21` trap #2 — the same boundary applies here: `root_prompt` must still never
    fold in page content). Neither applies to OOLONG: it is not an ingested corpus
    document (there is nothing for `ingest/manifest.py` to verify), and the per-task
    question genuinely *is* the correct root_prompt — OOLONG's own base-paper harness
    (`.vendor/rlm/training/environments/oolong/oolong/env.py`) uses each task's own
    question as its `root_prompt` too. A caller cannot reach this function by accident
    while trying to run a measured study-guide generation — it takes an OOLONG task
    dict, not a `document_id`.

    `context_lines` is the shared 131K-token OOLONG context window, split one line per
    list element (matching the benchmark's own framing: "the following lines contain
    N general-knowledge questions, one per line") — never re-chunked into
    `[[page:N]]`-marked pages, because this context was never ingested through
    `ingest/cli.py` and has no such markers.
    """
    return _run_vanilla_rlm_pages(
        context_lines,
        task["question"],
        document_id=f"oolong_trec_coarse_ctxwin_{task['context_window_id']}",
        task_prompt_is_frozen=False,
        root_model=root_model,
        sub_model=sub_model,
        logger=logger,
        max_iterations=max_iterations,
        max_concurrent_subcalls=max_concurrent_subcalls,
        max_retries=max_retries,
        sampling_args=sampling_args,
        sub_sampling_args=sub_sampling_args,
        verbose=verbose,
    )


def _run_vanilla_rlm_pages(
    pages: list[str],
    task_prompt: str,
    *,
    document_id: str,
    task_prompt_is_frozen: bool,
    root_model: str,
    sub_model: str,
    logger: RunLogger,
    max_iterations: int,
    max_concurrent_subcalls: int,
    max_retries: int,
    sampling_args: dict[str, Any] | None,
    sub_sampling_args: dict[str, Any] | None,
    verbose: bool,
) -> RLMChatCompletion:
    fork_sha = zhang_rlm_fork_sha()
    logger.log_event(
        "vanilla_config",
        {
            "rlm_fork_sha": fork_sha,
            "root_model": root_model,
            "sub_model": sub_model,
            "max_depth": VANILLA_MAX_DEPTH,
            "max_iterations": max_iterations,
            "max_concurrent_subcalls": max_concurrent_subcalls,
            "max_retries": max_retries,
            "sampling_args": sampling_args or {},
            "sub_sampling_args": sub_sampling_args or {},
            "page_count": len(pages),
            "document_id": document_id,
            "task_prompt_is_frozen": task_prompt_is_frozen,
            "subcall_callbacks_reachable": VANILLA_MAX_DEPTH >= 2,
        },
    )

    # Wired for a hypothetical max_depth>=2 config; at our fixed max_depth=1 these
    # never fire (module docstring) — no vanilla_subcall_start/complete events
    # appear in this run's events.jsonl. Real per-sub-call detail (count, timing,
    # tokens) comes from _log_subcall_detail's trajectory walk instead, after the
    # run completes; this callback wiring is not what that data depends on.
    def on_subcall_start(depth: int, model: str, prompt_preview: str) -> None:
        logger.log_event(
            "vanilla_subcall_start",
            {"depth": depth, "model": model, "prompt_preview": prompt_preview},
        )

    def on_subcall_complete(depth: int, model: str, duration: float, error: str | None) -> None:
        logger.log_event(
            "vanilla_subcall_complete",
            {"depth": depth, "model": model, "duration_s": duration, "error": error},
        )

    trajectory_logger = RLMLogger()

    rlm_instance = RLM(
        backend="openai",
        backend_kwargs={"model_name": root_model, "max_retries": max_retries},
        other_backends=["openai"],
        other_backend_kwargs=[{"model_name": sub_model, "max_retries": max_retries}],
        max_depth=VANILLA_MAX_DEPTH,
        max_iterations=max_iterations,
        max_concurrent_subcalls=max_concurrent_subcalls,
        sampling_args=sampling_args,
        sub_sampling_args=sub_sampling_args,
        on_subcall_start=on_subcall_start,
        on_subcall_complete=on_subcall_complete,
        logger=trajectory_logger,
        verbose=verbose,
    )

    try:
        with rate_limit_visibility(logger):
            response = rlm_instance.completion(prompt=pages, root_prompt=task_prompt)
    except _LIMIT_EXCEEDED_ERRORS as err:
        # A failed run, not a degraded one — docs/18 §5.6 / the brief's trap #6.
        # RunLogger's context manager (runlog/run.py __exit__) turns this re-raise
        # into status="failed" with the traceback; nothing else to do here.
        logger.log_event(
            "vanilla_limit_exceeded",
            {"error_type": type(err).__name__, "error": str(err)},
        )
        raise
    finally:
        rlm_instance.close()

    _log_root_trajectory(logger, trajectory_logger, max_iterations=max_iterations)
    _log_usage(logger, response, root_model=root_model)
    subcall_detail = _log_subcall_detail(logger, trajectory_logger.get_trajectory())
    _reconcile_usage(logger, response, subcall_detail)

    logger.log_event(
        "vanilla_run_summary",
        {
            "execution_time_s": response.execution_time,
            "subcall_count": subcall_detail["subcall_count"],
            "subcall_wall_clock_max_s": subcall_detail["subcall_wall_clock_max_s"],
            "subcall_wall_clock_sum_s": subcall_detail["subcall_wall_clock_sum_s"],
            "concept_count": _count_concepts(response.response),
            "page_count": len(pages),
            "usage_summary": response.usage_summary.to_dict(),
        },
    )
    logger.save_artefact("vanilla_answer.md", response.response)
    return response


def _log_root_trajectory(
    logger: RunLogger, trajectory_logger: RLMLogger, *, max_iterations: int
) -> None:
    """Log each root iteration's real prompt/response text (available from Zhang's
    own `RLMLogger`, which has no per-iteration token counts — those only exist in
    the run-level `usage_summary` — so this is qualitative trajectory data, not
    what feeds cost accounting) and flag truncation explicitly.

    Zhang_RLM does not raise when `max_iterations` is exhausted — `RLM.completion`
    (`rlm/core/rlm.py`) falls through to `_default_answer()` and returns a normal
    `RLMChatCompletion`, indistinguishable from a natural stop unless the iteration
    count is checked directly. "Truncation is a failure, not a low score" (brief
    trap #6) has no exception to hang off here; it must be computed.
    """
    trajectory = trajectory_logger.get_trajectory() or {"iterations": []}
    iterations = trajectory["iterations"]
    for entry in iterations:
        logger.log_event(
            "vanilla_root_iteration",
            {
                "iteration": entry.get("iteration"),
                "response": entry.get("response"),
                "final_answer": entry.get("final_answer"),
                "iteration_time": entry.get("iteration_time"),
            },
        )

    natural_stop = any(it.get("final_answer") for it in iterations)
    if len(iterations) >= max_iterations and not natural_stop:
        logger.log_event(
            "vanilla_truncated",
            {
                "max_iterations": max_iterations,
                "iterations_run": len(iterations),
                "note": (
                    "Hit max_iterations without a natural final_answer; the response "
                    "returned is Zhang_RLM's forced _default_answer(), not a genuine "
                    "completion. Report this, do not score it as a low-quality answer."
                ),
            },
        )


def _log_usage(logger: RunLogger, response: RLMChatCompletion, *, root_model: str) -> None:
    """One aggregate `log_call` per model from `usage_summary` — this, and only this,
    is what feeds `RunLogger.totals()`'s `RateCard` pricing (`docs/30` §1's
    tokens/cost fields). Deliberately never derived from `_log_subcall_detail`'s
    per-call walk below, even though that walk usually reconciles exactly: a gap in
    trajectory capture (e.g. a call that reaches `usage_summary` through a code path
    that doesn't append to `_pending_llm_calls`) must never silently under-count real
    spend. `prompt`/`response` are labelled placeholders, not a literal single call's
    transcript — the real per-root-iteration text is in `_log_root_trajectory`'s
    events, and real per-subcall text in `_log_subcall_detail`'s.
    """
    for model, usage in response.usage_summary.model_usage_summaries.items():
        role = "root" if model == root_model else "tier2_subcall"
        logger.log_call(
            role=role,
            model=model,
            prompt=(
                f"<aggregate of {usage.total_calls} {role} call(s) to {model}; "
                "Zhang_RLM's usage_summary does not expose individual call prompts>"
            ),
            response=response.response if role == "root" else "<see vanilla_subcall_detail events>",
            input_tokens=usage.total_input_tokens,
            output_tokens=usage.total_output_tokens,
            depth=0 if role == "root" else 1,
            metadata={"total_calls": usage.total_calls, "reported_cost_usd": usage.total_cost},
        )


def _walk_subcalls(trajectory: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Flatten every individual sub-call recorded across all root iterations' code
    blocks — `llm_query`/`llm_query_batched`/`rlm_query`/`rlm_query_batched` alike
    (`local_repl.py`: all four append their result to `self._pending_llm_calls`,
    despite the field surfacing as `REPLResult.rlm_calls`). Each entry is a real
    `RLMChatCompletion.to_dict()` with a real, distinct prompt and response, captured
    by `RLMLogger` regardless of whether `on_subcall_start`/`on_subcall_complete`
    ever fire (they don't, at our fixed `max_depth=1` — module docstring).

    **`usage_summary`/`execution_time` are only trustworthy per-call for
    non-batched calls (`llm_query`/`rlm_query`, one prompt at a time).** For a
    batched call (`llm_query_batched`/`rlm_query_batched`, N prompts concurrently),
    `LMHandler._handle_batched` (`rlm/core/lm_handler.py`) calls
    `client.get_last_usage()` once *after* `asyncio.gather()` returns and stamps
    that single, last-writer-wins snapshot onto every entry in the batch —
    `execution_time` is `total_batch_time / N`, an average Zhang's own comment
    labels "approximate per-prompt time." Verified first-hand against a real B1 run
    (`docs/18` §4.2 addendum, second correction) whose 7-prompt batches each logged
    7 byte-identical token counts. `_log_subcall_detail`'s `Σ` recovers the true
    batch total regardless (N × average = total); its `max` does not — see there.
    """
    if not trajectory:
        return []
    calls: list[dict[str, Any]] = []
    for iteration in trajectory.get("iterations", []):
        for block in iteration.get("code_blocks", []):
            result = block.get("result") or {}
            calls.extend(result.get("rlm_calls", []))
    return calls


def _log_subcall_detail(logger: RunLogger, trajectory: dict[str, Any] | None) -> dict[str, Any]:
    """Log real per-sub-call prompt/response/timing/tokens via `log_event` (never
    `log_call` — see `_log_usage`'s docstring for why cost must not depend on this),
    and return the aggregates `docs/30` §1 actually asks for: sub-call count and
    both `max` and `Σ` wall-clock over sub-calls.

    `subcall_wall_clock_sum_s` is a genuine total even across batched calls (see
    `_walk_subcalls`): N copies of `total_batch_time / N` sum back to
    `total_batch_time`. `subcall_wall_clock_max_s` is **not** a true peak
    single-call latency when any batched calls occurred — it is, at best, the
    largest batch's *average* per-prompt time, since Zhang's batched path never
    records true individual timings. State this precisely wherever it is quoted.
    """
    calls = _walk_subcalls(trajectory)
    durations: list[float] = []
    granular_totals: defaultdict[str, dict[str, int]] = defaultdict(
        lambda: {"input_tokens": 0, "output_tokens": 0, "calls": 0}
    )
    for call in calls:
        model = call.get("root_model", "unknown")
        exec_time = call.get("execution_time")
        if isinstance(exec_time, int | float):
            durations.append(exec_time)
        usage = (call.get("usage_summary") or {}).get("model_usage_summaries", {})
        input_tokens = sum(u.get("total_input_tokens", 0) for u in usage.values())
        output_tokens = sum(u.get("total_output_tokens", 0) for u in usage.values())
        for m, u in usage.items():
            granular_totals[m]["input_tokens"] += u.get("total_input_tokens", 0)
            granular_totals[m]["output_tokens"] += u.get("total_output_tokens", 0)
            granular_totals[m]["calls"] += u.get("total_calls", 0)
        logger.log_event(
            "vanilla_subcall_detail",
            {
                "model": model,
                "execution_time_s": exec_time,
                "prompt_preview": str(call.get("prompt", ""))[:500],
                "response_preview": str(call.get("response", ""))[:500],
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            },
        )
    return {
        "subcall_count": len(calls),
        "subcall_wall_clock_max_s": max(durations) if durations else None,
        "subcall_wall_clock_sum_s": sum(durations) if durations else None,
        "granular_totals": {m: dict(v) for m, v in granular_totals.items()},
    }


def _reconcile_usage(
    logger: RunLogger, response: RLMChatCompletion, subcall_detail: dict[str, Any]
) -> None:
    """Compare the granular trajectory walk's per-model token sums against
    `usage_summary`'s aggregate. They should match; a mismatch means some call
    reached `usage_summary` without going through a path that appends to
    `_pending_llm_calls` (or vice versa) — surface it, don't silently trust either
    side (`CLAUDE.md`'s measurement-discipline rule, applied to our own logging
    pipeline, not just to the corpus)."""
    granular = subcall_detail["granular_totals"]
    for model, agg in response.usage_summary.model_usage_summaries.items():
        seen = granular.get(model)
        if seen is None:
            continue  # the root model has no granular entries by design; not a mismatch
        if (
            seen["input_tokens"] != agg.total_input_tokens
            or seen["output_tokens"] != agg.total_output_tokens
        ):
            logger.log_event(
                "vanilla_usage_reconciliation_mismatch",
                {
                    "model": model,
                    "granular_input_tokens": seen["input_tokens"],
                    "granular_output_tokens": seen["output_tokens"],
                    "usage_summary_input_tokens": agg.total_input_tokens,
                    "usage_summary_output_tokens": agg.total_output_tokens,
                },
            )


def _count_concepts(answer_markdown: str) -> int:
    """Count study-guide entries for the O4 saturation observation: if a 20-page
    slice and the full 916-page document yield roughly the same concept count, that
    is direct evidence against blind exploration buying more coverage.

    Numbered level-2 headings (`## 12. Some Concept`) are what the B1/seed-11 run
    produced; a plain `##`-per-concept structure is one plausible alternative. But a
    real run (B1/seed-23, `docs/18` §4.2 addendum, third correction) instead nested
    concepts one level deeper — 14 `## Chapter N` wrapper headings holding 190 real
    `### Concept Name` entries — and a `##`-only count silently reported the wrapper
    count (14) as the concept count, the opposite conclusion from the real one. The
    frozen prompt (`docs/21` §3.1) never mandates a heading structure, so this must
    stay robust to whichever level the model actually used: take the count of
    whichever heading level (numbered `##`, plain `##`, or `###`) is *highest* —
    concepts are the model's finest structural unit, so they always outnumber any
    chapter/part wrapper level, never the reverse.
    """
    numbered_h2 = re.findall(r"^##\s+\d+\.", answer_markdown, re.MULTILINE)
    plain_h2 = re.findall(r"^##\s+\S", answer_markdown, re.MULTILINE)
    h3 = re.findall(r"^###\s+\S", answer_markdown, re.MULTILINE)
    return max(len(numbered_h2), len(plain_h2), len(h3))
