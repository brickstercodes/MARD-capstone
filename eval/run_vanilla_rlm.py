"""The vanilla-RLM control (A1) -- issue #20's core W1 deliverable.

A1 is "envelope removed" (docs/13-W0_DECISIONS_LOG.md): the unmodified base
RLM library, single backend, no MARD envelope, no plan. It feeds every
comparison in both manuscripts, so this script deliberately does nothing
clever -- it is the library exactly as vendored, pointed at the frozen W0
subsets (eval/frozen_subsets.md, issue #19), with every call accounted for
through runlog per CLAUDE.md's "every run logged, no exceptions" rule.

**"Exactly as vendored" is now literally true.** Under the Vertex backend it
was not: the control ran upstream *plus* five local patches to a gitignored
directory (docs/15's constructor patch, the 20 Aug `_text_or_empty` fix, and
docs/16's three fixes), each of which had to be reapplied by hand after any
re-clone. On the OpenAI path `.vendor/rlm` is a clean checkout of upstream and
none of those patches apply -- docs/16 §2b/2c/2e established the failure they
worked around as a property of the Gemini model lineage, reproduced across
three independent RLM implementations and both tier models. This is the real
argument for the pivot: it makes the control's provenance a commit SHA rather
than a prose document. See docs/17-OPENAI_PIVOT.md.

The backend itself is no longer hardcoded here -- see eval/backends.py.

Two frozen datasets, two very different cost profiles:

  - OOLONG (n=50): one shared 131K-token context window, cheap and
    predictable per task. Safe default for a first end-to-end run.
  - BrowseComp-Plus (n=20): each query embeds full gold/negative/evidence
    document text. Sizes range from ~870KB to ~8.3MB of raw text per query
    in this frozen file -- some queries are far larger than others, and
    this has not been re-sized against the OpenAI context limit or the
    trial budget on a per-query basis. Do not batch-run the full n=20
    without doing that sizing first; run one at a time and watch the cost
    this script prints.

Scoring here is a smoke-test proxy (substring match against the frozen
answer), not the real task-quality scorer -- docs/30-MEASUREMENT_PROTOCOL.md
§2 leaves that scorer's internals to Track 3, to be built against
Track 4's document-native ground truth, which is a separate axis from
these two general-capability benchmarks.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from rlm import RLM
from rlm.logger import RLMLogger

from eval.backends import BackendProfile, active_profile
from eval.rates import rate_card_for
from runlog import CAMPAIGN_SEEDS, RunLogger

FROZEN_DIR = Path(__file__).parent / "frozen_subsets"
BROWSECOMP_FILE = FROZEN_DIR / "browsecomp_plus_frozen_20.jsonl"
OOLONG_TASKS_FILE = FROZEN_DIR / "oolong_trec_coarse_50_frozen_tasks.jsonl"
OOLONG_CONTEXT_FILE = FROZEN_DIR / "oolong_context_window_131k.txt"

RUNS_ROOT_ENV = "MARD_RUNS_ROOT"

# Matches upstream's own quickstart.py convention. Not a MARD/ablation
# setting -- A1 is the library's own defaults, this just bounds a smoke run.
MAX_ITERATIONS = 10


def runs_root() -> Path:
    """Where this campaign's runs and spend ledger live.

    Defaults to the active backend's own root (eval/backends.py explains why
    the ledgers are separate), overridable by MARD_RUNS_ROOT for the rare case
    of re-pricing or re-analysing someone else's directory. The 122 Vertex runs
    stay exactly where they are, untouched and still resumable.
    """
    override = os.environ.get(RUNS_ROOT_ENV)
    return Path(override) if override else Path(active_profile().runs_root)


# ----------------------------------------------------------------- loading


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def load_browsecomp_task(index: int) -> dict[str, Any]:
    tasks = _read_jsonl(BROWSECOMP_FILE)
    return tasks[index]


def load_oolong_task(index: int) -> tuple[dict[str, Any], str]:
    tasks = _read_jsonl(OOLONG_TASKS_FILE)
    context_window = OOLONG_CONTEXT_FILE.read_text(encoding="utf-8")
    return tasks[index], context_window


# ------------------------------------------------------------- prompt shape


def build_prompt_browsecomp(task: dict[str, Any]) -> str:
    sections = []
    for key in ("gold_docs", "negative_docs", "evidence_docs"):
        for doc in task.get(key, []) or []:
            sections.append(f"[{key} docid={doc.get('docid')}]\n{doc.get('text', '')}")
    documents = "\n\n".join(sections)
    return (
        "Answer the question using only the documents provided below. "
        "Give a direct, concise final answer.\n\n"
        f"Question: {task['query']}\n\n"
        f"Documents:\n{documents}"
    )


def build_prompt_oolong(task: dict[str, Any], context_window: str) -> str:
    return f"{context_window}\n\n{task['question']}"


# ------------------------------------------------------------------ scoring


def score_answer(response: str, expected: str | list[str]) -> bool:
    """Substring-match proxy. Not the real scorer -- see module docstring."""
    expected_list = expected if isinstance(expected, list) else [expected]
    response_lower = response.lower()
    return any(str(ans).lower() in response_lower for ans in expected_list)


# ------------------------------------------------------------ crash-safe log


@contextlib.contextmanager
def live_call_logging(run: RunLogger, profile: BackendProfile) -> Iterator[None]:
    """Log every real provider call the instant it returns, not after the
    whole (possibly recursive, possibly iterating-to-exhaustion) completion
    finishes.

    The failed OOLONG run this was built in response to hit a library crash
    after 10 real, billed calls -- and because the previous version of this
    script only walked the call tree after `.completion()` returned
    successfully, that run's summary.json showed "calls": 0, "cost": 0.0.
    Real spend, invisible. runlog's own design intends the opposite: a
    crashed run should explain itself, not erase what happened before it.

    Patching the *class* rather than one instance is what makes this cover
    recursive child calls too -- rlm/core/rlm.py constructs each child's client
    itself via get_client(), so this script never gets a handle to hand a
    wrapped instance down. Which class to patch now comes from the active
    backend profile instead of a hardcoded import.
    """
    client_class = profile.client_class()
    original_completion = client_class.completion
    original_acompletion = client_class.acompletion

    def _log(client: Any, prompt: Any, response: Any) -> None:
        usage = client.get_last_usage()
        run.log_call(
            role="live",
            model=client.model_name or "unknown",
            prompt=prompt if isinstance(prompt, str) else json.dumps(prompt),
            response=str(response),
            input_tokens=usage.total_input_tokens,
            output_tokens=usage.total_output_tokens,
        )

    # Both wrappers log a stringified copy but return the client's own return
    # value untouched. The previous version returned `str(...)`, which quietly
    # turned a None completion into the string "None" before the library saw
    # it -- an observability wrapper must not change what is being observed.
    def logged_completion(self: Any, prompt: Any, model: str | None = None) -> Any:
        response = original_completion(self, prompt, model=model)
        _log(self, prompt, response)
        return response

    async def logged_acompletion(self: Any, prompt: Any, model: str | None = None) -> Any:
        response = await original_acompletion(self, prompt, model=model)
        _log(self, prompt, response)
        return response

    client_class.completion = logged_completion
    client_class.acompletion = logged_acompletion
    try:
        yield
    finally:
        client_class.completion = original_completion
        client_class.acompletion = original_acompletion


# ------------------------------------------------------------------- runner


def run_one(dataset: str, index: int, seed: int) -> Path:
    profile = active_profile()

    if dataset == "oolong":
        task, context_window = load_oolong_task(index)
        document_id = f"oolong-trec_coarse-{task['id']}"
        prompt = build_prompt_oolong(task, context_window)
        expected = task["answer"]
    elif dataset == "browsecomp":
        task = load_browsecomp_task(index)
        document_id = f"browsecomp_plus-{task['query_id']}"
        prompt = build_prompt_browsecomp(task)
        expected = task["answer"]
    else:
        raise ValueError(f"Unknown dataset: {dataset!r}. Use 'oolong' or 'browsecomp'.")

    rlm = RLM(
        backend=profile.name,
        backend_kwargs=profile.backend_kwargs(),
        environment="local",
        max_iterations=MAX_ITERATIONS,
        sampling_args=profile.sampling_params(seed),
        logger=RLMLogger(),
    )

    with RunLogger.start(
        runs_root=str(runs_root()),
        system="vanilla_rlm",
        document_id=document_id,
        seed=seed,
        models={"root": profile.tier1_model},
        # `backend` and `reasoning_effort` are recorded because they change the
        # number without changing anything else visible in the run directory --
        # exactly the kind of variable a config snapshot exists to pin.
        params={
            "dataset": dataset,
            "index": index,
            "max_iterations": MAX_ITERATIONS,
            "backend": profile.name,
            "reasoning_effort": profile.reasoning_effort,
        },
        rate_card=rate_card_for(profile.name),
    ) as run:
        run_dir = run.run_dir
        with live_call_logging(run, profile):
            result = rlm.completion(prompt)
        # The structured recursion tree (depth, parent/child) is saved as a
        # readable artefact once the run succeeds -- live_call_logging above
        # is what's crash-safe and authoritative for cost/tokens, this is
        # just the human-readable trajectory on top of it.
        if result.metadata is not None:
            run.save_artefact(
                "rlm_trajectory.json", json.dumps(result.metadata, default=str, indent=2)
            )
        correct = score_answer(result.response, expected)
        run.set_result(
            {
                "task_score": 1.0 if correct else 0.0,
                "predicted": result.response,
                "expected": expected,
            }
        )

    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["oolong", "browsecomp"], default="oolong")
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--seed", type=int, default=CAMPAIGN_SEEDS[0])
    args = parser.parse_args()

    profile = active_profile()
    print(f"backend: {profile.name}  model: {profile.tier1_model}  runs_root: {runs_root()}")

    run_dir = run_one(args.dataset, args.index, args.seed)

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    print(f"run_dir: {run_dir}")
    print(f"status: {summary['status']}")
    print(f"calls: {summary['totals']['calls']}")
    print(
        f"tokens: {summary['totals']['input_tokens']} in / {summary['totals']['output_tokens']} out"
    )
    print(f"cost (USD): {summary['totals']['cost']}")
    if summary["result"]:
        print(f"task_score: {summary['result']['task_score']}")
        print(f"predicted: {summary['result']['predicted'][:200]!r}")
        print(f"expected: {summary['result']['expected']!r}")
    else:
        print(f"error: {summary['error']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
