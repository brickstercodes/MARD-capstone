# 42 — Implementation brief: a second document, and a bounded harness check

**Paste this whole file as the first message of a fresh Claude Code session opened in
`~/Desktop/Capstone/MARD-capstone`.**

Written 28 Aug 2026, late. The manuscript is submitted **Sunday 30 Aug**.

> ### ⚠️ BUDGET — ONE AUTHORITATIVE FIGURE, READ BEFORE PLANNING
>
> **Approximately $25 remains.** Stated by Anugrah directly on 28 Aug 2026 and superseding
> an earlier $5–7 estimate in a previous draft of this brief. Every other figure in the
> repository is stale or wrong and must not be used as the budget:
> `MARD_SPEND_CAP_USD=120` in `.venv/bin/activate` and `.env.example`; a `$60` ceiling in
> `runs/_ledger.json`, whose own note ("Rs 75,000 at Rs 95.13/USD") arithmetically gives
> $788, not $60. **Do not resolve that contradiction yourself — report it.**
>
> **True spend to date is $11.59, not the ledger's $10.71.** Two runs with real cost are
> absent from `runs/_ledger.json` while it reports `uncounted_runs: []`:
> `20260828T075502__mard__introcs__s11__b9c660` ($0.6507) and
> `20260828T094054__mard_a1f__introcs__s42__8a3517` ($0.2271). Both were excluded from
> results, which is presumably why they were skipped — but the money was spent. Fixing the
> ledger's accounting is a legitimate small task; doing it silently is not, so note it in
> your write-up.
>
> **This still reorders the work.** Job B (a second document, ~$3.50) is the priority.
> Job A is **not a reproduction** at any affordable sample size:
>
> - OOLONG at ~$0.20–0.70/task buys ~15–40 tasks. Even at n=40 the ±2 SE interval is
>   ±16 points against a 12-point gap (56.0 vs 44.0), so the interval contains both
>   hypotheses. The number would look like evidence and would not be evidence.
> - BrowseComp-Plus is worse: ~700k tokens per task, ≥$1.22 each to read once.
>
> So Job A remains an optional, explicitly-labelled **harness check**, run only if Job B
> completes and budget remains. See §1.
>
---

## 0. Read first


1. `docs/00-START_HERE.md` — the higher-number-wins rule and the concurrent-writing protocol.
2. `docs/18-W3_PROVIDER_SWITCH.md` §6 — why the base-paper reproduction is load-bearing and
   why it became possible only after the provider switch.
3. `docs/40-LITERATURE_LOG.md` row 1 — the verified target figures.
4. `eval/frozen_subsets.md` — the subset is **frozen**. You do not regenerate, resample or
   "improve" it. Not one line of `eval/frozen_subsets/` changes.

Then `scripts/preflight.sh`.

**Budget: see the banner above. $11.59 spent, ~$25 remains.** `MARD_SPEND_CAP_USD` is 120,
far above the real limit — **set it to 37 before your first run** so the guard matches the
money.

---

## 1. Job A — OPTIONAL, and it is NOT a reproduction

**Run this only if Job B is complete and at least $2 remains.** If in doubt, skip it: the
manuscript is already correct without it.

### 1.1 What it is and is not

`paper/main.tex` §3.2.2 states that the base-paper reproduction **was not performed**, and
§4.8.1 names it the largest threat to the baseline's validity. **This job does not change
either statement.** At the affordable n, accuracy cannot be estimated (see the budget
banner). What it can establish is narrower and still worth something:

> Our vanilla-RLM arm executes the published benchmark end-to-end and returns answers the
> benchmark's own scorer can parse.

That is a **harness check**. Anywhere it appears — your doc, and any sentence the
manuscript later lifts — it must be called that, never a reproduction, and it must carry
the n. If you find yourself computing an accuracy figure and comparing it to 56.0, stop:
that is the comparison this budget cannot support.

### 1.2 Scope

**4–6 tasks**, taken in file order from the frozen subset (not sampled — sampling at this n
invites a choice, and there is no budget to justify one). Report per task: ran / errored,
whether `_synth_score` parsed the output, run id, tokens, cost, wall-clock.

Report the raw correct-count if you have it, **with an explicit statement that at n≤6 it
is not an accuracy estimate and no comparison to the published 44.0 → 56.0 is drawn.**

### 1.3 What already exists — do not rebuild it

- `eval/frozen_subsets/oolong_trec_coarse_50_frozen_tasks.jsonl` — 50 tasks; fields
  `id`, `question`, `answer`, `task`, `task_group`, `answer_type`, `context_window_id`.
- `eval/frozen_subsets/oolong_context_window_131k.txt` — 317 KB. **All 50 tasks share
  `context_window_id: 0`**, so there is exactly one context, loaded once.
- `.vendor/rlm/training/environments/oolong/oolong/env.py` — the base paper's own scorer,
  `_synth_score(datapoint, output) -> float`, with `_attempt_answer_parse` beside it.

**Use the vendored scorer; do not write your own.** A check scored by a reimplemented
metric tells you nothing about the implementation under test. Import it from vendored code
and say in your write-up that you did.

`eval/frozen_subsets/` is **immutable**. You do not resample, regenerate or trim it. Taking
the first 6 of 50 is a read, not an edit.

### 1.4 The runner

`vanilla.run.run_vanilla_rlm` accepts `task_prompt`, and its docstring says a *measured
run* must never override it, because for the study-guide task the frozen prompt is part of
the measurement. **OOLONG is a different task and the per-task question legitimately is the
prompt.** That is a real exception, not a licence to bypass a guard quietly: add an explicit
code path with a comment saying why the study-guide freeze does not apply, so a reader of
`vanilla/run.py` cannot mistake one for the other.

Everything else identical to the study-guide runs: same models, `max_concurrent_subcalls=4`,
same depth, `RunLogger`, all seven `docs/30` §1 fields.

### 1.5 Stop conditions

- Run **one** task first. Report its actual cost before running any more.
- Stop at **6 tasks** or **$2.50 spent on this job**, whichever comes first.
- If a single task costs more than $0.80, stop after it and report.

### 1.6 Deliverable

`docs/43-BASE_PAPER_HARNESS_CHECK.md` — note the filename: *harness check*, not
reproduction. Include the per-task table, the total cost, and a plain paragraph stating
what this does **not** establish and that §4.8.1 stands unchanged.

## 2. Job B — a second document (THE PRIORITY — do this first)

`paper/main.tex` §4.8.4 concedes that every headline number comes from one document. `axler` is
already ingested and pinned (404 pages, source hash `b40b1da1cbca`), and one MARD run
exists on it.

Run **MARD full × 3 seeds** and **B1 × 3 seeds** on `--document-id axler`. Six runs,
roughly **$3.50** and **40 minutes** — most of the remaining budget, which is why it comes
first and why §4's ordering has you price one run before committing to the rest.

Cost asymmetry to plan around: the MARD run on axler cost **$0.296**, but B1 on `introcs`
averaged **$0.83** and varied 5× across seeds. **Run the three MARD seeds first** — they are
cheap and predictable — then B1 seeds one at a time, checking the ledger between each. If
the budget dies after two B1 seeds, report two B1 seeds and say so; three arms' worth of
MARD against two of B1 is a legitimate, disclosed asymmetry, and a fabricated third is not.

The existing seed-11 MARD run
(`20260828T144524__mard__axler__s11__3fed30`) may be reused as one of the three if its
configuration matches; say explicitly in your write-up whether you reused or re-ran it.

**State the limit plainly:** axler has no learning-objective blocks, so there is **no task
score** on this document (`docs/16`). What a second document extends is the determinism,
token-cost and cross-chapter-ablation findings — not the coverage null. Do not let a
reader infer otherwise.

Report the same structure as `docs/38` §2: concept counts per run, edge counts,
cross-chapter fraction, never-declared rejections, tokens, cost, wall-clock — mean and
min–max across the three repeats, for both arms.

Deliverable: `docs/44-SECOND_DOCUMENT_RESULTS.md`.

---

## 3. Footprint

**Yours:** `scripts/`, `vanilla/` (the §1.4 exception only), `eval/oolong_*` if you need new
modules, `runs/`, `docs/43`, `docs/44`.

**Read-only:** `eval/frozen_subsets/` (immutable), `corpus/`, `ingest/`, `mard/`,
`envelope/`, `orchestrate/`, `plan/`.

**Do not touch `paper/`.** It has one writer and it is not you. Your numbers go into
`docs/43` and `docs/44` and are lifted into the manuscript from there.

**Deliverables, so the mapping is unambiguous:**

| Job | Writes |
|---|---|
| **A** — optional OOLONG harness check | `docs/43-BASE_PAPER_HARNESS_CHECK.md` |
| **B** — second document (axler) | `docs/44-SECOND_DOCUMENT_RESULTS.md` |

This brief is `docs/42`. `docs/40` is the literature log; `docs/41` is the negative-control
results. Do not reuse a number that is taken.

---

## 4. Order

1. Preflight.
2. **Job B first.** One MARD run on axler, report its actual cost, then decide whether the
   remaining five fit the budget.
3. Job A **only if** Job B finished and $2+ remains.
4. If the budget runs out mid-way, stop and report what was completed. A partial Job B with
   two seeds reported as two seeds is fine; three seeds reported when two were run is not.

Report back with: the axler determinism table (concepts, edges, cross-chapter fraction,
tokens, cost, wall-clock — mean and min–max per arm), the exact spend, and if Job A ran,
how many tasks executed and parsed. Unrounded, with run ids.
