# 32 — Groundedness results, and the stronger finding underneath them

**Status:** Recorded 28 Aug 2026 · Owner: Track 1 (groundedness detector, `docs/26` Task B)
· **Amends** `docs/24-GROUNDEDNESS_AND_SEED42.md` §4 · **Read before writing paper §4**
(the reading list in `docs/27` §0 should include this file)

Written after Anugrah validated the detector against the seed-42 hand-trace — the gate
`docs/26` §4's definition-of-done asked for — and asked for three follow-ups: a fourth
concept class for root-authored writing, an independence check on the "41 of 75" figure,
and this write-up. All three are here. Code: `eval/groundedness.py`. Tests:
`tests/test_groundedness.py::TestRealRuns`.

---

## 1. The detector is validated

`eval.groundedness.score_run` on the seed-42 run resolves "Trees and balanced trees" to
its last generating call — no `SOURCE:` text, 88 input tokens, `runs/20260827T195512__
vanilla_rlm__introcs__s42__1dbe85/events.jsonl` — the exact call `docs/24` §1 traced by
hand, and classifies it `ungrounded`. **This is the gate `docs/26` §4 asked for, and it
passed.**

`docs/26` §3's validation wording — "seed 42 should show a markedly lower groundedness
rate than 11 and 23" — could not be checked as originally phrased, because seeds 11 and
23 turn out to have zero concepts individually delegated to an inspectable generating
call. That is not a detector defect. It is §4 below, and it is a stronger result than
the rate comparison it replaces.

---

## 2. A fourth class: `root_authored`

`docs/24` §5 specified three per-concept classes (grounded / ungrounded / mis-sourced)
assuming every concept traces to an inspectable per-concept call. Reading all three
runs' `events.jsonl` by hand shows that only seed 42 delegates at concept granularity.
Seeds 11 and 23 delegate only at chapter granularity and the root writes every
individual explanation itself — not because the detector failed to find a call, but
because none exists in the trajectory to find.

Neither `grounded` nor `ungrounded` fits that case, and neither does a bare `unresolved`
— unlike a truly evidence-free case, these runs' background sub-calls (the ones that
happened, just not scoped to one concept) are themselves fully inspectable. `eval/
groundedness.py` now reports a fourth status, `root_authored`, plus a run-level
`root_authored_context` field classifying exactly those background calls with the same
`_classify_call` heuristic used everywhere else:

| Seed | `root_authored` concepts | Background calls checked | Grounded | Ungrounded |
|---|---|---|---|---|
| 11 | 156 / 156 | 14 (chapter extraction) | 14 | 0 |
| 23 | 190 / 190 | 29 (14 chapter extraction + 14 JSON-repair + 1 final edit) | 29 | 0 |
| 42 | 0 / 75 | 24 (23 chapter extraction + 1 outline consolidation) | 24 | 0 |

Every background call in all three runs is grounded — real per-chapter chunk text,
20,000–37,000 input tokens each — including seed 42's, whose background calls exist
(the chapter-level extraction pass it also ran) but produce zero `root_authored`
concepts, because every one of seed 42's 75 concepts additionally resolves to its own
dedicated call. So "grounded at one remove" is the evidence-backed reading for seeds 11
and 23 specifically, not an assumption folded into the class name: the class itself is
purely structural (no per-concept call exists), and the strength of "at one remove" is
a separate, checked field, run by run. `unresolved` is kept for the case this doesn't
cover — a run with no sub-calls anywhere in its trajectory — which none of the three
logged runs hit.

`groundedness_rate` is unchanged in definition (`grounded / (grounded + ungrounded)`)
and `root_authored` concepts stay out of both numerator and denominator, for the reason
§1's validation note already gives: folding them into either side would assert a
per-concept check that was never performed.

---

## 3. "41 of 75" is confirmed — and it is one signal, not two

`docs/24` §4 flagged "≥41 of 75 concepts ungrounded" `[UNVERIFIED]`: it came from a
`missing_outline` counter printed to the console at seed 42's iteration 15 and never
captured in any logged artefact. Anugrah asked whether the detector's independently
computed 41 corroborates that figure or is the same signal read twice. It is the
second. Reading the code that computes `missing_outline`
(`runs/20260827T195512__vanilla_rlm__introcs__s42__1dbe85/events.jsonl`, the
`vanilla_root_iteration` events at iteration 15–16) shows why:

1. `missing_outline` is built from concepts with no successfully-parsed explanation as
   of iteration 14.
2. Every name in it is immediately re-generated with `gen_no_source_prompt` — the exact
   zero-source template (`Concept: …\nModule: …`, no `SOURCE:` field) this detector's
   `_classify_call` calls `ungrounded`.
3. The result unconditionally overwrites `explanations[name]`, and no further
   regeneration round follows — iteration 16 only assembles the final markdown.

So `missing_outline`'s members and this detector's `ungrounded` concepts are the same
set by construction. Verified directly, not inferred from reading the code alone
(`tests/test_groundedness.py::test_ungrounded_count_is_exactly_the_missing_outline_
batch`):

- Exactly **41** sub-calls match the zero-source template (no `SOURCE:` marker,
  `input_tokens < 500`).
- They name exactly **41 distinct concepts** — one call each, no duplicates.
- **All 41 are the last trajectory entry for their concept** — zero are superseded by
  a later, better-sourced attempt.

That third point is the one that rules out coincidence: it is exactly the shape a
never-revisited `missing_outline` fill-in batch produces, and nothing else plausibly
produces it. **Report this as: the `[UNVERIFIED]` figure is now confirmed reproducible
from committed artefacts, not as two independent measurements landing on the same
number.** The manuscript should cite the detector's count (traceable to
`runs/…s42…/events.jsonl`) and retire the `missing_outline` console figure, not report
both as if they were separate evidence.

---

## 4. The stronger finding: three repeats, three architectures

`docs/24` §2 already established that seed 42's baseline is unstable in output volume,
cost, and faithfulness (156 / 190 / 75 concepts; $0.32 / $0.58 / $1.60; clean / clean /
ungrounded). Building the groundedness detector surfaces a finer-grained instability
underneath that one: **the three repeats did not just produce different outputs from
one generation strategy — the root wrote three structurally different generation
strategies**, each invented fresh, at the level of what gets delegated to a sub-call
versus authored directly.

| Seed | Root iterations | Sub-calls | Sub-call composition | Concepts | Delegation granularity |
|---|---|---|---|---|---|
| 11 | 8 | 14 | 14 chapter-level concept-list extractions (JSON) | 156 | **Chapter.** ~11 concepts authored directly per extraction call, entirely inside the root's own iteration code. No per-concept call of any kind. |
| 23 | 11 | 29 | 14 chapter extractions + 14 JSON-repair calls + 1 whole-document final-editing pass (44,075 tokens) | 190 | **Chapter, plus one document-wide edit.** Still no per-concept call — the root added a repair loop and a single large consolidation call that seed 11 didn't need. |
| 42 | 17 | 151 | 23 chapter extractions + 1 outline-consolidation call + 36 per-concept calls with a `SOURCE:` field + 50 per-concept calls with no `SOURCE:` field but high token counts + 41 per-concept zero-source calls | 75 | **Concept.** Every one of the 75 final concepts has its own dedicated generating call, several with 2–3 regenerated attempts. |

Cost and wall-clock (`docs/24` §1's table) track this directly: $0.32/152.5s (11) →
$0.58/437.2s (23) → $1.60/776.1s (42), which is not simply "seed 42 tried harder" — it
is 151 sub-calls' worth of per-concept delegation and retries versus 14 or 29 calls'
worth of chapter-level extraction, chosen by the root itself, fresh each run, with no
signal in the frozen task prompt (`docs/21` §3.1) that would predict which one a given
run lands on.

**Why this is a stronger claim than the groundedness rate.** The groundedness rate says
seed 42's baseline produced ungrounded content in 41 of 75 cases. This finding says
something upstream of that: the baseline does not have a stable *strategy* for solving
the task at all — three runs of the identical frozen prompt against the identical
document produced three different divisions of labour between "written by the root
from a digest" and "written by a delegated call with the source text in hand," and
groundedness failures only *arise* in the one strategy (seed 42's) that delegates
finely enough to be individually checked. Seeds 11 and 23 are not verified grounded in
the same direct sense seed 42's `grounded` concepts are — they are `root_authored`,
grounded only at one remove (§2) — so the honest reading is not "two clean runs and one
bad one," it is "one run fine-grained enough to catch its own failures, and two that
weren't, by the root's own unprompted choice of architecture." `docs/24` §1's framing —
"the root has no structural view of the document" — extends to: the root has no stable
view of its *own* method, either.

### What this means for §4, as measurement constraints (not framing choices)

Framing and emphasis are `docs/27`'s and Anugrah's call, per `CLAUDE.md`'s escalation
list. What is not optional, because it follows directly from §§1–3 above:

- The groundedness rate cannot be reported as one comparable number across all three
  repeats. Seed 42 has a rate (45.3%, 34/75); seeds 11 and 23 do not have a rate at
  all — `resolved = 0` for both — and reporting `0%` or omitting them would misstate
  what was measured.
- The per-repeat delegation-granularity table above (or the numbers in it) belongs
  next to whatever variance framing `docs/24` §2 already uses for concept
  count/cost/wall-clock — it is the same instability, one layer down, not a separate
  result competing for space.
- "41 of 75" should be cited as this detector's count against `runs/…s42…`, not
  alongside the `missing_outline` console figure as if they were two numbers (§3).

---

## 5. Housekeeping

- the project's unverified-claims register — the `docs/24` §4 entry is superseded by this
  document; the figure is now verified, with the caveat in §3 above attached.
- `docs/24-GROUNDEDNESS_AND_SEED42.md` carries a banner pointing here.

### How this document came to be canonical, not just first

Anugrah was independently writing the same finding directly into `docs/24` §8–§9 while
this document was being drafted — same architectural-instability observation, same
`root_authored` class, arrived at separately from the same run data. Two live accounts
of one finding, in two places, moving independently: exactly the failure `docs/00`'s
"higher-numbered wins" rule exists to prevent, mid-occurrence rather than after the
fact — the ordinary failure mode of edits landing in parallel with no lock between them,
not a mistake either side made.

It resolved cleanly because the two drafts differed in a checkable way, not an
opinion-based one. `docs/24` §8–§9 stated the finding; this document additionally cites
the code paths, pins numbers to `tests/test_groundedness.py` assertions, and — critically
— *answers* the independence question §4 had only flagged as open, rather than
restating that it was open. Anugrah read both, judged this one more complete on those
grounds, and collapsed `docs/24` §8–§9 into the single pointer that now stands there.
That is the resolution this note confirms from the other side: nothing here was written
to compete with `docs/24`'s account, and once it was clear the two would only diverge by
being redundant, the fix was to remove the redundancy, not to merge or arbitrate two
prose versions of the same claim.
