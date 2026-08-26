# 18 — Why our token accounting under-reports, in the base library

**Status:** Root-caused from source 25 Aug 2026 · Owner: Track 3 (Arav) · **Blocks O6** · Explains a discrepancy on *both* providers, so it is not a Vertex or an OpenAI finding — it is ours.

## The observation

| Provider | Our reported spend | Provider's actual | Ratio |
|---|---|---|---|
| Vertex (122 runs, `runs/_ledger.json`) | $5.33 | ~₹4,000 (~$42) | **~8×** |
| OpenAI (2 `verify_rlm_openai.py` runs) | $0.13 | **$0.86** | **~6.6×** |

Two providers, two SDKs, two transports, the same order-of-magnitude under-count. That rules out a provider-side explanation and points at the code path both estimates were made through.

**It is not the rates.** Even substituting the (higher, disputed) launch-coverage figures for the OpenAI pair — terra $2.50/$15, luna $1/$6 instead of the $1.00/$6.00 and $0.10/$0.60 on the provider's page — the OpenAI estimate rises only to ~$0.22, still 4× short. Token counts, not prices, are the dominant term.

## Root cause: `UsageSummary` is not a total

Both under-counted estimates were derived from `result.usage_summary` — the library's own aggregate. Reading the source, it cannot be a total. Three independent defects:

### A. `LMHandler.get_usage_summary()` merges by model name, so same-model clients overwrite

`rlm/core/lm_handler.py`:

```python
merged = {}
merged.update(default_summary.model_usage_summaries)      # keyed by model name
if self.other_backend_client is not None:
    merged.update(other_summary.model_usage_summaries)     # overwrites on key collision
for client in self.clients.values():
    merged.update(client_summary.model_usage_summaries)    # overwrites again
```

`dict.update` **replaces** a value on key collision; it does not sum. The key is the model name.

**This project runs single-backend by design** (A1 is "the library exactly as vendored, single backend"), so root, children and fallbacks all report under the *same* model name — and the merge collapses every one of them to whichever client was merged last. The defect is invisible in a multi-model configuration and total in ours.

The same constructor makes it worse: `register_client(client.model_name, client)` keys `self.clients` by model name too, so that dict can only ever hold **one client per model** regardless of how many exist.

### B. Recursive children build clients the handler never sees

`rlm/core/rlm.py` constructs clients locally in at least three places — line 234, `_fallback_answer` (709), and `_subcall`'s max-depth branch (746) — via `get_client(...)`. None of those are passed to `register_client`. Their usage accrues on objects the parent's handler has no reference to, so it cannot appear in any merge, correct or not.

The `RLMChatCompletion` these return does carry its own `usage_summary`, but the only thing the parent does with it is line 846:

```python
self._cumulative_cost += result.usage_summary.total_cost
```

— cost, not tokens. And see C.

### C. `total_cost` is always `None` on OpenAI, so the library's own budget guard is inert

`OpenAIClient._track_cost` sets `last_cost` only from `usage.cost` / `usage.model_extra["cost"]` — fields **OpenRouter** returns and the OpenAI API does not. So `ModelUsageSummary.total_cost` is `None`, `UsageSummary.total_cost` is `None`, line 846 never adds anything, and `_cumulative_cost` stays `0.0` forever.

Consequence: RLM's own `max_budget` check (`rlm/core/rlm.py` 555–556, `BudgetExceededError`) **can never fire on OpenAI.** It is not a second line of defence; it is decoration. Same for the `remaining_budget` calculation at line 774.

## What is *not* affected, and why it matters

**`eval/run_vanilla_rlm.py` does not have this bug.** `live_call_logging` patches the **class** — `OpenAIClient.completion` / `.acompletion` — not an instance:

> *Patching the class rather than one instance is what makes this cover recursive child calls too — rlm/core/rlm.py constructs each child's client itself via get_client(), so this script never gets a handle to hand a wrapped instance down.*

Every call through every instance is logged at the moment it returns, including the invisible children of defect B, and token counts come from `get_last_usage()` on that instance during that call, which is unaffected by the merge in defect A.

So the split is:

| Path | Trustworthy? |
|---|---|
| `eval/run_vanilla_rlm.py` → `live_call_logging` → `runlog` | **Yes** (class-level patch) |
| Anything reading `result.usage_summary` | **No** — under-reports |

**This retroactively explains part of the Vertex gap.** `docs/16` §2b, §2c and §2d each record diagnostic spend "reconciled after the fact from `usage_summary`" because those scripts ran outside `RunLogger`. Those reconciliations were made through the defective path and are all low by an unknown factor. §2d even notes its own accounting gap explicitly.

## Fixes

| # | Fix | Where | Status |
|---|---|---|---|
| 1 | **Never read `usage_summary` for money.** Route every script that spends through `live_call_logging` + `RunLogger` | `scripts/verify_rlm_*.py`, any future diagnostic | **to do** |
| 2 | **Reconcile against the provider, not ourselves.** One logged run, then compare `summary.json` totals to the OpenAI dashboard's per-model breakdown for the same window. That settles token counts and rates together | Track 3 | **to do — do this before any cost figure is quoted** |
| 3 | **Do not rely on RLM's `max_budget`.** The real guards are `runlog.SpendCap` (client-side) and a hard project budget limit in the OpenAI dashboard (server-side) | ops | server-side limit **not yet set** |
| 4 | **Re-mark the docs/16 §2b/2c/2d cost figures as under-estimates**, with this document as the reason | docs/16 | **to do** |
| 5 | Do not "fix" `.vendor/rlm`. Patching the library reintroduces exactly the provenance problem `docs/17` §3 exists to remove. Work around it in our code and report it upstream | — | decided |

## A related risk, not yet a bug

`get_last_usage()` reads `self.last_prompt_tokens` / `self.last_completion_tokens`, instance attributes written by `_track_cost` on each call. Under **concurrent** calls sharing one client instance, a second response can overwrite those attributes before the first is logged — silently mis-attributing tokens.

Nothing today triggers it: the vanilla control is sequential. **Track 2's W2 deliverable is an asyncio bounded worker pool with fork-join**, which is precisely the condition that triggers it, and W6 runs it at scale. Flagged now, while it is cheap.

## Paper consequence

O6's cost model must be built from `runlog`'s class-patched call log, reconciled against provider billing — never from the library's own usage aggregate. That is one sentence in the methods section and it is worth writing, because a reviewer who has used this library may well have the buggy number.

The `-8×`/`-6.6×` observation is also, in itself, a reportable result about instrumenting recursive LM systems: **usage that accrues on objects the orchestrator never holds a reference to is invisible to instance-level accounting**, and recursion is exactly the pattern that creates such objects.
