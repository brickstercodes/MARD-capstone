# Rate-limit budget

**Owner:** Track 2 (Parth Sangani, @parthparu) · **Closes:** the *"rate-limit
budget documented"* box on [#11](https://github.com/brickstercodes/MARD-capstone/issues/11)
· **Reviewed:** every Friday gate review

Risk #5 in CONTEXT.md §3.7 is *"API cost or rate limits throttle W6."* The spend
half of that risk is enforced in code by `runlog.SpendCap`. This document is the
other half: how many **requests per minute** the campaign needs, how many the
providers will give us, and what the orchestrator does when those two numbers
disagree.

They are genuinely different failure modes. A spend breach stops the campaign and
you notice immediately. A rate-limit breach degrades it silently — retries
inflate wall-clock, a run dies at hour six of a matrix, and the hole in the table
gets discovered on the day the manuscript is due.

> **Status.** The demand side below is derived and stands on its own. The supply
> side cannot be filled in until API keys exist and the model pair is decided
> ([#44](https://github.com/brickstercodes/MARD-capstone/issues/44)) — provider
> limits are per-account and per-tier, so there is no honest number to write yet.
> The table is specified, not populated. Populating it is one sitting once keys
> land, and it must happen **before W3**, not before W6.

---

## 1. Demand — how much traffic the campaign actually generates

### 1.1 Runs

Both figures come straight from CONTEXT.md §2.1 and §3.3.

| Campaign | Composition | Runs |
|---|---|---|
| **Manuscript A** (W3, 24–27 Aug) | 1 document · MARD vs vanilla RLM · negative control on flat context · 1 ablation · 3 seeds | ~15 |
| **Manuscript B** (W6, 7–13 Sep) | 4 documents × 5 systems × 3 seeds | **60** |
| **B, ablations** | see §1.2 — count is not yet determined | 36+ |

The 5 systems are 4 baselines + MARD (§2.2 item 2): full-context, naive chunking,
embedding RAG, vanilla RLM, MARD.

### 1.2 Two open questions that change the run count materially

Both are Track 1/Track 3 calls, not mine, and both are cheap to answer now and
expensive to answer in W6.

1. **Is the depth sweep inside the ablation grid or beside it?** §2.1 lists the
   grid as *"envelope removed · plan withheld from Tier 2 · reordering disabled ·
   depth swept"* — four items. §3.3's W6 row says *"the ablation grid **and**
   depth sweep"* — two things. If the sweep is separate and has *k* depth
   settings, that is an extra *k* × documents × seeds runs that nothing has
   budgeted for.
2. **Do ablations run on all 4 documents or a subset?** Nothing in CONTEXT.md
   says. All four gives 3 × 4 × 3 = 36 runs; one document gives 9. The
   difference is 27 runs of frontier-model traffic in the tightest week.

Raised with Track 1 — see §6.

### 1.3 Requests per run

This is the number that actually meets the rate limit, and it is **not one
request per run**. For MARD:

```
requests(MARD run) = 1        Pass 0, skeleton extraction
                   + C        Pass 1, one enriched exploration per chapter
                   + D        Pass 2+, targeted deep dives
                   + N        Tier 2 builders, fork-join, concurrent
```

`C`, `D` and `N` are document-dependent and none of them is known yet. `N` is the
one that bites: Tier 2 is *N builders in parallel on a cheap model* (§1.1), so a
single MARD run issues a burst of concurrent requests, not a stream of sequential
ones. Ten concurrent runs each forking twelve builders is 120 simultaneous
requests from what the run log will cheerfully record as "ten runs."

**These constants get measured, not guessed.** `runlog` already records
`calls_issued` per run, so W1's first end-to-end MARD run and W2's fork-join work
produce them for free. Pin them in the table below before W3 and re-derive §2's
concurrency ceiling from them.

| System | Requests per run | Binding limit | Measured |
|---|---|---|---|
| Full-context | 1 | **tokens**/min — one enormous prompt | — |
| Naive chunking | ⌈doc_tokens / chunk_size⌉ | requests/min | — |
| Embedding RAG | E embeddings (once per document, cache it) + k + 1 | separate embedding-endpoint limit | — |
| Vanilla RLM | recursive, unbounded a priori | requests/min | — |
| MARD | 1 + C + D + N, bursty at Tier 2 | requests/min | — |

Two consequences worth stating plainly, because they rule out the obvious design:

- **A single global concurrency number is wrong.** Full-context saturates a
  token-per-minute quota with one call; MARD Tier 2 saturates a request-per-minute
  quota while barely touching tokens. Sizing one number for both means throttling
  MARD to protect a limit it was never going to hit.
- **Embedding RAG draws on a different quota entirely.** Its index-time
  embeddings are a separate endpoint with separate limits, and they are computed
  once per document, not once per run. Cache them to disk under `runs/` or pay
  for them 15 times.

### 1.4 The lever that makes this tractable

CONTEXT.md §3.7 risk #5 and §4.1's tech stack both call for **vLLM + open weights
(incl. `RLM-Qwen3-8B`) for ablation sweeps without API spend.** Taken seriously,
that moves the entire ablation grid — the largest and least certain block in
§1.1 — off the API rate limit and onto local compute, where the constraint is GPU
hours rather than a provider's quota.

That is the single biggest decision available here, and it is Track 2's to make
and Track 3's to live with. It should be settled before W5, because it changes
what "resumable runs" has to mean.

---

## 2. Supply — what the providers will give us

**Unfillable until keys are provisioned.** Limits are per-account, per-tier and
change with spend history; there is no number that is honest to write today.

The discipline is the same one `runlog.pricing.RateCard` already enforces for
prices, for the same reason — §4.3 rule 4, and the "15–25× cost reduction" claim
that died with the rate it rested on:

- The number comes from **the provider's own dashboard or docs**, not from an
  aggregator, not from a blog, not from memory.
- It is recorded with the **date read** and the **URL**.
- It is re-checked when it is more than 30 days old. W0 → W6 is five weeks, so
  whatever gets written here in August **must be re-read in September**.

| Provider | Model / endpoint | Requests/min | Tokens/min | Concurrency | Read on | Source |
|---|---|---|---|---|---|---|
| — | frontier tier (Tier 1 root) | — | — | — | — | — |
| — | budget tier (Tier 2 builders) | — | — | — | — | — |
| — | embeddings (RAG baseline) | — | — | — | — | — |
| local | vLLM / open weights | n/a | n/a | GPU-bound | — | — |

Models are named **only at selection time** (§2.3 — named 2024-era models are a
dead claim). Until #44 lands, these rows stay "frontier tier" and "budget tier".

---

## 3. Policy — what the orchestrator does about it

These are Track 2 decisions. They are not in CLAUDE.md's escalate-to-Anugrah
list, so they are made here, with reasons, and are changeable on evidence.

**Ceiling per model pool, not per campaign.** The bounded worker pool built in W2
takes a concurrency limit *per pool* — frontier, budget, embeddings — because
§1.3 shows they hit different quotas. One global semaphore is the design that
looks simpler in W2 and throttles the wrong thing in W6.

**Run at ≤ 70% of the measured per-minute ceiling.** Retries draw from the same
bucket as first attempts, so a pool sized at 100% converts a transient 429 into a
retry storm that sustains itself. 70% leaves room for the retries a long run will
certainly need. This is deliberately stricter than the 0.75 spend warning in
`runlog.budget` — that one is a warning, this one is a hard ceiling.

**A 429 is data, not noise.** Rate-limit responses get logged into the run record
with their timestamp and `Retry-After`, not swallowed by the retry wrapper. Two
reasons: the W6 post-mortem needs to distinguish "the provider throttled us" from
"our code is slow", and the reproducibility appendix in W7–W9 has to explain why
wall-clock varies across seeds.

**Honour `Retry-After`; exponential backoff with jitter otherwise.** Without
jitter, N builders that fork together get throttled together and retry together,
which reproduces the burst that caused the throttle.

**Bounded attempts, then fail the run loudly.** `runlog` already writes
`summary.json` with `status: "failed"` and the traceback on a crashed run, so a
hole in the matrix explains itself. Infinite retry against a hard quota burns
wall-clock in the week that has none.

**Nobody raises a ceiling mid-campaign to make a run finish.** Same rule as the
spend cap. After Feature freeze B (Sun 13 Sep) it is also a results problem, not
just a courtesy one — changing concurrency changes timing, and timing is a
measured number in the O6 cost model.

---

## 4. When it is checked

| When | What |
|---|---|
| On key provisioning | Fill §2 from the provider dashboards. Record date + URL. |
| End of W1 | First real `calls_issued` numbers. Fill the `Measured` column in §1.3. |
| End of W2 | Pool ceilings derived from §1.3 × 0.70 and set in config. |
| **Before W3** | §1.3 and §2 both populated. A/B measurement weeks do not start against an unmeasured quota. |
| Every Friday | Gate review: 429 count from the week's run logs, alongside the spend-ledger status. |
| Start of W6 | Re-read §2 — the August numbers are past `MAX_RATE_AGE` by then. |

---

## 5. What is not covered here

- **Dollars.** `runlog.budget.SpendCap` / `SpendLedger`, ceiling pending
  [#46](https://github.com/brickstercodes/MARD-capstone/issues/46).
- **Which models.** [#44](https://github.com/brickstercodes/MARD-capstone/issues/44),
  Anugrah's call.
- **GPU capacity for the vLLM path.** Not costed anywhere yet. If §1.4 is adopted,
  it needs an owner.

## 6. Asks

| # | Ask | Who | By |
|---|---|---|---|
| 1 | Resolve §1.2 — is the depth sweep inside the ablation grid, and how many documents do ablations run on? | Track 1 / Track 3 | before W5 |
| 2 | Confirm §1.4 — ablations on local open weights rather than API | Track 3 | before W5 |
| 3 | Keys, so §2 can be populated | me | before W3 |
