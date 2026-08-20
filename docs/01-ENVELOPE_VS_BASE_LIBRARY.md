# 01 — The envelope vs. the base library's own metadata

**Status:** Frozen 9 Aug 2026 · Owner: Track 1 · Source: Track 2's `docs/RLM_BASELINE_SURVEY.md` §2, read into `docs/00-CLAIM.md`'s companion note · **This is paper content for O1 / §3 Method, not implementation notes** — write it into the method section directly, per the source document's own recommendation.

`CONTEXT.md` §1.2 already requires stating, before a reviewer does, that the frontier-root/cheap-worker split is not our contribution. Track 2's W0 survey of the vendored RLM library (`.vendor/rlm`, pinned `72d6940`) found a second, sharper version of the same hazard, and it lands directly on the word "metadata" in MARD's own name. This document freezes the distinction so it survives into the manuscript rather than staying buried in a Track 2 working doc.

## The base library already ships something metadata-shaped

First-hand from `.vendor/rlm/rlm/core/types.py` (citations are file-and-line into the pinned vendored copy, so they are checkable): `RLMMetadata` carries `root_model`, `max_depth`, `max_iterations`, `backend`, `environment_type`; `RLMChatCompletion.metadata` carries the full trajectory — iterations, code blocks, nested `llm_calls`/`rlm_calls`, each with its own metadata, recursively; `UsageSummary` and `QueryMetadata` track tokens, cost, and context lengths per call. The library ships an example, `depth_metadata_example.py`, whose entire purpose is demonstrating metadata captured at every depth level and flowing back up the recursion tree.

**A reviewer who reads that example and then reads "Metadata-Augmented Recursive Decomposition" will reasonably ask what we added.** This document is the answer, stated once, precisely, so it goes into §3 rather than getting discovered in review.

## The answer: direction of flow, checkable in the source

**In the base library, metadata flows upward and is observational.** It is a record of what happened, assembled after the fact for inspection and logging. It never re-enters a prompt and never influences a child call. When a parent RLM spawns a child (`rlm/core/rlm.py:807–836`):

- The child gets `logger=RLMLogger() if self.logger else None` — a **fresh, empty** logger (`rlm.py:824`). The library's own comment: *"Give child its own logger so its trajectory is captured in metadata"* — capture, not inform. The parent's accumulated trajectory is explicitly not passed down.
- `child.completion(prompt, root_prompt=None)` (`rlm.py:836`) — the child receives only the prompt string the parent's REPL code passed to `rlm_query()`. Nothing else.

**In MARD, the envelope flows downward and is operative.** Skeleton, accumulated findings, and parent directive are injected into the child's context *before* it runs, changing what the child can see and therefore what it does. That is the entire claim in `CONTEXT.md` §1.1 and the disjunction in `docs/00-CLAIM.md`: exploration that *confirms a hypothesis* instead of *discovering blindly*.

**Same word, opposite direction, and only one of them changes model behaviour.** This sentence, or a close paraphrase of it, belongs in the paper.

## The trap inside the answer — and the rebuttal, ready in advance

The library has a `root_prompt` parameter (`rlm.py:303`, documented `rlm.py:337`) that lets the root LM see a small user-specified prompt alongside its context — and children are explicitly passed `root_prompt=None`. So the library **has a downward-injection slot and deliberately declines to use it for children.**

Expect this exact objection at review: *"you just used `root_prompt`."*

**The rebuttal is about what fills the slot, not whether the slot exists.** `root_prompt` is designed for a fixed, small, user-authored string — the docstring's own example is the user's original question. The envelope is accumulated state that *grows across calls*: a structural skeleton from Pass 0, findings compounded from every prior call, and a parent-issued directive specific to *this* child. Nothing in the base library constructs, propagates, or compounds that; there is no mechanism carrying one child's findings to the next.

Stated plainly, because it is also the more honest version of the claim: **the base library gives us a place to put the envelope. What is ours is the envelope itself** — what goes in it, how it accumulates across the Pass 0/1/2 structure (`CONTEXT.md` §1.1), and the typed Master Plan that makes Tier 2 dispatch structure-aware rather than section-blind.

## Where this goes in the manuscript

Per the source survey's own recommendation (worth repeating because it's right): **O1's formalisation should open by naming what the base library already provides and drawing the upward/downward line explicitly, before defining the envelope.** Written that way, it reads as precision — a team that read the library they're building on closely enough to draw a line inside it. Written the other way — envelope first, distinction buried in related work, or omitted — it reads as something a reviewer caught.

## Consequence for `docs/00-CLAIM.md`

No change needed to the claim sentence itself. This document is the mechanistic backing for why the claim says "envelope," not "recursion" or "metadata" unqualified — the base library already has recursion and already has metadata; it does not have accumulated, downward-flowing, operative state. That precision is what the claim sentence is protecting.
