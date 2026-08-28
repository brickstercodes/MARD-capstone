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

**The deliverable is a manuscript, not a product.** Working code is a means. A
change that makes the code nicer but invalidates a measured number is a net
loss.

## If you arrived from the paper

Every number in the manuscript is computed from a logged run in `runs/`. Nothing
is transcribed by hand. To check any of them:

```bash
python scripts/demo_results.py     # the headline table, recomputed from runs/
```

| Paper claim | Where it comes from |
|---|---|
| Task scores, tokens, cost (Table VI) | `eval/scoring_report.json`, `docs/35` |
| Structural stability (Table VII) | `eval/structure_report.json`, `docs/38` |
| Ablation by envelope channel (Table X) | `runs/*__mard_a1*`, `docs/28` |
| Negative control (Table XI) | `runs/*__introcs_flat__*`, `docs/41` |
| Second document (Table VIII) | `runs/*__axler__*`, `docs/44` |
| Groundedness (Table IX) | `eval/groundedness_report_*.json`, `docs/32` |
| OOLONG harness check | `docs/43` |

Each run directory carries its full configuration snapshot, the per-call log and
its own cost accounting, so a table can be recomputed without an API key. The
parsed corpora are not redistributed — `corpus/SOURCES.json` records each source
document's URL, SHA-256 and retrieval date, and `scripts/fetch_corpus.sh`
reproduces them from the publishers.

`docs/` is the supplementary record: the measurement protocol, the design
decisions that were fixed before any result existed, and the results themselves.
See [`docs/README.md`](docs/README.md) for an index. Documents internal to
building the system — task briefs, project bookkeeping — are not part of the
public record, so the numbering has gaps.

## Layout

| Path | Contents |
|---|---|
| `ingest/` | PDF → text + structural markers + page map |
| `envelope/` | MARD passes 0/1, envelope growth semantics |
| `mard/` | the MARD arm's run entry point |
| `vanilla/` | the vanilla-RLM control arm |
| `plan/` | Master Plan Pydantic models, boundary validation |
| `orchestrate/` | asyncio worker pool, fork-join, retry, isolation |
| `provider/` | model client, rate card, typed seams |
| `eval/` | scorers, groundedness detector, ablation analysis |
| `corpus/` | parsed documents + document-native ground truth |
| `runlog/` | run logging, config snapshots, seeds, cost accounting |
| `runs/` | logged transcripts, envelope states, summaries (generated) |
| `docs/` | decision records, implementation briefs, results |
| `paper/` | LaTeX source, figures, bibliography |
| `scripts/` | bootstrap, preflight, campaign runners, figure generation |

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

Nothing gets measured outside a `RunLogger`: a number that cannot be traced
back to a logged run is not admitted to the paper.

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

## Citation

If you use this work, please cite the manuscript in `paper/`. The state of this
repository as submitted is tagged `v1.0-manuscript`.

## Licence

Source in this repository is MIT licensed (`LICENSE`). Corpus documents are not
redistributed here and remain under their publishers' terms; the vendored RLM
reference implementation is MIT and is fetched, not committed. See `NOTICE.md`.
