# 37 — Implementation brief: structural determinism (Track A) and per-chapter coverage (Track B)

**For the session that built `eval/` — the `docs/26` / `docs/35` agent.** Paste as a new
message; you keep your context and your ownership of `eval/`.

Written 28 Aug 2026. Both tracks use **existing runs only. No new model calls. $0.**

---

## 0. Read first

1. `docs/36-PLAN_PROVE_O3.md` — why these two tracks exist and what the paper will claim.
   §2 has numbers I measured by hand; **re-derive them, do not trust them.**
2. `docs/35-SCORING_RESULTS.md` — your own results. Track B replaces its §1 metric.
3. `docs/00-CLAIM.md` — structure and reproducibility are pre-existing claims, not new ones.

Then `scripts/preflight.sh`.

---

## 1. Footprint

**Yours:** new modules under `eval/`, their tests, `docs/38-DETERMINISM_RESULTS.md`.
**Read-only:** `runs/` — the `docs/25` session may be writing negative-control runs. Never write there.
**Do not touch:** `mard/`, `envelope/`, `orchestrate/`, `provider/`, `plan/`, `paper/`, `.vendor/`, `eval/frozen_subsets/`.

---

## 2. Track A — structural determinism and fidelity

The paper's new headline. Build `eval/structure.py`.

### A1. Parse structure from each artefact

For B1 (`artefacts/vanilla_answer.md`): markdown heading tree — count `^## ` and `^### `,
and record the heading texts. For MARD (`artefacts/master_plan.json` + `tier2_output.md`):
concept count, edge count, cross-chapter edge count from the plan; heading tree from the prose.

### A2. Determinism — variance across seeds, per system

Report per system: **n runs, values per seed, mean, min–max, and coefficient of variation**
for each of: top-level section count, subsection count, word count, and (MARD only) concept
count, edge count, cross-chapter edge count.

**Report the MARD edge variance prominently.** My hand count: concepts 84 in all 5 runs;
edges 124–136. The honest claim is *"deterministic scaffold, variable elaboration"* — not
"MARD is deterministic". A paper that reports its own system's variance is believed about the
rest; one that reports only the invariant number is not.

Exclude `*_smoke*` runs and the pre-fix MARD s11 runs (per `docs/28`); state in your doc
exactly which run ids you included and which you excluded, and why.

### A3. Fidelity — does the output match the book's real structure?

Ground truth: `corpus/introcs/chapters.json` — `chapter_count: 15`, `explored_by_pass1: 14`,
one unnumbered front-matter chapter excluded. **14 numbered chapters is the reference.**

Per run report: number of top-level sections, and how many map to a real book chapter vs are
**invented** (no corresponding chapter) or **absent** (a book chapter with no section).
B1 s42 appears to emit 16 top-level sections against a 14-chapter book — verify and
characterise the extra two rather than just counting them.

Note the B1 s11 case explicitly: 156 top-level sections, **0 subsections**. That run produced
a flat list, not a hierarchy. Say so plainly; it is the single most legible piece of evidence
in the whole study.

### A4. Provenance

Count resolvable source citations per artefact — a page range or section id that resolves
against `corpus/introcs/sections.json`. My hand count for B1: 0, 1, 0 across the three seeds.
For MARD, you already have 84/84 concepts carrying `source.section_id` and page range, 0 of
677 mis-cited (`docs/35`). Put both in one table.

---

## 3. Track B — per-chapter coverage re-score

`docs/35` §1.3 already names the problem: whole-document recall saturates at 94–97%, so the
metric cannot separate any two systems. Fix the granularity.

For each of the 14 numbered chapters: take that chapter's learning objectives, and score them
**only against the part of the output that corresponds to that chapter**, not the whole
document. Same `score_overlap`, same three thresholds (0.5 / 0.6 / 0.7), mean and min–max
across seeds.

The mapping from output to chapter is the hard part and is where the honesty lives:

- MARD: each concept carries `source.section_id`, so chapter attribution is exact.
- B1: attribution has to be inferred from the heading tree, and **for s11 it cannot be done at
  all** — 156 flat headings, no chapter structure to map to.

**Do not silently fall back to whole-document scoring for the runs you cannot map.** Report
them as unmappable. "One of three baseline runs cannot be scored per-chapter because it
emitted no chapter structure" is a finding about the baseline, not a gap in your method. If
you do also compute a whole-document fallback for comparison, label it as such in its own
column and never mix the two in one mean.

Report which chapters each system covers and which it misses. A system that covers 14/14
chapters at 80% beats one that covers 9/14 at 95%, and the current metric hides that.

---

## 4. Standing constraints

- Every number traces to a run id (`docs/30` §1, all seven fields).
- Three seeds, mean **and** spread. Never a single run as *the* number.
- A null result is reported as null. `docs/36` §5: we have enough without these two tracks;
  neither is permitted to be talked into a positive.
- Do not merge the seed-42 grounding anomaly (`docs/32`) into the determinism finding. Two
  independent observations, reported separately.
- The cross-chapter fraction stays MARD-internal. B1 has no concept graph (`result: null` in
  all three summaries) — it is never an O3 comparison.

## 5. Definition of done

- `eval/structure_report.json`, `eval/chapter_scoring_report.json`
- `docs/38-DETERMINISM_RESULTS.md` — the tables the paper lifts, with run ids, inclusions and
  exclusions, and an explicit list of what could not be measured and why
- tests for both modules; `scripts/preflight.sh` no worse than you found it
- **no writes in `runs/`**

Report back with: section-count spread per system, invented/absent chapter counts, resolvable
citations per system, and the per-chapter coverage table. Unrounded figures.

Track A before Track B. If time runs out, A alone carries the paper.
