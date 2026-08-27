# Implementation brief — wire the MARD arm onto Arav's `replm` fork

**⚠ SUPERSEDED, 28 Aug 2026 — historical only.** `docs/18-W3_PROVIDER_SWITCH.md` §4.2's
addendum reverses the `replm` decision this whole document implements: the control is
now `Zhang_RLM @ 62acf7b`, `replm` is retired (not kept as a fallback), and every
`replm`-specific fact and file/line citation below (`sub_caller.py:96`, `a0ca553`'s
`client.py`, the `(enable_sub_calls, max_recursion_depth)` pair, etc.) describes a
library no longer in this repo. Kept unedited as the record of what was built and why,
not as current instructions.

**Paste this whole file as the first message of a fresh Claude Code session, opened
in `~/Desktop/Capstone/MARD-capstone`.**

Written 27 Aug 2026. Everything below was verified first-hand against the repo and
the two upstream libraries on 26–27 Aug. Where something is unverified it says so.

---

## 0. Read these first, in this order

1. `docs/18-W3_PROVIDER_SWITCH.md` — **the current state.** Where it and any other
   doc disagree, `18` wins. §4.2 is the decision you are implementing; §5 is the
   list of traps; §10 is the cost model.
2. `docs/31-ABLATIONS.md` — what A1 and A2 toggle. Read the banner.
3. `docs/30-MEASUREMENT_PROTOCOL.md` — the seven fields every run must record.
   Read the banner.
4. `docs/TRACK3_HANDOFF.md` — how `runlog` works. You will use it.
5. `envelope/pass1.py` and `envelope/pass0.py` — the two seams you are filling.

Do **not** read `docs/12-MODEL_PAIR.md` or `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md`
except as history. Both are void: the project left Vertex/Gemini for OpenAI on
26 Aug.

---

## 1. What the project is, in one paragraph

MARD (Metadata-Augmented Recursive Decomposition) extends Recursive Language
Models. An RLM never puts the document in the prompt: the document lives in a
Python REPL, and a root model writes code to explore it, delegating reading to
`llm_query` sub-calls. MARD's observation is that those sub-calls are
*structurally blind* — each gets a raw slice with no view of the document's shape,
no record of what sibling calls found, and no statement of why it was called.
MARD threads a **metadata envelope** (skeleton + accumulated findings + parent
directive) into every call, so exploration confirms a hypothesis instead of
discovering blindly. The deliverable is **two manuscripts, not code.** Code that
does not serve a manuscript is a net loss.

---

## 2. The decision you are implementing

**Both arms run on Arav's fork, `github.com/FalseAdvertising/Vanilla_RLM_Python`,
pinned at `a0ca553`.** Vanilla RLM is an *envelope-disabled configuration of the
same system*. `alexzhang13/rlm` is cited as the specification, not measured as the
artefact.

The justification, which is now in the paper, is **implementation parity**:
ablation A1 requires the arms differ *only* in the envelope, and running the
baseline on a second codebase would confound the envelope with two independent
implementations.

**The justification is NOT rate limits.** Do not write that reasoning into any
code comment, commit message, or doc. It is factually backwards —
`alexzhang13/rlm` ships `max_concurrent_subcalls=4` by default and `replm` has no
concurrency cap at all — and it is checkable in five minutes. `docs/18` §4.2 has
the detail.

---

## 3. **STOP — settle this before writing code**

There is a latent inconsistency in `docs/31` that you must not resolve on your
own. Escalate to Anugrah (Track 1) and wait.

`docs/31` A1 says the envelope-removed ablation *"is architecturally 'vanilla
RLM'"* and that *"A1 and the vanilla-RLM control are the same run — do not
implement or execute it twice."*

But the two are not obviously one flag apart:

- **Vanilla RLM** is a root REPL loop issuing flat `llm_query` sub-calls.
- **MARD** is Pass 0 → Pass 1 (per chapter) → Master Plan → 120 Tier 2 builders →
  join in plan order.

These are different *architectures*, not one architecture with a boolean. So
"envelope removed" admits two readings:

| Reading | What A1 is | Consequence |
|---|---|---|
| **(a) Stripped envelope** | MARD's pass structure, envelope emptied. `envelope/envelope.py` already has `.stripped()` and `.is_stripped` — the lever exists. | Cheap and truly one-flag-apart. But it is **not vanilla RLM**, so O3 would not be comparing against the base paper's architecture, and the paper cannot call it that. |
| **(b) Actual vanilla RLM** | `replm`'s `Orchestrator` root loop, `max_recursion_depth=1`, `enable_sub_calls=True`, same models, same document, same controls. | Genuinely the base paper's method, which is what O3 claims. But it is a *second pipeline*, so "the same run" in `docs/31` is wrong and A1 ≠ a toggle. |

**My reading is (b)**, because `docs/00-CLAIM.md` measures MARD "relative to
vanilla RLM" and the abstract already promises that. Under (b), `.stripped()` is
still worth running as a *third* configuration — it isolates the envelope inside
MARD's own architecture, which is arguably a cleaner cut than A1 — but it is not
A1 and must not be labelled as such.

Ask Anugrah which reading is authoritative, and whether `.stripped()` becomes a
fifth configuration. Do not pick one because it is easier to build.

---

## 4. What already exists — do not rebuild any of it

All of this is on disk, tested, `ruff` and `mypy` clean. 54 tests pass.

| Module | What it does |
|---|---|
| `ingest/` | PDF → `document.jsonl` / `document.txt`, sections, chapters, outline, parse quality. **Done.** `corpus/{introcs,physics1,axler}/` already populated. |
| `envelope/skeleton.py` | `Skeleton.from_sections()`, `.render()`, `.is_empty`, `.provenance` |
| `envelope/envelope.py` | `Envelope.from_skeleton()`, `.with_findings()`, `.for_child(section_id, directive)`, `.stripped()`, `.is_stripped`, `.render()`, `.to_dict()`; and `Finding` |
| `envelope/pass0.py` | `run_pass0(document_id, sections, labeller=None)` → `(Skeleton, trace)`. Seam: `TopicLabeller` protocol. |
| `envelope/pass1.py` | `run_pass1(envelope, chapters, section_titles, explorer=None)` → `Pass1Result`. Seam: `ChapterExplorer` protocol. |
| `envelope/compile_plan.py` | `compile_master_plan(...)` → `CompiledPlan`; topological ordering, `UnsequenceablePlanError`, move rationale |
| `plan/models.py`, `plan/validation.py` | The typed Master Plan and its validator |
| `orchestrate/builder.py` | `briefs_for`, `execute_plan`, `execute_plan_sync`, `join_in_plan_order`, `StubBuilder`, `IncompleteArtefactError` — fork-join, retry, failure isolation |
| `orchestrate/lm_builder.py` | `LmBuilder` (Tier 2 backed by a real model), `prompt_for(brief)`, `LanguageModel` protocol |
| `runlog/` | `RunLogger`, `load_run`, `RateCard`, `SpendCap`, `SpendLedger`, `CAMPAIGN_SEEDS = (11, 23, 42)` |

**Everything currently runs offline** with `NoOpTopicLabeller`, `NoOpChapterExplorer`
and `StubBuilder`. Your job is to put real models behind those three seams and add
the vanilla arm. That is the whole task.

---

## 5. The tasks

### T1 — Provider client + throttle (**do this first; everything depends on it**)

Build one OpenAI-backed client used by *both* arms, with a **global concurrency
limiter**. `replm` has none — bare `asyncio.gather`, no semaphore anywhere in
`src/`. You are building what `alexzhang13/rlm` gets for free.

Requirements:

- A single `asyncio.Semaphore` (or bounded pool) shared across **Tier 1, Tier 2
  and the vanilla arm's sub-calls**, so total in-flight requests are capped
  regardless of which arm is running.
- Concurrency limit and max sub-call input size both come from **config, not
  literals**, and both land in `runlog`'s config snapshot. The paper reports them.
- Run at **≤70% of the measured per-minute ceiling** (`RATE_LIMIT_BUDGET.md` §3).
  Retries draw from the same bucket as first attempts.
- Honour `Retry-After`; exponential backoff **with jitter** otherwise. Without
  jitter, builders that fork together throttle together and retry together,
  reproducing the burst.
- **A 429 is data.** Log it into the run record with its timestamp and
  `Retry-After`. Do not swallow it in a retry wrapper.
- Bounded attempts, then **fail the run loudly**. `runlog` already writes
  `summary.json` with `status: "failed"` and a traceback.

### T2 — Adapters for the three seams

There is a real signature mismatch to bridge. Check each against the source
before writing:

- `envelope.pass0.TopicLabeller` → `label(self, prompt: str, section_ids: list[str]) -> dict[str, str]`
- `envelope.pass1.ChapterExplorer` → `explore(self, prompt: str, chapter: Chapter) -> dict[str, Any]`,
  returning `{"concepts": [...], "prerequisites": [...]}`
- `orchestrate.lm_builder.LanguageModel` → `async acompletion(self, prompt: str) -> str`

**`replm`'s client does not satisfy the last one.** Its `OpenAIAdapter.acomplete`
takes `(model, messages, temperature, max_tokens, reasoning_effort)` — a different
shape entirely. Write a thin adapter; do not change `LmBuilder`'s protocol, and do
not import `replm` types into `orchestrate/` (see that module's docstring on the
editable-install trap).

Notes that will bite you:

- `pass1.run_pass1` already catches explorer exceptions and records them as a
  trace entry with an `error` field rather than crashing — *"a failed chapter is a
  finding, not a crash."* Keep that. Do not let your adapter swallow errors before
  they reach it.
- `_accept_concepts` / `_accept_edges` already validate and record rejections.
  Return raw parsed JSON; do not pre-filter.
- `pass1` dispatches **per chapter (14 for `introcs`), not per section (120)** —
  deliberate, `docs/17`. Section-level rendering put the envelope at ~1,970 tokens
  against a ~500 budget. Do not "optimise" this back.

### T3 — Reasoning-model config

If the pair is GPT-5-family (open decision, `docs/18` §7 item 1):

- Send `max_completion_tokens`, **not** `max_tokens`.
- Do **not** send `temperature` — those endpoints reject it. `RLMConfig.temperature`
  and `sub_temperature` become **dead config**. Either omit them from the run
  manifest or mark them explicitly not-applied; recording a value that was never
  sent corrupts `docs/30` §1's config snapshot.
- `reasoning_effort` is the live knob and is **root-only** — sub-calls ignore it.
  Make it a first-class snapshot field.
- Both fixes are already in `a0ca553`'s `client.py`. Read that diff before
  reimplementing.

### T4 — Pricing

`RLMConfig.cost_per_input_token` and `cost_per_output_token` default to `0.0`, and
`RLMResponse.cost` is just `tokens × those`. Left unset, **every run reports a cost
of `0.0` that looks like a measurement.**

Feed rates from `runlog.pricing.RateCard` — never hardcode. `RateCard` raises
`StaleRateError` on a rate older than 30 days, which is deliberate. `runlog` reports
cost as `null`, never `0.0`, when a model is unpriced; keep that asymmetry.

### T5 — The vanilla arm

Per §3's resolution. Assuming reading (b):

- `replm` `Orchestrator` / `RLMWrapper`, **`max_recursion_depth=1`,
  `enable_sub_calls=True`.** Library default and the base paper's primary reported
  condition.
- **`max_recursion_depth=0` is a trap.** The guard at `sub_caller.py:96` is
  `self._depth + 1 < max_recursion_depth`; the root starts at `_depth=0`, so 0 and
  1 take the *same* branch. Setting 0 does not disable sub-calls and the trace is
  indistinguishable. The real no-sub-calls condition is `enable_sub_calls=False`.
- **Log depth as an `(enable_sub_calls, max_recursion_depth)` pair**, never a
  single integer, in `runlog`'s `params`. A single integer makes A4's depth-0 row a
  silent duplicate of depth-1. This also answers Parth's open request in
  `TRACK3_HANDOFF.md`.
- Record the **fork's** git SHA, not upstream's.
- Same models, same document, same throttle, and the **same structural controls**
  as the MARD arm — front matter excluded, `outline.json` withheld. If the arms get
  different inputs the comparison isolates nothing.

### T6 — Wire `runlog` around both arms

All seven `docs/30` §1 fields per run: task score, tokens (in/out separately in the
log), calls issued split by tier, cost, wall-clock (**both `max` and `Σ` over
builders**), run identity, full config snapshot. A number that cannot be traced to
all seven from a logged run is not a number.

`MARD_SPEND_CAP_USD` must be exported or `SpendCap.from_env()` refuses to run. Set
it to something real: `docs/18` §10 measures all of Manuscript A at **~$9**. **The
old $780 is void** — that was free Vertex credits, now stranded. All money is out
of pocket. Suggest `MARD_SPEND_CAP_USD=60` for Phase A.

### T7 — Smoke run, then the matrix

1. One MARD run on `introcs` with **1 chapter**, throttled, real model. Inspect the
   rendered envelope in the trace before scaling.
2. Confirm the envelope is actually flowing: `tests/test_pass1.py::
   test_a_later_chapters_prompt_contains_an_earlier_chapters_findings` and
   `test_child_envelope_carries_parent_findings`. **If the envelope stops flowing
   downward, MARD is vanilla RLM, every O3 number measures nothing, and nothing
   else in the suite fails.** These two tests guard the entire contribution.
3. Full `introcs` MARD run. Then vanilla. Then 3 repeats of each.

---

## 6. Traps, each verified first-hand

1. **`max_recursion_depth=0` ≠ no sub-calls.** §T5.
2. **Batched sub-calls bypassed recursion before `a0ca553`.** Upstream `replm`'s
   `make_batch_fn` always used the non-recursive path, so at depth ≥ 2 a batched
   call ran flat *while logging as deeper*. The system prompt encourages batching.
   **Pin `a0ca553` or later; no A4 number from an older build is valid.** Async
   path only — and Tier 2 fork-join is the async path.
3. **`max_sub_calls=500` is global across all depths**, via one `SharedBudget`. At
   depth ≥ 2 one greedy inner orchestrator can starve its siblings and the run
   still returns an answer. Treat `MaxSubCallsExceeded` as a **failed** run. Log
   call counts per depth.
4. **Cost silently logs `0.0`.** §T4.
5. **No `seed` parameter exists in `replm`.** `docs/30` §4's "3 seeds" is
   operationally **3 repeat runs at default sampling, variance across repeats**.
   `CAMPAIGN_SEEDS` are run *identifiers*. Do not add a seed parameter to buy the
   word; OpenAI's is best-effort, not deterministic.
6. **Truncation must fail, not score low.** `join_in_plan_order` already checks for
   empty `span.text` per plan step and raises `IncompleteArtefactError` — this fix
   has landed, do not regress it. A throttled run producing empty responses would
   otherwise yield an artefact short by a section with every identity check
   satisfied and a complete-looking log.
7. **Depth numbering is off by one** between MARD's passes and `replm`'s parameter:
   MARD {0,1,2,3} ↔ `replm` {1,2,3,4}, because MARD depth 0 already issues flat
   sub-calls. **`[UNVERIFIED]`** — derived from docs, not from
   `envelope/pass1.py`'s call structure. **Checking this is a task**: confirm it and
   report back, do not assume it.

---

## 7. Rules that override your judgement

- **Feature freeze A was 23 Aug; results freeze A is 27 Aug.** A pipeline change
  invalidates every number measured before it. You are wiring seams that were
  designed for this, not adding features. If you find yourself wanting to change
  `pass1`'s prompt, `prompt_for`'s wording, or the Master Plan schema — **stop and
  ask.** Those are re-runs of the whole matrix.
- **3 repeats on every number, variance reported.** Non-negotiable.
- **A null result is publishable**, framed by the O4 structure-dependence boundary.
  Never tune toward a positive after the fact.
- **No number without a logged run. No citation without a verified row in
  `docs/40-LITERATURE_LOG.md`.** If you cannot verify something, mark it
  `[UNVERIFIED]` and surface it — never quietly assert it, never quietly drop it.
- **Escalate rather than invent.** You are one of four workstreams. If you invent a
  decision that belongs to someone else, three other sessions will invent three
  different ones. §3 is the live example.
- **Report findings, instinct and options.** Anugrah wants everything surfaced.
  A contradiction the docs do not cover is a bug to report, not a thing to resolve.

---

## 8. Acceptance criteria

- [ ] §3's A1 ambiguity escalated and answered before any arm is coded.
- [ ] One shared concurrency limiter caps total in-flight calls across both arms;
      limit and sub-call size are config-driven and appear in the run manifest.
- [ ] 429s logged with timestamp and `Retry-After`; jittered backoff; bounded
      attempts then a loud failure.
- [ ] Real `TopicLabeller`, `ChapterExplorer` and Tier 2 `LanguageModel` behind the
      existing protocols, with no change to those protocols.
- [ ] Cost non-zero and sourced from `RateCard`; `MARD_SPEND_CAP_USD` exported.
- [ ] Vanilla arm at `(enable_sub_calls=True, max_recursion_depth=1)`, logged as a
      pair, fork SHA recorded, identical structural controls to MARD.
- [ ] Both envelope-flow tests pass against real model output, not stubs.
- [ ] Truncated artefacts fail the run rather than scoring low.
- [ ] `ruff check`, `ruff format --check`, `mypy` clean; all existing tests still
      pass; new code has tests.
- [ ] One MARD run and one vanilla run on `introcs` in `runs/`, each with all seven
      `docs/30` §1 fields populated.
- [ ] The depth-mapping `[UNVERIFIED]` in `docs/18` §5.2 either confirmed against
      `envelope/pass1.py` or still flagged, with what you found.
- [ ] Nothing anywhere attributes the library choice to rate limits.
