# 36 — Plan: what O3 can and cannot claim, and how we get there

Written 28 Aug 2026, after `docs/35`. Presentation 29 Aug, paper 30 Aug.

---

## 1. Where we actually stand

`docs/35` returned three results. Read honestly they say:

| Axis | Result | Usable? |
|---|---|---|
| Explanation quality (objective coverage) | B1 94.2%, MARD 95.7%, ranges overlap | **No.** Metric saturates at 94–97% for everything. |
| Forward-reference violations | Clean null; plan order == book order at chapter level | **No.** Metric can't see within-chapter reordering. |
| Tokens / cost | 1.49M vs 94K input, 15.84× | **Yes, with a stated confound.** |

And one architectural finding that changes the framing: `orchestrate/lm_builder.py:75-83`
sends Tier 2 a concept label, a section id, a page range and a directive — **never the
document's prose.** 0 of 677 builder calls carried source text. So part of the 15.84×
reduction is MARD not reading. That must be stated, not hidden.

**Conclusion: the paper cannot claim MARD writes better explanations than vanilla RLM.**
Nothing in the logged data supports it and the deadline does not allow the experiment that
would.

---

## 2. What the data *does* support

Measured first-hand from the run artefacts on 28 Aug:

**Vanilla RLM's output structure is unstable across seeds.**

| Run | Top-level sections | Subsections | Words |
|---|---|---|---|
| B1 s11 | 156 | 0 | 21,410 |
| B1 s23 | 14 | 190 | 14,552 |
| B1 s42 | 16 | 75 | 17,645 |

Same document, same system, same config. One run emits a flat list of 156 items with no
hierarchy; one emits 14 chapters; one invents 16. The book has **14 numbered chapters**
(`corpus/introcs/chapters.json`: `chapter_count: 15`, `explored_by_pass1: 14`, one unnumbered
front-matter chapter excluded). Page citations across all three B1 runs: **0, 1, 0.**

**MARD's scaffold is invariant.**

| Run | Concepts | Edges | Cross-chapter |
|---|---|---|---|
| MARD s11 (a) | 84 | 126 | 121 |
| MARD s11 (b) | 84 | 136 | 130 |
| MARD s11 (c) | 84 | 124 | 115 |
| MARD s23 | 84 | 128 | 119 |
| MARD s42 | 84 | 133 | 119 |

**State this precisely: the concept set is deterministic, the edge set is not.** 84 every
time because the skeleton is computed from the verified corpus rather than sampled; edges
range 124–136 because they come from model judgement. Reporting the edge variance ourselves
is what makes the concept-count claim credible rather than overblown. Do not write
"MARD is deterministic." Write "MARD's scaffold is deterministic; its elaboration is not."

**Keep separate from the above:** the seed-42 grounding anomaly in `docs/32`. It is another
instance of vanilla's run-to-run variance, but it is a *different observation* with a
different mechanism. Two observations that agree are stronger than one merged number that a
reviewer can unpick.

---

## 3. The claim the paper makes

> Against a vanilla RLM baseline on the same document, MARD produces a **reproducible,
> structurally faithful, and provenance-auditable** artefact at **15.8× fewer input tokens**.
> On explanation coverage the two are indistinguishable under our metric, which saturates;
> we report that as a null and say why.

Four axes we can defend, one we concede. Conceding the quality axis in the paper's own voice
is what buys credibility for the other four.

The A1f ablation (cross-chapter linkage 91.7% → 1.4%, never-declared rejections 0 → 57 when
findings are suppressed) remains the causal evidence that the **envelope** produces the
structure. That is the mechanism claim and it is untouched by any of the above.

---

## 4. Tracks

**Track A — structural determinism and fidelity.** Free, no new runs, ~1h. `docs/37`.
**Track B — per-chapter coverage re-score.** Free, no new runs, ~1h. `docs/37`.
**Track C — grounded Tier 2.** ~$15, ~1.5h, Saturday morning, only if A and B land early.
Puts cited section text into the builder prompt and re-runs 3 MARD seeds, to remove the
"cheap because it doesn't read" confound. **Violates Feature Freeze A** (`CONTEXT.md` §3.4),
so it is reported as a *second configuration* beside the frozen one, never as a replacement.
If there is any doubt on Saturday morning, drop Track C. The paper does not need it.

**Not doing:** more vanilla seeds. The instability is the finding; more seeds cannot change it
and might tempt a post-hoc pick.

---

## 5. The line we do not cross

`CONTEXT.md` §3.4: never tune toward a positive result after the fact. Tracks A and B measure
things `docs/00-CLAIM.md` already names — structure and reproducibility are what MARD is
*for*. That is why they are legitimate to add now. If Track A or B comes back null, it goes
in the paper as null. We have enough without it.
