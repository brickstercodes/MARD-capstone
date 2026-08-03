# Handoff: run logging harness — Track 2 → Track 3

**For:** Arav Sharma (@FalseAdvertising) · **From:** Parth Sangani (@parthparu)
**Unblocks:** the last checkbox on [#11](https://github.com/brickstercodes/MARD-capstone/issues/11)
— *"Track 3 has confirmed the harness meets their needs"*

`runlog/` is ready. It captures the five things CONTEXT.md §3.4 requires of every
run — envelope state, transcripts, token counts, config snapshot, seed — plus
cost accounting and a campaign spend ledger. Please read this, try it against
one of your scorers, and either sign off on #11 or tell me what's missing.
**Say so before 9 Aug** — after that it's changes during a week you need it working.

## 30-second version

```python
from runlog import RunLogger, CAMPAIGN_SEEDS

with RunLogger.start(
    runs_root="runs",
    system="vanilla_rlm",          # your control
    document_id="ostep",
    seed=CAMPAIGN_SEEDS[0],        # (11, 23, 42)
    models={"root": "<frontier>"},
) as run:
    call_id = run.log_call(
        role="root", model="<frontier>",
        prompt=prompt, response=response,
        input_tokens=n_in, output_tokens=n_out, depth=0,
    )
    run.log_call(..., depth=1, parent_call_id=call_id)
    run.set_result({"task_score": score})
```

Read it back for your per-number audit (#23, #27):

```python
from runlog import load_run
r = load_run("runs/20260802T081500__vanilla_rlm__ostep__s11__a1b2c3")
r["summary"]["totals"]["input_tokens"]
r["calls"]          # full transcripts, with depth and parent_call_id
r["envelopes"]      # {} for vanilla, populated for MARD
```

## What lands on disk

```
runs/<run_id>/
├── manifest.json      config snapshot: git SHA + dirty flag, package versions,
│                      platform, python, models, params, seeding report
├── calls.jsonl        one record per model call — prompt, response, tokens,
│                      latency, depth, parent_call_id
├── events.jsonl       retries, validation failures, joins
├── envelope/pass_N.json
├── artefacts/         Master Plan, joined output, anything you want scored
└── summary.json       status, wall clock, per-model totals, cost, your result
```

`run_id` is `<UTC timestamp>__<system>__<document>__s<seed>__<uuid6>` — sortable,
greppable, and collision-safe under the concurrent W6 matrix.

## Four things you should know before you rely on it

**1. A crashed run still writes `summary.json`.** Status is `"failed"` with the
exception type, message and traceback, and the calls made before the crash are
still counted. Your matrix will have holes in W3 and W6; this makes each hole
explain itself instead of just being absent.

**2. Cost is `null`, never `0.0`, when a model has no rate.** `summary.json`
carries `unpriced_models` so an unpriced run cannot be silently averaged in as
free. Rates go in a `RateCard`:

```python
from datetime import date
from runlog import ModelRate, RateCard

card = RateCard.empty().with_rate(ModelRate(
    model="<frontier>",
    input_per_million=..., output_per_million=..., currency="USD",
    retrieved_on=date(2026, 9, 7),                    # the day you read it
    source_url="https://<provider>/pricing",          # provider's own page
))
```

A rate older than 30 days raises `StaleRateError` rather than quietly ageing into
a table. That's §4.3 rule 4 in code — it's verification debt item 7, and it's
yours.

**3. JSONL is flushed per line**, and `load_run` skips a truncated final record.
A killed process leaves readable data.

**4. Seeding is one call and it reports what it actually seeded.** `manifest.json`
distinguishes "numpy was seeded" from "numpy wasn't installed", so a variance
result can't rest on an unseeded library. Note `sampling_params_for(seed)` for
the provider side — local seeding does nothing to a hosted model, which is part
of why we report variance rather than assume determinism.

## Spend ledger

Cumulative cost across a campaign, for risk #5:

```python
from runlog import SpendCap, SpendLedger
ledger = SpendLedger("runs", SpendCap.from_env())   # MARD_SPEND_CAP_USD
ledger.check_before_run(estimated_usd)              # raises BudgetExceededError
ledger.record(summary)                              # after each run
ledger.status()                                     # warns at 75%
```

`SpendCap.from_env()` **refuses to run without an explicit ceiling** — no default,
because the number is Anugrah's call ([#46](https://github.com/brickstercodes/MARD-capstone/issues/46),
still open). Unpriced runs are listed in `uncounted_runs` rather than counted as zero.

## Sign-off checklist

- [ ] `pip install -e ".[dev]"` then `./scripts/check.sh` passes on your machine
- [ ] You can wrap one baseline in `RunLogger` without contorting your code
- [ ] `load_run` gives you everything a per-number audit needs
- [ ] Token accounting matches what your provider reports for the same call
- [ ] The 3-seed loop plumbs through the way you expect
- [ ] Anything you need that isn't here — tell me now, not in W3

## Two requests back

1. **Fix and freeze your BrowseComp-Plus and OOLONG subsets in writing** (#19) and
   put the file in the repo, so the run manifest can reference the subset by name
   rather than by description.
2. **Tell me what identifies a run for you.** Right now `params` is a free-form
   dict. If depth, chunk size or top-k need to be first-class so your tables can
   group on them, easier to change now than after the freeze.
