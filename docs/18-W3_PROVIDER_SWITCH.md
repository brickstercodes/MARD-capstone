# 18 — W3 provider switch: Vertex/Gemini → OpenAI, and the replm control

**Status:** Decided 26 Aug 2026, mid-W3 · Decision owner: Anugrah Shetty (Track 1) ·
Type: ADR-style, per global `CLAUDE.md` Part 7 · **Supersedes** `docs/12-MODEL_PAIR.md`
on provider and model pair, and `docs/30-MEASUREMENT_PROTOCOL.md` §6 on the sanity check.

This record exists because a provider change after Feature freeze A (23 Aug) touches
almost every frozen document at once. Rather than rewrite frozen text — which
`docs/30` §8 and `docs/31`'s preamble both forbid without an explicit protocol change —
the frozen documents keep their bodies and carry a dated banner pointing here. **This
document is the current state; where it and an older document disagree, this one wins.**

> **⚠ §4.2's CLOSED decision below is REVERSED, 28 Aug 2026, on Anugrah's direct
> instruction.** The control library is `Zhang_RLM` (`FalseAdvertising/Zhang_RLM @
> 62acf7b`), not `replm`. §1 items 2–3, §4.2, and §5–§5.6 below describe the
> superseded `replm` decision and are kept as the historical record of why the
> control library changed — read the new addendum at the end of §4.2 first, then
> treat everything naming `replm` as history, not current state. `docs/19` and
> `docs/20` name `replm` throughout and carry the same superseded status.

---

## 1. Decision

1. **Provider is OpenAI.** Google Cloud Vertex AI is abandoned for the remainder of the
   project.
2. ~~The vanilla RLM control runs on `replm`~~ **REVERSED 28 Aug 2026 — see §4.2
   addendum.** The control is
   [`github.com/FalseAdvertising/Zhang_RLM`](https://github.com/FalseAdvertising/Zhang_RLM),
   **pinned to full SHA `62acf7b9fb70baf78b899213fec5aea9951c8341`**. `replm` is
   retired, not kept as a fallback.
3. ~~Control configuration is `max_recursion_depth=1`, `enable_sub_calls=True`~~
   **REVERSED — see §4.2 addendum.** Control configuration is `max_depth=1` — Zhang's
   own default, and the base paper's primary reported condition (`CONTEXT.md` §1.6).
4. **The model pair is not yet re-decided.** `docs/12-MODEL_PAIR.md`'s Gemini pair is
   void; no OpenAI pair has been selected on evidence. See §7 item 1 — this is the
   single largest open item and it blocks the O6 cost model.

## 2. Context — why

Vanilla RLM could not be made to run against Vertex AI. The failure mode was
**malformed function call errors** from the Gemini endpoint, not a defect in our code,
and it consumed roughly **₹2,000 beyond the free credit allocation** before the switch
was called. The ₹90,000 Vertex credit balance that justified the Gemini pair in
`docs/12-MODEL_PAIR.md` is therefore stranded: it is redeemable through Vertex only, and
we are no longer running on Vertex.

Two things follow that are worth naming plainly rather than discovering later:

- **The budget premise is gone, and the money is now out of pocket.** `MARD_SPEND_CAP_USD=780`
  was ₹75,000 at ₹95.13/USD on 9 Aug, drawn against a **₹90,000 Google Cloud credit
  balance that was free**. That balance is stranded — redeemable through Vertex only —
  and **there is no replacement grant**. Every OpenAI token from 26 Aug onward is paid
  personally by the team. The $780 figure is void as both a ceiling and a budget: it
  described money that was given to us, not money we have. See §10 for what the work
  actually costs, which is the number that matters now.
- **This happened after Feature freeze A.** Per `CONTEXT.md` §3.4 a pipeline change
  invalidates every number measured before it. No Manuscript A number existed on 26 Aug,
  so nothing was invalidated in practice — but the freeze's letter was broken, and the
  manuscript's §3 must say so rather than present a pipeline that was never frozen as
  frozen.

## 3. What this voids

| Document | What is now void | What replaces it |
|---|---|---|
| `docs/12-MODEL_PAIR.md` | The entire decision: both models, the provider, the GDM-MRCR v2 evidence table, and the ₹75,000-from-credit budget framing | Nothing yet — §7 item 1 |
| `docs/30-MEASUREMENT_PROTOCOL.md` §6 | "Reproduce Google's GDM-MRCR v2 for `gemini-3.6-flash` on Vertex" | §6 below — reproduce a **base-paper** number instead |
| `docs/30-MEASUREMENT_PROTOCOL.md` §1, "Cost" row | "same-day published Vertex AI rate" | Same-day published **OpenAI** rate, same discipline |
| `RATE_LIMIT_BUDGET.md` §2 | The whole supply table: Vertex per-project quotas, `location=global`, "Vertex AI only" | Unwritten. Its own deadline was "before W3" — that is now past |
| `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md` | The entire document — it patches a Vertex path we do not use | Nothing. Retain for the record, do not maintain |
| `RLM_BASELINE_SURVEY.md` §1, §3 | The 14-example inventory and the blocked-on-keys list — they describe `alexzhang13/rlm`, not `replm` | §4 below |
| `RLM_BASELINE_SURVEY.md` §2 | **Not void — but its citations now point at a library that may not be the control.** See §4 | §4 below |
| `docs/40-LITERATURE_LOG.md` rows 3–10 | Not void as *verified sources* — they were correctly verified. But rows 3–7 and 10 no longer support any live decision | Rows stay; a status column note marks them as historical |

**Nothing in `docs/00-CLAIM.md`, `docs/16-PRIMARY_DOCUMENT.md`, `docs/17-W1_DECISION_POINTS.md`
or `docs/31-ABLATIONS.md`'s definitions is affected.** The claim is provider-agnostic, the
primary document is `introcs` on evidence, the two-pass decision stands, and the four
ablations toggle the same things they always did. `docs/31` gains one clarification only
(§5 below), not a redefinition.

## 4. The library question — **open, and it is Track 1's to answer**

This is the consequence most likely to be missed, so it is stated first among the risks.

`RLM_BASELINE_SURVEY.md` documents `alexzhang13/rlm` — the base paper's *own* library —
vendored at `.vendor/rlm`, installed as `rlms==0.1.3`, **MIT** (the survey's `72d6940`
and "CC BY 4.0" are both wrong — the vendored copy is at `caf0bff`; see §4.1). The
control now runs on **`replm`**, a *different* implementation: MIT licensed, version
0.1.0, `Development Status :: 3 - Alpha`, no shared lineage with `alexzhang13/rlm` in its
history.

**A reviewer will ask why the vanilla-RLM baseline is not the RLM authors' own code.**
That question has a good answer available — the authors' `GeminiClient` had no Vertex
path (`docs/12-MODEL_PAIR.md` Consequence 2), and `replm` is OpenAI-native — but the
answer has to be *written down and defended*, not left implicit. Whatever `replm` does
differently from `alexzhang13/rlm` is now part of the measured baseline, and O3's entire
delta is measured against it.

Two things this changes that are already paid for:

- **`RLM_BASELINE_SURVEY.md` §2.2 still holds, and holds more cleanly.** Verified
  first-hand in `replm` on 26 Aug: `sub_caller.py` constructs the inner orchestrator with
  `query=prompt, context=prompt` and a shared budget, and **nothing else** — no parent
  findings, no skeleton, no directive. The upward/observational vs downward/operative
  distinction that §2.2 draws is, if anything, sharper here.
- **§2.3's trap disappears, and that is a small loss.** `replm` has no `root_prompt`
  equivalent — there is no user-injectable downward slot to be accused of having used.
  But the objection *"you just used `root_prompt`"* is about the base paper's reference
  implementation, so §2.3 still belongs in related work even though it no longer
  describes the control. Its file-and-line citations into `.vendor/rlm` remain valid
  **as citations of `alexzhang13/rlm`** and must be labelled as such, not as citations
  of the system we ran.

### 4.1 Does `alexzhang13/rlm` run on OpenAI without the fixes Arav had to make?

Checked first-hand on 26 Aug 2026 against a clean clone, because it changes §7 item 2.
**Neither of the two defects Arav fixed in `replm` exists there.**

| Arav's fix in `replm` `a0ca553` | Status in `alexzhang13/rlm` |
|---|---|
| `max_tokens` → `max_completion_tokens` for reasoning models | **Already done.** `_normalize_sampling_args` (`rlm/clients/openai.py`) renames it, with a docstring explaining it matches verifiers' client. Verified: `N({'max_tokens': 8192})` → `{'max_completion_tokens': 8192}` |
| Don't send `temperature` to reasoning models | **Cannot occur by default.** `replm` hardcoded `temperature=temperature` into every request. Here temperature is *opt-in* via `sampling_args`, which `base_lm.py:28` defaults to `{}`, and nothing in the codebase sets it. Verified: `N({})` → `{}` — an empty request body |
| Batched sub-calls silently bypass recursion | **Structurally impossible.** `_rlm_query_batched` (`local_repl.py:335`) routes through **the same `self.subcall_fn`** as single `rlm_query` (`:326` vs `:358`/`:374`). `replm`'s bug existed because its batch path was a *separate* function that forgot the depth check |

**Keyless smoke test passed** (the `MockLM` pattern from `RLM_BASELINE_SURVEY.md` §1.2,
with `get_client` monkeypatched): root loop → REPL code execution → `llm_query` sub-call
→ FINAL, 5 calls, `sampling_args={'seed': 11}` carried through intact. This proves the
orchestration path executes; it does **not** prove the OpenAI wire format, which needs a
real key.

**Three things it has that `replm` does not**, all of which matter to us:

- **`sampling_args` accepts `seed`** (`base_lm.py:26` names it explicitly, verified
  carried through). `replm` has no seed parameter at all. This partially restores
  `docs/30` §4's literal reading — still best-effort at OpenAI, but the plumbing exists.
- **`other_backends` + `sub_sampling_args` route depth-1 sub-calls to a different
  model** — the Tier 1 / Tier 2 split as a first-class library feature.
- **`on_subcall_start` / `on_subcall_complete` / `on_iteration_start` callbacks carry
  depth**, which is most of what `runlog` needs to record per-depth call counts.

**Two API differences Track 3 must absorb**, neither hard: the constructor arg is
`environment=`, not `environment_type=`; and `completion()` takes **one prompt string
with the context inline** (as the library's own `quickstart.py` does), not `replm`'s
separate `query=` / `context=`.

**The strongest single signal:** the library's own `quickstart.py` targets
**`gpt-5-nano`** — a reasoning model on OpenAI — as its default example. The path we
need is the path its authors demonstrate.

**Depth semantics differ slightly, and in Zhang's favour.** `max_depth=1` means root RLM
+ flat sub-calls, identical to `replm`'s `max_recursion_depth=1`, so §5.2's mapping
table is unchanged. But `max_depth=0` is *meaningful* here — `if self.depth >= self.max_depth`
(`rlm/core/rlm.py:350`) makes the root itself fall back to a plain LM call — rather than
being `replm`'s silent duplicate of 1. §5.1's trap is a `replm` trap only.

**Licensing:** both are **MIT**. `RLM_BASELINE_SURVEY.md`'s "CC BY 4.0" for
`alexzhang13/rlm` is **wrong** — its `LICENSE` reads *"MIT License, Copyright (c) 2026
Alex Zhang"*, `pyproject.toml` declares `license = "MIT"`, and no "CC BY" or "Creative
Commons" string appears anywhere in the repository (checked 26 Aug 2026). Corrected in
that document. The W9 reproducibility appendix attributes MIT either way.

### 4.2 CLOSED, 27 Aug 2026 — both arms on one implementation

**Decision.** MARD and vanilla RLM are both executed on Arav's fork
(`FalseAdvertising/Vanilla_RLM_Python`). Vanilla RLM is implemented as an
**envelope-disabled configuration of the same system**, which is what `docs/31` A1
already specifies. `alexzhang13/rlm` is cited as the *specification we implement
against*, not measured as the artefact.

**The justification is implementation parity.** A1 requires the two arms differ *only*
in the presence of the envelope. Running the baseline on a second codebase would confound
the envelope with two independent implementations — different prompt templates, different
REPL surfaces, different stopping criteria — none of which is the variable under study.
This is a standard and defensible methodological choice, and it is true.

**The justification is NOT rate limits, and that reasoning must not appear anywhere.**
It was considered on 27 Aug and rejected as factually wrong in a way any reviewer can
check in five minutes:

- **Rate limits are a property of the OpenAI account, not of a library.** The tier caps
  apply identically to both. `replm`'s Tier 2 fork-join produces the same burst —
  `RATE_LIMIT_BUDGET.md` §1.3 predicted its shape exactly.
- **The comparison runs the wrong way.** `alexzhang13/rlm` ships a concurrency limiter
  by default (`max_concurrent_subcalls = 4`, threaded through the environment and
  semaphore-gated: `rlm/core/rlm.py:72`, `environments/local_repl.py:366`,
  `environments/ipython_repl.py:136` and `:586`). **`replm` has no concurrency cap at
  all** — bare `asyncio.gather`, no semaphore anywhere in `src/`. Claiming we left Zhang's
  over concurrency says we left the library that has a throttle for the one that does not.
- **The degradation was ours.** The incomplete and inaccurate responses came from a
  hand-rolled throttling patch — which was reimplementing `max_concurrent_subcalls` —
  not from the reference implementation. Reporting that as baseline underperformance
  would attribute our harness's degradation to the control and **inflate MARD's delta**.
  That is precisely what A1 exists to prevent.

**Consequences we accept, and must state.**

1. **The baseline is our own implementation of RLM, not the authors'.** One sentence in
   limitations. The mitigation is `docs/30` §6's harness sanity check — reproduce a
   published base-paper number first-hand — which is **now load-bearing**, because it is
   the only evidence the vanilla arm is a faithful RLM. On OpenAI this is finally
   possible (§6).
2. **We inherit the concurrency gap.** Adopting `replm` means *building* the throttle
   Zhang's already had. This is a required task, not an optimisation — without it Tier 2
   fires 120 builders at once.
3. **Throttling is a study-wide operating constraint, disclosed in §4 and limitations,
   and applied identically to both arms.** If only one arm is throttled the comparison is
   void — and the direction of that error favours MARD, which is the worst way to be wrong.

**Still uncompared ⚠ (debt row 2):** prompt templates, REPL surface, stopping criteria.
Under this decision these matter *less* — we are no longer comparing two implementations
against each other — but they still decide how faithfully our vanilla arm reproduces the
published RLM, which is what item 1's sanity check has to establish.

### 4.2 addendum — REVERSED, 28 Aug 2026

**Decision.** Both arms move from `replm` to `Zhang_RLM`
(`github.com/FalseAdvertising/Zhang_RLM`, pinned to full SHA
`62acf7b9fb70baf78b899213fec5aea9951c8341`, 27 Aug 2026, Arav Sharma — a fork of
`alexzhang13/rlm` that fixes a Windows/UTF-8 encoding defect in the REPL's context
loading and bundles an example script). `replm` is retired entirely: not deprecated,
not kept as a fallback — `.vendor/replm` is deleted and `scripts/bootstrap_replm.sh`
is removed.

**On whose authority, and why now rather than 27 Aug.** Anugrah instructed the switch
directly, 28 Aug 2026. The reasoning above — implementation parity, "not rate
limits" — is not wrong and is not being retracted; §4.1's own comparison (written the
same day as the CLOSED decision it now overturns) already laid out why a
Zhang-lineage library is the stronger choice: `alexzhang13/rlm` ships
`max_concurrent_subcalls` where `replm` has no cap at all, `other_backends` +
`sub_sampling_args` give a first-class Tier 1 / Tier 2 model split, `sampling_args`
carries a real `seed`, and `orchestrate/lm_builder.py`'s `LanguageModel` protocol was
declared structurally *because* `rlm.clients.base_lm.BaseLM` satisfies it and
`replm`'s `OpenAIAdapter.acomplete(...)` does not — meaning `Zhang_RLM` gives both
arms a **shared client layer**, which is *stronger* parity than `replm` provided, not
weaker. The prior decision weighed "one fewer implementation to defend" against these
gaps and chose the former; this decision weighs them the other way. **The rate-limit
prohibition still applies and is not what changed:** nothing about this reversal is
justified by throughput, and that reasoning must not appear anywhere either.

**What is actually different from the real `Zhang_RLM` API** — verified first-hand
against the pinned commit, not inferred from a prior draft of this plan: there is no
`RLMWrapper`/`RLMConfig` (everything is a constructor kwarg on `rlm.core.rlm.RLM`
itself); `.completion(prompt, root_prompt)` is **synchronous**, not `.agenerate()`;
there is no `reasoning_effort` parameter; `on_iteration_start`/`on_iteration_complete`
are declared but **never invoked** at this pinned commit (verified by grep across the
whole fork — dead code, not a wiring bug on our side); and there is **no
client-injection seam** — `RLM.__init__`'s `backend_kwargs` always builds its own
`openai.OpenAI`/`openai.AsyncOpenAI` internally, so `provider.openai_client
.ThrottledAsyncOpenAI` cannot be handed to it the way `replm`'s
`RLMWrapper(client=...)` allowed. `vanilla/run.py` and
`vanilla/openai_logging_bridge.py` document the resulting design (429/retry
visibility via the `openai` SDK's own logger, not via client injection).

**Consequences accepted, updating §4.2's original three:**

1. The baseline is still our own implementation of RLM, not the authors' — unchanged.
2. **The concurrency gap is gone, not inherited.** `Zhang_RLM` ships
   `max_concurrent_subcalls` (default 4) and its own per-environment
   semaphore/thread-pool gating. `provider/throttle.py`'s hand-rolled `Throttle` is
   **not** threaded through the vanilla arm's calls — it remains in place only for
   MARD's own Tier 1/2 calls via `provider/seams.py`, which never go through Zhang's
   `RLM` at all.
3. Throttling is still a study-wide, disclosed, identically-applied constraint —
   unchanged in spirit, different mechanism per arm.

**Correction, 28 Aug 2026 — §4.1's `on_subcall_start`/`on_subcall_complete` claim
(line 139) is incomplete, found from a real smoke run, not from reading source.**
§4.1 says these callbacks "carry depth, which is most of what `runlog` needs" —
true only when a sub-call actually recurses (`next_depth < max_depth`). At our fixed
`max_depth=1`, `next_depth` is always `1`, so `_subcall()`'s
`if next_depth >= self.max_depth:` branch is taken every time — the plain-LM-completion
early return, which calls the client directly and returns *before* either callback
later in the function. A real 20-page smoke run confirmed this empirically: `gpt-5-mini`
was clearly called (29,730 input / 17,235 output tokens landed in `usage_summary`),
and `events.jsonl` contains zero `vanilla_subcall_*` records.

**This was first written up as a limitation ("cannot be satisfied for the vanilla
arm") and that framing was wrong — caught and corrected the same day.** The
measurement is not lost, only the callback: `_llm_query`/`_llm_query_batched`/
`_rlm_query`/`_rlm_query_batched` (`local_repl.py`) all append the real
`RLMChatCompletion` they get back — real prompt, real response, its own
`usage_summary`, its own `execution_time` — to `self._pending_llm_calls`, which
surfaces as `REPLResult.rlm_calls` on every code block inside the `RLMLogger`
trajectory this wrapper already attaches, independent of whether the callbacks fire.
`vanilla/run.py`'s `_walk_subcalls`/`_log_subcall_detail` now read that directly:
real per-sub-call timing feeds genuine `max`/`Σ` wall-clock, and real per-sub-call
prompt/response/tokens are logged via `vanilla_subcall_detail` events —
`_reconcile_usage` cross-checks the granular sum against `usage_summary` and logs a
`vanilla_usage_reconciliation_mismatch` event if they ever diverge, rather than
trusting either silently. Cost/token totals still come from `usage_summary` alone
(`_log_usage`), never from this granular walk, so a gap in trajectory capture can
never under-count real spend. No limitation to write into Manuscript A after all —
losing the callbacks cost real-time verbose-output convenience during a run, not any
measurement `docs/30` §1 requires.

**Second correction, same day, from the first full-corpus run rather than the
20-page smoke test: batched sub-calls' per-call metadata is unreliable, in a way
`_reconcile_usage` was built to catch and did.** The B1 run (`runs/…s11__ec9d17`)
issued two `rlm_query_batched`/`llm_query_batched` calls of 7 prompts each (one per
chapter — real, distinct prompts and responses, verified by reading them). Within
each batch, all 7 logged entries shared byte-identical `execution_time` and token
counts. Traced to `LMHandler._handle_batched` (`rlm/core/lm_handler.py`): it calls
`client.get_last_usage()` **once, after `asyncio.gather()` returns**, and stamps
that single snapshot onto every completion in the batch. `OpenAIClient.get_last_usage()`
(`rlm/clients/openai.py`) reads `self.last_prompt_tokens`/`last_completion_tokens` —
plain instance attributes with no lock, last-writer-wins under N concurrent async
tasks. `execution_time` is `total_batch_time / len(prompts)`, an average, labelled as
such in Zhang's own code comment ("approximate per-prompt time"). Real bug (or at
minimum severe imprecision) in the vendored library's batched path, not in this
wrapper's reading of it — the B1 run's `vanilla_usage_reconciliation_mismatch` event
(granular sum 431,151 in / 57,750 out vs. `usage_summary`'s 482,998 / 50,982) is
exactly this, caught by the check built for exactly this kind of thing.

**What still holds and what doesn't, precisely:** cost/token totals (`_log_usage`,
never derived from the granular walk) are unaffected — `usage_summary` comes from
the client's own cumulative counters, correct regardless of this bug. `Σ` over
sub-calls stays meaningful for a batch (N copies of `total_time/N` sum back to the
true `total_time`). `max` over sub-calls does **not** — comparing averages-per-batch
is not comparing true peak single-call latency, and likely understates real
intra-batch variance. State this precisely if `docs/30` §1's wall-clock figure for
B1 goes in Manuscript A: `Σ` is real, `max` is a batch-average proxy, not a peak.

**Third correction, same day: B1's `concept_count` figure was wrong on the second
repeat, in the direction that looked like a collapse.** Seed 11 reported 156
concepts; seed 23 initially reported **14** — read as-is, that looks like a
catastrophic variance between two repeats of the same frozen prompt on the same
document. It was a counting bug, not a result: seed 23's answer nested concepts one
level deeper than seed 11's (14 `## Chapter N` wrapper headings, each holding
several `### Concept Name` entries — 190 of them), and `_count_concepts`
(`vanilla/run.py`) only ever looked at `##`, so it silently reported the *wrapper*
count as the concept count. The frozen prompt (`docs/21` §3.1) does not mandate a
heading structure, and this is the second time in one day a fixed-format assumption
broke on real model output (the first being the `on_subcall_start` claim above) —
fixed to take whichever heading level (numbered `##`, plain `##`, or `###`) has the
*most* matches, since concepts are always the finest structural unit and so always
outnumber any wrapper level. Corrected count: **190**, not 14. Re-verified against
both real answer files directly, not just re-read from code.

**The corrected saturation picture, with real numbers from two repeats:** 49
concepts (20 pages) → 156 (seed 11, full 916 pages) → 190 (seed 23, full 916
pages). Full-document counts are in the same 150–190 range across two independent
repeats — much closer to each other than either is to the 20-page slice — which is
a real, if noisy, signal of *something* stabilizing at full-document scale. It is
not the clean "saturates at ~50" story hoped for, and the seed-11-vs-23 spread
(156 vs 190, ~20%) is exactly the kind of variance `docs/30` §4's "3 repeats,
variance reported" exists to catch before anyone quotes a single run's count as if
it were the number.

**Fourth finding, same day, from B1's third repeat (seed 42) — not a harness bug,
a real property of the vanilla arm at full-document scale worth reporting.**
Seed 42's `concept_count` is 75 — apparently converging further, not diverging.
It doesn't: at least 41 of those 75 concepts (`runs/…s42__1dbe85`, iteration 14's
own `missing_outline` count) were generated **with no textbook grounding at all**,
traced precisely via `vanilla_subcall_detail`. For "Trees and balanced trees":
attempt 1 (correct source chunks) failed JSON parsing and was discarded; attempt 2
pulled a completely unrelated chunk — a multiple-choice quiz page about
"enterprise architecture levels" — because the root's self-authored
`chunks_for_includes` mismatched concept names to chunk indices, and that attempt
was also discarded on a parse failure; attempt 3 dropped source text entirely
(`SOURCE:` empty, 88 input tokens) and generated the explanation from
`gpt-5-mini`'s general knowledge alone. That third, sourceless response is the
exact text that appears in the published final study guide — confirmed by matching
phrasing verbatim. Nothing in the final answer or in `status: "ok"` shows this: the
content itself reads as accurate, coherent CS material, and the sourceless model
didn't get derailed by the earlier mismatched chunk, it simply answered from its
own knowledge. But it is not what the frozen prompt (`docs/21` §3.1) asks for —
"the textbook available in `context`" — for at least 55% of this run's concepts.

**This is the root model's own bug, in code it wrote itself** (a regex splitting
"Explanation:"/"Check yourself:" sections, and the includes→chunk-index matching),
not a defect in `vanilla/run.py` or `Zhang_RLM`. It is a genuine, reportable finding
about vanilla RLM's robustness at full-document scale: when the root orchestrates
its own multi-stage pipeline (extract → cluster → retrieve source → explain), a bug
in its self-authored glue code can silently degrade a large fraction of the output
to ungrounded generation, invisible without walking the full trajectory — no
exception, no truncation flag, no TOC artifact, nothing `docs/30` §1's aggregate
fields would ever surface. Worth its own line in Manuscript A's limitations or
discussion, not something to quietly fix or drop. Also explains seed 42's cost/time
outlier ($1.60, 776.1s vs $0.32/152.5s and $0.58/437.2s) — iterations 11–16 were
largely the root fighting its own parsing failures.

**Concept counts across all three B1 repeats, corrected:** 156 (seed 11) / 190
(seed 23) / 75 (seed 42, ≥41 of which are known-ungrounded). This is a much wider,
noisier spread than the two-repeat picture above suggested, and seed 42's number
carries an asterisk the other two don't. Do not average these three into a single
"vanilla arm produces ~140 concepts" figure without carrying this caveat forward.

**§5–§5.6 below describe `replm` and are superseded, kept as the historical record of
the decision this reversed — not current state.** The A4 depth-numbering mapping in
§5.2 does *not* transfer to `Zhang_RLM`'s `max_depth`; re-derive it against
`envelope/pass1.py`'s actual call structure rather than assuming the table above still
applies (still `[UNVERIFIED]` either way — see §8 item 1).

## 5. `replm` facts established first-hand (source read 26 Aug 2026) — SUPERSEDED, historical only

> Everything in this section describes `replm`, which is no longer the control
> (§4.2 addendum, 28 Aug 2026). Kept unedited as the record of why `replm` was chosen
> and then left, not as a description of the current harness.

Each of these was read out of the pinned source, not inferred from the README.

### 5.1 `max_recursion_depth=0` is a trap — it does **not** disable sub-calls

The recursion guard is `self._depth + 1 < self._config.max_recursion_depth`
(`sub_caller.py:96`). The root orchestrator starts at `_depth=0`, so:

| Setting | Guard evaluates | Behaviour |
|---|---|---|
| `max_recursion_depth=0` | `1 < 0` → False | flat one-shot sub-calls |
| `max_recursion_depth=1` | `1 < 1` → False | flat one-shot sub-calls — **identical** |
| `max_recursion_depth=2` | `1 < 2` → True | inner orchestrator spawned |

Setting 0 silently produces a depth-1 run whose trace is indistinguishable from a
genuine depth-1 run. The real no-sub-calls condition is `enable_sub_calls=False`, which
`config.py` documents as *"Set to `False` to reproduce the 'RLM (no sub-calls)' ablation
from the paper."*

**Consequence for `docs/31-ABLATIONS.md` A4:** the depth sweep must be recorded as an
**`(enable_sub_calls, max_recursion_depth)` pair, never a single integer.** A single
integer makes the depth-0 row a silent duplicate of the depth-1 row. This also answers
Parth's open request #2 in `TRACK3_HANDOFF.md` — *"tell me what identifies a run for
you"*: depth must be **two** first-class fields in `runlog`'s `params`, not one.

### 5.2 Off-by-one between `docs/31` A4 and `replm`'s numbering

`docs/31` defines A4 depth as the recursion depth of *Pass 2 deep-dive calls*, with MARD
depth 0 meaning Pass 0 + Pass 1 only. But MARD at depth 0 **already** has a root issuing
flat sub-calls — Pass 1 per chapter, Tier 2 builders per section — which is `replm`
depth 1, not 0.

| MARD A4 depth | `replm` `max_recursion_depth` |
|---|---|
| 0 — two-pass, Manuscript A | **1** |
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |

`docs/31` A1 requires depth held fixed between the MARD arm and the control. **Setting
the control to `replm` 0 or 3 to "match" a MARD depth number makes O3 measure a depth
difference wearing the envelope's name.** This is a clarification of A4's operational
meaning, not a redefinition of what A4 toggles.

**Recommendation, not yet decided (§7 item 3):** redefine A4's sweep as `replm` {1,2,3}
= MARD {0,1,2} and stop there, rather than paying for `replm` 4 to satisfy a "3" that was
chosen against a different numbering scheme. `docs/31` already authorises cutting from
the top: *"cut from the top (depth 3 first), never from depth 0/1."*

**Caveat, flagged rather than asserted:** this mapping is derived from `docs/31`'s prose
plus the W1 decisions in `docs/17`. It has **not** been checked against
`envelope/pass1.py`'s actual call structure. Do that before it hardens into a table
caption.

### 5.3 The batch-recursion bug Arav fixed — and what it would have cost us

Commit `a0ca553` fixes a defect in upstream `replm`'s async path.
`AsyncSubCallManager.make_batch_fn()` always dispatched through `_async_llm_query` — the
**plain, non-recursive** path — regardless of `max_recursion_depth`. Only single
`llm_query()` calls ever recursed.

The root model's system prompt contains explicit batching guidance, so the root is
*encouraged* to call `llm_query_batch`. The net effect: **any depth ≥ 2 run through the
async orchestrator in which the root batched would have executed at depth 1 while being
logged as depth 2 or 3.** Every A4 point above depth 1 would have been silently wrong,
and the run log would have agreed with the label.

This is precisely the failure class `RATE_LIMIT_BUDGET.md` §intro names — *"a run dies at
hour six of a matrix, and the hole in the table gets discovered on the day the manuscript
is due"* — except worse, because there would have been no hole, just a wrong number.

The fix routes batched prompts through `_async_recursive_query` when
`depth + 1 < max_recursion_depth`, gathering them concurrently, and ships with a
regression test (`test_batch_respects_recursion_depth`) that asserts
`sub_call_start` events carry `recursive: True`.

**The synchronous `SubCallManager` has no batch function at all**, so this defect is
async-path-only. MARD's fork-join Tier 2 is the async path.

**Therefore: no A4 number may be quoted from any `replm` build older than `a0ca553`.**
The `runlog` config snapshot already records a git SHA and dirty flag
(`TRACK3_HANDOFF.md`), which is what makes this auditable — the SHA must be the SHA of
the *fork*, not of upstream.

### 5.4 Reasoning models reject `temperature` — and the seed policy follows

The same commit fixes `OpenAIAdapter` for reasoning-model families (`o1`, `o3`, `o4`,
`gpt-5`): those endpoints require `max_completion_tokens` rather than `max_tokens`, and
**reject a custom `temperature`** — they run at the default only.

Consequences, if the pair selected in §7 item 1 is GPT-5-family:

- `RLMConfig.temperature=0.6` and `sub_temperature=0.4` become **dead configuration**.
  They will be recorded in the `runlog` manifest and will not have been applied. That is
  a `docs/30` §1 "config snapshot" integrity problem, and the manifest must either omit
  them or mark them not-applied.
- `reasoning_effort` becomes the live knob instead, and it is **root-only** — `config.py`
  states sub-calls are unaffected. It must be a first-class field in the config snapshot.
- **There is no `seed` parameter anywhere in `replm`.** `client.py` sends only
  `model / messages / max_completion_tokens` (+ `temperature` for non-reasoning models,
  + `reasoning_effort` via `extra_body`). Confirmed by grep across `src/`.

`docs/30` §4's "3 seeds on every number" therefore means, operationally: **three repeat
runs at the API's default sampling, with variance reported across repeats.** This is not
a weakening. `TRACK3_HANDOFF.md` already anticipated it — *"local seeding does nothing to
a hosted model, which is part of why we report variance rather than assume
determinism"* — and `runlog`'s `CAMPAIGN_SEEDS = (11, 23, 42)` continue to serve as **run
identifiers** rather than as decoding seeds. Against SRLM's *"your improvement is noise"*
attack (`CONTEXT.md` §1.7 challenge 3), variance across genuine repeats is the stronger
evidence anyway.

A ~5-line patch could pass OpenAI's `seed` through, but OpenAI documents it as
best-effort rather than deterministic. **Recommend not patching** — it would buy the word
"seed" and not the property.

### 5.5 Cost silently logs as zero unless configured

`RLMConfig.cost_per_input_token` and `cost_per_output_token` default to `0.0`, and
`RLMResponse.cost` is simply `tokens × those`. Left unset, every `replm` run reports a
cost of `0.0` that looks like a measurement.

`runlog` gets this right in the opposite direction — `TRACK3_HANDOFF.md` item 2: cost is
`null`, never `0.0`, when a model has no rate, and unpriced models are listed in
`unpriced_models`. **The rate must reach `replm` from `runlog.pricing.RateCard`, not be
hardcoded**, or there will be two prices and one of them will go stale — the exact
failure `CONTEXT.md` §2.3 records for the dead "15–25× cost reduction" claim.

### 5.6 Available for free on `RLMResponse`

`total_input_tokens`, `total_output_tokens`, `sub_calls`, `iterations`,
`elapsed_seconds`, and the full `history` trace. Between these and `runlog`, six of
`docs/30` §1's seven required fields are covered without new code; the seventh, task
score, is Track 3's scorer.

Other defaults worth knowing: `max_iterations=25` per orchestrator, and
`max_sub_calls=500` shared **globally across all depths** through a single
`SharedBudget`. At depth ≥ 2 one greedy inner orchestrator can consume the whole budget
and starve its siblings while the run still returns an answer. **Treat
`MaxSubCallsExceeded` as a failed run, not a degraded one**, and log call counts per
depth.

## 6. Replacement sanity check — and the one thing the switch improved

`docs/30` §6 requires that a published benchmark number be reproduced on our own harness
before any MARD number is trusted. `docs/12-MODEL_PAIR.md` Consequence 1 had to
substitute a Google MRCR v2 reproduction for the base-paper reproduction *because* the
pair was Gemini and the base paper is GPT-5-family only.

**That constraint is gone.** On OpenAI, Track 3 can do what `CONTEXT.md` §3.3 originally
assigned and `docs/12` had to give up: **reproduce a base-paper number first-hand**
(RLM, arXiv:2512.24601 — `docs/40` row 1 has the verified figures). SRLM is GPT-5-family
too, so a second anchor is available if wanted.

This is a strict improvement over the Gemini-era substitute and should be stated as such
in the manuscript's limitations rather than buried: the provider change was forced, and
it happened to restore the stronger check.

**Owner:** Track 3. **Before** any MARD number is quoted.

## 7. Open decisions — Track 1's, not resolved here

Per `CONTEXT.md` §4.2 and this project's escalation discipline, these are surfaced, not
decided.

| # | Decision | Blocks | Needed by |
|---|---|---|---|
| 1 | **The OpenAI model pair.** Tier 1 and Tier 2 model IDs, on published evidence, with same-day rates from OpenAI's own pricing page. `docs/12`'s successor. | O6 cost model, every run, `RateCard` | Immediately — it blocks §6 too |
| 2 | ~~Is the control `replm` or `alexzhang13/rlm`?~~ CLOSED 27 Aug on `replm` — **REVERSED 28 Aug, see §4.2 addendum.** Both arms now run on `Zhang_RLM @ 62acf7b`. Justification is still **implementation parity**, not rate limits; the instantiation changed, not the argument. | — | Closed |
| 3 | **A4's sweep range** under the corrected mapping (§5.2) — `replm` {1,2,3} or {1,2,3,4}. | W6 provisioning, `RATE_LIMIT_BUDGET.md` §1.1 arithmetic | Before W5 |
| 4 | **The out-of-pocket ceiling.** §10 measures the whole project at roughly **$150–200**, so this is a decision about an affordable number rather than a constraint on the science. But `SpendCap.from_env()` refuses to run without an explicit value and `MARD_SPEND_CAP_USD` is still not exported anywhere persistent. **Set it to something real and small** (§10 suggests $60 for Phase A) rather than carrying $780 forward. | Every run | Immediately |
| 5 | **Whether Pass 2 runs for the 29 Aug review.** Reverses `docs/17`'s Trigger B decision, and confounds envelope with depth if the control stays at `replm` 1. Acceptable as a *system-vs-system* demo; not as the O3 isolation number. | What §3 and every results caption say | 28 Aug |
| 6 | **`RATE_LIMIT_BUDGET.md` §2's OpenAI rewrite**, including whether the vLLM/open-weights lever (§1.4) survives the provider change. | W6 concurrency ceilings | Before W5 |

## 8. Verification debt opened by this record

Per `CONTEXT.md` §4.3 item 5 — mark and surface, never quietly assert.

| # | Item | Status |
|---|---|---|
| 1 | The MARD↔`replm` depth mapping (§5.2) is derived from prose, not from `envelope/pass1.py`'s call structure | **[UNVERIFIED]** — check before any A4 table caption |
| 2 | Whether `replm` differs from `alexzhang13/rlm` in ways that change what "vanilla RLM" means for O3 (§4) | ⚠ **Partial** — §4.1 compares the OpenAI adapter, the batch/recursion path, depth semantics and the constructor API. **Prompt templates, REPL surface and stopping criteria are still uncompared**, and those are what decide whether the two produce the same baseline |
| 3 | Whether `_is_reasoning_model`'s prefix list (`o1`, `o3`, `o4`, `gpt-5`) covers whatever pair §7 item 1 selects | Not yet applicable — re-check at selection |
| 4 | OpenAI rate-limit tiers for the selected pair — `RATE_LIMIT_BUDGET.md` §2's replacement | Not started; was due "before W3" |
| 5 | Whether the ₹→USD ceiling arithmetic survives (§2) | Open — §7 item 4 |

## 10. What the work actually costs — measured 26 Aug 2026

Now that the money is out of pocket (§2), this is the number that governs planning. It is
built from **measured** corpus figures plus **named** assumptions, so each assumption can
be argued with individually and replaced with a real `calls_issued` figure after the first
run.

> **⚠️ CORRECTED 27 Aug 2026.** §10.2–§10.4 below were computed against the GPT-5.6
> Sol/Terra/Luna rate card. **That is not the pair that ran.** The actual pair is
> `gpt-5.2` (Tier 1, $1.75/$14.00 per 1M) + `gpt-5-mini` (Tier 2, $0.25/$2.00), recorded
> first-hand in `provider/rates.py` and written up in
> [`22-MODEL_PAIR_OPENAI.md`](22-MODEL_PAIR_OPENAI.md), which carries the corrected model:
> **MARD ≈ $0.94/run projected, vanilla $0.32–$1.60 measured (n=3), remaining matrix ≈ $11.**
> The "$25–35 for Manuscript A" figure derived from §10.3 is **withdrawn**. §10.1's measured
> corpus quantities and §10.4's two conclusions still hold; only the prices were wrong.

### 10.1 Measured inputs

| Quantity | Value | Source |
|---|---|---|
| `introcs` characters | 2,468,431 | `corpus/introcs/document.txt` |
| `introcs` tokens | **~617,000** | derived at 4.0 chars/token — **[UNVERIFIED]**, see §10.5 |
| Sections (Tier 2 builders) | 120 | `corpus/introcs/sections.json` |
| Chapters explored by Pass 1 | 14 | `corpus/introcs/chapters.json` |
| Sum of section characters | 2,432,597 | `sections.json` `char_count` |

### 10.2 Prices — OpenAI, read 26 Aug 2026

Promotional pricing, stated as available **at least through 21 Nov 2026**, which covers the
entire project window to 30 Sep. `RateCard`'s 30-day staleness rule still applies.

| Model | Input $/1M | Cached input $/1M | Output $/1M |
|---|---|---|---|
| GPT-5.6 Sol | 4.00 (was 5.00) | 0.40 | 20.00 (was 30.00) |
| GPT-5.6 Terra | 2.00 | 0.20 | 12.00 |
| GPT-5.6 Luna | 0.20 | 0.02 | 1.20 |

### 10.3 One textbook, both arms — Sol scout + Luna swarm

| | input | output | cost |
|---|---|---|---|
| MARD Tier 1 — Pass 0 + 14 chapter calls | 53k | 31k | $0.83 |
| MARD Tier 2 — 120 builders | 704k | 120k | $0.29 |
| **MARD, one run** | | | **$1.12** |
| Vanilla root loop (12 iterations) | 123k | 10k | $0.68 |
| Vanilla sub-calls (25 chunks) | 630k | 12k | $0.14 |
| **Vanilla, one run** | | | **$0.83** |

- Both arms, 1 repeat: **$1.94**
- Both arms × 3 repeats (`docs/30` §4): **$5.82**
- **Manuscript A complete** (+ A2 × 3): **~$9.20** ≈ ₹875
- **Manuscript B complete**, 4 docs × 5 systems × 3 seeds + full ablation grid: **~$147**

### 10.4 The two conclusions that follow

**Cost is not the constraint. Throughput is.** The entire project is under $200. What
stopped Track 3 was rate limits, not spend — and `RATE_LIMIT_BUDGET.md` §1.3 predicted
exactly the shape of it: MARD Tier 2 fires 120 builders as a burst.

**We cannot climb OpenAI's usage tiers by running the experiment**, because the experiment
is too cheap to move a cumulative-spend threshold. Any tier increase has to be a
deliberate pre-purchase of credits — now a personal expense, and therefore a real
decision rather than a formality. Try `max_concurrent_subcalls` and the §3 ≤70% ceiling
first.

### 10.5 Where this estimate is soft

| Assumption | Value used | If wrong |
|---|---|---|
| Chars per token | 4.0 | 3.6 → $6.47, 4.3 → $5.42 for both arms ×3. Barely moves. `tiktoken` could not download its BPE file behind either sandbox proxy — **pin this with a real tokenizer run before quoting it in the paper** |
| Vanilla root iterations | 12 (cap is 25) | The largest single uncertainty. Doubling it adds ~$0.70/run |
| Vanilla reads the book once | 1 sweep | A re-read adds only ~$0.14 at Luna prices |
| Tier 2 output per section | 1,000 tokens | Linear; 2,000 would add ~$0.14/run |
| Tier 1 reads 4% of the document | `CONTEXT.md` §1.5 says 3–5% | Linear in Tier 1 input, which is the small half |

**Keep Luna as the swarm.** Substituting Terra in Tier 2 takes Manuscript A from $9 to
$28, because 120 builders × 704k input tokens is where all the volume lives. The scout
model barely matters by comparison.

## 9. References

- **Control, pinned (28 Aug 2026 —):** `github.com/FalseAdvertising/Zhang_RLM` @
  `62acf7b9fb70baf78b899213fec5aea9951c8341`, MIT (fork of `alexzhang13/rlm`)
- Superseded control (27–28 Aug 2026), historical only: `github.com/FalseAdvertising/Vanilla_RLM_Python` @ `a0ca553` — MIT; upstream `github.com/dschulmeist/replm`
- Base-paper library: `github.com/alexzhang13/rlm` @ `caf0bff` — **MIT**
  (upstream has since moved to `854e688`, 25 Aug 2026); `Zhang_RLM` is a fork of this
- Base paper: Zhang, Kraska & Khattab, arXiv:2512.24601 — `docs/40` row 1
- Superseded: `docs/12-MODEL_PAIR.md`, `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md`
- Amended: `docs/30-MEASUREMENT_PROTOCOL.md` §1/§6, `docs/31-ABLATIONS.md` A4,
  `RATE_LIMIT_BUDGET.md` §2, `RLM_BASELINE_SURVEY.md` §1–§3, `docs/19`, `docs/20`
  (both name `replm` throughout — superseded by this record's §4.2 addendum)
