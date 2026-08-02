# 12 — Model pair decision record

**Status:** Decided 2 Aug 2026 (within the Sun 9 Aug deadline, `CONTEXT.md` §4.2 item 2) · Decision owner: Anugrah Shetty · Type: ADR-style, per global `CLAUDE.md` Part 7.

## Decision

- **Tier 1 (the Scout):** `gemini-3.6-flash` — Google Cloud Vertex AI, model ID `gemini-3.6-flash`.
- **Tier 2 (the Swarm):** `gemini-3.1-flash-lite` — Google Cloud Vertex AI, model ID `gemini-3.1-flash-lite`.
- **Provider:** Google Cloud Vertex AI only. No AI Studio / Gemini Developer API connection — the ₹90,000 credit balance is redeemable via Vertex only.
- **Budget ceiling:** ₹75,000 maximum, spendable only from that credit balance (`CONTEXT.md` §4.2 item 3).

## Context

`CONTEXT.md` §2.3 killed the 2024-era named-model lineup and said "name models only at selection time." That time is now. The base paper (RLM, arXiv:2512.24601) runs entirely on GPT-5/GPT-5-mini and SRLM (arXiv:2603.15653) is GPT-5-family as well — neither paper gives us a Gemini number to anchor against, so this pair stands on Google's own published evaluations, not on continuity with the base paper.

## Evidence — GDM-MRCR v2 (8-needle)

Long-context retrieval is the axis that matters most for both tiers: Tier 1 must hold a document's structure across a large context to produce a usable skeleton and plan; Tier 2 builders each work from a plan directive plus a section slice and must not lose track of either. GDM-MRCR v2 is the only long-context benchmark Google publishes across the full current Gemini family, using a released, reproducible dataset (`github.com/google-deepmind/eval_hub/tree/master/eval_hub/mrcr_v2`).

| Model | Status (Vertex) | MRCR v2 128k (avg) | MRCR v2 1M (pointwise) | Input $/1M | Output $/1M | Source |
|---|---|---|---|---|---|---|
| **Gemini 3.6 Flash** | GA, released 21 Jul 2026 | **91.8%** | **54.0%** | $1.50 | $7.50 | [deepmind.google/models/gemini/flash](https://deepmind.google/models/gemini/flash/) |
| Gemini 3.1 Pro | Preview | 84.9% | 26.3% | $2.00 | $12.00 | [deepmind.google/models/gemini/pro](https://deepmind.google/models/gemini/pro/) |
| Gemini 3.5 Flash | GA | 77.3% | 26.6% | $1.50 | $9.00 | [deepmind.google/models/gemini/flash](https://deepmind.google/models/gemini/flash/) |
| Gemini 3.5 Flash-Lite | GA | 72.2% | 21.3% | $0.30 | $2.50 | [deepmind.google/models/gemini/flash-lite](https://deepmind.google/models/gemini/flash-lite/) |
| **Gemini 3.1 Flash-Lite** | GA, released 7 May 2026 | 60.1% | 12.3% | $0.25 | $1.50 | [deepmind.google/models/gemini/flash-lite](https://deepmind.google/models/gemini/flash-lite/) |

All figures are **vendor self-reported** (Google's own eval harness), pass@1, no majority voting — flagged per `CONTEXT.md` §4.3's discipline, not presented as independently verified. No independent third-party long-context leaderboard (LMArena, Artificial Analysis, Epoch AI) was found publishing a comparable Gemini 3.6/3.1 breakdown at time of writing; this is noted as residual verification debt below.

## Why Gemini 3.6 Flash for Tier 1, not Gemini 3.1 Pro

**Gemini 3.6 Flash outperforms Gemini 3.1 Pro on the one benchmark that matters most for this role, and costs less doing it.** At the 1M-token pointwise setting, 3.6 Flash scores roughly double 3.1 Pro (54.0% vs 26.3%); at 128k it leads by 7 points (91.8% vs 84.9%). Input is 25% cheaper ($1.50 vs $2.00/1M) and output 37.5% cheaper ($7.50 vs $12.00/1M).

This directly overturns the deck's "frontier tier" framing (`CONTEXT.md` §2.3: "Say 'frontier tier' and 'budget tier'. Name models only at selection time"). Naming Gemini 3.1 Pro "frontier" here would mean picking the label over the evidence — exactly what `CONTEXT.md` §4.3's evidence-discipline rules exist to prevent. **The paper should describe the Tier 1 model by its role (the Scout) and by the published benchmark that justifies it, not by a marketing tier name.** If a reviewer asks why the "Pro"-branded model isn't in the root position, the MRCR table above is the answer, cited directly.

Gemini 3.1 Pro remains preview-status on Vertex with no published retirement date — an additional, secondary reason not to anchor the pipeline on it for a project running through 30 Sep.

## Why Gemini 3.1 Flash-Lite for Tier 2, not a newer Flash-Lite

Gemini 3.5 Flash-Lite scores higher on MRCR (72.2/21.3 vs 60.1/12.3) but costs 20% more on input and 67% more on output ($0.30/$2.50 vs $0.25/$1.50 per 1M). Tier 2 is N parallel builders per document across 4 documents × 3 seeds × a full ablation grid in W6 (`CONTEXT.md` §2.1) — call volume is the dominant cost driver here, not per-call quality ceiling, since each builder only needs to reliably consume its plan directive and section slice and emit valid JSON against the Master Plan schema, not perform open-ended long-context retrieval itself. **Gemini 3.1 Flash-Lite is chosen as the cheaper GA model with a published MRCR number**, prioritizing surviving the ₹75,000 budget ceiling across W6's run volume over a marginal quality gain that Tier 2's task profile may not need. This is a budget-driven choice, not a benchmark-driven one, and is recorded as such rather than dressed up with a benchmark citation it doesn't really rest on.

**Flagged for the W5 optional 2×2 sweep** (`CONTEXT.md` §2.2 item 3): if slack exists, re-run a small slice of the matrix with Gemini 3.5 Flash-Lite as Tier 2 to check whether the extra MRCR headroom actually moves Tier 2's output quality, since the task-profile argument above is reasoning from first principles, not from a measured number.

## Consequences

### Positive
- Both models are GA (not preview) except noted; Tier 1 pick has no announced retirement date, Tier 2 pick retires no earlier than 7 May 2027 — both outlive the 30 Sep 2026 delivery date with margin.
- Cost frontier is favorable: Tier 1 is simultaneously better and cheaper than the alternative considered, which is an unusually clean result to report.

### Negative — things this decision costs us, stated plainly
1. **We cannot reproduce a base-paper number as a sanity check.** `CONTEXT.md` §3.3 Track 3 W1 explicitly assigns "reproduce one published base-paper number as a sanity check" — that number is GPT-5-family only. **Replacement sanity check, assigned here:** Track 3 should instead reproduce Google's own GDM-MRCR v2 number for `gemini-3.6-flash` directly against Vertex AI, using the released `eval_hub/mrcr_v2` dataset, before trusting any MARD-specific measurement. This is a protocol amendment — see `docs/30-MEASUREMENT_PROTOCOL.md`.
2. **The RLM reference library (`github.com/alexzhang13/rlm`, MIT license) has no Vertex AI code path.** Its `GeminiClient` (`rlm/clients/gemini.py`) is hardcoded to the direct `google-genai` API-key flow (`GEMINI_API_KEY`), not `vertexai=True`/project/location. This blocks Track 2's W0 "RLM library installed and running its own examples" task as written. **Resolution:** Anugrah has a working Vertex AI Gemini client from a prior project; Track 2 is to port that implementation into a patched `GeminiClient` (or an equivalent new backend) rather than building Vertex support from scratch. This is now a named W0/W1 Track 2 task, not a silent assumption — flagged in `docs/30-MEASUREMENT_PROTOCOL.md` for Track 2 to size and confirm feasible before end of W0.
3. **Both models are new enough (May/Jul 2026 GA) that no independent third-party benchmark exists yet.** All evidence in this record is vendor self-reported. If an independent long-context leaderboard publishes comparable numbers before Manuscript A's draft (3 Sep), Track 1 should re-check this table and add the citation; if not, the paper's model-selection paragraph should say "vendor-reported" plainly rather than implying independent verification.

### Risks
- Preview-status models on Vertex can change behavior or pricing without the retirement-date guardrails GA models have — this applies to nothing in the final pick (both are GA) but ruled out Gemini 3.1 Pro as a candidate in part for this reason.
- If Track 2's Vertex port of the RLM client has bugs the upstream OpenAI-path testing wouldn't catch, that risk lands entirely on Track 2's W0/W1 timeline, which is already the second-heaviest track. Flagged, not owned, by Track 1.

## Verification debt opened by this record

Per `CONTEXT.md` §4.3 item 5: mark and surface, don't quietly assert.

| # | Item | Status |
|---|---|---|
| 1 | No independent (non-Google) long-context benchmark found comparing Gemini 3.6 Flash vs 3.1 Pro | [UNVERIFIED] — re-check before Manuscript A draft, 28 Aug |
| 2 | Whether Track 2's ported Vertex client preserves the RLM library's existing retry/backend-abstraction behavior | Not yet attempted — Track 2, W0/W1 |
| 3 | Cache-storage pricing for context caching on Vertex (relevant to Tier 1's repeated envelope reads) — current pricing page states no separate storage-per-hour line item, but this silence is not confirmed as "free" | [UNVERIFIED] — Track 3, before W6 cost modelling |
