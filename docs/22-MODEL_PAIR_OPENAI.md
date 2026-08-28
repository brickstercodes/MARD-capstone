# 22 — Model pair decision record (OpenAI)

**Status:** Decided 27 Aug 2026 · Decision owner: Anugrah Shetty (Track 1, holding both
arms) · Type: ADR-style, per global `CLAUDE.md` Part 7 · **Supersedes
`docs/12-MODEL_PAIR.md` in full**

## Decision

| Role | Model | Input $/1M | Output $/1M |
|---|---|---|---|
| **Tier 1 — the Scout** (root) | `gpt-5.2` | 1.75 | 14.00 |
| **Tier 2 — the Swarm** (sub-calls / builders) | `gpt-5-mini` | 0.25 | 2.00 |

**Provider:** OpenAI. **Rates read first-hand** from
`developers.openai.com/api/docs/pricing` on **27 Aug 2026**.

## Where these numbers live, and why only there

`provider/rates.py` is the single place these prices are typed in, and it is the source of
truth for this record rather than the other way round. Neither the vanilla arm's vendored
`Zhang_RLM` nor any per-model cost field on it is ever fed a price: cost is computed once,
centrally, from `RunLogger.totals()` against the `RateCard` that module builds. That is
`docs/18` §5.5's "two prices, one goes stale" trap avoided in code rather than by discipline.

`RateCard.cost_for` raises `StaleRateError` past 30 days, so **the page must be re-read and
`RETRIEVED_ON` updated before 26 Sep 2026** or every run refuses to price itself.

**Cached-input rates** ($0.175/1M and $0.025/1M) are on the same page and are deliberately
**not** wired: nothing in the pipeline tracks a cached-vs-uncached split
(`CompletionResult` reports only `input_tokens`/`output_tokens`), and recording a rate
nothing reads would be exactly the unused, silently-stale figure the discipline exists to
prevent.

## Context

`docs/12`'s Gemini pair died with the provider switch on 26 Aug (`docs/18` §2, §3). This
record replaces it. Unlike `docs/12`, the justification here is **not** a published
long-context benchmark table: no equivalent vendor-published breakdown was read for these
two models, and inventing one after the fact would be worse than saying so.

**What actually justifies the pair, stated honestly:**

1. **Role fit, reasoned rather than measured.** Tier 1 runs once per document, must hold the
   envelope and the document skeleton across 14 sequential chapter calls, and emits the typed
   Master Plan that everything downstream depends on — so it takes the stronger model. Tier 2
   is $N$ independent builders each consuming one section plus a directive and emitting prose;
   call volume, not per-call ceiling, is the dominant cost driver there.
2. **The cost frontier makes the split cheap.** Tier 2 carries roughly 93% of the token
   volume (704k of 757k input tokens on `introcs`, per `docs/18` §10.3) at one-seventh the
   input rate and one-seventh the output rate. Putting the Scout model in Tier 2 would
   multiply the matrix cost several-fold for a quality gain Tier 2's task profile may not
   need.
3. **It ran.** Three logged vanilla runs on `introcs` completed at $0.32, $0.58 and $1.60
   (`runs/`, seeds 11/23/42), which is the only first-hand evidence in this record.

**This is a budget-and-role-driven choice, not a benchmark-driven one, and the manuscript
should say so** rather than implying a sweep that was never run — the same correction
`CONTEXT.md` §2.2 item 3 already applied to the deck's claimed 3×3 Pareto sweep.

## Corrected cost model

`docs/18` §10.3's figures were computed against the GPT-5.6 Sol/Terra/Luna rate card, which
is **not** the pair that ran. Recomputed at the rates above:

| | Input | Output | Cost |
|---|---|---|---|
| MARD Tier 1 — Pass 0 + 14 chapter calls | 53k | 31k | $0.53 |
| MARD Tier 2 — 120 builders | 704k | 120k | $0.42 |
| **MARD, one run (projected)** | | | **≈ $0.94** |
| **Vanilla RLM, one run (MEASURED, n=3)** | | | **$0.32 – $1.60, mean $0.83** |

Remaining Manuscript A matrix — MARD ×3, A1 ×3, negative control ×3 per arm — is
**≈ $11**, against $2.66 already spent and a $120 ceiling.

**Conclusion: cost is not a constraint on this manuscript and the cap will not bind.** An
earlier estimate of $25–35 was computed against the wrong rate card and is withdrawn.

## Consequences

### Positive
- Rates are recorded once, in code, with a source URL, a retrieval date and an enforced
  staleness ceiling. This is stricter than `docs/12` managed.
- The measured vanilla costs bound the projection from below with real data.

### Negative — stated plainly
1. **No published benchmark justifies this pair.** `docs/12` could at least cite a vendor
   MRCR table. This record cannot, and the manuscript's model-selection sentence must be
   correspondingly modest.
2. **The Tier 1 / Tier 2 split is untested.** Item 1 of the justification above is reasoning
   from task profile, not measurement. The 2×2 model sweep that would test it is deferred.
3. **`docs/18` §10's cost model was wrong** for two weeks and nobody noticed, because no run
   had priced itself yet. It is corrected above; the lesson is that a projection built on a
   rate card the pipeline does not use is not a projection of anything.

### Risks
- `RETRIEVED_ON` expires 26 Sep 2026, four days before Manuscript B is due. **Re-read the
  pricing page before the W6 matrix**, not after it fails.
- Reasoning-family parameter handling (`max_completion_tokens`, no `temperature`) is in
  `provider/reasoning.py` and applies to both models. A future pair outside that family
  would need that path re-checked.

## Verification debt

| # | Item | Status |
|---|---|---|
| 1 | No published long-context benchmark comparing `gpt-5.2` against alternatives for the Scout role | **[UNVERIFIED]** — none sought; the manuscript must not imply one |
| 2 | Whether Tier 2 would benefit measurably from the Scout model | Not tested — deferred 2×2 sweep |
| 3 | Cached-input accounting | Deliberately unwired; revisit only if a token-split field appears |
