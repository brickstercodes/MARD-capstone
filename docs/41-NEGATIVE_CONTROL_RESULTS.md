# 40 — Negative control results, and the axler figure run

**Status:** Recorded 28 Aug 2026 · Owner: MARD-arm session (`docs/25`/`docs/39`)

Implements the negative-control brief. Scoring is `docs/26`'s to do — this
document names run ids and states what happened; it does not compute task scores.

**Both original blockers were resolved by others, verified independently here before
spending on real runs, not taken on trust:**

- The B1-vs-page-markers conflict (§1.2 as originally written) was fixed by a peer session:
  `eval/flatten.py`'s `render_text` now emits page markers renumbered sequentially in the
  *shuffled* order, carrying no information about original book order while still giving
  `vanilla.run.split_pages` something to chunk on. Confirmed directly: `grep -c "\[\[page:"
  corpus/introcs_flat/document.txt` → 1008; `vanilla.run.split_pages` on the regenerated file
  → 1008 chunks, no exception; `python -m ingest.manifest corpus --document-id introcs_flat`
  → clean; full test suite and `scripts/preflight.sh` both green before any run was started.
- `axler`'s missing provenance (§2 as originally written) was supplied by Anugrah: source
  sha256 `b40b1da1cbca`, 404 pages. Confirmed: `corpus/axler/manifest.json` now exists and
  `python -m ingest.manifest corpus --document-id axler` verifies clean, 6 artefacts pinned,
  hash matching what was supplied.

---

## 0. Task 1 — document parameterisation (done)

`scripts/run_vanilla_full.py` and `scripts/run_mard_full.py` both take `--document-id`
(default `introcs`), so every existing campaign command still runs unchanged.

**Dry check before spending anything**, per §2's instruction not to trust the paragraph:
loaded `corpus/introcs_flat/document.jsonl` through the real pipeline —
`ingest.sections.build_sections` → 0 sections, `ingest.chapters.group_into_chapters` →
0 chapters, over 9,291 real blocks. Confirmed by running the code, not by reading
`eval/flatten.py`'s docstring.

---

## 1. Task 2 — the negative control: all 6 runs complete

### 1.1 MARD full on `introcs_flat` — 3/3 seeds, all degenerate as predicted, $0

| Run id | Seed | Status | Concepts | Edges | Cross-chapter | Tokens in/out | Cost | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| `20260828T140626__mard__introcs_flat__s11__e55946` | 11 | ok | 0 | 0 | 0 | 0 / 0 | $0.00 | 0.061s |
| `20260828T140658__mard__introcs_flat__s23__bad85d` | 23 | ok | 0 | 0 | 0 | 0 / 0 | $0.00 | 0.048s |
| `20260828T140658__mard__introcs_flat__s42__5baafe` | 42 | ok | 0 | 0 | 0 | 0 / 0 | $0.00 | 0.047s |

**The skeleton is empty and `degenerate: true`, exactly as `run_pass0`'s own contract
promises — it did not raise.** `build_sections` finds zero heading-kind blocks (every one
relabelled `body` by `eval.flatten._strip_heading`); `run_pass0` short-circuits *before
issuing any model call*; `chapters == []`; `run_pass1`'s loop never executes; `run_mard`
takes its existing "no concepts, nothing to compile" branch. **All three seeds are
bit-for-bit identical** because no model call happens at all — nothing stochastic to vary.
This is expected, not a `docs/38`-style determinism finding: `docs/38`'s claims are about
runs that call a model.

### 1.2 B1 (vanilla RLM) on `introcs_flat` — 3/3 seeds, real spend, produces output

| Run id | Seed | Status | Concept count | Tokens in/out | Cost | Wall-clock |
|---|---|---|---|---|---|---|
| `20260828T142853__vanilla_rlm__introcs_flat__s11__403918` | 11 | ok | 70 | 532,694 / 64,119 | $0.796418 | 313.14s |
| `20260828T143418__vanilla_rlm__introcs_flat__s23__be02f1` | 23 | ok | 356 | 225,268 / 39,260 | $0.465128 | 173.76s |
| `20260828T144042__vanilla_rlm__introcs_flat__s42__c9c869` | 42 | ok | 588 | 1,056,353 / 123,140 | $0.656794 | 270.72s |

(Excluded from this table, kept on disk, not deleted: `20260828T140618__vanilla_rlm__
introcs_flat__s11__f8651e`, `status: "failed"` — the pre-fix attempt against the
page-marker-free corpus, superseded once the marker fix landed, the same discipline
`docs/28` §4 applies to a superseded run.)

**Concept count spread (70 / 356 / 588) is far wider than B1's own spread on the real,
unshuffled `introcs` (156 / 190 / 75, `docs/38` §2.1) — consistent with `docs/36`'s framing
("vanilla RLM's output structure is unstable across seeds") rather than a new phenomenon,
but a wider instance of it: on scrambled input, the instability got worse, not better.**
Seed 42's token volume (1.06M input) is roughly double any of the real-`introcs` B1 runs —
the root evidently iterated far more against the shuffled, page-renumbered text.

### 1.3 The coherence finding: B1 confabulates confidently, it does not notice the scrambling

**Read directly, not sampled by keyword search alone** (`runs/*/artefacts/vanilla_answer.md`
for all three seeds, full text plus a targeted search for any hedge language: "scramble",
"shuffle", "disorder", "jumbled", "out of order", "non-linear", "reorganized", "the excerpt",
"appears to be"/"seems to be"). **Zero genuine hits in any of the three runs.** The only
keyword matches are false positives — the source material's own vocabulary ("inconsistent
formats" in a data-quality section, "inconsistencies" in a file-systems section) discussing
CS topics, never the model commenting on its own input.

**All three runs read as fluent, confidently organised study guides, indistinguishable in
tone and structure from B1's runs on the real, unshuffled document.** Each opens with a
`# Study Guide` heading and proceeds through titled sections with "Key terms" and "Quick
check" blocks, exactly the same house style B1 uses on `introcs` itself. **Seeds 23 and 42
both spontaneously open with `## 1.1 Computer Science`** — the real book's actual opening
topic — despite the input being shuffled into a random section order with headings
stripped. The model did not receive this ordering from its input; nothing in the shuffled,
heading-free text signals "this is the beginning." It reconstructed a textbook-plausible
opening from its own prior knowledge of how a CS textbook is conventionally organised, not
from anything actually present in what it was given to read.

**This is the result, stated plainly and not softened, per the brief's own instruction:**
B1 does not become visibly confused, does not hedge, and does not flag the disorder when fed
structure-ablated, order-scrambled input. It silently imposes a confident, coherent-*looking*
organisation on top of scrambled material. A reader handed only the output would have no way
to tell it was generated from shuffled input rather than the real book in order. **This is a
faithfulness failure mode specific to B1** — MARD's equivalent behaviour on this same input is
§1.1's `compiled: false`: MARD does not produce a confident-looking anything from
structureless input, it declines to produce output at all rather than confabulate one. That
contrast — decline vs. confident confabulation — is the negative control's actual finding, and
it favours MARD's design on exactly the axis (faithfulness/auditability) `docs/36` §3 already
stakes the paper's non-conceded claims on.

---

## 2. Task 3 — the `axler` run: unblocked, run once, labelled a figure not a result

**Provenance confirmed** (Anugrah, 28 Aug): source sha256 `b40b1da1cbca`, 404 pages.
`corpus/axler/manifest.json` now exists; `python -m ingest.manifest corpus --document-id
axler` verifies clean, 6 artefacts pinned.

**One MARD full run, seed 11 only, as instructed — not three, and not a result:**

| Run id | Seed | Status | Concepts | Edges | Cross-chapter | Tokens in/out | Cost | Wall-clock |
|---|---|---|---|---|---|---|---|---|
| `20260828T144524__mard__axler__s11__3fed30` | 11 | ok | 54 | 116 | 76 (65.5%) | 22,709 / 69,799 | $0.295535 | — |

`compiled: true`, artefact saved, zero truncated Tier 2 outputs (54/54 checked), no
concept-id merges fired. **Label wherever this appears: a single unreplicated run, for
Figure 1 panel (c) only. Not a campaign data point, not averaged or compared against
anything, and never presented with a range or error bar it does not have.**

---

## 3. Runs excluded, and why

- `20260828T140618__vanilla_rlm__introcs_flat__s11__f8651e` (B1 seed 11, pre page-marker
  fix) — `status: "failed"`, superseded by the fix, kept on disk, not deleted. See §1.2.
- Nothing else excluded. All 9 runs this brief produced (3 MARD-flat + 3 B1-flat + 1 axler +
  the 1 superseded B1-flat attempt, plus the earlier smoke/dry checks which spent nothing)
  are on disk under `runs/`.

---

## 4. Test-count reconciliation

**Not a stale tree or lost files — the eval/ session added its own new test files between
this session's earlier full-suite run (241 passed) and now.** `pytest --collect-only -q`
currently collects **339 tests** from 23 files, run just now: `test_budget.py,
test_chapter_scoring.py, test_compile_plan.py, test_envelope.py, test_flatten.py,
test_groundedness.py, test_groundedness_mard.py, test_groundtruth.py,
test_groundtruth_scoring.py, test_ingest.py, test_lm_builder.py, test_manifest.py,
test_mard_run.py, test_ordering.py, test_pass1.py, test_plan_models.py,
test_plan_validation.py, test_runlog.py, test_runs.py, test_structure.py,
test_stub_builder.py, test_sync_seams.py, test_task_score.py, test_vanilla.py`.
`test_chapter_scoring.py`, `test_groundedness.py`, `test_groundedness_mard.py`,
`test_ordering.py`, `test_runs.py`, `test_structure.py`, `test_task_score.py` did not exist
at this session's last full-suite run — they are `docs/26`/`docs/35`/`docs/38`'s own eval
modules' tests, added concurrently in the same shared repo. **All 339 pass**, `ruff check`
and `mypy` clean, `scripts/preflight.sh` green (full suite now takes ~3.5 minutes, unchanged
in kind from `docs/38` §7's note, just larger).

---

## 5. Report back, unrounded

**No single "B1-vs-MARD delta" — MARD produced nothing on `introcs_flat` (by design,
$0, 0 concepts) while B1 produced full-length output at real cost, so the two are not a
subtraction against each other, they are a contrast in kind:**

- **MARD: `compiled: false` in all three seeds. 0 concepts, 0 edges, $0.00, sub-100ms,
  every seed identical.**
- **B1: succeeded in all three seeds, at $0.796418 / $0.465128 / $0.656794 (mean
  $0.639447), producing 70 / 356 / 588 "concepts" (mean 338, a wider spread than B1's own
  156/190/75 on the real document) and 532,694 / 225,268 / 1,056,353 input tokens (mean
  604,772).**
- **The qualitative result — confident confabulation with zero hedging or self-reported
  disorder across all three B1 runs, versus MARD's outright decline to produce anything —
  is the finding this control was built to produce, and it is reported exactly as found,
  per the brief's instruction not to soften either direction.**

Task 3: `axler` run `20260828T144524__mard__axler__s11__3fed30` — `compiled: true`, 54
concepts, 116 edges, 76 cross-chapter (65.5%), $0.295535 — a single unreplicated run for
Figure 1 panel (c).

Nothing further open for Anugrah from this brief; both original blockers (§1.2, §2) are
resolved and reflected above.
