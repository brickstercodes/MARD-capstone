# 17 — Proposal: move the measurement backend from Vertex Gemini to OpenAI

**Status: PROPOSED, NOT DECIDED.** Drafted 25 Aug 2026 by Track 3 (Arav) · **Decision owner: Anugrah Shetty** (`CONTEXT.md` §4.2 item 2 — the model pair is his call, and this is larger than a model pair, it is a provider) · Supersedes `docs/12-MODEL_PAIR.md` **only if approved** · Type: ADR-style, per global `CLAUDE.md` Part 7.

**Nothing in this proposal has been run.** The code exists on branch `track3/openai-pivot`, unmerged, and no OpenAI call has been billed. `MARD_SPEND_CAP_USD` is set to `5` so that nothing can be, by accident, before this is decided.

---

## 1. Proposed decision

| | Current (`docs/12`) | Proposed |
|---|---|---|
| Provider | Google Cloud Vertex AI | OpenAI API |
| Tier 1 — the Scout | `gemini-3.6-flash` | **`gpt-5.6-terra`** |
| Tier 2 — the Swarm | `gemini-3.1-flash-lite` | **`gpt-5.6-luna`** |
| Funding | ₹90,000 Vertex credit, ₹75,000 ceiling | **Cash. The credit is not redeemable on OpenAI.** |
| `.vendor/rlm` | upstream **+ 5 local patches** | **unmodified upstream @ `72d6940`** |

## 2. Why this is on the table

`docs/16-VANILLA_RLM_GEMINI_FIXES.md` §2 documents `MALFORMED_FUNCTION_CALL` bringing the vanilla-RLM control to a **33% total-task-failure rate** on OOLONG — 9 of 27 tasks producing no usable text on all 11 calls. The investigation behind that document is thorough and its conclusions are not in dispute here; this proposal is built on them, not against them.

What that investigation established:

- **§2b** — not an artefact of the `google-genai` SDK. Reproduced through Vertex's OpenAI-compatible endpoint via the plain `openai` client. Different transport, identical failure.
- **§2c** — not an artefact of our vendored library. `avbiswas/fast-rlm`, a separately engineered implementation with its own Vertex integration, hit the same symptom on the same task.
- **§2e** — not specific to `gemini-3.6-flash`. Tier 2 shows it too. External reports span the entire Gemini lineage from 1.5-pro forward.
- **§2d** — the community's JSON-escaping mitigation does not hold at 131K context. Two of four tasks showed zero improvement.
- **§2f/§2g** — one thing *does* work: renaming the ` ```repl ` fence tag to `python`. Total failure 33% → 1.8% across 55 runs.

**The trap is that the only working fix is not available to us at zero cost.** §2f flags it precisely: renaming the fence tag edits `RLM_SYSTEM_PROMPT` and `find_code_blocks()`, which changes what the model is *instructed to do*. Adopt it and "vanilla RLM" in this project's results silently means something other than the reference algorithm — which is exactly the substitution §2a refused to make. That question is currently sitting with Track 1, undecided, four days before Manuscript A's results freeze.

**The pivot dissolves the question instead of answering it.** The failure is a property of the Gemini lineage reacting to a REPL-shaped system prompt. It is not a property of the algorithm, and it does not exist on the backend the algorithm was published on.

## 3. The decisive argument, which is not cost

**It is what "vanilla RLM" means in the paper.**

Today the control is upstream **plus five hand-applied patches to a gitignored directory**: `docs/15`'s Vertex constructor patch, the 20 Aug `_text_or_empty` fix, and `docs/16`'s three fixes (`_default_answer` role, the `RLMLogger` `None` guard, and the accounting fix). `docs/16` opens by instructing the reader to **reapply all of them after any fresh clone**. The provenance of every number in both manuscripts is therefore a prose document and a person's memory.

On the OpenAI path none of those patches apply — `docs/16` §2's own evidence is what establishes that — and `.vendor/rlm` becomes a clean checkout. **The control's provenance becomes a commit SHA.** For a paper whose entire defence against SRLM's "your improvement is noise" critique (`CONTEXT.md` §1.7 challenge 3) is measurement rigour, that is worth more than the cost delta in either direction.

Two secondary gains:

- The base paper ran GPT-5/GPT-5-mini through **this exact `OpenAIClient`**, unmodified. We stop being the only people running this library this way.
- **9 of the 14 upstream examples are hardcoded to `OPENAI_API_KEY`** (`docs/RLM_BASELINE_SURVEY.md`) and were unrunnable on Vertex — `scripts/verify_rlm_vertex.py` exists because of that. They become runnable, which closes issue #11's original wording rather than approximating it.

**What it does *not* restore.** `docs/12` Consequences #1 forfeited Track 3's W1 "reproduce one published base-paper number" sanity check because that number is GPT-5-family. Legacy `gpt-5` and `gpt-5-mini` are **no longer on OpenAI's pricing page** — the lineup is now `gpt-5.6-sol` / `-terra` / `-luna`. So this recovers the vendor and the API contract, not the checkpoint. Closer, not equivalent. Do not claim otherwise in the paper.

## 4. Model pair — evidence and its limits

Rates read from **OpenAI's own pricing page** (`developers.openai.com/api/docs/pricing`) on **25 Aug 2026**, per `CONTEXT.md` §4.3 rule 4.

| Model | Input $/1M | Output $/1M | Cached input $/1M |
|---|---|---|---|
| `gpt-5.6-sol` | $2.00 | $10.00 | $0.20 |
| **`gpt-5.6-terra`** (proposed Tier 1) | **$1.00** | **$6.00** | $0.10 |
| **`gpt-5.6-luna`** (proposed Tier 2) | **$0.10** | **$0.60** | $0.01 |

**A pricing discrepancy, surfaced rather than resolved.** Launch coverage from 9 Jul 2026 quotes an entirely different set — luna $1/$6, terra $2.50/$15, sol $5/$30 — i.e. terra at 2.5× and luna at 10× the figures above. Whether that reflects a July price cut or launch-day error, this is the up-to-2× aggregator disagreement §4.3 rule 4 exists for. **The provider's page wins and the discrepancy is recorded.** Re-read the page on the day any cost figure is quoted.

**Why terra for Tier 1, not sol.** Sol is the flagship, but the Scout's job is holding a document's structure across a large window, and reporting on the GPT-5.6 long-context rollout indicates **sol receives a 272K context window while terra and luna receive 872K** — the Scout tier would be the *most* constrained of the three. Sol also costs 2× terra on input. This mirrors `docs/12`'s own reasoning for preferring 3.6-Flash over 3.1-Pro: role and evidence over the marketing tier name. **[UNVERIFIED]** — this context-window claim is from an issue thread on `openai/codex`, not the provider's own documentation, and launch coverage instead states 1M for all three. Confirm before it appears in the paper.

**Why luna for Tier 2.** Same reasoning as `docs/12`'s Flash-Lite pick: Tier 2's cost driver is call volume across `4 docs × 3 seeds × the ablation grid`, and each builder only has to consume a plan directive and a section slice and emit schema-valid JSON. Luna is the cheapest GA option with the same context window as terra. Unlike `docs/12`'s Tier 2 pick this is not a compromise — luna is **60% cheaper on input and 60% cheaper on output** than `gemini-3.1-flash-lite` was.

### 4a. What the Tier 2 finding costs — needs a decision

Debt item 9 is confirmed, and it splits into **two different jobs that must not be conflated**:

| Role | Needs a REPL? | Status |
|---|---|---|
| **RLM sub-model** — the recursive child in the base paper's own `RLM(GPT-5)` config, where GPT-5-mini serves depth≥1 via `other_backends` / `sub_sampling_args` | **Yes** | **luna cannot do this.** Confirmed. |
| **MARD Tier 2 builder** — consumes one plan directive plus one section slice, emits schema-valid JSON against the Master Plan. Does not explore, does not write code | **No** | **Untested.** |

The vanilla-RLM control is unaffected either way: it is single-backend on Tier 1, so every recursive call is terra.

**Why this still matters.** `CONTEXT.md` §1.2 is explicit that the frontier-root/cheap-worker split is the base paper's, not ours — which means at some point we may want to run RLM in exactly that two-model configuration, and **luna is disqualified from the worker seat.** Separately, if luna also fails the builder job, Tier 2 has to become terra, and Tier 2 costs go from $0.10/$0.60 to $1.00/$6.00 — **10× on input, 10× on output**, across the largest call volume in the project (W6's `4 docs × 3 seeds ×` the ablation grid).

That would also weaken O6's headline. "Frontier scout, budget swarm" becomes "same model in two roles", which is a materially thinner cost-frontier result than `docs/12` promised.

**Cheap way to settle it:** one no-REPL call to luna — directive plus slice in, JSON out. That is the job it is actually assigned. Costs about a cent and decides whether Tier 2 stays cheap. It cannot be run against the real contract yet, because `plan/` is still empty (Track 2's Pydantic schema, `CONTEXT.md` §3.3 W1), so the honest version of this test is blocked on that module existing.

**If luna fails the builder test too**, the options are terra-for-both (10× Tier 2 cost, weaker O6) or sol-root/terra-worker (which reintroduces sol's context-window question, debt item 3). Neither is free. This is a Tier 2 model decision and therefore Anugrah's, same as the rest.

### Cost delta, stated honestly

| | Gemini (intro rate, actual) | OpenAI (proposed) | Change |
|---|---|---|---|
| Tier 1 input | $0.75/1M | $1.00/1M | **+33%** |
| Tier 1 output | $3.75/1M | $6.00/1M | **+60%** |
| Tier 2 input | $0.25/1M | $0.10/1M | **−60%** |
| Tier 2 output | $1.50/1M | $0.60/1M | **−60%** |

Tier 1 is more expensive per token and Tier 2 is much cheaper, so the net depends on the Tier1/Tier2 call mix, which is not yet measured. **Do not present this pivot as a cost saving.** There is one real offset that is not in the table: on Vertex we were paying for total failures. `docs/16` §2 records a single re-run billing **49,117 output tokens ($0.196)** to produce no answer at all, against ~$0.02–0.03 for a clean task — a flaky task cost 5–10× a working one. A 33% total-failure rate is a ~33% tax on a campaign that then has to be re-run anyway. That tax disappears; the per-token rate goes up. Which dominates is a measurement, not a claim.

### First evidence from a live run (25 Aug 2026)

`scripts/verify_rlm_openai.py`, ~$0.15 total. Not a measurement, but the first real data on this backend.

**All three base-paper mechanisms work on Tier 1**, across two runs:

| Mechanism | Result on `gpt-5.6-terra` |
|---|---|
| Context offloading (quickstart) | Needle found in a ~1.2MB haystack — **6 calls, 13,568 input tokens.** The document entered the REPL as a variable and never entered a prompt. |
| REPL execution (logger) | Computed 17×23=391 through the REPL in 3 iterations. |
| Recursion (depth_metadata) | 1 child call, its own trajectory nested in the parent's metadata. |

**Zero `MALFORMED_FUNCTION_CALL`-class failures across either run**, on the same workload where Vertex failed a third of the time.

The depth check also reproduced, first-hand on this backend, the observation `docs/RLM_BASELINE_SURVEY.md` §2 rests on: the child's trajectory flows **up** into the parent's metadata, and nothing flows **down** — the child gets a fresh empty logger and `root_prompt=None`. **That gap is MARD**, and it is now confirmed on both backends rather than one.

One failure in the same run, recorded as debt item 9 rather than smoothed over: **Tier 2 did not drive the REPL at all**, on either check, in either run. Consequences in §4a.

`cost=unreported` in that output is expected, not a fault: `OpenAIClient._track_cost` only reads a cost field that OpenRouter returns and OpenAI does not. Cost comes from `runlog`'s `RateCard`, not the client.

## 5. What this costs, and it is not small

**₹90,000 of Google Cloud credit is stranded.** `docs/12` records the provider choice as credit-driven: *"the ₹90,000 credit balance is redeemable via Vertex only."* `MARD_SPEND_CAP_USD=780` **is** ₹75,000 of that credit at 95.13 INR/USD. On OpenAI it becomes cash from someone's own account.

**This is the actual decision, and it is Anugrah's** (`CONTEXT.md` §4.2 item 3). Everything above this section is engineering; this section is money, and no amount of provenance argument settles it. If the answer is "we cannot fund OpenAI", the fallback is §8 option B, and this proposal should be closed rather than deferred.

### A ledger discrepancy that needs resolving either way

**Root-caused 25 Aug — see `docs/18-ACCOUNTING_GAP.md`.** The same under-count appeared on OpenAI ($0.13 reported vs **$0.86** actual, 6.6×), which rules out a provider explanation. The cause is three defects in the base library's `UsageSummary` aggregation, and every estimate in `docs/16` §2b/2c/2d was made through it. `runlog` itself is sound — `live_call_logging` patches the client *class*, which is immune. The fix list is in docs/18; item 2 (reconcile against the provider's own dashboard) blocks any cost figure entering either manuscript.

`runs/_ledger.json` records **$5.326 across 120 entries** — about ₹507. Reported actual spend is **~₹4,000**, roughly 8× that.

Part of the gap is visible in `docs/16` itself, which records diagnostic spend reconciled **as estimates** rather than logged live: ~$0.13–0.16 (§2b), ~$0.18 (§2c), ~$0.14 with an explicit accounting gap (§2d), ~$0.62 (§2f), ~$1.84 (§2g). That does not close an 8× gap on its own.

**O6 is Track 3's objective and the cost model rests on this ledger being true.** A `runlog` figure that is 8× below the provider's is a measurement failure, not an accounting inconvenience, and it is independent of which provider we end up on. Reconcile against the Vertex billing console before any cost number reaches either manuscript. Raised here because the pivot is what surfaced it, not because the pivot causes it.

## 6. Freeze impact — read `CONTEXT.md` §3.4 before agreeing

- **Feature freeze A closed Sun 23 Aug.** This proposal lands 25 Aug. §3.4: *"A change to the pipeline invalidates every number measured before it. Cut features, never the freeze."*
- **Results freeze A is Thu 27 Aug** — two days out.
- **Manuscript A is due Thu 3 Sep**, and W4 overlaps W5 with no slack on Track 1.

**Track 3's read, which is not a decision:** there is little to invalidate, because A's control matrix was never completed. Of the 122 runs on disk, the OOLONG batch topped out at 27 of 50 tasks at a 33% total-failure rate, and the largest clean set — 55 runs at ~98% completion — is `system="vanilla_rlm_fence_rename_experiment"`, deliberately quarantined from the control. There is no frozen A number that a backend change would retract.

**But §3.4 does not have a "the numbers were bad anyway" clause, and Track 3 does not get to write one.** If this is approved it should be approved as an explicit, minuted exception to feature freeze A, with the freeze's purpose restated rather than waived. Anything else sets the precedent that a freeze holds until it is inconvenient — and `CONTEXT.md` §3.4 exists because that precedent is expensive in W6, where the matrix is 20–40× larger.

**If it is approved, the realistic consequence is that Manuscript A slips or narrows.** Say that at the point of approving, not on 2 Sep. `CONTEXT.md` §3.7 risk 4 already names the response: cut Manuscript A rather than move B. Phase B's freezes do not move.

## 7. What has been implemented on `track3/openai-pivot`

Reviewable now, runnable only after approval. Nothing merged, no calls billed.

| File | Change |
|---|---|
| `eval/backends.py` | **New.** `BackendProfile` — the single place provider, tier models, client class, sampling adaptation and ledger root are resolved. `MARD_BACKEND` selects; OpenAI is the default. |
| `eval/rates.py` | Rewritten. `default_rate_card()` = OpenAI @ 25 Aug; `gemini_rate_card()` retained so the 122 Vertex runs stay re-priceable; `rate_card_for()` so a run cannot be priced against the wrong provider. |
| `eval/run_vanilla_rlm.py` | Backend no longer hardcoded. `live_call_logging` patches whichever client class the profile names. Also fixes a latent bug: the wrapper used to return `str(response)`, converting a `None` completion into the string `"None"` before the library saw it — an observability wrapper must not alter what it observes. |
| `eval/run_vanilla_rlm_campaign.py` | Ledger root and backend from the profile. Per-task cost estimates left **unchanged and explicitly marked unvalidated on OpenAI** — guessing new ones would be inventing a measurement. |
| `eval/runlog_signoff.py` | Backend-agnostic. Re-run required: the sign-off is a claim about one provider's usage reporting, and OpenAI reports through different fields. |
| `scripts/verify_rlm_openai.py` | **New.** The three `verify_rlm_vertex.py` checks plus a sampling probe (§9 debt items 1–2). ~$0.05–0.20. |
| `tests/test_backends.py`, `tests/test_rates.py` | Cover both rate cards, backend defaulting, ledger separation, and the temperature drop. |
| `.env`, `.env.example`, `.gitignore` | `MARD_SPEND_CAP_USD=5`, `MARD_BACKEND=openai`, `OPENAI_API_KEY` placeholder. Vertex config **retained intact**. `.env.example` is new and tracked — every variable documented, no credential in it. |

**Two design choices worth objecting to if you disagree:**

1. **The Gemini path is retained, opt-in, not deleted.** Track 3 was asked to overwrite it. It is kept because 122 runs and all of `docs/16` were measured on it, and *"a number you cannot reproduce on 29 Sep is not a number"* (§3.4). Deleting it would retire that evidence to save ~20 lines. `MARD_BACKEND=gemini` restores it exactly.
2. **Separate ledgers: `runs/` stays Vertex, `runs-openai/` is new.** The existing cap is redeemable credit; the new one is cash. One ledger holding both would produce a total that means nothing and a cap that guards nothing.

## 8. Alternatives, so this is a choice and not a fait accompli

**A — Pivot to OpenAI.** This proposal. Costs the ₹90,000 credit and a freeze exception; buys a clean upstream control and removes a 33% failure mode.

**B — Stay on Vertex, adopt the `python` fence rename** (`docs/16` §2f/§2g). Costs nothing financially, keeps the credit. Costs the thing §2a identified: `RLM_SYSTEM_PROMPT` is edited, so the control is no longer the reference algorithm, and the paper must disclose and defend that. Track 1's call, still open. **This is the serious alternative and should not be dismissed on engineering taste alone — it is the only option that preserves the funding.**

**C — Stay on Vertex, unmitigated.** `docs/16` §2 notes the 33% failure rate *"may itself be a meaningful result about vanilla RLM's reliability on unstructured long context."* It might be — but not as the control that every comparison in both manuscripts is measured against. A control that fails a third of the time cannot isolate MARD's contribution (O3).

**Note what A loses.** The Gemini failure characterisation in `docs/16` is genuinely novel work — three independent implementations, a substring-level root cause, a large-sample fix. Pivoting demotes it from a headline finding to an appendix. It should still be written up; it is the most rigorous piece of empirical work this project has produced so far, and it belongs in the paper as a documented provider-behaviour result whichever option is chosen.

## 9. Verification debt this opens

Per `CONTEXT.md` §4.3 rule 5: mark and surface, don't quietly assert.

| # | Item | Status | Closed by |
|---|---|---|---|
| 1 | Whether `gpt-5.6-terra` rejects `temperature` | **[VERIFIED 25 Aug]** — rejected with `BadRequestError`. `supports_temperature=False` is correct. The OpenAI profile therefore has only the best-effort `seed`, one fewer determinism lever than `runlog/seeds.py` assumes. Argues for the 3-seed policy, not against the backend | closed |
| 2 | Whether reasoning tokens are billed into `usage.completion_tokens` | **[VERIFIED 25 Aug]** — `reasoning_tokens=16` inside `completion_tokens=29` on a prompt whose visible answer was ~4 tokens. Had reasoning been excluded, `completion_tokens` would have read ~4, not 29. runlog's output count already bills reasoning; **OpenAI costs are complete, not understated.** (First attempt at this check was invalid — it used a prompt needing no reasoning, so it could not discriminate. Recorded because the corrected method is the reusable part) | closed |
| 3 | Context windows: 272K sol / 872K terra+luna is from an `openai/codex` issue thread; launch coverage says 1M for all three | **[UNVERIFIED]** | provider docs before the paper's setup section |
| 4 | Cached-input rates ($0.10/1M terra, $0.01/1M luna) are not modelled — `runlog.ModelRate` has no cached field. Relevant to Tier 1's repeated envelope reads; mirrors `docs/12` debt item 3 | **[NOT MODELLED]** | Track 2, before W6 cost modelling |
| 5 | Per-task cost estimates in the campaign runner are Vertex-derived | **[UNVALIDATED]** | first real OpenAI batch |
| 6 | BrowseComp-Plus per-query sizing (~870KB–8.3MB raw text) has not been redone against OpenAI limits | **[NOT DONE]** | before any `--dataset browsecomp` batch |
| 7 | The $5.33-vs-₹4,000 ledger discrepancy (§5) | **[OPEN — blocks O6]** | reconcile against the Vertex billing console |
| 9 | **`gpt-5.6-luna` does not drive the RLM REPL.** Reproduced across two independent runs, both checks, 6 iterations each: luna emits no ` ```repl ` blocks, makes zero recursive calls, and replies that it cannot see the context (*"the actual user question and the 110-character context..."* — it reads RLM's own scaffolding as a malformed user turn). **Cleanly attributed:** `terra` passed the identical checks in the same run — 17×23=391 computed via the REPL, 1 child call with nested metadata. Not a harness bug | **[CONFIRMED — 2 runs, 1 seed]** | consequences in §4a; needs a decision, not more evidence |
| 8 | No independent benchmark comparing `gpt-5.6-terra` against the Gemini pair on long-context retrieval. `docs/12` chose its pair on GDM-MRCR v2; **no equivalent evidence is offered here** — this proposal rests on the control-provenance argument (§3), not on a claim that terra retrieves better | **[UNVERIFIED, and load-bearing]** | Track 1, before the model-selection paragraph is written |

**Debt item 8 is the honest weak point of this proposal.** `docs/12` picked its pair on published long-context numbers. This one does not, because no comparable head-to-head exists. If the paper's model-selection paragraph needs a benchmark justification, that work has not been done.

## 10. What Anugrah needs to decide

1. **Fund OpenAI with cash, stranding ₹90,000 of Vertex credit — yes or no?** Everything else is downstream. (§4.2 item 3)
2. If yes: **approve `gpt-5.6-terra` / `gpt-5.6-luna` as the pair**, superseding `docs/12`. (§4.2 item 2)
3. **Grant an explicit, minuted exception to feature freeze A**, and state what it does to Manuscript A's 3 Sep date. (§3.4, §3.7 risk 4)
4. **Set the real spend cap.** `5` is a provisional trial ceiling set by Track 3 and is not a budget. (§4.2 item 3)
5. **Tier 2, in light of debt item 9** (§4a): keep luna and accept it can never serve as an RLM sub-model, or promote Tier 2 to terra at 10× the per-token cost and a thinner O6 result? Blocked on the luna builder test, which is blocked on `plan/` existing.
6. If no: **close this and rule on `docs/16` §2f** — the fence rename — instead. That decision is already yours and is currently the blocker either way.

---

*Track 3 has run nothing and merged nothing. Reviewing the branch costs nothing; `scripts/verify_rlm_openai.py` costs about twenty cents and settles debt items 1 and 2.*
