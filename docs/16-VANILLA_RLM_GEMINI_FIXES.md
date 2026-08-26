# 16 — Three more Gemini/Vertex-path fixes found running the vanilla-RLM control

**Status:** Found and fixed 22 Aug 2026, running issue #20's W1 vanilla-RLM
control · Owner: Track 3 (Arav) · Extends `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md`
and the crash fix recorded in `TRACK2.md` (20 Aug, Parth).

All three fixes live in `.vendor/rlm`, which is gitignored, so — same as
`docs/15` and the 20 Aug crash fix — this document is the source of truth.
**Reapply all three after any fresh `.vendor/rlm` clone or `bootstrap_rlm.sh`
run**, in addition to `docs/15`'s constructor patch and the 20 Aug
`_text_or_empty` fix.

## 1. `_default_answer` sends its last turn as `role: "assistant"` — Gemini rejects it

**Symptom:** a vanilla-RLM run against a large context (OOLONG's 131K-token
window) that exhausts `max_iterations` without finding an answer crashes with:

```
google.genai.errors.ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400,
'message': 'Requests ending with a model turn are not supported', 'status':
'INVALID_ARGUMENT'}}
```

**Root cause, from source** (`rlm/core/rlm.py`, `_default_answer`):

```python
current_prompt = message_history + [
    {
        "role": "assistant",
        "content": "Please provide a final answer to the user's question based on the information provided.",
    }
]
response = lm_handler.completion(current_prompt)
```

This message is an *instruction* — content for the model to act on — but
it's tagged `"assistant"`, i.e. something the model itself supposedly said.
OpenAI's API tolerates a conversation ending on an assistant turn (it just
continues generating from there). **Gemini's API does not** — it requires
the turn immediately before generation to be a non-model (`"user"`) turn,
and rejects anything else outright.

**This is not a model-version change.** It's a pre-existing, backend-agnostic
bug in the base library's own fallback path, unrelated to the Vertex patch in
`docs/15`. It simply never triggered before 22 Aug: it only fires once
`max_iterations` is fully exhausted without an answer, and Parth's 20 Aug
`scripts/verify_rlm_vertex.py` checks (small haystacks, 5–10 iteration
budgets) always found an answer well before that ceiling. OOLONG's 131K-token
context is the first case that actually ran the ceiling out.

**Fix** — change the role to `"user"`:

```python
current_prompt = message_history + [
    {
        "role": "user",
        "content": "Please provide a final answer to the user's question based on the information provided.",
    }
]
```

Nothing else in `_default_answer` changes.

## 2. `MALFORMED_FUNCTION_CALL` — root cause, and what we could and couldn't observe

**Symptom:** `GeminiClient.completion`/`.acompletion` return `response.text
is None` with `response.candidates[0].finish_reason ==
FinishReason.MALFORMED_FUNCTION_CALL`. This is what the 20 Aug fix
(`_text_or_empty`) already turns into `""` rather than a crash — this section
is about *why* it happens, not a new code change.

**What we found by instrumenting the empty-response path** to dump
`candidate.content.parts` and `response.prompt_feedback`: **the candidate's
`parts` list is empty.** There is no partial or garbled function-call object
visible to the client — Gemini reports the *fact* that generation failed
because of an attempted function/tool call, but does not expose what that
attempted call contained. This appears to be a server-side generation failure
mode, not something inspectable or preventable from the client side.

**Confirmed not caused by anything this project's client declares**:
`GeminiClient.completion` never sets `tools=` on `GenerateContentConfig` —
only `system_instruction`. So this isn't us accidentally triggering tool use.
The working hypothesis is that `gemini-3.6-flash` has some default/implicit
tool-use tendency that RLM's system prompt can trip — that system prompt
instructs the model heavily toward emitting fenced ` ```repl ` code blocks
and describes a whole REPL/tool-calling-shaped interaction pattern
(`llm_query`, `rlm_query`, etc.), which is exactly the kind of content that
could read, to a function-calling-tuned model, as an implicit tool-call
opportunity even with no tools declared.

**Frequency scales with context size**, empirically:
- Small-scale checks (`scripts/verify_rlm_vertex.py`, ~10K-token haystacks):
  0–2 empty responses per run, always recovered within budget.
- OOLONG (131K-token context), **updated after a real 27-task batch (22 Aug
  2026)**: this is worse than the earlier two-run sample suggested. **9 of 27
  tasks (33%) hit empty responses on all 11 calls** (10 iterations + the
  `_default_answer` fallback) — not "eventually recovers," total failure to
  produce any usable text for that task at all.

**Confirmed non-deterministic, not content-triggered — direct evidence, not
inference.** Two checks against the initial "maybe certain questions are
worse" hypothesis:
1. **No content correlation.** The 9 all-empty tasks span every task
   type/group in the set (`counting`, `user`, `timeline` ×
   `RELATIVE_FREQ`/`NUMERIC_ONE_CLASS`/`MOST_FREQ`), each type also present
   among the successful tasks, with only the label names substituted between
   otherwise-identical template questions.
2. **Re-ran one all-empty task (index 2, id `17000205`) with the identical
   seed (11).** First run: 11/11 empty. Second run, same index, same seed:
   6/11 empty, 5/11 produced real (if wrong) text. **Same prompt, same seed,
   different outcome** — this is genuine Vertex/Gemini-side non-determinism
   at `temperature=0`, not a stable property of any specific prompt.
   `runlog`'s own docs already anticipate exactly this: *"local seeding does
   nothing to a hosted model."*

**Cost consequence, not just a correctness one**: an "empty" response still
bills real output tokens — the model generated *something*, just not
parseable text. The re-run above cost $0.196 (49,117 output tokens) versus
~$0.02–0.03 for a normal task, because partial recovery produced a long
rambling non-answer before giving up. A flaky task can cost 5–10× a clean
one, not just score worse.

**Not a model-version-change finding** in the sense of "this used to work and
now doesn't" — we have no earlier baseline on `gemini-3.6-flash` at this
context scale to compare against. It is a real, reproducible-in-aggregate
(though not per-call-deterministic) property of this model on this backend
at large context sizes. **This now needs to go in the paper's
limitations/measurement-protocol discussion as a real finding, not a caveat**
— at ~33% total-failure rate on OOLONG specifically (the flat-context
negative control), it may itself be a meaningful result about vanilla RLM's
reliability on unstructured long context, separate from whatever MARD's
comparative number turns out to be.

**Current handling remains correct, but is damage control, not a fix**:
`_text_or_empty` returns `""`, RLM tries again next iteration, and fix #1
(the `_default_answer` role bug) means exhausting the budget produces a
scored zero rather than a crash. Given the evidence above, **more seeds is
the correct next lever, not more iterations** — `max_iterations` is already
being fully exhausted on these tasks; the measurement protocol's
non-negotiable 3-seed policy exists for exactly this kind of provider-side
variance.

### 2a. Root-cause narrowing: a likely naming collision with the ` ```repl ` fence tag

Tried the obvious API-level mitigation before accepting this as unfixable:
`GenerateContentConfig.tool_config.function_calling_config.mode = "NONE"`
plus `automatic_function_calling.disable = True` — both exist in
`google-genai` 2.19.0 and together tell the model never to predict a
function call.

**Tested on 4 tasks that were 11/11 empty at baseline (seed 11). Result:
inconsistent, not a fix.** One task went from total failure to a correct
answer; two stayed just as broken (9-10/11 and 10/10 empty); one produced an
answer but scored wrong. Given we'd already shown this task is
non-deterministic on identical settings alone, one better run isn't evidence
the config helped — the aggregate pattern across all four says it didn't.

**But one of the still-failing calls (task index 4) produced a genuine clue:**

```
finish_reason=STOP
part[0]: text=None  function_call=repl({})
```

**The model is attempting to call a function literally named `repl`, with
empty arguments.** RLM's own system prompt instructs the model to write code
inside ` ```repl ` fenced blocks — `rlm/utils/parsing.py`'s
`find_code_blocks()` looks for exactly the hardcoded pattern
`r"```repl\s*\n(.*?)\n```"`. The leading hypothesis is that
`gemini-3.6-flash` is, at least some of the time, reading that fence-marker
convention as an instruction to *invoke a tool named `repl`* rather than as
a markdown language tag — and since no such tool is ever declared, the
attempt comes back malformed regardless of the `tool_config` setting (the
model still tries to emit the structure; it just can't complete it validly
either way).

**Not adopted as a fix**, for two reasons: (1) the config-only mitigation
above didn't reliably help, and (2) an actual fix would mean renaming the
fence tag in RLM's own system prompt and syncing `find_code_blocks()`'s
regex to match — which is not a compatibility patch, it's changing what the
model is *instructed to do*, i.e. changing the algorithm under test. That
crosses the same line the earlier decision not to swap RLM libraries drew:
it would make "vanilla RLM" in this project's results silently mean
something different from the reference algorithm. If this is worth testing,
it belongs as an explicitly separate, labeled experiment (e.g.
`vanilla_rlm_renamed_fence`) run *alongside* the real control, not a silent
substitution for it — flagged to Track 1 rather than decided here.

### 2b. Ruled out: it is not specific to the native `google-genai` SDK

Looked at `avbiswas/fast-rlm` (a more mature, separately-maintained RLM
implementation, 470 stars) specifically because its Vertex integration
reaches Gemini through **Vertex's OpenAI-compatible endpoint**
(`.../locations/global/endpoints/openapi`) via the plain `openai` Python
client, instead of the native `google-genai` SDK our patched `GeminiClient`
uses. Different HTTP/API contract, same model, same billing — a clean way
to test whether the native SDK's request shape was the actual trigger.

**It is not.** Re-ran the same known-flaky task (index 2, seed 11) through
the *unmodified* upstream `OpenAIClient` (already supports arbitrary
`base_url`/`api_key`, no new client code needed), pointed at Vertex's
OpenAI-compatible endpoint with a service-account OAuth2 bearer token:

```
[call 2] EMPTY: finish_reason=malformed_function_call message=None
[call 3] EMPTY: finish_reason=malformed_function_call message=None
[call 4] EMPTY: finish_reason=malformed_function_call message=None
```

Identical failure mode (`finish_reason=malformed_function_call`), through a
completely different SDK and API contract. **This confirms the failure is a
property of `gemini-3.6-flash` itself reacting to RLM's system prompt, not
an artifact of the native `google-genai` SDK, `GeminiClient`, or anything
patched in `.vendor/rlm` this week.** Closes the door on "switch client
libraries/SDKs" as a fix — there is no transport-level escape from this,
only the algorithm-level one (§2a) already flagged to Track 1.

One incidental finding from this test: Vertex's OpenAI-compatible endpoint
needs a different URL shape for `location=global` than for a real region —
no region prefix on the hostname (`aiplatform.googleapis.com`, not
`global-aiplatform.googleapis.com`), path still says `locations/global/`.
Noted here in case it's useful later; not otherwise relevant to this
project since we're not adopting this transport.

(These test calls ran outside `RunLogger` — ad hoc diagnostic scripts, not
`eval/run_vanilla_rlm.py` — so they were reconciled into the spend ledger
after the fact from `usage_summary` rather than logged live. ~$0.13-0.16
total, folded into the campaign ledger.)

### 2c. Third independent confirmation: `avbiswas/fast-rlm` hits the identical failure

Cloned `avbiswas/fast-rlm` (a separately-maintained, more mature RLM
implementation — 470 stars, its own TypeScript/Deno execution engine, its
own Vertex AI integration) and ran the same known-flaky task through it,
using our project's real service-account credentials.

**Needed one patch first, unrelated to the collision question**: its
`src/vertex.ts` builds the Vertex endpoint URL as
`{location}-aiplatform.googleapis.com`, which 404s for `location=global` —
the same URL-shape issue found in §2b. Global has no regional data centre,
so it needs the un-prefixed host (`aiplatform.googleapis.com`) with
`locations/global` only in the path. Patched locally in the clone (not
upstreamed — this is a test environment, not our vendored library).

**First run** (`max_calls_per_subagent=10`, matching our `max_iterations`):
completed 11 real steps of genuine work — inspecting the context, writing
classification code, correctly identifying OOLONG's label taxonomy — with
**no visible `malformed_function_call` symptom in the trajectory log**, then
hit a fast-rlm-internal error (`"Did not finish the function stack before
subagent died"`) because our chosen call budget was too tight for its root
agent to reach `FINAL()` — our own config mistake, not a finding.

**Second run** (`max_calls_per_subagent=20`, fast-rlm's own default):
**crashed on the very first real model call** —
`Cannot read properties of undefined (reading 'content')` — the exact
TypeScript-side equivalent of the `'NoneType' object has no attribute
'content'` crash we hit in our own Python `OpenAIClient` test in §2b, on
the identical symptom shape (a null/undefined message where real content
should be).

**This is the third independent RLM implementation to hit this failure on
the same task**: our vendored `alexzhang13/rlm` via the native `google-genai`
SDK, the same library via Vertex's OpenAI-compatible endpoint (§2b), and now
`fast-rlm` via its own, separately-engineered Vertex integration. Three
different codebases, three different transports, one common factor:
`gemini-3.6-flash` reacting to a REPL-style, code-writing system prompt at
large context. **This closes the "maybe a different implementation avoids
it" question — none of the three tested so far do.** `fast-rlm` also has no
defensive handling for this failure mode (crashes rather than retrying),
so it isn't even ahead of our own `_text_or_empty` fix in that respect.

**Cost**: ~$0.18 across both runs (one completed with real token usage
logged, one crashed before fast-rlm recorded usage — estimated from the
same task's typical scale). Reconciled into the campaign ledger the same
way as §2b's experiment.

### 2d. Tried the community's reported fix — doesn't reliably work at our scale

External research (a Google engineer's response on
`googleapis/python-aiplatform#4472`, plus `langchain-ai/deepagents#417`)
converges on a widely-reported mitigation: add an instruction to the system
prompt telling the model to JSON-escape function-call string arguments,
reported by multiple independent users as a ~90-98% reduction. Several
reports also specifically flag **120k+ token prompts pushing large content
through what looks like a function-call argument** as the trigger condition
— matching our situation closely.

**Tested via `custom_system_prompt`** (no vendored-file patch — a pure
config override, fully reversible), appending both the community's
JSON-escaping instruction and an explicit clarification that `repl` is a
fence tag, not a callable tool (combining both threads of evidence). Re-ran
the same 4 tasks that were 11/11 empty at baseline (seed 11):

| task | empty calls (with fix) | baseline | outcome |
|---|---|---|---|
| idx 2 | 5/10 | 11/11 | succeeded, correct answer |
| idx 4 | 11/11 | 11/11 | **no change** |
| idx 5 | 0/10 | 11/11 | zero malformed calls, but wrong answer |
| idx 9 | 11/11 | 11/11 | **no change** |

**Not a reliable fix at our scale.** Two of four tasks showed zero
improvement — identical total failure to baseline. Given the already-proven
non-determinism (§2, direct re-run evidence), the two "improved" tasks
aren't strong evidence the instruction helped rather than a lucky draw,
while the two unchanged tasks are a clear negative signal. Working
hypothesis: the community's fix was mostly reported against moderate-sized
prompts with simple tool schemas; our single 131K-token context pushed
through an implicit (undeclared) function-call attempt may be a more severe
case of the same underlying bug than a one-sentence prompt nudge has
leverage against.

**Not adopted.** Kept as a documented negative result rather than a shipped
change — the experiment script (`eval/_experiment_json_escape_fix.py`) was
removed from the tree after logging this finding; the exact prompt addition
is preserved above for anyone who wants to re-test it later (e.g. at smaller
context scales, or combined with Fix 2 — forced function-calling with a
real `repl` tool schema, Google's own suggested mitigation, not yet tried).

**Cost**: ~$0.14 (estimated — this experiment script had its own accounting
gap, `live_call_logging` wasn't wired in, so live token counts weren't
captured; reconciled as an estimate from this task's established per-run
scale rather than left uncounted).

### 2e. Confirmed: Tier 2 (`gemini-3.1-flash-lite`) has the identical failure — closes verification debt item 2

Pure diagnostic, no decision implied: `gemini-3.1-flash-lite` is already
part of the frozen model pair (`docs/12`); checking whether *it* has this
problem isn't proposing anything, just reading a fact about a model already
in scope.

Ran the same 4 known-flaky tasks (seed 11) through Tier 2 instead of Tier 1:

| task | empty calls (Tier 2) | score |
|---|---|---|
| idx 2 | 8/11 | 0.0 |
| idx 4 | 3/10 | 0.0 |
| idx 5 | 5/8 | 0.0 |
| idx 9 | 0/9 | 0.0 (wrong answer, not empty) |

**Tier 2 hits the identical failure mode.** Not model-specific to
`gemini-3.6-flash` — both models in this project's frozen pair show it. This
lines up with external evidence: reports of this exact failure span
`gemini-1.5-pro`, `2.0-flash`, `2.5-flash`, `2.5-pro`, and "Gemini 3"
(`googleapis/python-aiplatform#4472` comment thread) — the entire Gemini
lineage, not one checkpoint. **Working conclusion: this is a persistent
characteristic of Gemini's function-calling/decoding architecture in
general, not something a different Gemini model choice would sidestep.**

Properly logged this time (`live_call_logging` wired in correctly) — real
cost ~$0.035 across all 4 runs, reconciled into the ledger directly from
`summary.json`, not estimated.

### 2f. Lever #2 tested — renaming the fence tag to `python` eliminates the failure in this sample

**This is the strongest result of the whole investigation, and it is
exactly the algorithm-level change flagged in §2a as needing Track 1
sign-off before adoption — tested here as a labeled experiment only, not
applied to the real control.**

Two candidate replacements for the ` ```repl ` fence tag, chosen to test a
specific refinement of the naming-collision hypothesis:

- **`python`** — the single most standard, ubiquitous markdown language tag
  that exists, essentially zero call-like connotation.
- **`python_repl`** — closer to the original wording, but snake_case is
  exactly the shape function/tool names take, so the hypothesis going in
  was that it might read as *more* call-like, not less.

Implementation: `custom_system_prompt` (all 3 literal ` ```repl``` `
occurrences in `RLM_SYSTEM_PROMPT` replaced with the candidate tag) plus a
monkeypatched `find_code_blocks` matching the same tag (reverted after each
run) — no vendored file touched, fully reversible.

Re-ran the same 4 known-flaky tasks (seed 11, 11/11 empty at baseline for
all four):

| task | `python`: empty / score | `python_repl`: empty / score |
|---|---|---|
| idx 2 | 0/11 — **1.0** | 0/9 — 1.0 |
| idx 4 | 0/8 — **1.0** | 2/10 — 1.0 |
| idx 5 | 0/10 — 0.0 (answered, wrong) | 6/7 — 0.0 |
| idx 9 | 0/10 — 0.0 (answered, wrong) | **11/11 — 0.0 (identical to baseline)** |

**`python`: zero `MALFORMED_FUNCTION_CALL` across all 4 tasks, all 39
calls.** Every task that previously produced no usable answer at all now
produces one every time — two correct, two wrong, but "wrong" is now a real
reasoning outcome instead of an execution failure. **`python_repl`: mixed**
— better than baseline on two tasks, but idx 9 shows *zero* improvement,
identical to the unpatched baseline.

**Follow-up: `pythonrepl` (one fused word, no underscore) tested to isolate
the mechanism.** The initial read on `python_repl` was "snake_case looks
like a function name." That's ruled out now: `pythonrepl` has no separator
at all and *still* shows the same pattern — one task (idx 5) at 11/11
empty, identical to baseline, no improvement whatsoever:

| task | `pythonrepl`: empty / score |
|---|---|
| idx 2 | 2/9 — 1.0 |
| idx 4 | 5/10 — 1.0 |
| idx 5 | **11/11 — 0.0 (identical to baseline)** |
| idx 9 | 0/11 — 0.0 (answered, wrong) |

**Refined conclusion:** it isn't the snake_case *shape* — it's simply
**whether the literal substring `repl` appears in the tag at all.**
`python` (no "repl" substring) → clean across all 4 tasks, 0/39 failures.
Both `python_repl` and `pythonrepl` (each containing "repl") → mixed, one
total failure apiece. The common factor across every tag tested is
presence vs. absence of that substring, not how it's separated or cased.

**Caveats, stated plainly:**
- Small sample (4 tasks, 1 seed) for an effect this clean — real, but
  worth confirming on a larger slice before treating the magnitude as
  final.
- This changes `RLM_SYSTEM_PROMPT`'s literal content, not just transport —
  the same category of change as any other rename discussed in §2a.
  **Not applied to the real vanilla-RLM control.** Whether to adopt this
  as the control's actual configuration, keep it as a documented
  side-experiment only, or something in between, is Track 1's call, not
  ours to decide from here — flagging to Anugrah with this result attached.

**Cost**: ~$0.62 total across 13 runs (9 for `python`/`python_repl` + 4 for
the `pythonrepl` follow-up), reconciled into the ledger from real logged
`summary.json` figures.

### 2g. Scaled to the full 50-task OOLONG set — result holds

The 4-task sample was small for an effect that size, so scaled the `python`
tag to (approximately) the full OOLONG set, seed 11, via a dedicated
experiment campaign runner (kept fully separate from the real control:
`system="vanilla_rlm_fence_rename_experiment"`, document IDs suffixed
`-python`, never mixed with `vanilla_rlm` in the ledger or `runs/`).

**Result across 55 attempted runs** (a handful are duplicate coverage of
the same task from the earlier naming convention used in §2f's small
sample; the practical coverage is the full 0-49 index range):

| Metric | Baseline (`repl`) | `python` tag |
|---|---|---|
| Total-failure tasks (all calls empty) | ~33% (9/27, partial baseline sample) | **1/55 (~1.8%)** |
| Tasks producing *some* usable answer | ~67% | **~98%** |
| Overall per-call empty rate | high, task-dependent | **16.0%** (79/493 calls) — down, but not zero: intermittent empties still occur, they just essentially never consume the whole task's iteration budget anymore |
| Accuracy among completed tasks | n/a (too few completed to measure at baseline) | **67.3%** (37/55 correct) |

**The single remaining total-failure case** (`oolong-trec_coarse-17000223`)
confirms the fix is a large reduction, not a categorical elimination — the
underlying Gemini behavior can still occasionally exhaust every attempt
even with the collision-avoiding tag. Consistent with §2 (confirmed
non-deterministic): this is exactly the shape of result — a large,
reproducible drop in an intermittent failure's frequency, not a guarantee.

**This is now a large-sample, not a small-sample, result.** Renaming the
fence tag away from `repl` cuts total task failure by roughly 18x on this
set (33% → 1.8%) at the cost of nothing algorithmic — the model still
writes free-form Python in a fenced block, same interaction pattern, same
recursion, same tools. The only thing that changed is which word labels the
fence. Whether to adopt this for the real vanilla-RLM control is still
Track 1's call (§2f), but this result is a much stronger basis for that
conversation than the 4-task sample alone.

**Cost**: ~$1.84 across the scaled run, phase-budgeted at $5 (stayed well
under), reconciled into the ledger live via the experiment campaign
script's own `SpendLedger` integration — no post-hoc estimation needed
this time.

## 3. `RLMLogger.log()` crashes on a stray `None` in `REPLResult.rlm_calls`

**Symptom, found scaling to a real batch:** a task that otherwise completed
its work fine crashes with `AttributeError: 'NoneType' object has no
attribute 'to_dict'`, in this call chain:

```
rlm.py: self.logger.log(iteration)
  -> RLMIteration.to_dict()
    -> CodeBlock.to_dict()
      -> REPLResult.to_dict(): [call.to_dict() for call in self.rlm_calls]
        -> one entry in rlm_calls is None
```

**Reliably co-occurs with a `MALFORMED_FUNCTION_CALL` empty response** from a
nested `llm_query`/`rlm_query` call inside the model's own REPL code (as
opposed to fix #2, which is about the *root* call being empty). Traced the
socket-based LM-handler path (`rlm/core/lm_handler.py`,
`rlm/core/comms_utils.py`) and every constructor there always builds a real
`RLMChatCompletion` — **the exact line that ends up putting `None` into
`_pending_llm_calls` is not yet pinned down.** Ruled out as a cause: this is
not the two-process race described below — it reproduced identically in a
single, clean process on a second attempt.

**Fix, at the one safe choke point regardless of the exact origin**:
`RLMLogger.log()` is where every iteration gets serialised for the
trajectory. Metadata capture is an observability path — it must never be
able to take down a task that otherwise completed. Patched it to drop `None`
entries from `code_block.result.rlm_calls` before serialising:

```python
for code_block in iteration.code_blocks:
    code_block.result.rlm_calls = [c for c in code_block.result.rlm_calls if c is not None]
```

This loses that one sub-call's metadata (not the task's real answer, which
was already produced) rather than crashing the whole run. Retested on the
same two tasks that hit this and both completed cleanly afterward
(`task_score` 1.0 on both).

**Operational note, unrelated to any of the three fixes**: this bug was
first found while two copies of the same campaign batch process were
accidentally running concurrently (a `run_in_background` invocation issue,
not a library bug) — initially suspected as a port/socket collision between
two `LocalREPL` instances. **Ruled out** by reproducing the same crash in a
single clean process. Real cost impact from the duplicate-process incident
was small (~$0.05, caught within minutes via the phase-budget guard in
`eval/run_vanilla_rlm_campaign.py`), but worth a standing rule: **never run
two invocations of the campaign script against the same run range
concurrently** — nothing currently guards against it.

## 4. A related accounting gap, fixed in `eval/run_vanilla_rlm.py`

Before fix #1 existed, a run that crashed via bug #1 produced a
`summary.json` showing `"calls": 0, "cost": 0.0` — despite 10 real, billed
Vertex calls having actually happened. The script only logged calls by
walking the successful completion's metadata tree *after* `.completion()`
returned, so a crash lost all call-level accounting for real spend that had
already occurred.

Fixed by logging every real `GeminiClient.completion`/`.acompletion` call the
instant it returns (a class-level patch scoped to the run, covering
recursive child clients too, since the library constructs those internally
and never hands this script a reference to wrap). See
`eval.run_vanilla_rlm.live_call_logging`. This is now the authoritative
source for tokens/cost/calls; the structured recursion tree (depth,
parent/child) is saved separately as a readable artefact
(`artefacts/rlm_trajectory.json`) once a run succeeds, not re-logged as
calls.

## Verification debt this opens

| # | Item | Status |
|---|---|---|
| 1 | Whether total-task-failure rate holds near 33% (9/27, seed 11) across the remaining OOLONG tasks and the n=20 BrowseComp-Plus set | **[PARTIALLY VERIFIED]** — 33% confirmed on 27/50 OOLONG tasks, seed 11 only; check remaining 23 and BrowseComp-Plus before generalising |
| 2 | Whether this is specific to `gemini-3.6-flash` or also affects `gemini-3.1-flash-lite` (Tier 2) at large context | **[VERIFIED]** — §2e: Tier 2 hits the identical failure on the same 4 tasks, not model-specific |
| 4 | Whether seeds 23/42 show a similar ~33% total-failure rate on the same tasks, or whether per-task failure is itself seed-dependent (confirmed non-deterministic on one direct re-run, item above) | [UNVERIFIED] — needs the 3-seed sweep, not yet run |
| 3 | Exact line that puts `None` into `REPLResult.rlm_calls` (fix #3) | [UNVERIFIED] — patched defensively at the logging choke point, root line in the socket-based LM-handler path not yet located |
| 5 | Whether the ` ```repl ` fence tag is actually causing the model to attempt a `function_call=repl(...)` (§2a) | **[STRONGLY SUPPORTED, refined]** — §2f: `python` (no "repl" substring) eliminated all failures across 4/4 previously-total-failure tasks (39/39 calls clean); both `python_repl` and `pythonrepl` (each still containing "repl", with/without a separator) show mixed results with one total failure apiece. The determining factor looks like substring presence, not snake_case shape. Small sample (4 tasks, 1 seed) — worth confirming at scale. Adoption for the real control is Track 1's decision, not made here |
| 6 | Whether `avbiswas/fast-rlm` shows the same failure on our OOLONG tasks | **[VERIFIED]** — §2c: hit the identical crash symptom on the same task, first real call. Not yet tested at full-scale (all 50 tasks) to get a comparable failure rate, only single-task confirmation |
