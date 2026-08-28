# 14 — Track 1 responses to Track 2's W0 asks

**Status:** Answered 9 Aug 2026 · Owner: Track 1 (Anugrah Shetty) · Responds to: `docs/RATE_LIMIT_BUDGET.md` §6, `docs/drafts/issue46-anugrah.md` (issue #46), issue #44, and the `eval/` naming question raised in `TRACK2.md` and `eval/__init__.py`'s own docstring.

Four asks, answered in the order Track 2 asked them.

---

## 1. Budget ceiling (#46) — the number, in the shape `SpendCap` needs

**`docs/12-MODEL_PAIR.md` already froze the campaign ceiling at ₹75,000**, spendable only from the existing Vertex AI credit balance. `SpendCap.from_env()` reads `MARD_SPEND_CAP_USD`, so this needs converting, and I'm not going to hand over a number I invented — the conversion rate is sourced and dated, same discipline `runlog.pricing.RateCard` already enforces for model prices.

**USD/INR spot rate, 9 Aug 2026: ₹95.13 per USD** (Investing.com / Xe, read today). ₹75,000 ÷ 95.13 ≈ $788.60.

**Set `MARD_SPEND_CAP_USD=780`.** Rounded *down* from $788.60, not to the nearest ten — a spend cap that's slightly conservative costs nothing; one that's slightly optimistic against a moving exchange rate risks exceeding the actual credit balance. This is a campaign ceiling covering W3 and W6 together, per your ask, not a monthly figure.

**Re-check before spending against it if this sits unused for a while** — same 30-day staleness rule your own `RateCard` enforces on model prices. If W6 (7–13 Sep) is more than 30 days after 9 Aug (it is — 29 days, right at the edge), re-read the exchange rate before the matrix runs and adjust the cap if the rupee has moved materially.

## 2. Model pair (#44) — confirmed, with the citation your rate-limit table needs

**Tier 1 (the Scout): `gemini-3.6-flash`. Tier 2 (the Swarm): `gemini-3.1-flash-lite`. Both on Vertex AI, no other provider.**

Full decision record with the benchmark citation (GDM-MRCR v2, both models beat the deck's original "3.1 Pro is frontier" framing on long-context retrieval) is in `docs/12-MODEL_PAIR.md`. Pull the model IDs and Vertex-specific details you need for `docs/RATE_LIMIT_BUDGET.md` §2 directly from there — the rate-limit table's "frontier tier" / "budget tier" rows can now be named rows.

**One thing that lands squarely on you, not just FYI:** the upstream RLM library's `GeminiClient` (`.vendor/rlm/rlm/clients/gemini.py`) is hardcoded to the direct API-key flow (`GEMINI_API_KEY` via `google-genai`) with no `vertexai=True`/project/location path. Since your credits are Vertex-only, this needs a patch before any real call can be made against either model. I have working Vertex Gemini client code from a prior project I can hand over — say what shape is most useful (a diff against the vendored copy, or just the relevant client class) and I'll get it to you. This is now the single thing most likely to slip W0/W1 if it isn't sized soon.

## 3. `eval/` shadows the builtin — keeping it, closing the question

**Keep `eval/` as named.** Your own docstring in `eval/__init__.py` already made the case I'd have made: matching `CONTEXT.md` §4.1's tree matters more than the builtin-shadowing risk, which is a minor lint concern (nobody does `from repo import eval` and then calls the builtin `eval()` in the same scope without ruff or mypy catching it), not a correctness one. Renaming now would touch `pyproject.toml`'s `packages` list and the `eval` extras group, plus anything Track 3 is about to start importing — real churn for a cosmetic fix. Not worth it the week W1 starts.

This closes the question — no need to raise it again.

## 4. Ablation grid scope — resolved, `CONTEXT.md` didn't actually contradict itself but the wording was ambiguous enough to read that way

Answering both parts of your §1.2 exactly:

**The depth sweep is inside the four-item ablation grid, not a separate fifth thing.** `docs/31-ABLATIONS.md`, written this same W0, enumerates exactly four ablations — A1 (envelope removed), A2 (plan withheld), A3 (reordering disabled), A4 (depth sweep, depths ∈ {0,1,2,3}). `CONTEXT.md` §3.3's "the ablation grid and depth sweep" phrasing was describing the same four-item grid with its one multi-valued member called out for emphasis, not announcing a fifth axis. My apologies that the wording supported your reading — it's genuinely ambiguous as written, and this document is the fix.

**Ablations run on all 4 documents for Manuscript B.** `docs/31-ABLATIONS.md`'s closing section says the full grid runs "layered on top of the 4-doc × 5-system × 3-seed matrix" — that's the 36-run answer, not the 9-run one. This is the more expensive reading, and I'm making the cost explicit rather than letting it arrive as a surprise in W6: that's roughly 3 non-sweep ablations × 4 docs × 3 seeds = 36 runs, plus A4's depth sweep (4 depths × 4 docs × 3 seeds = 48 runs, though depth 0/1 already overlaps with cheaper conditions in practice) on top of the 60-run main matrix.

**If §1.4's vLLM/open-weights lever for the ablation grid is real** — and it should be, this is exactly the kind of traffic that doesn't need to touch a rate-limited API — take it. That decision is yours and Track 3's to make and live with, as your document already says; I'm just confirming the run count that decision needs to absorb.

---

## What this doesn't answer

Track → person assignment (§4.2 item 1), venue (item 4), and guide review windows (item 6) are still open and are not Track 1's or Track 2's to resolve — see `docs/13-W0_DECISIONS_LOG.md` §2.
