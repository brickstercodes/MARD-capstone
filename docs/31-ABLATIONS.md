# 31 — Frozen ablation set

> ### ⚠️ CLARIFIED — 26 Aug 2026 (A4 only; no ablation redefined)
>
> All four ablations toggle exactly what they always toggled. Two operational notes on
> A4, from reading the `replm` source first-hand — see
> [`18-W3_PROVIDER_SWITCH.md`](18-W3_PROVIDER_SWITCH.md) §5.1–§5.3:
>
> - **`max_recursion_depth=0` does not disable sub-calls.** The guard is
>   `self._depth + 1 < max_recursion_depth`, so 0 and 1 take the same branch and produce
>   indistinguishable traces. The real no-sub-calls condition is `enable_sub_calls=False`.
>   **Record A4 as an `(enable_sub_calls, max_recursion_depth)` pair.**
> - **A4's depth numbering is offset by one from `replm`'s.** MARD depth 0 (two-pass)
>   already issues flat sub-calls, which is `replm` depth **1**. Mapping: MARD {0,1,2,3}
>   ↔ `replm` {1,2,3,4}. **A1 requires depth held fixed** — setting the control to
>   `replm` 0 or 3 to "match" a MARD number makes O3 measure a depth difference instead of
>   the envelope. Whether the sweep ends at `replm` 3 or 4 is open (`18` §7 item 3).
> - **No A4 number may be quoted from a `replm` build older than `a0ca553`** — batched
>   sub-calls silently bypassed recursion before that fix, so every depth ≥ 2 point would
>   have run at depth 1 while being logged correctly. `18` §5.3.

**Status:** Frozen W0 (2 Aug 2026) · Owner: Track 1 · Read by: Track 3 before building scorers/runner (`CONTEXT.md` §3.3 W2: "ablation runner (envelope removed)").

Four ablations, per `CONTEXT.md` §2.1/§2.2/§3.2. This document fixes *how each one is operationalised* — i.e., exactly what toggles, what stays fixed, and what output it's expected to produce — so Track 3 can build the ablation runner against a stationary target. Changing any definition below after Track 3 has built against it is a protocol change, not a bug fix, and must go through Track 1.

## A1 — Envelope removed

**What toggles:** every recursive call receives the raw text slice only — no skeleton, no accumulated findings, no parent directive. This is architecturally "vanilla RLM," so **A1 and the vanilla-RLM control are the same run**; do not implement or execute it twice. Track 3's W1 "vanilla RLM running end-to-end" task and this ablation are one artifact.

**What stays fixed:** model pair (`docs/12-MODEL_PAIR.md`), document, seed, Tier 1/Tier 2 split, depth.

**What it isolates:** the entire MARD contribution in one cut — this is O3's primary comparison.

## A2 — Plan withheld from Tier 2

**What toggles:** Tier 1 still runs, still produces the Master Plan, but Tier 2 builders do **not** receive the plan's directive for their section — each builder sees only its raw section slice, exactly as if Tier 1 hadn't run. The Master Plan is still computed and joined-in-order (see below) purely for the join-order operation, since dropping the join order too would conflate two effects (RQ4-style ablation, `CONTEXT.md` §2.4).

**What stays fixed:** Tier 1 does full envelope-based exploration; join order comes from the Master Plan's `concept_graph` as normal.

**Why this is an ablation, not a baseline:** `CONTEXT.md` §2.2 item 2 — this was "single-tier without the plan" in the deck, demoted from a 5th baseline. It tests whether *Tier 2 dispatch* benefits from structure-awareness, distinct from A1's test of whether *exploration itself* does.

**Failure mode to watch:** if a builder's prompt template silently reconstructs plan-like context from the raw section text (e.g., because the section itself contains headings), this ablation under-measures the plan's contribution. Track 3: log the exact prompt sent to each Tier 2 builder in this condition so this is auditable, not asserted.

## A3 — Reordering disabled

**What toggles:** Tier 2 builder outputs are joined in **book order** (source document's linear page/section order) instead of **Master Plan order** (the dependency-derived ordering from `concept_graph.edges`).

**What stays fixed:** everything upstream of the join — envelope, plan, Tier 2 execution per builder — is identical to the full MARD run. Only the join-time sequencing changes.

**What it isolates:** the O5 dependency-ordering claim specifically. `CONTEXT.md` §2.4 notes book order is itself an expert baseline (the document's own author already sequenced it), so this is not a straw-man comparison — reordering has to beat a real ordering, not a random one.

**Scored via:** forward-reference violations, counted before vs after reordering (`CONTEXT.md` §3.3 Track 4, W3: "count forward-reference violations before vs after reordering"). This is the metric this ablation exists to produce — see `docs/30-MEASUREMENT_PROTOCOL.md`.

## A4 — Depth swept

**What toggles:** the maximum recursion depth of Pass 2 targeted deep-dive calls. This is the only ablation that is a **sweep** (multiple runs across a parameter), not a single on/off toggle.

**Depth values to run:** depth ∈ {0, 1, 2, 3}, where depth 0 means Pass 0 + Pass 1 only (no targeted deep dive — a "two-pass MARD" run, directly reusable if Track 1's 16 Aug decision point in `CONTEXT.md` §3.3 triggers the two-pass fallback), and depth 3 is the ceiling based on the base paper's own reported depth range (`CONTEXT.md` §1.6: RLM depth=1 numbers are the base paper's primary reported condition; OOLONG-Pairs at depth 3 is its deepest reported figure). **If Track 1's compute budget forces a smaller sweep, cut from the top (depth 3 first), never from depth 0/1** — those two are the ones the two-pass contingency and the base-paper comparison both depend on.

**What it isolates:** survives from the old RQ3 ("what % must be read") per `CONTEXT.md` §2.4 — at what depth does additional recursive exploration stop paying for itself in tokens spent vs. quality gained.

**Reported as:** a curve (quality and/or tokens vs. depth), not a single delta — this is the one ablation whose output is a plot, not a table row.

## What is explicitly not a fifth ablation

Model selection (frontier vs. budget) is **not** an ablation in this set — it is a fixed decision (`docs/12-MODEL_PAIR.md`), with an optional separate 2×2 sweep in W5 if slack permits (`CONTEXT.md` §2.2 item 3). Do not fold it into A4 or add it as A5 without going back to Track 1 — conflating "depth" and "model" sweeps in one grid would make neither one interpretable.

## Interaction with the measurement matrix

Manuscript A (W3, 4 days, one document) runs: vanilla RLM (= A1) · MARD full · negative control (OOLONG, flat context) · **one** ablation. Per `CONTEXT.md` §3.2/§3.3, the single ablation chosen for A should be **A2 (plan withheld)** — it is the cheapest to run (no depth sweep, no separate reordering scoring pipeline) and most directly supports the claim sentence's "structure-aware dispatch" framing in `docs/00-CLAIM.md`. A3 and A4 first appear in Manuscript B's full grid (W6). This choice is Track 1's call, made here so Track 3 doesn't have to guess which ablation to build first.

Manuscript B (W6) runs the full ablation grid: A1, A2, A3, and the full A4 sweep, layered on top of the 4-doc × 5-system × 3-seed matrix per `CONTEXT.md` §2.1.
