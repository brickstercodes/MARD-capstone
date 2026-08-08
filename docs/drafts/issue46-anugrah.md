# DRAFT — comment for #46, to Anugrah

**Not sent.** Post to
[#46](https://github.com/brickstercodes/MARD-capstone/issues/46) after review.
Four asks in one message because they are all his and W1 starts Monday; the
ordering is by how expensive each becomes if it slips.

---

@brickstercodes — four decisions, all yours, all needed before W1 starts Monday.
Bundled into one message rather than four tickets because they are one
conversation.

**1 · The budget ceiling (this issue).** Track 2's spend cap is built and
refuses to run without an explicit number — `SpendCap.from_env()` reads
`MARD_SPEND_CAP_USD` and raises if it is unset. No default, deliberately: a
"sensible" default here is exactly the invented decision CONTEXT.md §0.3 rule 3
warns about, and a budget control that fails silently is worse than none.

So this is one `export`, not new code. **What is the number?**

If it helps to answer in the right shape: I need a **campaign ceiling in USD**
covering W3 and W6 together, not a monthly figure. W6 alone is 4 docs × 5 systems
× 3 seeds = 60 runs before ablations.

**2 · The model pair (#44).** Blocking in a way I did not expect. I wrote the
rate-limit budget this week (`docs/RATE_LIMIT_BUDGET.md`) and the supply half of
it cannot be filled in at all without knowing which providers we are on —
rate limits are per-account and per-tier, so there is no honest number to write.
That table has to be populated **before W3**, not before W6, because W3 is a
measurement week and it should not start against an unmeasured quota.

**3 · `eval/` shadows the Python builtin `eval`.** I kept the name to match
CONTEXT.md §4.1 so the tree matches the document everyone navigates by. If we are
going to rename it to `evaluation/`, it has to be now — the window closes the
moment Arav starts importing it, and he starts in W1. **Rename, or keep and stop
asking?** Either answer is fine; I just need it before Monday.

**4 · One ambiguity in the ablation scope, as Track 1.** CONTEXT.md contradicts
itself slightly and it changes the W6 run count materially:

- §2.1 lists the ablation grid as *"envelope removed · plan withheld from Tier 2
  · reordering disabled · depth swept"* — four items, sweep included.
- §3.3's W6 row says *"the ablation grid **and** depth sweep"* — two separate
  things.

If the sweep is separate with *k* settings, that is an extra *k* × docs × seeds
runs nobody has budgeted. Related: **do ablations run on all 4 documents or a
subset?** All four is 36 runs, one document is 9 — a 27-run difference in the
tightest week of the calendar, on the frontier model.

I do not need this by Monday, but I do need it before W5, and it is cheap to
answer now.

---

Everything else on [#11](https://github.com/brickstercodes/MARD-capstone/issues/11)
that is mine is done or is waiting on keys. Details in this week's sync on
TRACK2.md.
