# 24 — Groundedness: the seed-42 decision, and turning it into a measurement

**Status:** Decided 27 Aug 2026 · Decision owner: Anugrah Shetty (Track 1, holding both arms)
· **Amends** `docs/30-MEASUREMENT_PROTOCOL.md` §1 and §4

## 1. What happened

Seed 42 of the vanilla-RLM arm on `introcs` completed with `status: "ok"`, no exception, and
a coherent 75-concept study guide. Walking the trajectory showed something the harness had
no way to surface:

The concept *"Trees and balanced trees"* went through three generation attempts. Attempt 1
was correctly sourced from real per-chapter chunks and was discarded on a JSON parse
failure. Attempt 2 pulled in **unrelated source text** — a multiple-choice quiz page about
enterprise-architecture levels — because the root's own `chunks_for_includes` matching
mismapped it; also discarded on a parse failure. Attempt 3 ran with **`SOURCE:` empty, 88
input tokens**, generating the explanation from the model's parametric knowledge alone.
**Attempt 3 is the version in the published guide**, confirmed by matching its exact phrasing
against iteration 15's source-less response.

The content reads as accurate CS material. It is simply **not grounded in the document**,
which the frozen task prompt requires ("the textbook available in `context`").

Cost and latency corroborate it: **$1.60 / 776 s** against $0.32 / 152 s and $0.58 / 437 s
for the clean repeats. Most of iterations 11–16 was the model fighting its own parse failures.

| Seed | Concepts | Cost | Wall-clock | Note |
|---|---|---|---|---|
| 11 | 156 | $0.32 | 152.5 s | clean |
| 23 | 190 | $0.58 | 437.2 s | clean |
| 42 | 75 | $1.60 | 776.1 s | ungrounded content, see §4 |

## 2. Decision: seed 42 stays. All three repeats are reported.

**No re-run. No asterisk. No mean over the three.**

The test for whether a run is a *failed run* or a *bad result* is whether the **protocol
executed**. A harness crash, a rate-limit storm, a truncated artefact, a skipped manifest
verification — the protocol did not execute, and those are re-runnable.

Here the protocol executed exactly as specified. **The root model authoring its own
exploration code is the method under test** — that is RLM's defining property
(`docs/RLM_BASELINE_SURVEY.md` §2, `zhang2025rlm`). A buggy regex written by the root is the
system's behaviour at document scale, not an artefact of our setup. There is no sense in
which this run failed to measure the thing it was measuring.

Two rules already settle it, and neither is ambiguous:

- `CONTEXT.md` §3.4 — *"never tune toward a positive result after the fact."*
- `docs/30` §4 — *"never seeds cherry-picked or dropped after the fact."*

Re-running the repeat in which the **baseline** performed worst is precisely what those
sentences exist to prevent. An asterisk is the same act in softer language: it invites the
reader to discount the run.

**And the spread is itself a result.** 156 / 190 / 75 cannot be averaged into a headline
number. `docs/30` §4 requires variance be reported as the finding when it swamps an effect;
here it does not swamp an effect, it *is* one — the baseline is unstable at full-document
scale, in output volume, in cost, and in faithfulness.

## 3. Why this is the strongest finding in the study so far

`docs/00-CLAIM.md` says recursive exploration is *structurally blind*. Seed 42 is that
sentence, demonstrated by the baseline, on our own primary document, unprompted:

> The root has no structural view of the document. When its self-authored chunk-matching
> code mismapped a concept onto an unrelated quiz page, **nothing caught it** — and when
> that attempt failed to parse, the fallback silently dropped source text entirely and
> returned `status: "ok"`.

MARD's defence is specific and citable in code, not rhetorical:

- Tier 2 briefs are constructed from the Master Plan's source span (`orchestrate.briefs_for`),
  so a builder receives its section **by construction** rather than by the model matching it.
- The Master Plan is validated at the tier boundary (`plan/validation.py`) and a malformed
  plan **fails loudly** rather than dispatching N subtly wrong builders.
- `join_in_plan_order` **raises `IncompleteArtefactError`** on empty span text rather than
  returning a short artefact that scores as complete.

So the claim available is stronger, and different in kind, from a coverage delta:

> **The baseline silently produced ungrounded content and reported success. MARD's typed
> contract makes that failure mode loud rather than silent.**

That is **faithfulness and auditability**, and it belongs in §1 and §6 alongside the
ordering claim — not only in limitations.

## 4. `[UNVERIFIED]` — the count is inferred, not measured

The figure "≥41 of 75 concepts ungrounded" comes from the run's own `missing_outline`
counter at iteration 14. **Exactly one concept was verified end-to-end** (*Trees and balanced
trees*).

**That number must not enter the manuscript until it is measured directly.** It is a strong
signal about the final guide, not a count of it. This project's own audit history
(`CONTEXT.md` §2.3) is a list of confident numbers that came from adjacent places.

## 5. The groundedness detector — spec

Turns one anecdote into a measured axis across every run and **both arms**. No new runs, no
scorer, no API spend: the trajectories are already on disk.

**Per concept in the final artefact**, resolve the generating call and classify:

| Class | Test |
|---|---|
| `grounded` | generating call carried non-empty `SOURCE:` text |
| `ungrounded` | generating call carried empty or absent `SOURCE:` text |
| `regenerated` | ≥1 prior attempt for this concept was discarded (parse failure or otherwise) |
| `mis-sourced` | source text present but drawn from outside the concept's own chapter span |

Report per run: **groundedness rate** = `grounded / total concepts`, plus regeneration count
and mis-sourced count. Add these to the seven `docs/30` §1 fields for any run whose system
produces per-concept output.

`mis-sourced` is the hardest of the four and may not be reachable by Sunday — it needs the
concept's expected chapter span, which the vanilla arm does not record. **Ship the first
three and say so.**

### Requirements on the write-up

- **Measure MARD's rate too, and report it whatever it is.** Claiming immunity without
  measuring is the same overclaim in the other direction.
- **State plainly that this was found by manual trajectory inspection**, and that the
  detector was built afterwards. Discovering a failure mode by hand and then instrumenting it
  is ordinary practice; presenting the detector as though it had been planned is not.
- If MARD's rate is also below 100%, that is a finding about MARD, and it goes in §6.

## 6. Amendment to `docs/30`

Two additions, recorded here rather than by editing frozen text:

1. **§4 gains an explicit failed-run definition.** A run is re-runnable only if the protocol
   did not execute (harness fault, provider fault, unverified corpus). A run in which the
   system under test behaved badly is a **result**, and is reported.
2. **§1 gains groundedness fields** for systems producing per-concept output: groundedness
   rate, regeneration count, and — where derivable — mis-sourced count.

## 7. The four same-day corrections this arm produced

Each caught by running the thing rather than trusting a plausible number. Recorded because
the pattern is the point:

| # | Claim that was wrong | Corrected to |
|---|---|---|
| 1 | Sub-call callbacks fire at our depth | At `max_depth=1`, `_subcall`'s `next_depth >= max_depth` early-return path never reaches them (`rlm/core/rlm.py`). Per-sub-call timing is still recoverable from the trajectory's nested `rlm_calls`, each carrying `execution_time` (`local_repl.py:218, 327, 581`) |
| 2 | Batched-call metadata was complete | Metadata bug found and fixed |
| 3 | Concept counts were 156 vs 190 | Counting heuristic was wrong; corrected to 156 / 190 / 75 |
| 4 | Seed 42 was a heading-format quirk | Confirmed ungrounded content, §1 above |
