# 28 — MARD arm: findings from the first real runs

**Status:** Living, opened 28 Aug 2026 · Owner: Track 1 · Read by: the results/manuscript
session (`docs/27`) before writing §4

Everything here came out of actually running the arm. Recorded as it happened, because three
of the four items would have been invisible in a summary.

---

## 1. The async/sync mismatch is fixed and confirmed

`provider/sync_seams.py` bridges the async seams to the sync protocols in
`envelope/pass0.py` and `envelope/pass1.py`. Verified offline **and against the live API**:
one real chapter yielded 6 concepts and 8 edges with zero coroutine-rejection entries in the
trace.

`docs/25` §2's prediction — coroutine returned, all 14 chapters rejected, empty plan, **no
exception** — was correct, and the fix is the one that brief specified: adapters in
`provider/`, frozen `envelope/` modules untouched.

---

## 2. Tier 2's token budget was silently too tight — and the join caught it

The first full MARD run (seed 11) failed with `IncompleteArtefactError`. **15 of 84 Tier 2
builder calls returned empty content having spent their entire 2048-token budget on
invisible reasoning tokens** — `gpt-5-mini` is a reasoning model. From `calls.jsonl`, every
empty response shows `output_tokens == 2048` exactly.

**This is a result, not merely a fix.** `join_in_plan_order`'s non-empty check is a design
decision the manuscript already claims (§3.1.5, and Table I's *empty generation* row). On the
first real run it caught a genuine failure that would otherwise have produced an artefact
short by fifteen sections, with every identity check satisfied and a complete-looking log.
**§4 should say so.**

**Fix:** Tier 2 budget raised to 4096 and `reasoning_effort="low"` set at that call site, in
`mard/run.py` rather than in the shared `provider/seams.py` defaults.

**Two consequences that must not be lost:**

- **`reasoning_effort="low"` is a behaviour change, not a budget change.** It belongs in the
  config snapshot and must be named in §3.2 as a per-tier setting. "Were both tiers at the
  same reasoning effort?" is a question a reviewer will ask, and the answer has to be in the
  paper rather than in a commit message.
- **The 69 successful calls used 608–1993 tokens, median 1510 — the old cap was marginal for
  them too.** An explanation truncated at, say, 1900 tokens does not hit the cap exactly, so
  the empty check never sees it: it simply ends mid-sentence and scores as complete.
  **Check the successful outputs for mid-sentence endings** before any of them is scored.

---

## 3. Duplicate concept ids across chapters — a latent bug in a frozen module

After the budget fix, seed 11's Tier 1 and Tier 2 completed cleanly, and
`compile_master_plan` raised `UnsequenceablePlanError` **with an empty list of implicated
concepts** — nonsensical on its face, and the tell that it is not a real cycle.

**Cause:** chapter 3 and a later chapter each independently declared a concept with the id
`abstraction-and-modeling`. `envelope/pass1.py` deduplicates ids *within* one chapter's call
and never *across* chapters, so `concepts` is a flat list with 84 entries and 83 unique ids.
`compile_plan.py`'s `_topological_order` collapses by id, finds fewer ordered nodes than
input entries, and takes the same branch a genuine cycle would.

### Resolution: merge, do not reject

**A duplicate id is signal, not noise.** Two chapters declaring the same concept means the
model recognised that the book teaches abstraction in chapter 3 and again later. A concept
graph is a graph over *concepts*, not over *(chapter, concept)* pairs, so the correct
behaviour is **one node carrying edges from both chapters**.

Rejecting the second declaration would have been the faster fix and would have **silently
reduced cross-chapter structure — the exact quantity being measured.** Collapse by id, union
the source spans and provenance, keep every edge.

### Why the feature freeze does not block this

`CONTEXT.md` §3.4 protects *measurements*, and there are none to protect: no MARD number
exists (seed 11 crashed), and B1's three runs never touch `compile_plan.py` — vanilla never
compiles a Master Plan. **The fix invalidates nothing.**

---

## 4. Re-measured — 115 of 124 edges cross-chapter (was `[UNVERIFIED]` at 121/126)

**Re-measured 28 Aug 2026, seed 11, post-fix (merge policy, `reasoning_effort="low"`,
`tier2_max_tokens=4096`), run `20260828T082226__mard__introcs__s11__13de68`: 84 concepts, 124
edges, 115 cross-chapter (92.7%).** `compiled: true`, artefact joined, cost $0.59. No
concept-id collision occurred in this particular run (`concepts_merged: []` in the compile
trace) — the merge path from §3 is confirmed present and correct but was not itself exercised
by this seed; it will be exercised whenever a future run does collide, rather than crashing.

The number moved (126→124 edges, 121→115 cross-chapter) between the buggy run and this one
because the buggy run's edge/concept counts were themselves computed over the pre-merge,
duplicate-laden data. **115/124 is the number to cite**, not 121/126 — that figure is
superseded, not merely unverified, and should not appear in the manuscript even with a
caveat.

An intermediate run (`...a38379`, the earlier reject-based fix, before the merge policy
landed) produced 84 concepts / 136 edges / 130 cross-chapter — also superseded, kept on disk
for the record but not a candidate number either.

**All three campaign seeds now complete, post-fix, `docs/30` §4's 3-repeat requirement met:**

| Seed | Concepts | Edges | Cross-chapter | Fraction | Never-declared | Cost | Wall-clock |
|---|---|---|---|---|---|---|---|
| 11 | 84 | 124 | 115 | 92.7% | 2 | $0.590 | 444.4s |
| 23 | 84 | 128 | 119 | 93.0% | 4 | $0.568 | 437.3s |
| 42 | 84 | 133 | 119 | 89.5% | 0 | $0.577 | 448.1s |

**Cross-chapter fraction: mean 91.7%, spread 89.5–93.0% (range 3.5 points).** Concept count is
identical (84) across all three seeds — a coincidence worth noting, not assumed to be
structural. Edge count and never-declared-rejection count both vary seed to seed, as expected
from real (non-deterministic) sampling — reported as spread, not averaged away
(`docs/30` §4). Runs: `...s11__13de68`, `...s23__d03195`, `...s42__548fe0`.

The concept-id merge path (§3) fired for real exactly once across the three seeds — seed 23,
chapters 11 and 12 both independently producing `microservices-and-service-decomposition`,
correctly collapsed to one node (chapter 11's declaration kept, chapter 12's folded into
`aliases`, both recorded in `concepts_merged`) rather than crashing. Seeds 11 and 42 had no
collision.

**Truncation re-checked on all three seeds' Tier 2 outputs (84, 83, 84 non-empty
respectively) — zero flagged in any of them.**

**Mid-sentence truncation check (item 2, resolved):** scanned all non-empty Tier 2 outputs
from both the pre-fix run (69 of 84, at the old 2048 cap) and the merge-fix run (84 of 84, at
the new 4096 cap) for truncation signs (missing terminal punctuation, dangling
conjunction/article, unclosed code fence). **Zero flagged in either run.** The closest calls
to the old 2048 cap (1891–1993 tokens) all end on a complete sentence. The empty-content
failure mode was binary at the old cap — either the full budget went to invisible reasoning
and the visible answer was `""`, or the call finished cleanly with room to spare — not a
gradient of silent partial truncations.

**Per-tier `reasoning_effort` in the config snapshot (item 3, resolved):** every MARD run's
`manifest.json` now records `config.params.tier1_reasoning_effort` (`null` — provider
default, Tier 1 uses default effort) and `tier2_reasoning_effort` (`"low"`) as explicit,
separate fields, plus `tier2_max_tokens` (`4096`). Not just a commit-message note.

---

## 6. The original A1 run tested a different hypothesis than intended — relabelled A1s

**Corrected framing (Anugrah, 28 Aug 2026): the first A1 run did not contradict the
"cross-chapter edges depend on the envelope" hypothesis. It never tested it.** The ablation
removed the skeleton, not the findings channel; findings survived, so — exactly as the
hypothesis predicts — the cross-chapter edges that findings carry survived too. That is a
consistent result, not a disconfirming one, and the runs are relabelled **A1s** (skeleton
removed) below rather than treated as a failed A1. §6.3 covers the cut that actually tests the
hypothesis.

### 6.1 What A1s measured

| System | Seed | Concepts | Edges | Cross-chapter | Fraction | Cost | Input tokens |
|---|---|---|---|---|---|---|---|
| MARD full | 11 | 84 | 124 | 115 | 92.7% | $0.590 | 94,258 |
| MARD full | 23 | 84 | 128 | 119 | 93.0% | $0.568 | 93,809 |
| MARD full | 42 | 84 | 133 | 119 | 89.5% | $0.577 | 94,660 |
| **MARD full — mean** | | | | | **91.7%** (range 89.5–93.0%) | $0.578 | 94,242 |
| A1s (skeleton removed) | 11 | 84 | 140 | 123 | 87.9% | $0.493 | 36,443 |
| A1s (skeleton removed) | 23 | 84 | 151 | 132 | 87.4% | $0.502 | 37,890 |
| A1s (skeleton removed) | 42 | 84 | 138 | 130 | 94.2% | $0.498 | 38,561 |
| **A1s — mean** | | | | | **89.8%** (range 87.4–94.2%) | $0.498 | 37,631 |

(These three runs are recorded on disk under `system: "mard_a1"`, the label current at the
time they ran — the run directories and `manifest.json` are not renamed after the fact; "A1s"
is this document's name for that same data going forward, and the code's `ablation=` value
for new runs is now `"a1s"` directly — see §6.3.)

### 6.2 Why the skeleton-only cut leaves cross-chapter structure essentially unchanged

**Confirmed by reading the trace, not inferred.** Every A1s run's final envelope snapshot
(`runs/<run_id>/envelope/pass_1_final.json`) shows `skeleton_sections: 0` (the skeleton
genuinely never renders) but `findings_total: 14` and `rendered_chars` in the 12,000–13,000
range — the envelope is not empty. `Envelope.stripped()`'s `is_stripped` property requires
`skeleton.is_empty and not findings and directive is None` (`envelope/envelope.py`).
`envelope.pass1.run_pass1` — frozen, not editable here — calls
`envelope.for_child(chapter.chapter_id, directive_for(chapter))` before every single chapter's
`render()`, and `directive_for` always returns a non-empty string. So `is_stripped` is `False`
from chapter 1 onward for both arms alike, and `render()` falls through to its per-field
branches rather than short-circuiting to `""`. The skeleton block is correctly suppressed, but
the `## FINDINGS SO FAR` block is not gated by `is_stripped` at all — it renders whenever
`self.findings` is non-empty, and `with_findings` (called at the end of every chapter's
`run_pass1` iteration) keeps accumulating regardless of which envelope state the run started
from. **A1s removes the skeleton and nothing else — as named, that is exactly what it is
supposed to do.** It just is not the cut `docs/25` §T5 described as "the run that earns the
paper's title."

**A1s's real, verified effect: a genuine decomposition of the envelope's cost.** Tier 1 input
tokens drop to ~40% of MARD-full's (37,631 vs 94,242 mean) with cross-chapter structure
essentially unchanged (89.8% vs 91.7%, overlapping ranges). The skeleton is expensive to
render on every one of 14 chapter calls and contributes little to cross-chapter structure; the
findings channel is what carries it. That is a real, useful, keepable result about the
envelope's internal cost/benefit split — it simply answers "how expensive is the skeleton"
rather than "does the envelope drive cross-chapter structure."

### 6.3 A1f — the cut that actually tests the hypothesis

Built and run 28 Aug 2026 (Anugrah's call — the results-freeze exception is the same one that
covered the §3 id-collision fix: no existing measurement is invalidated, A1s is relabelled
rather than discarded). `envelope/envelope.py` gains `suppress_findings: bool = False` (a new
field with a safe default — every existing caller is unaffected) and
`Envelope.findings_suppressed()`, the skeleton-kept complement to `.stripped()`: findings still
accumulate onto `self.findings` exactly as in MARD full (so `findings_total` still reports the
true count), but `render()`'s `FINDINGS SO FAR` block is gated on `suppress_findings` and never
appears. `mard/run.py`'s `ablation=` now takes `"a1s"` (renamed from the original `"a1"`) or
`"a1f"`.

**The hypothesis is confirmed. All three seeds complete.**

| System | Seed | Concepts | Edges | Cross-chapter | Fraction | Never-declared | Cost |
|---|---|---|---|---|---|---|---|
| A1f (findings suppressed) | 11 | 84 | 50 | 1 | 2.0% | 67 | $0.535 |
| A1f (findings suppressed) | 23 | 84 | 48 | 1 | 2.1% | 49 | $0.515 |
| A1f (findings suppressed) | 42 | 84 | 39 | 0 | 0.0% | 55 | $0.523 |
| **A1f — mean** | | | | | **1.4%** (range 0.0–2.1%) | 57.0 | $0.524 |

Contrast with §6.1: MARD full mean 91.7% (range 89.5–93.0%), A1s mean 89.8% (range
87.4–94.2%), **A1f mean 1.4% (range 0.0–2.1%) — seed 42 hit exactly zero.** Never-declared
rejections — zero in every MARD-full and every A1s run — average 57.0 under A1f (49–67): the
model keeps trying to reference concepts from earlier chapters it can no longer see, and
`_accept_edges`'s `known_ids` check correctly refuses every one of those attempts. Confirmed
mechanically from all three A1f runs' `envelope/pass_1_final.json`: `skeleton_sections: 120`
(kept, unlike A1s's 0), `findings_total: 14`, `findings_shown: 0`, `suppress_findings: true` —
the skeleton renders, the findings never do. Zero truncated Tier 2 outputs across all three
runs (753 non-empty outputs checked total across all nine runs, MARD full + A1s + A1f).

**This is the confirmation §6.1 was originally reported as being, and was not:** the
envelope's findings channel — not its skeleton — is what carries cross-chapter concept ids
forward. Removing findings collapses cross-chapter structure to near-zero (1.4% mean, one
seed at exactly zero); removing the skeleton alone leaves it essentially unchanged (89.8%,
statistically indistinguishable from MARD full's 91.7%). **This is the number that supports
docs/25 §T5's "this is the run that earns the paper's title" framing — for A1f, not A1s.**

**Blocker resolved:** the first attempt at seed 42 hit `openai.RateLimitError: ...
'credit_balance_exhausted'` during Pass 0 — the OpenAI account's real prepaid credit balance,
not the software `MARD_SPEND_CAP_USD=120` ceiling (`runs/_ledger.json` was at $7.98 of $120,
nowhere near the cap; multiple sessions draw on the same account concurrently). Anugrah added
credits; the re-run succeeded cleanly. A separate, unrelated bug was found and fixed en route:
the retry before that also exposed a `KeyError: 'rejected'` in `mard.run._never_declared_count`
(a chapter whose `explore()` call raises is recorded by `run_pass1`'s own except branch with
no `"rejected"` key) — fixed with `.get("rejected", [])`, tested
(`tests/test_mard_run.py::test_never_declared_count_tolerates_a_chapter_that_raised`), and
`mard.run.run_mard` now also saves a `pass1_trace.json` artefact per run (full per-chapter
trace, not just the aggregate event) specifically so a mid-pipeline crash like this one leaves
enough on disk to diagnose without needing a re-run.

**Campaign totals: 9 of 9 planned runs complete** (MARD full ×3, A1s ×3, A1f ×3), all
`compiled: true`, zero empty or truncated Tier 2 outputs across all nine.

---

## 7. A gap to record before anyone writes §3/§4: there is no O3 baseline for the
cross-chapter fraction

**The vanilla-RLM (B1) runs cannot be compared against MARD's cross-chapter fraction, because
B1 has no equivalent quantity.** B1 emits a study guide directly — prose, not a typed concept
graph — so there are no `(prerequisite, dependent)` edges to count cross-chapter or otherwise;
`runlog.load_run` on any of the three B1 runs (`docs/18` §4.2 addendum, seeds 11/23/42) shows
an empty `result` dict for exactly this reason. **The 89.8–91.7% figures in §4/§6 describe how
MARD's own Tier 1 behaves internally — envelope-full vs. skeleton-only vs. (pending)
findings-only — not an O3 A-vs-B comparison against the baseline.** A manuscript sentence that
presents this fraction as "MARD vs. vanilla RLM" would be citing a number against a baseline
that was never measured, because it cannot be. If O3 needs a cross-chapter-structure
comparison against B1 at all, that requires a different metric computed over B1's own prose
output (e.g. an ordering/reference check against the ground-truth extraction Track 4 already
built) — not this fraction, which is MARD-internal by construction.

---

## 8. Still open

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Re-measure cross-chapter edge count post-fix | MARD session | **Done — §4** |
| 2 | Check the 69 successful Tier 2 outputs for mid-sentence truncation | MARD session | **Done — §4, zero found** |
| 3 | Get `reasoning_effort` into the config snapshot and into §3.2 | MARD session, then `docs/27` | **Config snapshot done — §4.** §3.2 wording is `docs/27`'s to write. |
| 4 | A1 and negative-control runs | MARD session | **A1s done (3/3 — §6.1). A1f done (3/3 — §6.3), confirms the hypothesis: cross-chapter edges collapse to 1.4% mean.** Negative-control still waits on `docs/26`'s flattener, and is on hold regardless per Anugrah's 28 Aug instruction |
| 5 | Groundedness detector over the MARD runs once they land | `docs/26` session | Open |
| 6 | The depth off-by-one in `docs/18` §5.2, still derived from prose | either | Open |
| 7 | Decide how §3/§4 should describe A1s vs A1f, and whether either belongs in the title-earning claim | **Anugrah** | Open — A1f (§6.3) is the number that supports the title-earning claim; A1s (§6.1) is a separate, real cost-decomposition result |
| 8 | O3 needs its own B1-comparable metric — the cross-chapter fraction is not one (§7) | **Anugrah** | Open — escalated, §7 |
| 9 | Add credits to the OpenAI account, then run A1f seed 42 | **Anugrah** | **Done — credits added, seed 42 ran clean, 9/9 campaign runs complete (§6.3)** |
