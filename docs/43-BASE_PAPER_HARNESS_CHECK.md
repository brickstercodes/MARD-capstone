# 43 — Base-paper harness check (OOLONG), NOT a reproduction

**Status:** Job A of `docs/42`, run 28–29 Aug 2026 after Job B completed
(`docs/44-SECOND_DOCUMENT_RESULTS.md`). Total cost **$1.77030625**, against the
$2.50 stop threshold and $0.80-per-task threshold in `docs/42` §1.5 — neither was hit;
all 6 tasks ran to completion.

## 0. What this is and is not — read before the table

**This is not a reproduction of the base paper's OOLONG figure (44.0 → 56.0,
`docs/40` row 1).** At n=6, accuracy cannot be estimated with any interval that would
distinguish it from noise (`docs/42`'s budget banner: even n=40 gives a ±16-point
interval against a 12-point gap). **No accuracy figure is computed here, and none
should be read into the raw correct-count below.**

What this **does** establish, narrowly:

> Our vanilla-RLM arm executes the published OOLONG benchmark end-to-end — reads the
> real 131K-token context, dispatches its own recursive sub-call decomposition,
> produces an answer — and that answer is one OOLONG's own scorer can parse and score.

`paper/main.tex` §3.2.2 and §4.8.1 are **unchanged by this result**. The base-paper
reproduction still was not performed, and §4.8.1 still names its absence as the
largest threat to the baseline's validity. This document does not touch `paper/`.

## 1. Scope and method

- **4–6 tasks required by `docs/42` §1.2; 6 ran.** Taken in file order from
  `eval/frozen_subsets/oolong_trec_coarse_50_frozen_tasks.jsonl` (task ids 17000200,
  17000203, 17000205, 17000206, 17000207, 17000208) — not sampled, per the brief and
  per `eval/frozen_subsets.md`'s freeze. `eval/frozen_subsets/` was not modified;
  reading the first 6 records is a read, not an edit.
- **Shared context:** `eval/frozen_subsets/oolong_context_window_131k.txt` (all 50
  frozen tasks share `context_window_id: 0`), loaded once and split one line per list
  element — matching the benchmark's own framing ("the following lines contain 3182
  general-knowledge questions, one per line"). Never re-chunked into `[[page:N]]`
  markers; this text was never ingested through `ingest/cli.py` and has none.
- **Scorer:** the vendored base-paper scorer, imported unmodified —
  `eval/oolong_scorer.py` loads `_synth_score`/`_attempt_answer_parse` directly from
  `.vendor/rlm/training/environments/oolong/oolong/env.py` via `importlib`, with
  `rlm_train`, `verifiers` and `datasets` stubbed as empty placeholder modules purely
  so that file's top-level `import`/`from ... import` statements succeed — none of the
  three is touched by the two scoring functions (confirmed by reading `env.py`: they
  are only referenced inside `load_environment()`, which is never called, and behind
  `from __future__ import annotations`'s postponed type-hint evaluation). `dateutil`,
  which the scorer's `ANSWER_TYPE.DATE` branch genuinely calls, is a real installed
  dependency (`python-dateutil`, added this session — a small, legitimate scorer
  dependency, not a training-framework package), not stubbed. No part of the scoring
  logic itself was reimplemented or modified.
- **Runner:** a new `run_vanilla_rlm_oolong_task()` in `vanilla/run.py`, added
  specifically for this exception (`docs/42` §1.4). `run_vanilla_rlm()` (the
  study-guide arm) refuses to run without `ingest/manifest.py` provenance verification
  and defaults to the frozen study-guide prompt, because for that measured run the
  prompt is part of what's being measured. Neither applies to OOLONG: it is not an
  ingested corpus document, and the per-task question genuinely is the correct
  `root_prompt` — OOLONG's own base-paper training harness (`env.py`) uses each task's
  question as its `root_prompt` too. The new function takes an OOLONG task dict, not a
  `document_id`, so it cannot be reached by accident from a measured study-guide run;
  the shared execution body was factored into a private `_run_vanilla_rlm_pages()` that
  both the existing and new public functions call, so no behavior changed for the
  existing arm (`tests/test_vanilla.py`, 26/26 passing after the refactor).
- **Config:** identical to the B1 runs otherwise — `gpt-5.2` root / `gpt-5-mini` sub,
  `max_depth=1`, `max_concurrent_subcalls=4`, `max_iterations=30`, `RunLogger`, all
  seven `docs/30` §1 fields (seed fixed at 11 — this check does not claim a 3-seed
  variance measurement; see §4 below).
- **Script:** `scripts/run_oolong_harness_check.py`.

## 2. Per-task results

| # | Task ID | Task type | Run ID | Status | Parsed by scorer? | `synth_score` | Tokens in/out | Cost | Wall-clock |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 17000200 | `TASK_TYPE.MOST_FREQ` | `20260828T191508__vanilla_rlm_oolong_harness_check__oolong_trec_coarse_task_17000200__s11__eadf07` | ran | yes — `'numeric value'` | 1.0 | 64,544 / 107,942 | $0.2770275 | 185.58s |
| 2 | 17000203 | `TASK_TYPE.RELATIVE_FREQ` | `20260828T191814__vanilla_rlm_oolong_harness_check__oolong_trec_coarse_task_17000203__s11__d6ec13` | ran | yes — `'less common than'` | 1.0 | 85,731 / 117,809 | $0.34361875 | 211.70s |
| 3 | 17000205 | `TASK_TYPE.RELATIVE_FREQ` | `20260828T192146__vanilla_rlm_oolong_harness_check__oolong_trec_coarse_task_17000205__s11__aa119d` | ran | yes — `'less common than'` | 1.0 | 242,341 / 161,839 | $0.48663975 | 314.45s |
| 4 | 17000206 | `TASK_TYPE.RELATIVE_FREQ` | `20260828T192701__vanilla_rlm_oolong_harness_check__oolong_trec_coarse_task_17000206__s11__bf3a98` | ran | yes — `'less common than'` | 1.0 | 154,964 / 47,179 | $0.2551705 | 209.25s |
| 5 | 17000207 | `TASK_TYPE.RELATIVE_FREQ` | `20260828T193030__vanilla_rlm_oolong_harness_check__oolong_trec_coarse_task_17000207__s11__869e9a` | ran | yes — `'more common than'` | 1.0 | 71,550 / 1,750 | $0.1497125 | 33.92s |
| 6 | 17000208 | `TASK_TYPE.RELATIVE_FREQ` | `20260828T193105__vanilla_rlm_oolong_harness_check__oolong_trec_coarse_task_17000208__s11__f85a07` | ran | yes — `'more common than'` (gold: `'same frequency as'`) | 0.0 | 205,923 / 4,668 | $0.25813725 | 74.58s |

**Totals:** 6/6 ran (0 errored), 6/6 parsed by `_attempt_answer_parse`, tokens
825,053 in / 441,187 out, **cost $1.77030625**, wall-clock 33.9s–314.5s (mean 171.6s).

## 3. Raw correct-count — explicitly not an accuracy estimate

**5 of 6 (`synth_score == 1.0` on 5, `0.0` on task 6).** Stated again because it bears
repeating: **this is not an accuracy figure and no comparison to the published
44.0 → 56.0 OOLONG result is drawn.** At n=6 the confidence interval on any accuracy
estimate is wide enough to be meaningless (`docs/42`'s own arithmetic: n=40 already
gives ±16 points against a 12-point gap; n=6 is worse). Task 6's miss
(`'more common than'` vs. gold `'same frequency as'`) is one data point on one
comparison-type OOLONG task and says nothing about the system's accuracy in general —
it is reported because omitting a wrong answer while reporting right ones would be
exactly the kind of after-the-fact tuning `docs/30` §4 and `CONTEXT.md` §3.4 forbid.

## 4. Caveats and what this does not establish

- **Seed:** all 6 tasks used a single fixed seed (11) for `RunLogger`'s bookkeeping —
  no 3-seed repeat, no variance claim. `docs/42` §1.2 asked for a per-task table at
  n=4–6, not a seeded campaign; that is what was delivered.
- **Task diversity:** 5 of 6 tasks landed on `TASK_TYPE.RELATIVE_FREQ` (file order, not
  chosen) — this check exercises the harness's ability to run and be scored, not
  balanced coverage of OOLONG's task-type taxonomy.
- **No comparison to `docs/38`'s B1/MARD determinism numbers is implied.** This is a
  different task family (aggregate counting over a flat 131K-token list, not
  study-guide generation over a structured textbook) on a different benchmark.
- **`paper/main.tex` §3.2.2 and §4.8.1 stand exactly as written.** This check does not
  reproduce the base paper's reported accuracy, does not change what §4.8.1 names as
  the largest threat to baseline validity, and should not be cited as doing either.
  If a sentence from this document is lifted into the manuscript, it must be called a
  **harness check**, never a **reproduction**, and must carry n=6.

## 5. Spend

- Job A total: **$1.77030625** (6 tasks, none skipped, none truncated).
- Combined with Job B ($1.98521875, `docs/44`), this session's total new spend:
  **$3.755525**.
- All runs logged, priced, and recorded in `runs/_ledger.json`; no `unpriced_models` or
  `stale_rates` on any run.
