# MARD — Metadata-Augmented Recursive Decomposition

Recursive language model exploration is structurally blind: each recursive call
receives a raw text slice with no representation of the document's global
structure, so structure is rediscovered on every call and never carried forward.
MARD adds a **metadata envelope** that accumulates across calls, so exploration
confirms a hypothesis instead of discovering blindly.

```
vanilla RLM call →  [raw slice]
MARD call        →  [raw slice] + [skeleton] + [accumulated findings] + [parent directive]
```

Base paper: Zhang, Kraska & Khattab, *Recursive Language Models*, arXiv:2512.24601.

**The deliverable is two manuscripts, not a product.** Working code is a means.
A change that makes the code nicer but invalidates a measured number is a net
loss. Read `../CONTEXT.md` before changing anything here.

## Layout

| Path | Contents | Owner |
|---|---|---|
| `ingest/` | PDF → text + structural markers + page map | Track 4 |
| `envelope/` | MARD passes 0/1/2, envelope growth semantics | Track 1 |
| `plan/` | Master Plan Pydantic models, boundary validation | Track 2 |
| `orchestrate/` | asyncio worker pool, fork-join, retry, isolation | Track 2 |
| `eval/` | scorers, baselines, ablation runner | Track 3 |
| `corpus/` | parsed documents + document-native ground truth | Track 4 |
| `runlog/` | run logging, config snapshots, seeds, cost accounting | Track 2 |
| `runs/` | logged transcripts, envelope states, summaries | generated |
| `paper/` | LaTeX + bibliography | Track 4 |

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Add `.[ingest]` for the PDF pipeline and `.[eval]` for the measurement stack.
They are split so no track has to install another track's native dependencies
to run its own suite.

## Logging every run

Nothing gets measured outside a `RunLogger`. CONTEXT.md §3.4: *a number you
cannot reproduce on 29 Sep is not a number.*

```python
from runlog import RunLogger, CAMPAIGN_SEEDS

with RunLogger.start(
    runs_root="runs",
    system="mard",              # mard | vanilla_rlm | full_context | naive_chunk | rag
    document_id="ostep",
    seed=CAMPAIGN_SEEDS[0],
    models={"tier1": "<frontier>", "tier2": "<budget>"},
    params={"depth": 2},
) as run:
    run.log_envelope(0, skeleton)
    call_id = run.log_call(
        role="tier1", model="<frontier>",
        prompt=prompt, response=response,
        input_tokens=..., output_tokens=..., depth=0,
    )
    run.log_call(..., depth=1, parent_call_id=call_id)   # keeps recursion reconstructable
    run.save_artefact("master_plan.json", plan_json)
    run.set_result({"task_score": 0.71})
```

Each run writes one directory:

```
runs/20260802T081500__mard__ostep__s11__a1b2c3/
├── manifest.json      config snapshot, git SHA + dirty flag, package versions, seeding
├── calls.jsonl        one record per model call: transcript, tokens, depth, parent
├── events.jsonl       retries, validation failures, joins
├── envelope/pass_N.json
├── artefacts/         Master Plan, joined output
└── summary.json       status, wall clock, per-model totals, cost, result
```

Read it back with `load_run(run_dir)`.

### Three behaviours that are deliberate

- **A crashed run still writes `summary.json`**, with `status: "failed"` and the
  traceback. Rate limits and timeouts kill runs in W3 and W6; a hole in the
  matrix should carry its own explanation.
- **JSONL is flushed per line** and `load_run` skips a truncated final record, so
  a killed process leaves usable data rather than an unparseable file.
- **Cost is `null`, never `0.0`, when a model has no recorded rate.** Rates carry
  `retrieved_on` and a provider URL and are refused after 30 days
  (`StaleRateError`). CONTEXT.md §4.3 rule 4: aggregators disagreed by up to 2×,
  and a dead cost claim (§2.3) is what that discipline is protecting against.

## Hard rules

- Feature freezes **23 Aug** and **13 Sep** are absolute. After a freeze, a
  "small fix" is a re-run of the entire matrix.
- Results freezes **27 Aug** and **20 Sep**. A wrong result after these gets a
  limitation paragraph, not a re-run.
- **3 seeds on every number, variance reported.** `runlog.CAMPAIGN_SEEDS`.
- Never tune toward a positive result after the fact. A clean null against the
  O4 boundary is publishable.

## Conventions

`ruff format` · `ruff check` · `mypy`. Comments say *why*, never *what*.
File-level docstrings explain why a module exists. Rule of Three before
abstracting. Named constants over magic values.
