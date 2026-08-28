# 38 — Structural determinism, fidelity, and per-chapter coverage

**Status:** Recorded 28 Aug 2026 · Owner: Track 1 (`docs/26`/`docs/35` session) · Implements
`docs/37-HANDOFF_DETERMINISM_AND_CHAPTER_SCORING.md`

Code: [`eval/structure.py`](../eval/structure.py) (Track A),
[`eval/chapter_scoring.py`](../eval/chapter_scoring.py) (Track B). Data:
[`eval/structure_report.json`](../eval/structure_report.json),
[`eval/chapter_scoring_report.json`](../eval/chapter_scoring_report.json). Tests:
`tests/test_structure.py`, `tests/test_chapter_scoring.py`. Every run id used is the same
selection `eval.runs.select_run` resolved for `docs/35` — see that document §0 for the table;
not repeated here.

> ### ⚠️ AMENDED — 28 Aug 2026, three corrections, all verified against run artefacts
>
> **A.** `mard_chapter_texts` attributed MARD concepts to chapters via page range
> (`chapter_for_page`), which silently misattributed the majority of concepts near a chapter
> boundary (`docs/35` §2.2 has the full mechanism — every chapter boundary in
> `chapters.json` overlaps its neighbour by one page). This produced a false "chapters 10 and
> 13 missing from Pass 1" finding in §5 below. **Retracted and re-run**: attributed by
> `source.section_id` instead, all 11 MARD-family runs cover 14/14 chapters, 0 unresolved.
> **B.** `parse_mard` read `concepts_accepted` (Pass 1's pre-merge declaration count, uniformly
> 84) instead of `concept_graph.concepts`' real post-merge node count (83 in the three runs
> where a duplicate-id merge fired). §2.2 now reports both counts and why they differ.
> `docs/00`'s "deterministic scaffold, variable elaboration" framing is unchanged — 83-84 is
> still roughly 61× tighter than B1's own spread — but 83-84 is the honest figure, not 84
> rounded. **C.** The identical page-boundary bug, a third time: `ingest.groundtruth.
> extract_learning_objectives` attributed the ground-truth objectives themselves to chapters
> via `_chapter_for_page`. Fixed at the root (`ingest/groundtruth.py`, walk backward in block
> order to the nearest numbered heading; `extract_cross_references`'s citing-side
> classification fixed the same way, though it turned out not to change that function's
> output on the real corpus — see `docs/35`'s own amendment). **42 of 243 objectives sit on a
> shared boundary page; 39 move chapters** (chapter 11: 35→28, chapter 12: 11→15, chapter 10:
> 7→10, chapter 13: 14→17). §5 below is regenerated against the corrected objectives; the
> whole-document numbers in `docs/35` §1 are unaffected (they never grouped by chapter).

**Headline, not rounded:**

- Section-count spread: **B1 — chapter-level headings 20 / 14 / 16 (seeds 11/23/42),
  concept-level headings 156 / 190 / 75 (CV 0.3436). MARD full — concepts (post-merge)
  84 / 83 / 84 (CV 0.0056), edges 124 / 128 / 133 (CV 0.0287).**
- Invented/absent chapters (B1 seed 42, content-overlap threshold 0.3): **9 of 16 headings
  matched a real chapter, 7 invented; 5 of 14 real chapters matched no heading.** This is
  **not** a clean "14 matched + 2 extra" — see §3.3.
- Resolvable citations: **B1 0, 0, 0 across all three seeds** (revises `docs/36`'s hand
  count of "0, 1, 0" — re-derived and found lower, not higher). **MARD 84/84, 83/83, 84/84
  — every citation checked against the corpus directly, 0 incorrect** (`docs/35` §3.2, cited
  again here for the side-by-side table).
- Per-chapter coverage at threshold 0.6, pooled across all mappable (chapter, seed) pairs, with
  the corrected objective-to-chapter attribution: **B1 mean 0.6095 (37 scores) vs MARD full
  mean 0.6305 (42 scores) vs A1s 0.7263 vs A1f 0.6353.** A1s's lead holds whether the four
  most-reattributed chapters (10-13) are included or excluded (§5.4) — it is not an artefact
  of this correction. Compare to the whole-document numbers this replaces: B1 0.9424, MARD
  0.9575 (`docs/35` §1.3) — confirms the saturation diagnosis and recovers real spread the
  whole-document metric could not see.

---

## 1. Inclusions and exclusions

**B1:** the same three campaign runs as `docs/35` (seeds 11, 23, 42), `*_smoke*` excluded
(they never were candidates — different document ids/status).

**MARD full, seed 11 specifically — excluded two pre-fix attempts, kept one:**

| Run id | `compiled` | Edges | Cross-chapter | Why excluded / kept |
|---|---|---|---|---|
| `...4a62fd` (080609) | **`false`** | 126 | 121 | Compile crashed outright (`UnsequenceablePlanError`, the original id-collision bug, `docs/28` §3) — no `master_plan.json`, nothing to parse |
| `...a38379` (081414) | `true` | 136 | 130 | Compiled under the **reject-duplicate-id** fix, before the merge policy landed (`docs/28` §4) — different code, not a seed-variance data point |
| **`...13de68` (082226)** | `true` | **124** | **115** | **Kept — the merge-policy fix, the version every other number in this project (`docs/35`, this doc) is computed against** |

`docs/36` §2's own hand-derived table listed all three as "MARD s11 (a/b/c)" — mixing two
different code versions into what reads as seed-to-seed variance. `docs/37`'s instruction to
exclude pre-fix runs is followed literally: **Track A's MARD determinism numbers use only the
post-fix run for every seed**, i.e. the same three runs `docs/35` already used
(`eval.runs.select_run`'s normal selection, unchanged). A1s and A1f have no pre-fix history to
exclude — both were built after the merge-policy fix landed.

---

## 2. Track A2 — structural determinism

### 2.1 B1

| Seed | Chapter-level headings | Concept-level headings | Words |
|---|---|---|---|
| 11 | 20 (level 1) | 156 (level 2) | 21,410 |
| 23 | 14 (level 2) | 190 (level 3) | 14,552 |
| 42 | 16 (level 2) | 75 (level 3) | 17,645 |

| Metric | Values | Mean | CV |
|---|---|---|---|
| Chapter-level heading count | 20 / 14 / 16 | 16.7 | 0.1497 |
| Concept-level heading count | 156 / 190 / 75 | 140.3 | 0.3436 |
| Word count | 21,410 / 14,552 / 17,645 | 17,869.0 | 0.1573 |

**Which heading level counts as "chapter" vs "concept" is inferred, not declared by any run**
— see `eval/structure.py`'s module docstring for the exact rule (most-populated level =
concept level; the next-most-populated level with more than one heading = chapter level,
applied identically to all three runs with no per-seed tuning). It recovers a genuine, if
messy, chapter-grouping attempt in seed 11 that a bare "156 top-level, 0 subsections"
description elides: **seed 11's level-1 headings are mostly `"Chapter N"`, but repeat** —
`Chapter 2`, `Chapter 4`, and `Chapter 6` each appear twice, `Chapter 7` three times, 19
markers naming only 13 distinct numbers (plus the document's own title as a 20th level-1
heading). **The concept level (156, level 2) is genuinely flat — zero level-3 headings under
any of them** — but "flat list, no hierarchy at all" undersells it: there is an attempted,
broken chapter grouping one level up.

### 2.2 MARD (full, A1s, A1f)

**Two concept counts exist, and they disagree, and that is `compile_plan.py`'s duplicate-id
merge doing its job.** `summary.json`'s `result.concepts_accepted` counts Pass 1's raw
*declarations* per chapter — uniformly 84 across every one of the 9 logged runs, because it is
recorded before `compile_plan.py` ever runs and cannot see what compile does next.
`master_plan.json`'s `concept_graph.concepts` is the compiled plan's real node count — **after**
same-id concepts declared in two different chapters are collapsed into one (`docs/28` §3), and
it is 83 in exactly the three runs where that merge fired (`mard` seed 23, `mard_a1` seed 11,
`mard_a1f` seed 11 — §3.4 of `docs/35`, independently rediscovered here). **`concept_graph`'s
count is the correct one for determinism** — it is what the plan actually contains, not what
Pass 1 proposed before deduplication.

| System | Concepts, pre-merge (`concepts_accepted`) | Concepts, post-merge (`concept_graph`) | Edges | Cross-chapter edges |
|---|---|---|---|---|
| MARD full | 84 / 84 / 84 (CV 0.0000) | 84 / **83** / 84 (CV **0.0056**) | 124 / 128 / 133 (CV 0.0287) | 115 / 119 / 119 (CV 0.0160) |
| A1s (`mard_a1`) | 84 / 84 / 84 (CV 0.0000) | **83** / 84 / 84 (CV **0.0056**) | 140 / 151 / 138 (CV 0.0400) | 123 / 132 / 130 (CV 0.0301) |
| A1f (`mard_a1f`) | 84 / 84 / 84 (CV 0.0000) | **83** / 84 / 84 (CV **0.0056**) | 50 / 48 / 39 (CV 0.1048) | 1 / 1 / 0 (CV 0.7071*) |

\* A1f's cross-chapter count is near zero by design (`docs/28` §6.3 — findings suppression
collapses cross-chapter linkage to 1.4% mean); CV is a poor summary next to a near-zero mean
and is reported for completeness, not as evidence of "more variable" — the *absolute* spread
(0-1 edges) is smaller than any other row's, even though the *relative* figure is largest.

**Stated precisely, per `docs/36` §2's own instruction:** the concept set is *near-perfectly*
deterministic — 83 or 84 in all nine logged runs, CV 0.0056 for the post-merge count, never
anything else — because it is built by collapsing declarations against the verified corpus's
own section structure, not sampled freely from the model. **83-84 is still roughly 61× tighter
than B1's own concept-count CV of 0.3436** (§2.1) — an order of magnitude and then some — so
"deterministic scaffold" survives the correction; it is simply not *exactly* zero-variance, and
reporting the pre-merge 0.0000 alongside it would have hidden the one place where it isn't.
The edge set is far less constrained: it comes from Tier 1's own judgement per chapter, and CV
of 0.029-0.105 across the three configurations is real, reported, and non-zero. **"MARD's
scaffold is deterministic; its elaboration is not"** — never "MARD is deterministic" on its
own, which would overclaim both halves by omission.

**Kept separate, per `docs/37` §4:** the seed-42 grounding anomaly (`docs/32`) is B1's
instability in *content faithfulness*; this section is instability in *structural shape*
(B1) versus *elaboration volume* (MARD). Two independent observations from two different
mechanisms, not merged into one variance number.

### 2.3 MARD's prose carries no heading structure at all

Checked directly against `tier2_output.md` in all nine runs: **0 lines starting with `#` in
8 of 9; 8 lines in one** (`mard_a1f` seed 42 — one Tier 2 builder's own prose choice, not a
pipeline behaviour, and too small a sample to characterise further). MARD's structure lives
entirely in the typed `master_plan.json`, independently checkable from the prose it produced
— it is never inferred from headings the way every B1 number in this section is.

---

## 3. Track A3 — fidelity against the 14-chapter reference

`corpus/introcs/chapters.json`: `chapter_count: 15`, `explored_by_pass1: 14`, one unnumbered
front-matter chapter excluded — **14 numbered chapters is the reference set**, matching
`docs/37`.

### 3.1 B1 seed 23 — clean

All 14 headings are literally `"Chapter 1"`..`"Chapter 14"`. Matched by explicit number, no
fuzzy scoring needed: 14/14 matched, 0 invented, 0 absent.

### 3.2 B1 seed 11 — matched despite the repeats

19 of 20 level-1 headings are `"Chapter N"` for some real N (the 20th is the document's own
title, correctly left unmatched). Because repeated occurrences of the identical heading text
resolve to the identical chapter, **all 14 real chapters are covered** — 19/20 matched, 1
invented (the title), 0 absent. `docs/37` did not ask this be checked for seed 11 specifically
(only seed 42 is named), but the same matcher runs uniformly over every B1 run, so this is
reported too.

### 3.3 B1 seed 42 — not a clean "14 matched + 2 invented"

`docs/37` §2 anticipated roughly this shape for seed 42's 16-vs-14 heading count. The
mechanical result, at the stated content-overlap threshold (0.3), is messier:

| Automated match (score ≥ 0.3) | Unmatched (`invented`) |
|---|---|
| 9 of 16 headings, 9 of 14 chapters | 7 of 16 headings |

Absent chapters (no heading cleared the threshold): **9, 10, 11, 12, 14.**

**The mechanical count is not the last word — short chapter titles make automated matching an
approximate instrument (`eval/structure.py`'s own module docstring), and reading all 16
headings against the 14 real chapters by hand gives a different, more informative picture
than "14 correct + 2 extra":**

- Modules 2, 3, 6, 7, 8, 9 (`"Problem Solving..."`, `"Data Representation..."`, `"Data
  Structures..."`, `"Algorithms & Complexity..."`, `"Graph Algorithms..."`,
  `"Computability..."`) all draw on real chapters 3 ("Data Structures and Algorithms") and 4
  ("Models of Computation") — **the model split two real chapters into six finer-grained
  modules**, not invented content from nothing.
- Module 14 (`"Software Engineering & Architecture"`) folds real chapters 9 and 10
  ("Software Engineering Fundamentals", "Patterns Management") into one module — chapter 10
  has no module of its own anywhere in the 16.
- Module 12 (`"Networking & Internet"`) has no real single-chapter counterpart at all — the
  book covers networking only as part of chapter 11's web-applications material, never as its
  own chapter.

**So seed 42's structure is a genuine curriculum reorganisation — heavy subdivision in one
area (algorithms/data structures/theory, 2 real chapters → 6 modules), a fold in another
(9+10 → 1 module), and one module with no book-chapter counterpart — not simply "the right 14
plus 2 invented ones".** Report it this way; the mechanical table is supporting evidence, not
the finding itself.

---

## 4. Track A4 — resolvable citations

| System | Seed 11 | Seed 23 | Seed 42 | Method |
|---|---|---|---|---|
| B1 | 0 | 0 | 0 | page-number or resolvable-`section_id` citation found in `vanilla_answer.md` |
| MARD full | 84/84 | 83/83 | 84/84 | `attribution_correct` / `total_concepts`, `docs/35` §3.2 |

**B1: re-derived at 0, 0, 0 — not `docs/36`'s hand-counted "0, 1, 0".** Searched directly for
page citations (`page \d+`, `p\.\s*\d+`, `pp\.\s*\d+`) and for literal `introcs.<section-id>`
strings resolving against `corpus/introcs/sections.json`; neither construct appears anywhere
in any of the three runs. The only false-positive risk checked and excluded: "page" appears
56, 37, and 39 times respectively, but every occurrence is operating-systems vocabulary
("page table", "page fault", "demand paging") — a computer-science *topic*, never a citation
to the textbook's own pagination. `docs/36`'s "1" for seed 23 does not reproduce under this
search and is treated as superseded, the same discipline `docs/28` §4 already applied to a
different figure.

**MARD: every one of 677 citations across all nine runs (not just the three in this table)
resolves, and resolves correctly** — repeating `docs/35` §3.2's number here because Track A4
explicitly asks for it beside B1's in one table, not because it is newly measured.

---

## 5. Track B — per-chapter coverage

### 5.1 Correction, 28 Aug 2026 — chapters 10 and 13 were never missing

**Retracted.** This section originally reported MARD-family runs reaching a consistent 12/14
chapters, missing 10 and 13 in nearly every run, and read that as a Pass 1 extraction gap. It
was the identical bug `docs/35` §2.2 retracted: `mard_chapter_texts` attributed a Tier 2
response's chapter via `chapter_for_page` against its cited page range, and — because nearly
every chapter boundary in `chapters.json` overlaps its neighbour by one shared page — that
systematically misattributed concepts near a boundary to the earlier chapter. Fixed by
attributing through the same verified `section_id` citation (`chapter_for_section`) instead.
**Re-run: all 14 chapters are mappable in all 11 MARD-family runs** (`tests/test_chapter_
scoring.py::TestRealRuns::test_mard_full_covers_all_14_chapters_in_every_seed`).

### 5.2 Chapters each system reaches

| System | Seed 11 | Seed 23 | Seed 42 | Always mappable (all 3 seeds) |
|---|---|---|---|---|
| B1 | 14/14 | 14/14 | 9/14 | 9/14 |
| MARD full | 14/14 | 14/14 | 14/14 | **14/14** |
| A1s | 14/14 | 14/14 | 14/14 | **14/14** |
| A1f | 14/14 | 14/14 | 14/14 | **14/14** |

**Every MARD-family run reaches all 14 chapters, in every seed, every configuration.** B1
reaches all 14 only when it happens to produce a usable chapter structure at all (2 of 3
seeds) — seed 42's own heading fidelity gap (§3.3) is what costs it 5 chapters, not a Pass 1
extraction gap on MARD's side. **The coverage-reach axis `docs/37` §3 asked this track to
recover is therefore closer than the retracted draft suggested: both systems reach 14/14 when
their own structure lets them, and B1's shortfall is a structural-fidelity story (§3), not a
"MARD misses two chapters" story.**

### 5.3 Per-chapter coverage at threshold 0.6

**Regenerated after the third correction** (banner, item C): `ingest.groundtruth.
extract_learning_objectives` re-attributed 39 of 243 objectives to a different chapter once
attribution went through the nearest preceding heading instead of page range — chapter 11
loses 7 objectives (35→28), chapter 12 gains 4 (11→15), chapter 10 gains 3 (7→10), chapter 13
gains 3 (14→17). Every table below reflects the corrected reference set.

Blank = unmappable in that seed (B1 seed 42 only — every MARD-family cell is filled).

| Ch | B1 (11/23/42 → mean) | MARD full (11/23/42 → mean) | A1s (11/23/42 → mean) | A1f (11/23/42 → mean) |
|---|---|---|---|---|
| 1 | .583/.500/.583 → **.556** | .167/.583/.333 → **.361** | .750/.667/.667 → **.694** | .417/.333/.500 → **.417** |
| 2 | 1.00/.857/.286 → **.714** | .429/.571/.571 → **.524** | .714/.429/.571 → **.571** | .571/.429/.571 → **.524** |
| 3 | .800/.550/.650 → **.667** | .600/.450/.450 → **.500** | .700/.550/.600 → **.617** | .550/.550/.600 → **.567** |
| 4 | .923/.615/.615 → **.718** | .846/1.00/.923 → **.923** | .769/.769/.538 → **.692** | .846/.923/.615 → **.795** |
| 5 | .650/.350/.400 → **.467** | .400/.600/.550 → **.517** | .700/.800/.800 → **.767** | .350/.400/.400 → **.383** |
| 6 | .733/.400/.000 → **.378** | .800/.667/.667 → **.711** | .667/.800/.733 → **.733** | .933/.933/.733 → **.867** |
| 7 | .550/.600/.150 → **.433** | .650/.550/.800 → **.667** | .600/.550/.550 → **.567** | .600/.600/.650 → **.617** |
| 8 | .571/.257/.143 → **.324** | .514/.429/.543 → **.495** | .743/.714/.743 → **.733** | .400/.486/.686 → **.524** |
| 9 | .727/.545/— → **.636** (n=2) | .545/.455/.727 → **.576** | .727/.909/.818 → **.818** | .727/.909/.455 → **.697** |
| 10 | 1.00/.900/— → **.950** (n=2) | .800/1.00/.900 → **.900** | .800/1.00/1.00 → **.933** | .900/.800/.900 → **.867** |
| 11 | 1.00/.786/— → **.893** (n=2) | .643/.929/.714 → **.762** | 1.00/1.00/.857 → **.952** | .500/.857/.964 → **.774** |
| 12 | .667/.667/— → **.667** (n=2) | .667/.533/.800 → **.667** | .800/.867/.800 → **.822** | .600/.800/.733 → **.711** |
| 13 | .941/.765/.235 → **.647** | .647/.471/.706 → **.608** | .647/.824/.882 → **.784** | .706/.765/.588 → **.686** |
| 14 | .850/.700/— → **.775** (n=2) | .500/.750/.600 → **.617** | .400/.500/.550 → **.483** | .300/.500/.600 → **.467** |

Pooled across every (chapter, seed) pair that is mappable — the real headline, replacing
`docs/35` §1.3's saturated whole-document number:

| System | n scores | Mean | Min | Max |
|---|---|---|---|---|
| B1 | 37 | **0.6095** | 0.000 | 1.000 |
| MARD full | 42 | **0.6305** | 0.167 | 1.000 |
| A1s | 42 | 0.7263 | 0.400 | 1.000 |
| A1f | 42 | 0.6353 | 0.300 | 0.964 |

**Whole-document fallback, same runs, kept in its own column, never averaged with the above
(unaffected by this correction — it never grouped by chapter):**

| System | Mean | Range |
|---|---|---|
| B1 | 0.9424 | 0.8971-0.9712 |
| MARD full | 0.9575 | 0.9547-0.9630 |
| A1s | 0.9739 | 0.9712-0.9753 |
| A1f | 0.9630 | 0.9547-0.9712 |

**Per-chapter scoring recovers real, wide spread (0.000-1.000) the whole-document metric could
not see. MARD full's pooled mean (0.6305) edges ahead of B1's (0.6095), and A1s's (0.7263)
leads both** — still not the clean, one-number "MARD wins on quality" claim `docs/36` §1
already ruled out for the whole-document metric, but a real, checkable gap. B1's spread is
driven by individual weak chapters (6 and 8 are its worst — 6 hits exactly 0.000 in seed 42)
and by seed 42's structural-fidelity gap (§3.3), which costs it 5 chapters' worth of scoring
entirely rather than scoring them low. Whoever writes paper §4 should present the
coverage-reach table (§5.2) alongside this pooled mean, not the mean alone.

### 5.4 Re-checking the A1s lead against the reattribution

A1s's lead is the largest single number this brief produced, and it was flagged for a second
look precisely because chapters 10-13 — the four most reattributed by the objectives fix — are
also where A1s scores best (§5.3's table: 0.933, 0.952, 0.822, 0.784). Splitting the pooled
mean into "the four reattributed chapters" versus "the other ten" answers whether the lead is
an artefact of the correction:

| System | All (n=37-42) | Chapters 10-13 (n=9-12) | Chapters 1-9,14 (n=28-30) |
|---|---|---|---|
| B1 | 0.6095 | 0.7734 | 0.5568 |
| MARD full | 0.6305 | 0.7341 | 0.5890 |
| A1s | **0.7263** | **0.8731** | **0.6676** |
| A1f | 0.6353 | 0.7595 | 0.5856 |

**A1s leads on both halves, not just the reattributed one.** Every system scores higher on
chapters 10-13 than on the rest (these four happen to be well-covered material across the
board — not an A1s-specific effect), but A1s's margin over the other three configurations
holds on the *unaffected* ten chapters (0.6676 vs 0.5568-0.5890) just as it does overall. **The
lead is real, not a reattribution artefact** — though it remains a finding that fell out of
this correction rather than the brief's original focus, and still deserves the same scrutiny
any single-number lead gets before it goes in the paper (docs/34's standing seed-policy and
null-result rules apply to it exactly as to any other number here).

---

## 6. What could not be measured, and why

- **A true concept-level (not chapter-level) fidelity check for B1** — no ground truth maps
  individual textbook concepts to individual generated headings; only "Chapter N" is checkable
  against `corpus/introcs/chapters.json`.
- **Per-chapter coverage for B1 seed 42's 5 of 14 gaps** — genuinely unmappable given that
  run's own heading structure (§3.3), not a method limitation left unaddressed. (MARD-family
  runs have no such gap after §5.1's correction — all 14 chapters are mappable in every run.)

---

## 7. Checks

`ruff check`, `ruff format --check`, `mypy` clean on everything under this brief's footprint.
`scripts/preflight.sh` — full suite passes; no worse than found (real-data integration tests
in this project's style make the full run take several minutes, unchanged from before this
brief). No writes anywhere in `runs/`.
