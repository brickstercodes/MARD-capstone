# 27 — Implementation brief: scoring, figures, and filling the manuscript

**Paste this whole file as the first message of a fresh Claude Code session opened in
`~/Desktop/Capstone/MARD-capstone`.**

**Run this session only after the matrix is complete and frozen.** It converts logged runs
into a submittable paper. It does not produce runs, and it must not.

Written 27 Aug 2026, for the Saturday-afternoon-onward block.

---

## 0. Read first

1. **`docs/00-START_HERE.md`** — current state and standing rules.
2. `docs/30-MEASUREMENT_PROTOCOL.md` — including its banner. §1's seven fields decide what is
   admissible; §4's variance rule decides how it is reported.
3. `docs/24-GROUNDEDNESS_AND_SEED42.md` — **§2 and §4 in full.** The most likely way this
   session damages the paper is by tidying away the seed-42 result or printing an unverified
   count.
4. `docs/23-GROUNDTRUTH_SPEC.md` §6 — what §4 of the paper must disclose about ground-truth
   sources.
5. `docs/40-LITERATURE_LOG.md` — the citation gate.
6. `paper/main.tex` — read the whole file before editing it.

---

## 1. What you own

**Yours:** `paper/` (all of it), and any plotting or table-generation script you need.

**Read-only:** `runs/`, `corpus/`, everything else.

**You are the only session that writes to `paper/main.tex`.** Two agents editing one `.tex`
produces a conflict nobody has time to resolve.

---

## 2. The rules that make this session dangerous

Every one of these is a way to make the paper worse while appearing to improve it.

**Numbers come only from logged runs.** A figure that cannot be traced through
`runs/<run_id>/` to all seven `docs/30` §1 fields does not go in. If a number you need is
missing, the answer is a `\TODO`, not an estimate.

**After the results freeze, numbers are written up and never re-run.** A wrong result gets a
limitations paragraph. If a run looks bad, that is a finding.

**Do not average the three baseline repeats.** They are 156 / 190 / 75 concepts at
$0.32 / $0.58 / $1.60. `docs/30` §4 requires the spread be reported; here the spread *is* a
result — the baseline is unstable at document scale. A mean would delete the finding.

**No repeat was excluded, and the paper says so.** `docs/24` §2 gives the reason: a run is
re-runnable only when the *protocol* failed to execute. Seed 42's grounding failure is the
system under test behaving badly, which is a result. Do not soften this into an asterisk or
a footnote.

**"≥41 of 75" is `[UNVERIFIED]`** (`docs/24` §4) — it came from an intermediate counter, with
one concept verified by hand. Use the detector's count from `eval/groundedness.py`, or use
none.

**MARD's groundedness rate goes in whatever it is.** Reporting the baseline's failure while
omitting MARD's own rate is the same overclaim inverted.

**No citation without a verified row in `docs/40`.** Only two of the manuscript's seventeen
references have one. The citation-status block above the bibliography lists every
outstanding item — the SRLM title conflict, two unverified author lists, and a caution about
one reference that must never be cited for the claim it looks like it supports. Work through
it; do not delete it because it is untidy.

---

## 3. Tasks

### T1 — Fill the results tables

Every `\RESULT` in §4 comes from a logged run. Tables to fill: `tab:main` (B1 / A1 / MARD
with both deltas), `tab:grounding`, `tab:a2` if A2 ran, `tab:negcontrol`, and the cost rows
in `tab:cost`.

**The two edge-structure measures are the mechanism and belong in the paper**, not just in
the logs: **cross-chapter prerequisite edges** (edges whose endpoints sit in different
chapters) and **boundary rejections** reading `"names a concept that was never declared"`.
The prediction is that A1 collapses the first toward zero and spikes the second, because the
only channel carrying earlier concept IDs into a later prompt is the envelope's
`FINDINGS SO FAR` block, and `render()` returns `""` when stripped. If that prediction fails,
**report the failure** — it is the first direct test of whether the model *uses* the
envelope, as opposed to merely receiving it.

### T2 — Figure 1, panel (c)

Panels (a) and (b) exist. Panel (c) is a `\TODO` box awaiting MARD's concept graph for
*Linear Algebra Done Right*, rendered from the compiled Master Plan. It needs
`master_plan_trace.json` to report `compiled: true`.

**The panel must show prerequisite edges, not containment.** That distinction is the entire
point of the figure; a rendering that looks like another tree defeats it. If the plan for
that document does not exist, leave the stub and say so in the caption rather than
substituting a hierarchy.

### T3 — Write the prose that is still `% >>> PENDING` or `\TODO`

In dependency order: §4 results prose → §4.6 structure-dependence boundary → §4.7 structure
as a faithfulness mechanism → §6.1 limitations → **abstract results sentence** → §5
conclusion. Abstract and conclusion last, once the numbers are real.

The claim is a **disjunction** — quality and/or tokens. A win on either is the claimed
result. **A null is reported as a null**, framed by the O4 boundary, and is publishable.
Do not manufacture a positive framing for a null.

### T4 — Verification pass

- Every `\RESULT`, `\TODO` and `\VERIFY` resolved or consciously retained.
- **Delete the three macro definitions at the top of `main.tex`.** The document then fails to
  compile if any placeholder survived. That is the point — do this and fix what breaks.
- Every number traced back to a `runs/<run_id>/` once more, by hand.
- Page count checked. The guide requires **at least 10 pages**; the draft was at 10 with §4
  empty, so length is not a risk — do not cut for space.
- Recompile clean. Note that `IEEEtran.cls` may be missing locally; Overleaf has it.

---

## 4. Definition of done

- [ ] No `\RESULT` remains; every number traces to a logged run.
- [ ] The three baseline repeats are reported individually, not averaged, with an explicit
      statement that none was excluded.
- [ ] Groundedness reported for **both** arms.
- [ ] No unverified count anywhere; anything still uncertain marked `[UNVERIFIED]`.
- [ ] Cross-chapter edge counts and rejection counts reported for MARD and A1.
- [ ] Figure 1 panel (c) rendered from a compiled Master Plan, or the stub retained with the
      reason stated.
- [ ] Citation-status block worked through; unverified entries either verified or the claims
      resting on them removed.
- [ ] Macro definitions deleted; document compiles clean; ≥10 pages.
- [ ] Abstract and conclusion written last.

---

## 5. The disposition this session needs

The temptation here is to make the results look tidy. Resist it specifically:

- A wide spread is a finding, not noise to be smoothed.
- A failed baseline repeat is evidence, not an embarrassment.
- A null effect is publishable, and this project committed in advance to reporting one.
- An unverified number is worse than a missing one, because a missing one is visible.

`docs/24` §7 lists four claims this project got wrong and corrected — every one was caught by
running the thing rather than reasoning about it, and every one made the work better. That is
the standard for this session too.
