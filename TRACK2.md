# Track 2 — Orchestration & Tier 2 Execution

**Parth Sangani** · [@parthparu](https://github.com/parthparu) · issues #11–#18

Local mirror of the GitHub board. GitHub is authoritative; this file is for
working offline and for seeing the whole track on one screen. Tick here as you
go, sync to GitHub when convenient.

**Last synced with GitHub:** 8 August 2026

---

## Where we are

| | |
|---|---|
| Block | **W0** · Wed 29 Jul – **Sun 9 Aug** |
| Days left | **1** |
| Milestone | W0, due 9 Aug |
| Next freeze | 🔒 **Feature freeze A · Sun 23 Aug** — absolute |
| Current issue | [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) · status **Ready** · labelled `blocker` |

**Overdue as of 8 Aug:** the Thu 6 Aug chase to Arav did not happen and there is
still no reply on #11 since the 3 Aug handoff. The question to Anugrah has never
been asked — [#46](https://github.com/brickstercodes/MARD-capstone/issues/46) has
zero comments. Both are one message each and both gate a W0 box.

---

## W0 — [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) · Repo scaffolding, RLM library, API keys + spend cap, logging harness

Labelled `blocker`: **Track 3 cannot start W1 without the logging harness.**

### Definition of done

- [x] **Repo scaffolded** — package tree per CONTEXT.md §4.1, `pyproject.toml`,
      `.gitignore`, `README.md`, `CLAUDE.md`
- [x] **Pushed** — `track2/w0-scaffolding-runlog`, 2 commits (`1cf2118`,
      `eaaedd4`). **`main` is still empty** — merge before anyone clones without
      naming the branch.
- [x] **RLM library installed** (`github.com/alexzhang13/rlm`) — vendored as a
      working copy at `.vendor/rlm`, pinned to `72d6940`, installed as
      `rlms==0.1.3`. Evidence in `runs/_bootstrap/`, attached to #11.
      ⚠️ **The install silently broke on 4 Aug and was repaired on 8 Aug** — see
      "The editable-install trap" below. It is working again via a local
      `PYTHONPATH` workaround; the root cause is a process on this Mac, not the
      repo.
- [ ] **RLM examples run end-to-end** — 14 in `.vendor/rlm/examples`. 🚧
      **Blocked on keys, not broken.** All 14 surveyed and classified in
      `docs/RLM_BASELINE_SURVEY.md` §1. Five of them run on container or sandbox
      runtimes MARD does not use — recommend skipping; the local REPL is what we
      run on, and adopting Docker would be a change to CONTEXT.md §4.1's stack,
      not a detail.
      The useful part is the `MockLM` pattern those examples demonstrate:
      **verified on 8 Aug that `LocalREPL` runs keyless** — code execution,
      `llm_query`, batched queries and recursive `rlm_query` — with no provider
      call and no container. That means W1's stub builder and W2's fork-join can
      be built and tested with zero API spend and zero rate-limit exposure.
      The distinguishability question is answered in §2 of that doc, and the
      answer turned out to matter for the paper: the base library's metadata
      flows **upward** and is observational, MARD's envelope flows **downward**
      and is operative. Verified in source, `rlm/core/rlm.py:824` and `:836`.
      There is a `root_prompt` slot that invites the objection *"you just used
      `root_prompt`"* — §2.3 has the rebuttal. **Track 1 needs this for O1.**
- [ ] **API keys provisioned** — yours to do; keys never enter this repo
- [x] **Rate-limit budget documented** — `docs/RATE_LIMIT_BUDGET.md`. Demand side
      derived and complete; supply side is a specified-but-empty table, because
      provider limits are per-account and per-tier and there is no honest number
      to write before keys exist and #44 lands. **Fill it before W3, not W6.**
      Two open questions surfaced that change the W6 run count materially —
      whether the depth sweep sits inside the ablation grid, and whether
      ablations run on all 4 documents. Both are Track 1/3 calls; see §6 of the
      doc.
- [ ] **Spend cap set** — 🚧 blocked on the number, but the *mechanism* is built:
      `SpendCap.from_env()` reads `MARD_SPEND_CAP_USD` and **refuses to run
      without it**. When Anugrah answers, it is one `export`, not new code.
- [x] **Logging harness captures envelope state, transcript, token count,
      config snapshot, seed** — `runlog/`, 9 core + 11 budget tests green,
      ruff and mypy clean
- [x] **Handoff sent to Track 3** — `docs/TRACK3_HANDOFF.md`, posted to #11 on
      3 Aug, [@FalseAdvertising](https://github.com/FalseAdvertising) mentioned
- [ ] **Track 3 has confirmed the harness meets their needs** — ⏳ still nothing
      from Arav as of 8 Aug. **The Thu 6 Aug chase did not happen.** Five days
      of silence on a `blocker` box with one day left. Chase today; if there is
      no reply by the 9th, raise it at the Friday gate rather than carrying it
      quietly into W1.

### The editable-install trap

Recorded because it cost a day and will recur on any machine that does the same
thing.

`import rlm` died on **4 Aug** and nobody noticed until **8 Aug**. Something on
this Mac recursively re-applies the macOS hidden flag to everything under this
repo's dot-directories — `.venv`, `.vendor`, `.git`, the caches — within seconds
of it being cleared. CPython 3.14's `site.addpackage` **silently skips hidden
`.pth` files**, and both editable installs (`mard`, `rlms`) resolve through a
`.pth`. No warning, no error, exit code zero.

It survived four days because **`pytest` puts the repo root on `sys.path`**, so
all 20 tests passed and `./scripts/check.sh` stayed green while the install was
dead for anything run from another directory. Arav would have hit it on his first
script outside the repo root.

- **Guarded** — `scripts/check.sh` now imports `rlm` and `runlog` from `/` before
  it lints, and `scripts/bootstrap_rlm.sh` does its import check from `/` too.
  Testing an install from the directory that supplies the package proves nothing.
- **Worked around locally** — `PYTHONPATH` in `.venv/bin/activate`, which bypasses
  `.pth` entirely. Gitignored, so it does not reach anyone else.
- **Not fixed** — the process setting the flag is still unidentified. No folder
  action, no crontab, no `WatchPaths` agent, no login item. Next step is
  `sudo fs_usage -w -f filesys | grep -i chflags` while clearing the flag in
  another terminal.

Note the workaround defeats the guard *on this machine* — `PYTHONPATH` satisfies
the import probe. On a normal clone the guard still does its job.

### Blocked on

| What | Who | Ticket |
|---|---|---|
| Compute / API budget ceiling — the spend cap needs a number. **Never asked — #46 has zero comments.** | Anugrah | [#46](https://github.com/brickstercodes/MARD-capstone/issues/46) |
| Harness sign-off — sent 3 Aug, no reply in 5 days, wanted before 9 Aug | Arav | [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) |
| API keys — 12 of the 14 examples need them | me | [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) |
| Model pair — the rate-limit table cannot name a tier's limits without it | Anugrah | [#44](https://github.com/brickstercodes/MARD-capstone/issues/44) |
| Depth sweep & ablation breadth — changes the W6 run count by ~27 runs | Track 1 / Track 3 | `docs/RATE_LIMIT_BUDGET.md` §1.2 |

### Owed to others this block

| To | What | Why it matters |
|---|---|---|
| Track 3 (Arav) | Logging harness, working, by 9 Aug | Every number in both manuscripts passes through it — **delivered 3 Aug, awaiting sign-off** |

### What `runlog/` already does

| File | Purpose |
|---|---|
| `runlog/run.py` | `RunLogger` — one directory per run, written as it happens |
| `runlog/config.py` | Config snapshot: git SHA + dirty flag, package versions, platform |
| `runlog/seeds.py` | `seed_everything`, `CAMPAIGN_SEEDS = (11, 23, 42)` |
| `runlog/pricing.py` | `RateCard` / `ModelRate` with provenance; stale rates refused |
| `runlog/budget.py` | `SpendCap` + `SpendLedger` — campaign ceiling, risk #5 |
| `scripts/bootstrap_rlm.sh` | Clone, install and evidence the RLM base library |
| `scripts/check.sh` | ruff format · ruff check · mypy · pytest; refuses to run outside the venv |
| `docs/TRACK3_HANDOFF.md` | What Arav needs to sign off on #11 |
| `docs/RATE_LIMIT_BUDGET.md` | Requests/min the campaign needs vs what providers give; concurrency and retry policy |
| `docs/RLM_BASELINE_SURVEY.md` | All 14 examples classified; **what the base library already does and where MARD begins** |
| `tests/` | 20 tests, failure-mode focused |

Three deliberate behaviours worth knowing before you rely on it:

- A crashed run still writes `summary.json` with `status: "failed"` and the
  traceback. W3 and W6 runs die from rate limits; a hole in the matrix should
  explain itself.
- JSONL flushes per line, and `load_run` skips a truncated final record. A
  killed process leaves usable data.
- Cost is `null`, never `0.0`, when a model has no recorded rate. Rates carry
  `retrieved_on` + provider URL and expire after 30 days.

The spend ledger writes atomically (temp file + `os.replace`). A plain write
truncates before it fills, and a concurrent reader during the W6 matrix got a
JSON decode error — a crash in the one component whose job is to stop crashes
from costing money. Caught by the 60-writer/10-reader test.

### Open question for Anugrah

`eval/` shadows the Python builtin `eval`. Kept as-is to match CONTEXT.md §4.1
so the tree matches the document everyone navigates by. Rename to `evaluation/`
now if we're going to — after Track 3 starts importing it, it stops being free.

**Still unasked as of 8 Aug** — five days later, and W1 starts Monday. Send it
with #46 in one message; both are his, and the rename window closes the moment
Arav starts building against the tree. A draft is ready in
`docs/drafts/` — it needs sending, not writing.

---

## The rest of the track

### W1 · Mon 10 – Sun 16 Aug — [#12](https://github.com/brickstercodes/MARD-capstone/issues/12)

Master Plan Pydantic schema · loud-failing validation at the tier boundary ·
**stub Tier 2 builder consuming a hand-written plan**

- [ ] `plan/` Pydantic models — concept graph, ordered study sequence, rationale
- [ ] Validation that fails loudly rather than passing a malformed plan to N builders
- [ ] Stub builder that eats a hand-written plan

> The stub is the point: it fixes the contract before Track 1 can generate a real
> plan, so you are never blocked waiting on the envelope.

### W2 · Mon 17 – Sun 23 Aug — [#13](https://github.com/brickstercodes/MARD-capstone/issues/13)

asyncio bounded worker pool · fork-join · per-builder retry · failure isolation ·
provenance pointers on every generated span · join in Master Plan order

- [ ] Bounded worker pool
- [ ] Fork-join with wall-clock = max(builder), not Σ
- [ ] Per-builder retry and failure isolation
- [ ] Provenance pointer on every generated span
- [ ] Join respects Master Plan order, not book order

🔒 **Feature freeze A · Sun 23 Aug.** After this, a change to the pipeline
invalidates every number measured before it.

### W3 · Mon 24 – Thu 27 Aug — [#14](https://github.com/brickstercodes/MARD-capstone/issues/14)

Keep runs alive through Manuscript A measurement week. Effectively full-time.

**4 days, compressed from 7, with no recovery room.** A run that fails Wed 26 Aug
ships an incomplete matrix in Manuscript A.

🔒 **Results freeze A · Thu 27 Aug.**

### W4 · Fri 28 Aug – Thu 3 Sep — [#15](https://github.com/brickstercodes/MARD-capstone/issues/15)

Architecture and pipeline figures for Manuscript A · reproducibility notes

🚀 **Manuscript A submission-ready · Thu 3 Sep.** W4 overlaps W5 — you start
Phase B on Mon 31 Aug.

### W5 · Mon 31 Aug – Sun 6 Sep — [#16](https://github.com/brickstercodes/MARD-capstone/issues/16)

Scale the orchestrator to 4 documents: concurrency, seed plumbing, resumable
runs, cost telemetry per run

- [ ] Concurrent runs across 4 documents
- [ ] Seed plumbing (3 seeds, every number)
- [ ] Resumable runs — W6 is compute-bound and runs will die
- [ ] Cost telemetry per run

### W6 · Mon 7 – Sun 13 Sep — [#17](https://github.com/brickstercodes/MARD-capstone/issues/17)

Keep the full matrix alive: 4 docs × 5 systems × 3 seeds + ablation grid.
The week the orchestrator earns its keep.

🔒 **Feature freeze B · Sun 13 Sep.**

### W7–W9 · Mon 14 – Wed 30 Sep — [#18](https://github.com/brickstercodes/MARD-capstone/issues/18)

Deterministic replay verification · code cleanup · public artefact · figures for
Manuscript B · reproducibility appendix

🔒 **Results freeze B · Sun 20 Sep** · 🚀 **Manuscript B ready · Wed 30 Sep**

---

## Standing rules that bite this track

- **Feature freezes are absolute.** Cut features, never the freeze. After a
  freeze, a "small fix" is a re-run of the entire matrix.
- **Every run logged** — envelope state, transcripts, token counts, config
  snapshot, seed. A number you cannot reproduce on 29 Sep is not a number.
- **3 seeds on every number, variance reported.** Non-negotiable.
- **Daily 15-min standup. Friday 45-min gate review.** A missed gate is escalated
  the same day, not the next week.

## People

| Track | Person | GitHub |
|---|---|---|
| T1 · MARD core & paper lead | Anugrah Shetty | @brickstercodes |
| **T2 · Orchestration** | **Parth Sangani** | **@parthparu** |
| T3 · Evaluation harness | Arav Sharma | @FalseAdvertising |
| T4 · Corpus & manuscript production | Tanish Sharma | @Tanz101-tech |

Guide: Dr. Soni Sweta, Computer Engineering Department, MPSTME.
