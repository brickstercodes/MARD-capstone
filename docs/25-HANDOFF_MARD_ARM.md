# 25 — Implementation brief: the MARD arm, and the negative control

**Paste this whole file as the first message of a fresh Claude Code session opened in
`~/Desktop/Capstone/MARD-capstone`.**

Written 27 Aug 2026. Every fact below was verified first-hand against this repo. Anything
unverified says so.

**Goal:** three logged MARD runs on `introcs` and three logged A1 (envelope-stripped) runs.

**Footprint.** A parallel session (`docs/26`) owns `eval/flatten.py`, `eval/groundedness.py`
and `corpus/introcs_flat/`. **Yours:** `mard/`, `provider/sync_seams.py`, `runs/`. Do not
edit `paper/` — a third session owns it. The negative-control *runs* (T6) wait until that
session has built and verified the flattener; build everything else first.

---

## 0. Read first, in this order

0. **`docs/00-START_HERE.md`** — current state in ten lines, the higher-number-wins rule,
   and `scripts/preflight.sh`. **Run preflight before spending a token**; if it fails, fix
   that and nothing else.
1. `docs/18-W3_PROVIDER_SWITCH.md` — provider, control library, corrected cost model.
2. `docs/24-GROUNDEDNESS_AND_SEED42.md` — the groundedness finding and the failed-run
   definition. **The most important doc for interpreting what you produce.**
3. `docs/31-ABLATIONS.md` — read the rename banner. **B1 and A1 are different runs.**
4. `docs/30-MEASUREMENT_PROTOCOL.md` — the seven fields, plus the amendments in its banner.
5. `vanilla/run.py` and `provider/` — the arm that already works. You are mirroring it.

`docs/12-MODEL_PAIR.md` and `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md` are **void** — the
project left Vertex/Gemini for OpenAI on 26 Aug. History only.

---

## 1. Almost everything you need already exists

The vanilla arm built the shared layer. Do not rebuild any of it.

| Module | State |
|---|---|
| `ingest/` | Done. `corpus/introcs/` populated, 0 parse warnings, manifest pinned |
| `ingest/manifest.py` | Corpus provenance; `verify_or_raise` before any measured run |
| `envelope/` | `skeleton`, `envelope`, `pass0`, `pass1`, `compile_plan`, `fidelity` — all offline-clean |
| `plan/` | Typed Master Plan + Pydantic validation |
| `orchestrate/` | `briefs_for`, `execute_plan`, `join_in_plan_order`, `IncompleteArtefactError` |
| `provider/` | `openai_client`, `throttle`, `rates`, `reasoning`, **`seams`** |
| `runlog/` | `RunLogger`, `RateCard`, `SpendCap`, `SpendLedger` |
| `vanilla/run.py` | The working reference for how a run is assembled and logged |

**All three MARD seams are already written**, in `provider/seams.py`:
`OpenAITopicLabeller`, `OpenAIChapterExplorer`, `OpenAILanguageModel`. Its docstring
carries two rules verbatim from the modules they feed — **no repair, no pre-filtering**, and
**a parse failure is never swallowed to an empty result**. Keep both.

Three real vanilla runs are logged under `runs/` (seeds 11, 23, 42) at $0.32, $0.58 and
$1.60. Spend so far ≈ $2.66 of the $120 cap. Cost is not a constraint here.

---

## 2. **STOP — there is a live async/sync mismatch. Fix it first.**

Verified 27 Aug by reading both sides:

| Side | Signature |
|---|---|
| `envelope/pass0.py:49` — `TopicLabeller` protocol | `def label(...)` — **sync** |
| `envelope/pass1.py:119` — `ChapterExplorer` protocol | `def explore(...)` — **sync** |
| `provider/seams.py:65` — `OpenAITopicLabeller.label` | `async def label(...)` |
| `provider/seams.py:86` — `OpenAIChapterExplorer.explore` | `async def explore(...)` |
| `orchestrate/lm_builder.py` — `LanguageModel` protocol | `async def acompletion(...)` ✓ matches |

Call sites are synchronous: `envelope/pass1.py:307` is `raw = active.explore(prompt, chapter)`
and `envelope/pass0.py:107` is `raw_topics = active.label(prompt, [...])`. **No `await`, and
there is no sync bridge anywhere in `provider/`.**

**What happens if you run it as-is.** `explore()` returns a coroutine. `run_pass1` checks
`isinstance(raw, dict)`, finds it false, and appends
`"explorer returned coroutine, expected an object"` to `rejected` — for all 14 chapters.
You get **zero concepts, an empty Master Plan, and no exception.** Someone reading the
output concludes the model performed badly. It never ran.

`pass0` will probably throw instead, which is at least loud.

### The fix, and why it is architecturally right rather than a workaround

**Add sync adapters in `provider/` that wrap the async seams. Do not change
`envelope/pass0.py` or `envelope/pass1.py`** — they are post-freeze frozen modules and their
protocols are correct as written.

Tier 1 has nothing to parallelise. `run_pass1`'s own docstring:

> *"Book order, not plan order: the plan does not exist yet. Chapters are visited in the
> document's own sequence so a later chapter's call can see what earlier ones found, which
> is the accumulation the claim rests on."*

Pass 1 is **inherently sequential** — chapter *n* must see chapter *n−1*'s findings. So a
synchronous Tier 1 is not a compromise; concurrency there would break the mechanism the
paper is about. Tier 2 is where concurrency belongs, and `acompletion` already matches.

Implement something like `provider/sync_seams.py` with `SyncTopicLabeller` and
`SyncChapterExplorer` that own a loop (`asyncio.run`, or a persistent loop if the throttle's
semaphore must be shared with Tier 2 — check `provider/throttle.py:139`, the semaphore is
created per instance and is loop-bound). **Add a test that asserts `explore()` returns a
`dict`, not a coroutine.** That test is the whole point of this section.

---

## 3. Tasks

### T1 — Verify before spending

```bash
python -m ingest.manifest corpus --document-id introcs   # must pass
cat corpus/introcs/parse_quality.md                       # must show 0 warnings
```

Confirm `MARD_SPEND_CAP_USD` is exported (**$120**) or `SpendCap.from_env()` refuses.

### T2 — Fix §2, then smoke Tier 1 on ONE chapter

Run `run_pass0` then `run_pass1` restricted to a single chapter, with the real seams.
**Then read `corpus/introcs/pass1_trace.json` before doing anything else.** Check:

- The rendered envelope in `trace["envelope"]` is populated and roughly ~300 tokens.
- `concepts_accepted` is non-zero.
- `rejected` is empty or explicable. **Any entry reading `"explorer returned ..."` means
  §2 is not fixed.**

### T3 — Full Tier 1, and confirm the plan compiles

All 14 chapters, then `compile_master_plan`. Two things to watch:

- `corpus/introcs/master_plan_trace.json` currently reports **`compiled: false`**. That must
  become true. Until it does, `docs/30` §3's before/after forward-reference metric cannot be
  computed and `eval/groundtruth_scoring`'s Master-Plan half is blocked.
- **Cross-chapter edges are the headline measurement.** `_accept_edges` rejects any edge
  whose endpoints are not in `known_ids`, and the only channel carrying earlier concept IDs
  into a later prompt is the envelope's `FINDINGS SO FAR` block. Count edges whose
  prerequisite and dependent sit in different chapters, and count `rejected` entries reading
  `"names a concept that was never declared"`. Both go in the paper.
- `compile_master_plan` can raise `UnsequenceablePlanError` (a cycle). If it does, that is a
  **finding** — report the cycle, do not hand-edit the graph to remove it.

### T4 — Tier 2 and the join

`briefs_for` → `execute_plan` → `join_in_plan_order`, with `OpenAILanguageModel` behind
`LmBuilder`. 120 builders on `introcs`.

- Concurrency comes from `provider/throttle.py`. Run at ≤70% of the measured per-minute
  ceiling. Log every 429 with its `Retry-After`.
- **`join_in_plan_order` raises `IncompleteArtefactError` on empty span text. Do not catch
  it to keep a run alive.** A truncated artefact must fail, not score low — `docs/24` §5.

### T5 — A1, the envelope-stripped run

`Envelope.stripped()` already exists (`envelope/envelope.py`), and `render()` returns `""`
when stripped. Same architecture, same models, same document, same throttle — envelope
emptied.

**This is the run that earns the paper's title.** B1 (vanilla RLM) changes five things at
once; A1 changes only the envelope. Note that `.stripped()` requires
`skeleton.is_empty and not findings and directive is None`, so it removes the **structural
map as well as** the accumulated findings. That is correct for "envelope removed", but it
means skeleton and findings cannot be separated without a fourth variant — say so in the
limitations rather than implying a finer cut than was made.

**Prediction to test, not to assume:** cross-chapter edges should collapse toward zero and
`"never declared"` rejections should spike. If they do not, that is a finding about the
envelope and it goes in §6 unchanged.

### T6 — The flat-context negative control

**New, and it replaces OOLONG for this manuscript.** Reason: the frozen OOLONG subset is
n=50 tasks; at 150–800 s per run, ×2 systems ×3 seeds, it is days of wall-clock, not hours.

Build `eval/flatten.py`: read `corpus/introcs/document.txt`, **shuffle the section order and
strip the ATX heading markers**, write `corpus/introcs_flat/document.txt` plus a manifest.
Same content, structure removed.

The pipeline already anticipates this exactly. `run_pass0`'s docstring:

> *"An empty section list is not an error. It is the O4 boundary: a document with no
> exploitable structure yields an empty skeleton and MARD degenerates to vanilla RLM. The
> trace says so explicitly so the run log records degeneration as a finding rather than as a
> missing value."*

So confirm `Skeleton.is_empty` is true and `trace["degenerate"]` is `true`, then run MARD and
B1 on the flattened document, 3 repeats each.

**Why this is better than OOLONG**, and the sentence for §4: it holds content constant and
varies only structure, so it is a clean manipulation rather than a change of corpus. It also
parallels A1 — A1 ablates the envelope, this ablates the input's structure. Disclose it:
*"For this manuscript the flat-context control is a structure-ablated variant of the primary
document; the frozen OOLONG subset (`eval/frozen_subsets/`, n=50) is deferred to the full
study."* That is a scope decision disclosed, **not** an edit to a frozen subset.

**Do not touch `eval/frozen_subsets/`.** Its own README: *"Any future change to either
file's contents is a new, separately-named subset — never an edit to these two."*

### T7 — Groundedness detector

Per `docs/24` §5. Per concept in the final artefact, resolve the generating call and classify
**grounded / ungrounded / regenerated**. Run it over **all** runs, both arms — the three
existing vanilla runs included.

**Measure MARD's rate and report it whatever it is.** Claiming immunity without measuring is
the same overclaim inverted. Prediction: MARD's rate should be near 1.0, because
`briefs_for` constructs a brief from the plan's recorded source span rather than matching
text at generation time — but that is a prediction, not a result.

`docs/24` §4 flags `"≥41 of 75"` as **`[UNVERIFIED]`** — it came from an intermediate
counter, and only one concept was verified end-to-end. **The detector's count replaces it.
Do not carry the old figure forward.**

### T8 — Log everything, then the matrix

All seven `docs/30` §1 fields plus the groundedness fields. Three repeats each.

**Run in priority order**, so a binding cap or a clock costs the least important thing
first: **MARD → A1 → negative control**. B1 is already done.

---

## 4. Traps

1. **The async/sync mismatch (§2).** Fails silently into an empty plan. Fix and test first.
2. **`compiled: false`** blocks the ordering metric and half the scorer. T3.
3. **Truncation must fail, not score low.** Never catch `IncompleteArtefactError`.
4. **`UnsequenceablePlanError` is a finding**, not something to edit around.
5. **Reasoning-model parameters:** `max_completion_tokens`, and **never send `temperature`**.
   `provider/reasoning.py` handles this — read it before adding anything.
6. **Cost logs as zero if unconfigured.** Rates come from `runlog.pricing.RateCard`, which
   refuses a rate older than 30 days. Never hardcode.
7. **No `seed` parameter exists.** `CAMPAIGN_SEEDS = (11, 23, 42)` are run *identifiers*;
   variance comes from genuine repeats.
8. **Do not use `root_prompt` to carry the envelope.** The envelope belongs in the child
   prompt where `envelope/pass1.py` already puts it. Using the library's user-prompt slot
   would collapse the upward/downward distinction the entire contribution rests on
   (`docs/01-ENVELOPE_VS_BASE_LIBRARY.md`).
9. **The depth off-by-one** in `docs/18` §5.2 is still **`[UNVERIFIED]`**, derived from
   documentation rather than from `envelope/pass1.py`'s call structure. Confirm it and
   report what you find.

---

## 5. Definition of done

- [ ] A test asserts `explore()` and `label()` return concrete values, not coroutines.
- [ ] `pass1_trace.json` shows populated envelopes, non-zero `concepts_accepted`, and no
      `"explorer returned ..."` rejections.
- [ ] `master_plan_trace.json` shows **`compiled: true`** and the plan validates.
- [ ] Cross-chapter edge counts and `"never declared"` rejection counts recorded for MARD
      and for A1.
- [ ] `corpus/introcs_flat/` exists with `trace["degenerate"] == true`.
- [ ] Groundedness detector run over **all** runs, both arms, with MARD's rate reported.
- [ ] Nine new logged runs under `runs/` (MARD ×3, A1 ×3, flat ×3), all seven `docs/30` §1
      fields plus groundedness.
- [ ] Cost non-zero and from `RateCard`; real token counts reported so `docs/18` §10 can be
      corrected from measurement.
- [ ] `ruff check`, `ruff format --check`, `mypy` clean; existing tests pass; new code tested.
- [ ] The `[UNVERIFIED]` depth mapping either confirmed or still flagged, with findings.

---

## 6. Rules that override your judgement

- **Results freeze.** Numbers are written up, never re-run. A wrong result gets a
  limitations paragraph. If you want to change a prompt, the Master Plan schema, or
  `ingest/`'s behaviour — **stop and ask Anugrah.**
- **A run in which the system behaved badly is a result, not a failed run.** Re-run only
  when the *protocol* failed to execute — harness fault, provider fault, unverified corpus.
  `docs/24` §2.
- **3 repeats on every number, variance reported.** Never average away a spread that is
  itself the finding.
- **A null result is publishable**, framed by the O4 boundary. Never tune toward a positive.
- **No number without a logged run.** Mark anything unverifiable `[UNVERIFIED]` and surface
  it — never quietly assert it, never quietly drop it.
- **Report findings, instinct and options.** Anugrah wants everything surfaced, including
  what looks like your own mistake. The three most useful things this project has learned
  were all corrections to confident-sounding claims.
