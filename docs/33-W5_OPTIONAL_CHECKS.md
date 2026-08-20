# 33 — W5 optional checks: what to do if there's slack

**Status:** Frozen W0 (9 Aug 2026) · Owner: Track 1 · Consulted by: Track 2/3 during W5 resource planning

W5 is a 7-day block in which the heaviest single week's work happens — corpus expansion to 4 documents, 3 baselines implemented first-hand, seed control + variance harness, all in preparation for W6's full measurement matrix. Risk #4 (`CONTEXT.md` §3.7) is that Phase A slips further, and the response is to cut features, never to move the dates.

This document flags the *one* optional decision point that is genuinely buy-now-or-not-at-all: a **2×2 model sweep on Tier 2**, conditional on slack existing at the end of W5. If you do it, decide by Sun 6 Sep and feed the results into W6's table. If you don't, just move forward — nothing breaks.

---

## The optional check: Tier 2 model upgrade for quality headroom

**Context:** `docs/12-MODEL_PAIR.md` selected Gemini 3.1 Flash-Lite for Tier 2 (Swarm) on a cost argument, not a quality one. The reasoning was: "Tier 2 is N parallel builders per document across 4 documents × 3 seeds × a full ablation grid in W6 — call volume is the dominant cost driver, not per-call quality ceiling, since each builder only needs to reliably consume its plan directive and section slice and emit valid JSON against the Master Plan schema, not perform open-ended long-context retrieval."

That is reasoning from first principles, not from a measured number. A measured number would look like: "we ran a small sample with 3.5 Flash-Lite instead, and the output quality improved by X%, which matters for our final result."

**The optional check:** If W5 has slack at the end (you've finished corpus expansion, baselines, and seed harness with time left), run a spot check:

- **Same setup as the main W6 matrix.** One document, MARD system, 3 seeds, representative metrics (task score, tokens).
- **Two Tier 2 models:** 3.1 Flash-Lite (current pick) vs. 3.5 Flash-Lite (the upgrade candidate).
- **Result:** compare task scores. If 3.5 Flash-Lite's improvement is material (≥5% is the rough bar) *and* the cost difference per Tier 2 call is still tolerable within your W6 budget, switch. Otherwise, stick with 3.1 Flash-Lite.

**Cost delta:** 3.5 Flash-Lite input is $0.30/1M, output $2.50/1M. 3.1 Flash-Lite input is $0.25/1M, output $1.50/1M. Per call the difference is small (~20% more), but Tier 2 is the high-call-volume tier in W6, so running 4 docs × 5 systems × 3 seeds × ablations on the more expensive model could exceed the spend cap. This is why it's optional and only if slack exists.

## When to decide

**By Sun 6 Sep (end of W5).** If you're doing the check, it's now or never — W6's feature freeze is Sun 13 Sep, and the full matrix uses the model you pick. Switching mid-W6 invalidates prior runs.

If you're *not* doing it, just note that decision and move to W6 with 3.1 Flash-Lite as frozen.

## Who owns this

Track 1 (you) decides whether to run it. Track 2 sizes the cost impact. Track 3 runs the spot-check and reports the quality delta.

## Why it matters at all

If 3.5 Flash-Lite's quality improvement is real and material, the W6 tables will be noticeably cleaner — less variance, higher signal. If it's noise, you save ~20% of the Tier 2 budget by sticking with 3.1 Flash-Lite. Either way, *you'll know*, rather than arguing about it later on a what-if.

---

## If you're reading this in W5

This is your gate question: **Do you have spare compute budget and wall-clock time to run a 1-document, 2-model spot check?** 

If yes, run it, report quality delta by Sun 6 Sep, decide the Tier 2 model for W6.

If no, skip it, ship W6 with 3.1 Flash-Lite.
