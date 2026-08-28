# 44 — Second-document results: MARD and B1 on `axler`

**Status:** Job B of `docs/42`, completed 28–29 Aug 2026. Six runs: MARD × 3 seeds, B1
(vanilla RLM) × 3 seeds, all on `--document-id axler` (Axler, *Linear Algebra Done Right*,
4th ed., 404 pages, source hash `b40b1da1cbca…`, `corpus/axler/manifest.json`).

**Total Job B spend: $1.98521875** (MARD $0.86260975 + B1 $1.122609), against a budget of
roughly $3.50 projected in `docs/42` and ~$25 true remaining before this job started. All
six seeds in `runlog.CAMPAIGN_SEEDS` (11, 23, 42) completed for both arms — no truncation,
no skipped seed.

## 0. What this extends and what it does not

**`axler` has no learning-objective blocks.** There is therefore **no task score** on this
document (`docs/16`) for either arm, and none is computed or implied anywhere below. What a
second document extends is the **determinism**, **token-cost**, and **cross-chapter-edge**
findings from `docs/38` on `introcs` — nothing here bears on the coverage-null finding, and
no reader should infer a task-score comparison from this table.

The seed-11 MARD run (`20260828T144524__mard__axler__s11__3fed30`) was **reused, not
re-run** — its `manifest.json` config (`system: mard`, models `gpt-5.2`/`gpt-5-mini`,
`tier2_reasoning_effort: low`, `tier2_max_tokens: 4096`, no ablation) matches exactly what
this job would have produced. Seeds 23 and 42 for MARD, and all three seeds for B1, are new
runs from this session.

## 1. Run IDs

| Arm | Seed | Run ID | Reused? |
|---|---|---|---|
| MARD | 11 | `20260828T144524__mard__axler__s11__3fed30` | Yes (pre-existing) |
| MARD | 23 | `20260828T183945__mard__axler__s23__a94663` | No |
| MARD | 42 | `20260828T184344__mard__axler__s42__60218a` | No |
| B1 | 11 | `20260828T184857__vanilla_rlm__axler__s11__019050` | No |
| B1 | 23 | `20260828T185543__vanilla_rlm__axler__s23__b0c83d` | No |
| B1 | 42 | `20260828T190329__vanilla_rlm__axler__s42__a416a3` | No |

## 2. MARD arm

**Two concept counts exist, and they disagree, for the same reason `docs/38` §2 documents
on `introcs`:** `summary.json`'s `concepts_accepted` is Pass 1's raw per-chapter
declarations, recorded before `compile_plan.py`'s duplicate-id merge runs.
`master_plan.json`'s `concept_graph` is the compiled, post-merge count — the correct one
for determinism, per `docs/38`'s own instruction.

| Seed | Concepts (pre-merge) | Concepts (`concept_graph`, post-merge) | Edges (pre-merge) | Edges (post-merge) | Cross-chapter edges | Tokens in/out | Cost | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| 11 (reused) | 54 | 54 | 116 | 116 | 76 | 22,709 / 69,799 | $0.29553475 | 275.23s |
| 23 | 54 | 54 | 104 | 104 | 70 | 21,126 / 61,640 | $0.26876650 | 228.11s |
| 42 | 53 | 52 | 116 | 115 | 77 | 21,448 / 74,318 | $0.29830850 | 270.23s |

| Metric | Values (post-merge where applicable) | Mean | Min–max | CV |
|---|---|---|---|---|
| Concepts (post-merge) | 54 / 54 / 52 | 53.3 | 52–54 | 0.0177 |
| Edges (post-merge) | 116 / 104 / 115 | 111.7 | 104–116 | 0.0487 |
| Cross-chapter edges | 76 / 70 / 77 | 74.3 | 70–77 | 0.0416 |
| Cross-chapter fraction (of post-merge edges) | 0.655 / 0.673 / 0.670 | 0.666 | 0.655–0.673 | 0.0116 |
| Input tokens | 22,709 / 21,126 / 21,448 | 21,761 | 21,126–22,709 | 0.0314 |
| Output tokens | 69,799 / 61,640 / 74,318 | 68,586 | 61,640–74,318 | 0.0765 |
| Cost (USD) | 0.2955 / 0.2688 / 0.2983 | 0.2875 | 0.2688–0.2955 | 0.0463 |
| Wall-clock (s) | 275.23 / 228.11 / 270.23 | 257.86 | 228.11–275.23 | 0.0820 |

**Concept and edge counts on `axler` are tighter (CV 0.018–0.049) than the corresponding
`introcs` MARD numbers in `docs/38` §2.2** (concept CV 0.0056 pre-merge / same post-merge
pattern, edge CV 0.029–0.105) — both documents show the same qualitative shape: the
concept scaffold is near-deterministic, the edge set is not, and cross-chapter linkage is
substantial and stable (65.5–67.3% of edges here vs. `introcs` MARD's **89.5–93.0%**,
computed from `docs/38` §2.2's own edge/cross-chapter-edge columns — 115/124, 119/128,
119/133 — rather than quoted from its prose) — `axler`'s cross-chapter fraction is
markedly lower, consistent with a proof-based mathematics text having a more linear,
within-chapter dependency structure than the CS textbook `introcs`; this is a plausible,
not verified, explanation and is flagged as such.

## 3. B1 (vanilla RLM) arm

| Seed | Concept count (`_count_concepts`) | Tokens in/out | Cost | Wall-clock |
|---|---|---|---|---|
| 11 | 0 | 439,358 / 71,308 | $0.34314400 | 379.44s |
| 23 | 0 | 462,747 / 74,213 | $0.43237675 | 436.06s |
| 42 | 67 | 444,641 / 58,741 | $0.34708825 | 179.58s |

| Metric | Values | Mean | Min–max | CV |
|---|---|---|---|---|
| Input tokens | 439,358 / 462,747 / 444,641 | 448,915 | 439,358–462,747 | 0.0223 |
| Output tokens | 71,308 / 74,213 / 58,741 | 68,087 | 58,741–74,213 | 0.0986 |
| Cost (USD) | 0.3431 / 0.4324 / 0.3471 | 0.3742 | 0.3431–0.4324 | 0.1100 |
| Wall-clock (s) | 379.44 / 436.06 / 179.58 | 331.69 | 179.58–436.06 | 0.3317 |

**Finding not to skip: the `concept_count` column is not a real 0/0/67 measurement of B1's
output — it is `_count_concepts` failing to parse two of the three outputs.** Reading the
raw artefacts (`artefacts/vanilla_answer.md` in each run directory) shows all three seeds
produced substantive, complete study-guide content of comparable length. The difference is
**structural, self-authored, and inconsistent across seeds**, exactly the kind of instability
`docs/32` §4 already documented for B1 on `introcs` (156/190/75 architectures, never to be
averaged):

- **Seed 42** used markdown headings (`## 1. Vector Spaces`, `### Scalars and the Field F`),
  which `_count_concepts` recognizes — hence 67.
- **Seed 11** used a bare numbered-list format (`1. Complex numbers (C)` with no `#`
  markers) — `_count_concepts` finds nothing.
- **Seed 23** used a still different numbered/sub-numbered format (`1. Vector spaces`,
  `1.1 Notation: list of vectors`) — also invisible to the counter.

`_count_concepts`'s own docstring (`vanilla/run.py`, `_count_concepts`) already anticipates
that B1 seed-11 and seed-23 introcs runs produced different structures and says a plain
`##`-per-concept format is "one plausible alternative" — this `axler` result is a third,
independently-arising structural variant, reproducing the same instability finding on a
different document rather than contradicting it. **0/0/67 is not a measurement of
declining or improving coverage and must not be read as one; it is the counter's coverage
gap, disclosed here rather than reported as a real concept count.**

## 4. Cost and asymmetry, as ordered

MARD ran first (three seeds, $0.86 total) exactly as `docs/42` specified, before any B1
seed. All three B1 seeds then ran without needing to stop early — the highest single B1
cost on `axler` ($0.4324, seed 23) is well under `docs/42`'s $0.80-per-task stop threshold
and well under the `introcs` B1 average of $0.83 cited in the brief. **`axler` B1 costs
(0.343 / 0.432 / 0.347) show far less cross-seed spread than `introcs` B1's measured
5× variation** (`docs/18` §10 / `docs/38`) — on this document, wall-clock varied more
(179.58s–436.06s, driven by 8–13 root iterations) than cost did.

## 5. Ledger

- MARD subtotal: $0.86260975 (seed 11 reused — no new spend; seeds 23+42 = $0.5670750)
- B1 subtotal: $1.122609
- **Job B total new spend this session: $1.6896847** (excludes the reused seed-11 MARD run's
  already-recorded $0.29553475)
- Spend cap enforced this session: `MARD_SPEND_CAP_USD=37` (set per `docs/42` banner,
  superseding the stale `120` in `.venv/bin/activate`/`.env.example` and the ledger's own
  stale `$60` field, which this job did not touch or resolve — that contradiction is
  `docs/42`'s to report, not this job's to fix).
- All six runs completed, logged, and priced with no `unpriced_models` or `stale_rates`.
