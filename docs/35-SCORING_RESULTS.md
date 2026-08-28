# 35 — Scoring results: O3 quality, forward-reference violations, groundedness over MARD

**Status:** Recorded 28 Aug 2026 · Owner: Track 1 (`docs/26`/`docs/32` session) · Implements
the scoring brief

> ### ⚠️ AMENDED — 28 Aug 2026, §2 corrected in place
>
> §2's "chapters 10 and 13 missing / 40% unmappable / A1s slightly worse" was a bug in this
> session's own chapter-attribution code (`chapter_for_page`, page-range matching against a
> corpus whose chapter boundaries all overlap by one shared page), not a Pass 1 finding.
> Fixed by attributing through `source.section_id` instead. **Corrected result: all 14
> chapters covered in every run, plan order equals book order exactly in all 9 runs.** See
> §2.2 for the full account. Caught and re-derived following the same "verify against run
> artefacts" discipline `docs/37`/`docs/38` were built under.
>
> **A third instance of the same bug family, found afterward:** `ingest.groundtruth.
> extract_learning_objectives` (§1's reference-set source) attributed the ground-truth
> objectives themselves via the identical page-range mistake. Fixed at the root in
> `ingest/groundtruth.py` (walk backward to the nearest numbered heading in document order);
> `extract_cross_references`'s citing-page classification got the same fix, though it turned
> out not to change §2's numbers — none of the 50 real cross-references sit on a boundary
> page. **§1's whole-document numbers are unaffected** (they never grouped by chapter); the
> per-chapter re-score this enables lives in `docs/38` §5, not here.

Code: [`eval/task_score.py`](../eval/task_score.py) (Task A), [`eval/ordering.py`](../eval/ordering.py)
(Task B), [`eval/groundedness_mard.py`](../eval/groundedness_mard.py) (Task C). Data:
[`eval/scoring_report.json`](../eval/scoring_report.json),
[`eval/ordering_report.json`](../eval/ordering_report.json),
[`eval/groundedness_report_mard.json`](../eval/groundedness_report_mard.json). Tests:
`tests/test_runs.py`, `tests/test_task_score.py`, `tests/test_ordering.py`,
`tests/test_groundedness_mard.py`.

**Headline, as requested, not rounded:**

- Covered-objective fraction at threshold 0.6, mean across 3 seeds: **B1 0.9423868312757202,
  MARD full 0.9574759945130316** (range B1 0.897119341563786–0.9711934156378601; MARD
  0.9547325102880658–0.9629629629629629). The two overlap and are not meaningfully
  distinguishable at this granularity — see §1's caveat before reading anything into the
  0.015 gap.
- Token/cost contrast, mean input tokens: **B1 1,493,033.33 vs MARD 94,242.33 — a 15.8×
  reduction.** Mean cost: **B1 $0.8322643333 vs MARD $0.5783864167.**

---

## 0. Run ids used

Selected by `eval.runs.select_run` (last `status: "ok"` run per system/seed) and printed here
so every number below is traceable without re-running the selector.

| System | Seed 11 | Seed 23 | Seed 42 |
|---|---|---|---|
| B1 (`vanilla_rlm`) | `20260827T193317__vanilla_rlm__introcs__s11__ec9d17` | `20260827T194259__vanilla_rlm__introcs__s23__a39374` | `20260827T195512__vanilla_rlm__introcs__s42__1dbe85` |
| MARD full (`mard`) | `20260828T082226__mard__introcs__s11__13de68` | `20260828T083017__mard__introcs__s23__d03195` | `20260828T083754__mard__introcs__s42__548fe0` |
| A1s (`mard_a1`) | `20260828T084613__mard_a1__introcs__s11__a1a24e` | `20260828T085334__mard_a1__introcs__s23__6613c4` | `20260828T090031__mard_a1__introcs__s42__77b25a` |
| A1f (`mard_a1f`) | `20260828T092525__mard_a1f__introcs__s11__4372f1` | `20260828T093323__mard_a1f__introcs__s23__c3d7d1` | `20260828T095152__mard_a1f__introcs__s42__2f00df` |

`mard` seed 11 has three superseded pre-fix attempts on disk (`docs/28` §4) and `mard_a1f`
seed 42 has two rate-limited failures (`docs/28` §6.3); the run ids above are the correct,
final ones in both cases, selected the same way the other seven were, not hand-picked.

---

## 1. Task A — O3 quality score

### 1.1 The reference set is 243 objectives, not 61

`docs/34` §2 (following `docs/23` §2's table) says 61. That table counts 61
`learning_objectives` **marker blocks** — one per section with a "Learning Objectives"
heading. A marker block is not an objective: each introduces several `•`-delimited bullets,
and `ingest.groundtruth.extract_learning_objectives` returns one `LearningObjective` per
bullet. Run directly against `corpus/introcs/document.jsonl`: **243**
(`tests/test_task_score.py::test_load_objectives_count_is_243_not_the_61_marker_block_count`).
Reported as the measured figure; the "61" in earlier docs was itself never a claim about
objective count, just mislabelled once and repeated.

### 1.2 Coverage is scored against each system's whole generated document

Nothing aligns one objective to one generated section for either arm — B1's structure is
invented by the model, MARD's is driven by an extracted concept graph, and neither tracks the
textbook's own objective boundaries. `eval.groundtruth_scoring.score_overlap` (recall of a
short reference's stemmed tokens) is applied per objective against the **entire** candidate
document. This is the finest grain available without inventing an alignment step `docs/23`
never specified — but it is a real methodological choice with a consequence, below.

### 1.3 Results are near-ceiling for every system, and that is itself the finding

| Threshold | B1 mean (range) | MARD full mean (range) | A1s mean (range) | A1f mean (range) |
|---|---|---|---|---|
| 0.5 | 0.9808 (0.9588–0.9918) | 0.9877 (0.9835–0.9918) | 0.9945 (0.9918–0.9959) | 0.9877 (0.9835–0.9959) |
| **0.6 (default)** | **0.9424 (0.8971–0.9712)** | **0.9575 (0.9547–0.9630)** | **0.9739 (0.9712–0.9753)** | **0.9630 (0.9547–0.9712)** |
| 0.7 | 0.8491 (0.7490–0.9136) | 0.8765 (0.8683–0.8889) | 0.9424 (0.9342–0.9506) | 0.8875 (0.8642–0.9136) |

**Read this as a near-null on quality, not a MARD win.** Every system covers 85–99% of
objectives depending on threshold; the four configurations' ranges overlap at every
threshold; and B1's own within-system spread (e.g. 0.75–0.91 at threshold 0.7) is comparable
in size to the *between-system* gaps. This is very likely the whole-document-recall design
choice in §1.2 saturating: an objective is a handful of stemmed content words, and a
10,000+-word generated guide on the same subject matter contains most vocabularies somewhere
almost regardless of whether that guide is actually organised around the textbook's
objectives. **A per-section-aligned scorer would be a sharper test; none exists.** Whoever
writes paper §4 should not report B1-vs-MARD quality as a MARD win on this number — the
disjunction `docs/27` §3 T3 already anticipates ("quality and/or tokens... a win on either is
the claimed result") resolves here as a **null on quality**, with the token result in §1.4
carrying the O3 claim.

Full per-objective detail (`matched_tokens`/`reference_tokens` per objective, per run) is in
`eval/scoring_report.json` under each run's `objective_scores` — the number survives a
reviewer who wants to recompute at a different threshold without re-running anything.

### 1.4 Tokens, calls, cost, wall-clock — the real O3 differentiator

| | B1 (mean, range) | MARD full (mean, range) | A1s (mean, range) | A1f (mean, range) |
|---|---|---|---|---|
| Input tokens | 1,493,033 (516,875–3,315,432) | 94,242 (93,809–94,660) | 37,631 (36,443–38,561) | 78,064 (77,474–78,634) |
| Output tokens | 157,055 (53,775–273,866) | 112,399 (107,297–119,956) | 118,890 (118,517–119,344) | 107,189 (103,883–109,144) |
| Cost (USD) | $0.8323 ($0.3211–$1.6002) | $0.5784 ($0.5684–$0.5900) | $0.4976 ($0.4931–$0.5017) | $0.5241 ($0.5145–$0.5346) |
| Wall-clock (s) | 455.6 (152.9–776.5) | 443.3 (437.3–448.2) | 397.6 (393.1–400.8) | 434.7 (417.9–452.7) |
| Calls (Tier1 / Tier2) | varies 8-17 / 14-151 (self-authored, `docs/32`) | 15 / 84 (fixed) | 15 / 83-84 (fixed) | 15 / 83-84 (fixed) |

**Input tokens: B1 mean 1,493,033 vs MARD full mean 94,242 — a 15.84× reduction** (min-to-min:
B1's own best seed, 516,875, is still 5.5× MARD's worst seed). B1's seed 42 alone: 3,315,432
input tokens, $1.6002 — MARD's seed 42: 94,660 input tokens, $0.5767, **a 35× token
reduction on the seed where B1 also produced ungrounded content** (`docs/24`, `docs/32`).
Cost gaps are smaller than token gaps because B1's tokens are billed mostly at the cheap
Tier-2 rate while MARD's Tier-1 calls (gpt-5.2) are a larger fraction of its own total — the
token story and the cost story are not the same story, and both are reported rather than
collapsing to one.

**Call-count comparison needs a caveat B1's own architecture forces:** `docs/32` established
that B1's three seeds ran three structurally different self-authored programs — Tier1/Tier2
call counts of 8/14, 11/29, and 17/151 are not "the same system at three sample points," they
are three different systems. MARD's call counts are 15/84 (±1 for a merge) in every seed,
because its pipeline is fixed by construction (`eval/groundedness_mard.py`'s finding, §3
below). Comparing a mean call count across arms is therefore comparing a real number (MARD)
to the mean of three incommensurable numbers (B1) — reported here for completeness, not as a
claim either arm "makes fewer calls" in a way one summary statistic can carry.

---

## 2. Task B — forward-reference violations, book order vs Master Plan order

### 2.1 Method and the chapter-granularity limitation, stated plainly

`ingest.groundtruth.extract_cross_references` finds 50 in-text "Chapter N" mentions in
`corpus/introcs`; 33 are `forward` in book order (the O5 "before" count, unchanged, a property
of the document — identical for all nine runs). The "after" half compares the same 50
references against each run's compiled Master Plan, at **chapter granularity on both sides**:
a chapter's "position" is `min(plan position of every concept whose source page falls in that
chapter)`, the plan-order analogue of `page_start`. This is not a design preference — a
cross-reference only names a chapter, never a concept, so chapter granularity is the finest
grain the ground truth supports, and book order is scored the same way for the comparison to
be fair.

### 2.2 Correction, 28 Aug 2026 — chapters 10 and 13 were never missing

**Retracted.** This section originally reported chapters 10 and 13 as absent from the compiled
Master Plan's concept set in 8 of 9 runs, 20 of 50 references (40%) `unmappable` as a result.
That was wrong, and the error was in this document's own attribution code, not in Pass 1's
extraction. The concept-to-chapter mapping used `eval.ordering.chapter_for_page` — page-range
membership against `concept_graph.concepts[i].source.page_start` — and nearly every chapter
boundary in `corpus/introcs/chapters.json` overlaps its neighbour by exactly one page (chapter
N's `page_end` equals chapter N+1's `page_start`, since a chapter can begin partway down the
page the previous one ends on). `chapter_for_page` returned the *first* range match in book
order, which for a boundary page is always the earlier chapter — checked directly against one
run's 84 concepts, this silently misattributed 66 of them (79%), not only the handful that
would explain a 10/13-specific gap.

**Fixed by attributing through the concept's own `source.section_id`** against
`chapters.json`'s `section_ids` lists (`eval.ordering.chapter_for_section`,
`section_to_chapter_map`) — exact, no page arithmetic, no boundary ambiguity, and it is the
same citation already independently verified 100% correct against the corpus (§3.2 below).
**Re-run: every one of the 9 MARD-family runs covers all 14 chapters. Nothing is
`unmappable`, in any run.** `eval/ordering_report.json` and `tests/test_ordering.py::
TestRealRuns::test_no_references_are_unmappable_once_attribution_is_by_section_id` carry the
corrected figures.

### 2.3 The result: a clean null, exactly, in every one of the 9 runs

With attribution corrected, plan order matches book order's forward/backward split **exactly,
in all nine runs, at the full 50-reference count — not a subset**:

| System | Seed 11 | Seed 23 | Seed 42 |
|---|---|---|---|
| Book order (all seeds, all systems) | 33 forward / 17 backward | *(same)* | *(same)* |
| MARD full — plan order | 33 / 17 | 33 / 17 | 33 / 17 |
| A1s — plan order | 33 / 17 | 33 / 17 | 33 / 17 |
| A1f — plan order | 33 / 17 | 33 / 17 | 33 / 17 |

**The Master Plan does not reduce forward-reference violations relative to book order, at the
granularity this ground truth supports — the count is exactly identical to book order in every
one of the 9 logged runs, no exceptions.** This supersedes the previous draft's "small
regression for A1s": that finding also traced to the same page-boundary bug (the two "+2"
runs were seeds where a boundary-adjacent concept happened to flip a chapter's earliest
position under the wrong mapping). `docs/00-CLAIM.md` explicitly budgets for a null result
here; this is one, cleaner than first reported, and it is reported as such, not narrated
around.

**Why it comes out exactly equal: the compiled plan's *chapter-level* sequence is identical to
book order (1 through 14, strictly increasing) in every one of the 9 runs** —
`tests/test_ordering.py::TestRealRuns::test_mard_full_seed42_covers_all_14_chapters_in_book_
order` pins this for one run; the same pattern holds for all nine (`eval/ordering_report.json`
`plan_order_kept_chapter_only.forward == book_order.forward` in every row). Reordering that the
compile step does perform (`docs/28`'s `moves`/`moved_concepts`) happens **entirely within** a
chapter's own concepts — below the grain a chapter-level cross-reference can ever detect, for
every configuration, not just two of three. **This metric is measuring a real thing no MARD
configuration does at the chapter level (systematically reorder chapters relative to the
book), not failing to measure a thing one of them does.**

### 2.4 The alias/merge question, resolved

Nine runs, three concept-id merges — `mard` seed 23, `mard_a1` seed 11, `mard_a1f` seed 11
(one each; `docs/28` §3 documents only the first, the other two were found by reading each
run's own `mard_compile_plan` event directly rather than assumed absent). Primary mapping
attributes a merged concept to its kept chapter only; a secondary mapping additionally
attributes it to every chapter its pre-merge occurrences came from. **For all three affected
runs, the two mappings produce identical forward/backward/unmappable counts** — the choice
does not move the number (`eval/ordering_report.json`, `plan_order_kept_chapter_only` vs
`plan_order_with_aliases`).

---

## 3. Task C — groundedness over the MARD arm

### 3.1 The prediction, and what actually happened

`docs/24` §5 predicted MARD's groundedness rate would be "near 1.0, because
`orchestrate.briefs_for` constructs each brief from the plan's recorded source span." Reading
the frozen prompt-construction code directly (`orchestrate/lm_builder.py`'s `prompt_for`,
`envelope/pass1.py`'s `build_prompt`) and confirming it against every real, **fully logged,
untruncated** prompt in all nine runs' `calls.jsonl`: **no MARD prompt at any tier ever
embeds the document's own prose.** Tier 2 receives a concept label, a citation
(`Source: section {id}, pages {start}-{end}`), a plan position, and Tier 1's synthesised
directive — never the section's text. Tier 1 receives section ids and titles, never chapter
text. Token counts corroborate the code reading independently: Tier 2 prompts run 98-143
input tokens; an embedded excerpt would run into the thousands, as B1's `SOURCE:`-bearing
prompts actually do (`docs/32` §3).

**So under the literal criterion `eval.groundedness` applies to the vanilla arm — does the
generating call carry non-empty source *text* — every one of the 677 Tier 2 calls across all
nine runs is `ungrounded`, always, by architecture, not by failure.**

### 3.2 Attribution is separately, and perfectly, correct

`docs/24`'s prediction conflated two claims: *the model sees the source text* and *the model
is told the correct source*. MARD guarantees only the second, and does so completely: checked
against `corpus/introcs/sections.json` directly (not trusted from the plan's self-report),
**all 677 Tier 2 citations across all nine runs match their concept's true section and page
range exactly — zero `attribution_incorrect`.** B1's seed-42 failure (`docs/24` §1) mixed a
mismapped citation with missing text; MARD structurally cannot mismap (the citation comes from
`plan.models.SourceSpan`, not from the model re-deriving it), and structurally never has text.
These are the two separate, independently verified halves of what "near 1.0" was trying to
say in one number.

| | MARD full | A1s | A1f |
|---|---|---|---|
| Concepts scored (11 / 23 / 42) | 84 / 83 / 84 | 83 / 84 / 84 | 83 / 84 / 84 |
| Grounded (text present) | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Attribution correct | 84 / 83 / 84 | 83 / 84 / 84 | 83 / 84 / 84 |
| Regenerated | 0 / 0 / 0 | 0 / 0 / 1 | 0 / 0 / 1 |
| Template deviations | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Tier 1 text-grounded | No / No / No | No / No / No | No / No / No |

A concept count of 83 (instead of 84) is a compiler-side merge or a same-label-different-id
pair, not a missing concept — `eval/groundedness_mard.py` keys per-concept results by plan
**position** (parsed straight from the prompt), not by label, specifically because two
distinct concept ids were found sharing one label (`"abstraction-and-models"` vs
`"abstraction-and-modeling"`, both labelled "Abstraction and Modeling", `mard_a1` seed 42) —
keying by label would have miscounted that as one regenerated concept instead of two.

### 3.3 No `root_authored` case, and the s42 anomaly cannot reappear

`eval.groundedness`'s `root_authored` status exists for B1 concepts with no per-concept call
to inspect at all — a consequence of the root writing its own exploration code differently
each run (`docs/32`). MARD's Tier 2 fork always issues exactly one call per plan concept
(confirmed against every run), so nothing is ever `root_authored` here. And B1's seed-42
architectural divergence (`docs/32` §4) cannot reappear on this arm for the same underlying
reason: MARD's pipeline (Pass 0 → Pass 1 → compile → Tier 2 fork/join) is fixed by
construction, not self-authored, and its own cost/wall-clock are near-identical across all
three seeds ($0.568–$0.590, 437-448s, `docs/28` §4) — there is no mechanism left for one seed
to invent a different architecture.

### 3.4 What this means for §4

This is a finding about MARD, reported whatever it is, per `docs/24` §5's own instruction:
**MARD's faithfulness claim should rest on `attribution_correct` (100%, verified against the
corpus) and the typed-contract failure-loud arguments `docs/24` §3 already makes
(`IncompleteArtefactError`, plan validation), not on literal text-grounding — MARD does not
have any, at either tier, in any run.** Presenting MARD as "grounded" in the same sense B1's
34 grounded concepts are would overclaim in exactly the direction `docs/23` §1 already warned
against for a different measurement.

---

## 4. What could not be measured, and why

- **A per-section-aligned task-score metric** (§1.3) — no alignment ground truth exists
  between learning objectives and generated sections for either arm; building one was out of
  scope here and would need a Track 3 decision, not an assumption made inside a scoring
  script.
- ~~Forward-reference violations for chapters 10 and 13~~ — **retracted, §2.2.** Not a real
  gap: an earlier attribution bug in this document's own code, not a Pass 1 extraction gap. All
  14 chapters are covered in every run once concepts are attributed by `section_id` instead of
  page range.
- **`mis-sourced` groundedness** (carried over from `docs/24`/`docs/32`) — still not
  implemented for either arm; MARD's case is moot regardless, since nothing is `grounded` to
  begin with.

---

## 5. Checks

- `ruff check`, `ruff format --check`, `mypy` clean on everything under this brief's footprint.
- `scripts/preflight.sh` — see repo state at time of writing; no worse than found.
- No writes anywhere in `runs/`.
