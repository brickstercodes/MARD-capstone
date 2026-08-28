# 26 — Implementation brief: the negative control and the groundedness detector

**Paste this whole file as the first message of a fresh Claude Code session opened in
`~/Desktop/Capstone/MARD-capstone`.**

**This session runs in parallel with `docs/25`'s MARD-arm session.** Read §1 on footprint
before touching anything — you share a repository with another agent and a collision costs
both of you.

Written 27 Aug 2026.

---

## 0. Read first

1. **`docs/00-START_HERE.md`** — current state, the higher-number-wins rule, standing rules.
2. `docs/24-GROUNDEDNESS_AND_SEED42.md` — **the whole reason this session exists.** §5 is
   your detector spec; §2 is the methodology you must not quietly undo; §4 is a number you
   must not carry forward.
3. `docs/23-GROUNDTRUTH_SPEC.md` §7 — what already landed in `ingest/groundtruth.py`.
4. `docs/30-MEASUREMENT_PROTOCOL.md` — its banner, especially item 6 on the negative control.

Then run `scripts/preflight.sh`. If it fails, fix that and nothing else.

---

## 1. Footprint — you are not alone in this repo

**Yours to create:** `eval/flatten.py`, `eval/groundedness.py`, `corpus/introcs_flat/`,
`tests/test_flatten.py`, `tests/test_groundedness.py`.

**Read-only for you:** `runs/`, `corpus/introcs/`, `ingest/`, `envelope/`, `orchestrate/`,
`provider/`, `plan/`.

**Do not touch, another session owns them:** `mard/`, `provider/sync_seams.py`, `paper/`,
anything under `.vendor/`.

If you need a change in a file outside your footprint, **stop and report it** rather than
making it.

---

## 2. Task A — the flat-context negative control

### Why this and not OOLONG

The frozen OOLONG subset is n=50 tasks; ×2 systems ×3 seeds at 150–800 s per run is days of
wall-clock, not hours. It is **deferred to Manuscript B**, disclosed in the paper as a scope
decision. **Do not touch `eval/frozen_subsets/`** — that directory's own README forbids
edits, and nothing here needs it.

The control is instead a **structure-ablated variant of the primary document**: the same
text, section order shuffled, heading markers stripped. This is deliberately the stronger
design — it holds content constant and varies only structure, so it is a manipulation rather
than a change of corpus, and it parallels ablation A1 one level lower. A1 removes the
structure the *system* accumulates; this removes the structure the *document* supplies.

**`axler` is not a substitute and must not be used as one.** It has 17 headings but still 9
chapters and a 3-level outline — weak structure, not flat. That tests a gradient, not the
boundary.

### Build `eval/flatten.py`

Read `corpus/introcs/document.txt`, emit `corpus/introcs_flat/document.txt`:

- **Shuffle section order.** Use `corpus/introcs/sections.json`'s `source_spans` to find
  section boundaries rather than guessing from the text.
- **Strip ATX heading markers** (`^#{1,6} `). Keep the heading *text* — removing the words
  as well would ablate content, not just structure, and the manipulation would no longer be
  clean.
- **Decide and document what happens to `[[page:N]]` markers.** They are positional
  structure. My reading is they should go, since a model can reconstruct order from them —
  but state your choice in the module docstring either way, because it is exactly the kind
  of thing that quietly weakens a control.
- Write a `manifest.json` via `ingest.manifest.write_manifest` so the flattened corpus is
  pinned like any other. Record the shuffle seed in it.

### Then verify the ablation actually worked

Run `envelope.pass0.run_pass0` against the flattened corpus and confirm:

- `Skeleton.is_empty` is **true**
- `trace["degenerate"]` is **true**

`run_pass0`'s own docstring anticipates precisely this: *"An empty section list is not an
error. It is the O4 boundary: a document with no exploitable structure yields an empty
skeleton and MARD degenerates to vanilla RLM. The trace says so explicitly so the run log
records degeneration as a finding rather than as a missing value."*

**If the skeleton is not empty, the ablation is incomplete** — something is still carrying
structure and you need to find out what before any run happens. Report it; do not paper over
it by deleting more.

**Do not run the flat configuration yet.** It needs `mard/run.py`, which the other session
is building. Build and verify the flattener, then stop and hand over.

---

## 3. Task B — the groundedness detector

### What it is for

Read `docs/24` §1 before writing a line. In one baseline repeat the system completed
`status: "ok"` and produced a coherent study guide in which a large fraction of explanations
were generated **with no document in context**. That is currently an anecdote supported by
one hand-traced concept. This detector turns it into a measurement across every run and both
arms.

### Build `eval/groundedness.py`

For each concept in a run's final artefact, resolve the generating call in the trajectory
and classify it:

| Class | Test |
|---|---|
| `grounded` | generating call carried non-empty source text |
| `ungrounded` | generating call carried empty or absent source text |
| `regenerated` | ≥1 prior attempt for this concept was discarded |
| `mis-sourced` | source present but drawn from outside the concept's own chapter span |

Report per run: **groundedness rate** = grounded / total concepts, plus regeneration count.

**`mis-sourced` is the hard one** and may not be reachable — it needs the concept's expected
chapter span, which the vanilla arm does not record. **Ship the first three and say so
plainly** rather than approximating the fourth.

### Run it over everything

The three vanilla runs already under `runs/` (seeds 11, 23, 42) are your first inputs and
your validation set: seed 42 should show a markedly lower rate than 11 and 23. **If it does
not, the detector is wrong, not the finding** — the manual trace in `docs/24` §1 is solid
first-hand evidence and your code has to reproduce it before it can be trusted on runs
nobody has read by hand.

Then run it over the MARD runs as they land.

### Two things about honesty here

**`docs/24` §4 flags "≥41 of 75" as `[UNVERIFIED]`.** It came from an intermediate
`missing_outline` counter, not from a count of the final artefact, and exactly one concept
was verified end-to-end. **Your detector's count replaces it. Do not carry the old figure
forward into anything.**

**Measure MARD's rate too and report it whatever it is.** The prediction is that MARD's rate
is near 1.0, because `orchestrate.briefs_for` constructs each brief from the plan's recorded
source span rather than matching text at generation time. That is a prediction, not a
result. If MARD also produces ungrounded spans, that is a finding about MARD and it goes in
the paper unchanged.

---

## 4. Definition of done

- [ ] `eval/flatten.py` + tests; `corpus/introcs_flat/` exists with a pinned manifest
      recording the shuffle seed.
- [ ] `run_pass0` on the flattened corpus gives `is_empty == True` and
      `trace["degenerate"] == True`, demonstrated in a test.
- [ ] The `[[page:N]]` decision is made and justified in the module docstring.
- [ ] `eval/groundedness.py` + tests, classifying grounded / ungrounded / regenerated.
- [ ] The detector run over the three existing vanilla runs, with seed 42 showing the
      expected drop. If it does not, **stop and report** rather than adjusting until it does.
- [ ] `mis-sourced` either implemented or explicitly reported as not reachable, with why.
- [ ] `ruff check`, `ruff format --check`, `mypy` clean; full suite passes.
- [ ] Nothing outside the §1 footprint modified.

---

## 5. Rules that override your judgement

- **A run in which the system behaved badly is a result, not a failed run.** Re-run only
  when the *protocol* failed to execute. `docs/24` §2.
- **No number without a logged run.** No figure that cannot be traced to `runs/<run_id>/`.
- **Mark anything unverifiable `[UNVERIFIED]` and surface it.**
- **Escalate rather than invent.** Four things in this repo are currently wrong because
  somebody's plausible-sounding inference went unchecked; all four are listed in `docs/24`
  §7 and each was caught by running the thing rather than reasoning about it.

---

## 6. What landed, 28 Aug 2026

Both tasks complete. 232 tests pass; `ruff`, `mypy` and `scripts/preflight.sh` clean. Nothing
outside the §1 footprint was touched.

### Task A — `eval/flatten.py`

- **A text-level strip would have been a no-op ablation, and the session caught that.**
  `ingest.sections.build_sections` reads block `kind`/`level` (derived from PDF font metrics),
  never `document.txt`'s ATX markers — so stripping `#` characters alone would have left the
  structure fully intact while appearing to remove it. The flattener therefore relabels
  `kind="heading"` → `"body"` at the block level. **This is the difference between a real
  control and one that silently does nothing.**
- `[[page:N]]` markers dropped, as §2 leaned toward; documented in the module docstring.
- `corpus/introcs_flat/` exists with a pinned manifest recording `shuffle_seed: 20260827` and
  the section permutation.
- Verified through the real `build_sections` → `run_pass0` path rather than a hand-built empty
  list: `is_empty=True`, `degenerate=True`.
- The flat configuration has **not** been run — it needs `mard/run.py`.

### Task B — `eval/groundedness.py`

- Classifies via a `SOURCE:` marker check **corroborated by `input_tokens`**, which is robust
  against `vanilla/run.py`'s 500-character prompt-preview truncation.
- **Seed 42 measured at 41/75 ungrounded**, reproducing `docs/24` §1's hand-trace exactly.
  See `docs/24` §4 for the one confirmation still outstanding.
- `mis-sourced` deliberately **not** implemented — no expected chapter span is recorded, and
  source text is usually truncated past its origin. Reasons in the docstring.

### The finding that outgrew the brief

Seeds 11 and 23 have **no per-concept generating call at all**; the root wrote every
explanation itself. That makes §3's validation gate uncheckable as written, and it turned out
to be a larger result than the detector.

The session stopped and escalated rather than reinterpreting its own gate — Anugrah confirmed
the seed-42 hand-trace match was the real gate and it passed, then asked for three follow-ups:
a fourth concept class for root-authored writing, confirmation that the detector's 41/75 and
the old `missing_outline` figure are independent (they are not — same signal, two routes),
and this write-up. All three landed in
[`docs/32-GROUNDEDNESS_RESULTS_AND_ARCHITECTURAL_INSTABILITY.md`](32-GROUNDEDNESS_RESULTS_AND_ARCHITECTURAL_INSTABILITY.md),
now canonical; `docs/24` §4 and §8 point to it. Escalating rather than reinterpreting the gate
was the correct call and is the behaviour these briefs are trying to produce.
