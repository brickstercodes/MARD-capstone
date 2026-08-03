# Track 2 — Orchestration & Tier 2 Execution

**Parth Sangani** · [@parthparu](https://github.com/parthparu) · issues #11–#18

Local mirror of the GitHub board. GitHub is authoritative; this file is for
working offline and for seeing the whole track on one screen. Tick here as you
go, sync to GitHub when convenient.

**Last synced with GitHub:** 2 August 2026

---

## Where we are

| | |
|---|---|
| Block | **W0** · Wed 29 Jul – **Sun 9 Aug** |
| Days left | 7 |
| Milestone | W0, due 9 Aug |
| Next freeze | 🔒 **Feature freeze A · Sun 23 Aug** — absolute |
| Current issue | [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) · status **Ready** · labelled `blocker` |

---

## W0 — [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) · Repo scaffolding, RLM library, API keys + spend cap, logging harness

Labelled `blocker`: **Track 3 cannot start W1 without the logging harness.**

### Definition of done

- [x] **Repo scaffolded** — package tree per CONTEXT.md §4.1, `pyproject.toml`,
      `.gitignore`, `README.md`, `CLAUDE.md`
- [ ] **Pushed** — nothing has been committed yet; repo still has zero commits
- [ ] **RLM library installed and running its own examples end-to-end**
      (`github.com/alexzhang13/rlm`) — 👉 **run `./scripts/bootstrap_rlm.sh`**;
      it clones, installs, records the commit SHA and tees evidence to
      `runs/_bootstrap/`. Needs a machine with network, so it has to be yours.
- [ ] **API keys provisioned** — yours to do; keys never enter this repo
- [ ] **Rate-limit budget documented**
- [ ] **Spend cap set** — 🚧 blocked on the number, but the *mechanism* is built:
      `SpendCap.from_env()` reads `MARD_SPEND_CAP_USD` and **refuses to run
      without it**. When Anugrah answers, it is one `export`, not new code.
- [x] **Logging harness captures envelope state, transcript, token count,
      config snapshot, seed** — `runlog/`, 9/9 core + 9/9 budget tests green
- [ ] **Track 3 has confirmed the harness meets their needs** — 👉 send Arav
      ([@FalseAdvertising](https://github.com/FalseAdvertising))
      `docs/TRACK3_HANDOFF.md`; it ends in a sign-off checklist. Ask for a reply
      **before 9 Aug** — after that, changes land in a week he needs it working.

### Blocked on

| What | Who | Ticket |
|---|---|---|
| Compute / API budget ceiling — the spend cap needs a number | Anugrah | [#46](https://github.com/brickstercodes/MARD-capstone/issues/46) |

### Owed to others this block

| To | What | Why it matters |
|---|---|---|
| Track 3 (Arav) | Logging harness, working, by 9 Aug | Every number in both manuscripts passes through it |

### What `runlog/` already does

| File | Purpose |
|---|---|
| `runlog/run.py` | `RunLogger` — one directory per run, written as it happens |
| `runlog/config.py` | Config snapshot: git SHA + dirty flag, package versions, platform |
| `runlog/seeds.py` | `seed_everything`, `CAMPAIGN_SEEDS = (11, 23, 42)` |
| `runlog/pricing.py` | `RateCard` / `ModelRate` with provenance; stale rates refused |
| `runlog/budget.py` | `SpendCap` + `SpendLedger` — campaign ceiling, risk #5 |
| `scripts/bootstrap_rlm.sh` | Clone, install and evidence the RLM base library |
| `scripts/check.sh` | ruff format · ruff check · mypy · pytest |
| `docs/TRACK3_HANDOFF.md` | What Arav needs to sign off on #11 |
| `tests/` | 18 tests, failure-mode focused |

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
