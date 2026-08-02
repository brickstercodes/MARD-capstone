# 00 — The claim MARD is making

**Status:** Frozen W0 (2 Aug 2026) · Owner: Track 1 (Anugrah Shetty) · Supersedes nothing, first version.

## The one sentence

> **MARD's growing metadata envelope makes recursive document exploration structure-aware — improving output quality and/or reducing tokens consumed relative to vanilla RLM on documents with exploitable structure, while degrading gracefully to vanilla-RLM behaviour on documents without it.**

## Why the sentence is shaped this way

- **"Metadata envelope," not "recursion."** The frontier-root/cheap-worker split and the recursive call structure already exist in the base paper (RLM, arXiv:2512.24601). MARD's contribution is the envelope that accumulates across calls — see `CONTEXT.md` §1.2. The claim sentence must not credit MARD with something the base paper already does, or the architecture reads as a restatement.
- **"Improving output quality and/or reducing tokens" — an disjunction, not a conjunction.** We do not know yet which direction the effect runs, and O3/O6 measure both independently. Claiming both before any run exists is exactly the kind of overclaim `CONTEXT.md` §4.3 was written to prevent.
- **"Degrading gracefully… without it" is load-bearing, not a hedge.** This is O4, stated as a *prediction* going in, not a failure mode discovered after the fact. `CONTEXT.md` §1.3 requires we say this before a reviewer does. The negative control (OOLONG, flat context) exists specifically to test this half of the sentence.
- **Deliberately silent on magnitude.** No percentage, no multiple, no "state of the art." §2.3 lists exactly this kind of number (the dead "15–25× cost reduction" claim) as something that gets fabricated by repetition. The claim sentence names the *shape* of the result, not its size — the size is Track 3's job to measure, not Track 1's job to predict.
- **Silent on which baseline.** "vanilla RLM" is the isolation baseline (O3). The other three first-hand baselines (full-context, naive chunking, embedding RAG) and OpenCode+offloading (94.0, the standing high-water mark per `CONTEXT.md` §1.7 challenge 1) matter for Manuscript B's positioning, but the *claim about MARD itself* is a claim about the delta MARD adds on top of RLM, isolated from those baselines. Conflating "beats vanilla RLM" with "beats everything" is challenge 1's trap.

## What this sentence is compatible with

- A null or negative result on O3, reported honestly and framed by the O4 boundary (Risk #1, `CONTEXT.md` §3.7). The claim does not say MARD *will* win — it says what MARD *is for* and what "graceful degeneration" looks like if it doesn't.
- Either mechanistic explanation for RLM's own gains (recursion-driven, per the base paper, or not, per SRLM arXiv:2603.15653). The envelope reduces orientation cost regardless of which explanation is correct — `CONTEXT.md` §1.7 challenge 3.

## What would falsify or force a rewrite of this sentence

- MARD underperforms vanilla RLM even on high-structure documents, with variance across 3 seeds ruling out noise. This is not evidence the sentence is wrong — it is evidence the *effect* is null, which the sentence already allows for. The sentence would need rewriting only if the *mechanism* claim (envelope → structure-awareness) turns out false, e.g. if Pass 0 skeletons are consistently unusable (Risk #3, decision point 16 Aug).
- Evidence that the frontier/cheap-worker split alone (with no envelope) accounts for the entire gain — this would mean the claim is attributing effect to the wrong component.

## Escalation

This sentence is Track 1's to freeze per `CONTEXT.md` §3.3 W0 scope. It is not on the §4.2 escalation list. If another track needs it changed, that request goes to Track 1, not resolved independently.
