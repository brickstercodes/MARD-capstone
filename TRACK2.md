# Track 2 — Orchestration & Tier 2 Execution

**Parth Sangani** · [@parthparu](https://github.com/parthparu) · issues #11–#18

Local mirror of the GitHub board. GitHub is authoritative; this file is for
working offline and for seeing the whole track on one screen. Tick here as you
go, sync to GitHub when convenient.

**Last synced with GitHub:** 20 August 2026

---

## Where we are

| | |
|---|---|
| Today | **Thu 20 Aug 2026** |
| Nominal block | **W2** · Mon 17 – Sun 23 Aug · [#13](https://github.com/brickstercodes/MARD-capstone/issues/13) · **day 4 of 7** |
| Actually open | **W0** ([#11](https://github.com/brickstercodes/MARD-capstone/issues/11), closed 9 Aug) and **W1** ([#12](https://github.com/brickstercodes/MARD-capstone/issues/12), whole week passed, nothing built) |
| Next freeze | 🔒 **Feature freeze A · Sun 23 Aug — 3 days** — absolute |

**Read this before planning the week.** W0 closed 11 days ago and W1 passed
without a commit — `plan/` and `orchestrate/` are still bare `__init__.py`. W1
and W2 are both due Sunday, and Feature freeze A is absolute: after it, a change
to the pipeline invalidates every number measured before it.

Two things make this less bad than it reads, and one makes it worse.

- **Better:** the decisions that were blocking are all answered — spend cap,
  model pair, `eval/` naming, ablation scope (see below). And W1 needs no keys:
  `LocalREPL` + `MockLM` runs the whole REPL path offline.
- **Better:** the harness that Track 3 is blocked on has been delivered since
  3 Aug.
- **Worse:** W2's last box is *"end-to-end run completes on the primary
  document."* That needs `ingest/` (T4) and `envelope/` (T1), and **both are
  still empty on `main`.** No track has written pipeline code. This is not a
  Track 2 problem and cannot be solved inside Track 2 — escalate rather than
  absorb.

---

## W0 — [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) · Repo scaffolding, RLM library, API keys + spend cap, logging harness

Labelled `blocker`: **Track 3 cannot start W1 without the logging harness.**

### Definition of done

- [x] **Repo scaffolded** — package tree per CONTEXT.md §4.1, `pyproject.toml`,
      `.gitignore`, `README.md`, `CLAUDE.md`
- [x] **Pushed** — and **merged into `main` on 10 Aug** (`d6208b5`), together
      with Track 1's W0. `main` is no longer empty; a plain clone works.
- [x] **RLM library installed** (`github.com/alexzhang13/rlm`) — vendored as a
      working copy at `.vendor/rlm`, pinned to `72d6940`, installed as
      `rlms==0.1.3`. Evidence in `runs/_bootstrap/`, attached to #11.
      ⚠️ **The install silently broke on 4 Aug and was repaired on 20 Aug** — see
      "The editable-install trap" below. It is working again via a local
      `PYTHONPATH` workaround; the root cause is a process on this Mac, not the
      repo.
- [ ] **RLM examples run end-to-end** — 14 in `.vendor/rlm/examples`. 🚧
      **Blocked on the Vertex path, not broken.** Keys arrived 10 Aug but are
      unconfirmed here, and the examples target the direct-API `GeminiClient`
      that `docs/15`'s patch replaces — so this box needs both boxes above it
      first. All 14 surveyed and classified in
      `docs/RLM_BASELINE_SURVEY.md` §1. Five of them run on container or sandbox
      runtimes MARD does not use — recommend skipping; the local REPL is what we
      run on, and adopting Docker would be a change to CONTEXT.md §4.1's stack,
      not a detail.
      The useful part is the `MockLM` pattern those examples demonstrate:
      **verified 20 Aug that `LocalREPL` runs keyless** — code execution,
      `llm_query`, batched queries and recursive `rlm_query` — with no provider
      call and no container. That means W1's stub builder and W2's fork-join can
      be built and tested with zero API spend and zero rate-limit exposure.
      The distinguishability question is answered in §2 of that doc, and the
      answer turned out to matter for the paper: the base library's metadata
      flows **upward** and is observational, MARD's envelope flows **downward**
      and is operative. Verified in source, `rlm/core/rlm.py:824` and `:836`.
      There is a `root_prompt` slot that invites the objection *"you just used
      `root_prompt`"* — §2.3 has the rebuttal. **Track 1 needs this for O1.**
- [ ] **API keys provisioned** — service-account JSON sent directly by Anugrah on
      10 Aug. **Not yet confirmed working in this environment.** Set
      `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION=global`,
      `GOOGLE_APPLICATION_CREDENTIALS_JSON` in `.env` and run
      `python test_vertex_auth.py`. Use `global`, not `us-central1` — Anugrah hit
      a 404 there. Keys never enter this repo.
- [ ] **Vertex client patch re-applied locally** — `docs/15-…` →
      `.vendor/rlm/rlm/clients/gemini.py`. `.vendor/` is gitignored, so this did
      **not** arrive with the merge. Nothing real runs against either model until
      it is applied. `docs/12` §Consequences names this a Track 2 task, and its
      verification-debt item 2 — whether the port preserves upstream's
      retry/backend abstraction — is ours to close too.
- [x] **Rate-limit budget documented** — `docs/RATE_LIMIT_BUDGET.md`, updated
      20 Aug against the frozen pair. Demand side complete and now costed with
      real ablation numbers. Supply side is named but empty: **Vertex quotas are
      per-project and readable only from the GCP console**, so filling §2 needs
      the credential holder, not a decision. Do it before W3.
      One thing to settle: `docs/14` §4 and `docs/31` §A1 disagree by 12 runs on
      whether A1 counts separately from the vanilla control. Flagged in §6.
- [ ] **Spend cap set** — **the number arrived: `MARD_SPEND_CAP_USD=780`**
      (₹75,000 at ₹95.13/USD on 9 Aug, rounded down — `docs/14` §1).
      `SpendCap.from_env()` verified 20 Aug: it accepts 780 with provenance and
      still refuses when the var is unset. **All that remains is exporting it in
      an environment that persists** — it is not set anywhere yet, so the box
      stays open.
      Track 1 flags that the exchange rate goes stale on the same 30-day rule
      `RateCard` enforces, and W6 lands 29 days out: **re-read the rate before
      the matrix runs.**
- [x] **Logging harness captures envelope state, transcript, token count,
      config snapshot, seed** — `runlog/`, 9 core + 11 budget tests green,
      ruff and mypy clean
- [x] **Handoff sent to Track 3** — `docs/TRACK3_HANDOFF.md`, posted to #11 on
      3 Aug, [@FalseAdvertising](https://github.com/FalseAdvertising) mentioned
- [ ] **Track 3 has confirmed the harness meets their needs** — ⏳ **17 days,
      no reply on the harness.** Arav is not silent — he posted on 16 Aug that
      the BrowseComp-Plus (n=20) and OOLONG (n=50) subsets are frozen and
      hash-stamped (#19/#47) — he just has not answered this. The chase planned
      for 6 Aug never happened.
      He is now building against a harness he has not signed off on, and
      Feature freeze A is Sunday. Escalate at the gate rather than chasing
      again.

### The editable-install trap

Recorded because it cost sixteen days and will recur on any machine that does
the same thing.

`import rlm` died on **4 Aug** and nobody noticed until **20 Aug**. Something on
this Mac recursively re-applies the macOS hidden flag to everything under this
repo's dot-directories — `.venv`, `.vendor`, `.git`, the caches — within seconds
of it being cleared. CPython 3.14's `site.addpackage` **silently skips hidden
`.pth` files**, and both editable installs (`mard`, `rlms`) resolve through a
`.pth`. No warning, no error, exit code zero.

It survived sixteen days because **`pytest` puts the repo root on `sys.path`**, so
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
| ~~Compute / API budget ceiling~~ — **answered**, $780. #46 itself still has zero comments; Anugrah replied on #11 and in `docs/14` instead | — | done |
| Harness sign-off — sent 3 Aug, **17 days, still no reply on the harness**. Arav posted 16 Aug about the frozen eval subsets (#19/#47) but not this | Arav | [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) |
| API keys — JSON received 10 Aug, **not yet confirmed working here** | me | [#11](https://github.com/brickstercodes/MARD-capstone/issues/11) |
| ~~Model pair~~ — **answered**, `gemini-3.6-flash` / `gemini-3.1-flash-lite`, Vertex-only | — | done |
| ~~Depth sweep & ablation breadth~~ — **answered**; one 12-run arithmetic conflict left between `docs/14` §4 and `docs/31` §A1 | Track 1 | `docs/RATE_LIMIT_BUDGET.md` §6 |
| Vertex quotas for §2 of the rate-limit budget — needs GCP console access | me | before W3 |
| `ingest/` and `envelope/` — W2's end-to-end box cannot close without them | T4 / T1 | [#13](https://github.com/brickstercodes/MARD-capstone/issues/13) |

### Owed to others this block

| To | What | Why it matters |
|---|---|---|
| Track 3 (Arav) | Logging harness, working | Every number in both manuscripts passes through it — **delivered 3 Aug, still awaiting sign-off 17 days on** |

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

### Open question for Anugrah — closed

**Answered 9 Aug — `docs/14-W0_RESPONSES_TO_TRACK2.md` §3. Keep `eval/` as named.**
Matching CONTEXT.md §4.1's tree beats the builtin-shadowing risk, which is a lint
concern rather than a correctness one; renaming would churn `pyproject.toml`'s
`packages` list, the `eval` extras group, and whatever Track 3 is about to
import. Closed — do not raise it again.

The other three W0 asks were answered in the same document: the spend cap
(§1, $780), the model pair (§2), and the ablation scope (§4). Nothing Track 2
asked Track 1 in W0 is still open.

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
