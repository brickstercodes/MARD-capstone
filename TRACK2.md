# Track 2 — Orchestration & Tier 2 Execution

**Parth Sangani** · [@parthparu](https://github.com/parthparu) · issues #11–#18

Local mirror of the GitHub board. GitHub is authoritative; this file is for
working offline and for seeing the whole track on one screen. Tick here as you
go, sync to GitHub when convenient.

**Last synced with GitHub:** 22 August 2026

---

## Where we are

| | |
|---|---|
| Today | **Sat 22 Aug 2026** |
| Nominal block | **W2** · Mon 17 – Sun 23 Aug · [#13](https://github.com/brickstercodes/MARD-capstone/issues/13) · **day 6 of 7** |
| Actually open | **W2** ([#13](https://github.com/brickstercodes/MARD-capstone/issues/13)) — W1 ([#12](https://github.com/brickstercodes/MARD-capstone/issues/12)) delivered 20 Aug, nine days late |
| Next freeze | 🔒 **Feature freeze A · Sun 23 Aug — tomorrow** — absolute |

**Read this before planning the week.** W1 landed on 20 Aug, nine days late but
complete: `plan/` and `orchestrate/` are real, 87 tests pass, `check.sh` is
green, and it is up as [#48](https://github.com/brickstercodes/MARD-capstone/pull/48).
W2 is due tomorrow alongside Feature freeze A, which is absolute — after it, a
change to the pipeline invalidates every number measured before it.

**As of 22 Aug, #48 has no review and no comment.** Arav's [#47](https://github.com/brickstercodes/MARD-capstone/pull/47)
merged on 21 Aug with zero reviews, so work does land here — it just lands
unreviewed. Chase the merge rather than waiting for a review that is not coming.

- **W2's remaining work is Track 2's own:** bounded worker pool, per-builder
  retry, failure isolation. The `Builder` interface is already async and the
  join is already order-preserving, so the pool goes in underneath without
  changing callers.
- **W2's last box cannot close this week.** It is *"end-to-end run completes on
  the primary document,"* which needs `ingest/` (T4) and `envelope/` (T1). As of
  **22 Aug, the day before the freeze**, `envelope/__init__.py` is 282 bytes and
  `ingest/__init__.py` is 334 bytes — both still bare docstrings, and **T4 has
  never committed to this repo.** Commits on all branches in the last seven days:
  nine from Track 2, one from Track 3, none from Track 1 or Track 4. Not a Track 2
  problem and not solvable inside Track 2 — escalate rather than absorb.
  **The freeze and the missing pipeline cannot both hold**; that is Anugrah's call
  and it needs making today, not at Friday's gate review.
- **Two things other tracks have to agree to**, both introduced by the schema
  and neither inferable from CONTEXT.md:
  - T4: `SourceSpan` needs `section_id`, `book_position`, `page_start`,
    `page_end` out of `ingest/`.
  - T1: the boundary requires a `ReorderNote` for every concept whose plan
    position differs from its book position, so the scout prompt has to produce
    one per move. T3 should know `evidence` separates `cross_reference` from
    `inferred` edges before scorers are written.

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
      ⚠️ **The install silently broke on 4 Aug. Root cause found 20 Aug and
      fixed properly** — see "The editable-install trap" below. It was iCloud
      Drive: the repo lived on the Desktop, which is synced, and the file
      provider flags every dot-file `hidden`. CPython 3.14's `site.addpackage`
      skips a hidden `.pth`, so `import rlm` died while every test still passed.
      The repo now lives at `~/dev/Capstonee`, outside the synced tree. The
      `PYTHONPATH` workaround is gone and is not needed — `scripts/check.sh`
      now probes with `PYTHONPATH` cleared, so a broken install fails loudly
      instead of being masked by a local crutch.
- [x] **RLM examples run end-to-end** — on our stack, 20 Aug, evidence in
      `runs/_bootstrap/rlm_vertex_*.log`. **The 14 examples cannot be run as
      written**: 9 are hardcoded to `OPENAI_API_KEY` / `PORTKEY_API_KEY`, and 5
      target container or sandbox runtimes MARD does not use. Buying an OpenAI
      key would prove the library works on a stack we will never run on.
      `scripts/verify_rlm_vertex.py` runs what the three examples that matter
      actually test, against `backend="gemini"` with `use_vertex=True`:
      **needle-in-a-haystack** (quickstart — the base paper's core mechanism,
      context searched with code rather than attention), **trajectory capture**
      (logger_example), and **depth>1 recursion** (depth_metadata). All three
      pass on Tier 1 and Tier 2. Full survey in `docs/RLM_BASELINE_SURVEY.md`.
      The distinguishability answer is now demonstrated rather than only read:
      the child's trajectory flows **up** into the parent's metadata, and
      nothing flows **down** — `rlm.py:824` hands the child a fresh empty
      logger, `rlm.py:836` passes `root_prompt=None`. That gap is MARD.
      **Track 1 needs this for O1.**

      **This is the install, not the control.** Track 2's W0 asks whether the
      library runs on our stack; that is answered and closed. The **vanilla RLM
      control** — the same library driven end-to-end as a measured baseline, with
      the token/call/cost accounting wrapper and one reproduced base-paper number
      — is **Track 3's W1** (`CONTEXT.md` §3.3, [#20](https://github.com/brickstercodes/MARD-capstone/issues/20)),
      and it is not started as of 20 Aug. The two get confused because both are
      called "getting RLM running". They are different deliverables: one produces
      a working import plus evidence, the other produces a scored run every
      comparison in both papers is measured against. `runlog.RunLogger` — the
      harness Track 3 needs for it — has been delivered since 3 Aug.

      ⚠️ **Found a crash that will bite W3.** The first run failed
      intermittently with `TypeError: expected string or bytes-like object, got
      'NoneType'`. Cause: `GeminiClient.completion` returns `response.text`,
      which the SDK sets to `None` when the model emits no text part — a safety
      block, a MAX_TOKENS finish with nothing produced, or a function-call-only
      candidate. That `None` reaches `find_code_blocks`, which calls
      `re.finditer(pattern, None)` and dies. Upstream never sees it because the
      OpenAI client returns `""` in the same situation, so **this is specific to
      our Vertex path**.
      Patched in the vendored copy: both return sites now go through
      `_text_or_empty`, which returns `""` and prints the finish reason. RLM
      then finds no code blocks and iterates again — the right behaviour when
      one call in a few hundred comes back empty during W6. **This is an
      addition to `docs/15`'s patch and Track 1 should fold it in.**

      Note `cost=unreported` in the logs — the RLM client's own cost tracking
      yields nothing for Gemini. Harmless for us: `runlog` prices runs from
      `RateCard`, not from the client.
- [x] **API keys provisioned** — **confirmed working 20 Aug.**
      `test_vertex_auth.py` passes end to end: project
      `gen-lang-client-0468294301`, `location=global`, real completion against
      `gemini-3.6-flash`, tokens reported. `location=global` is required —
      `us-central1` 404s for this model. Keys live in `.env` only; never in this
      repo.
- [x] **Vertex client patch re-applied locally** — `docs/15-…` →
      `.vendor/rlm/rlm/clients/gemini.py`, applied 20 Aug. `use_vertex=True`
      path added; `completion`/`acompletion`/cost tracking untouched, so
      `docs/12`'s verification-debt item 2 (does the port preserve upstream's
      retry/backend abstraction) is closed by construction — the switch lives
      entirely in `__init__`.
      Verified both paths still fail loudly: no `GEMINI_API_KEY` on the direct
      path, no `GOOGLE_CLOUD_PROJECT` on the Vertex path.
      **`.vendor/` is gitignored — re-apply after every `bootstrap_rlm.sh`.**
      Revert with `git -C .vendor/rlm checkout rlm/clients/gemini.py`.

      ⚠️ **One inconsistency, left as-is deliberately.** The patch defaults
      `location` to `us-central1`, but Anugrah's #11 comment says
      `gemini-3.6-flash` 404s there and to use `global`, and `docs/15` itself
      flags billing location as unverified. Following the patch as written
      rather than silently changing Track 1's spec — **pass `location="global"`
      explicitly at every call site** until Track 1 confirms which default is
      right.
- [x] **Rate-limit budget documented** — `docs/RATE_LIMIT_BUDGET.md`, updated
      20 Aug against the frozen pair. Demand side complete and now costed with
      real ablation numbers. Supply side is named but empty: **Vertex quotas are
      per-project and readable only from the GCP console**, so filling §2 needs
      the credential holder, not a decision. Do it before W3.
      One thing to settle: `docs/14` §4 and `docs/31` §A1 disagree by 12 runs on
      whether A1 counts separately from the vanilla control. Flagged in §6.
- [x] **Spend cap set** — **`MARD_SPEND_CAP_USD=780`, live in
      `.venv/bin/activate` since 20 Aug** with `SET_BY` / `SET_ON` / `NOTE` so
      the ledger records who set it and when.
      Deliberately **not** in `.env`: nothing in `runlog` calls `load_dotenv`,
      so a `.env` entry would silently not apply and the cap would appear set
      while `SpendCap.from_env()` kept refusing.
      Origin: **the number arrived as `MARD_SPEND_CAP_USD=780`**
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

`import rlm` died on **4 Aug** and nobody noticed until **20 Aug**.

**Root cause, found 20 Aug: iCloud Drive.** The repo lived in `~/Desktop`, and
"Desktop & Documents Folders" sync was on — `~/Library/Mobile Documents/com~apple~CloudDocs/Desktop`
is a symlink to it. The iCloud file provider flags every dot-file and
dot-directory it syncs as `hidden`, recursively, and **re-applies the flag as it
re-syncs** — it came back twice within minutes of being cleared. CPython 3.14's
`site.addpackage` **silently skips a hidden `.pth`**, and both editable installs
(`mard`, `rlms`) resolve through one. No warning, no error, exit code zero.

The evidence was unambiguous once the scope was checked: `.git`, `.venv`,
`.vendor` and `.gitignore` were all flagged, across four unrelated Desktop
projects — while `~/.zshrc` and `~/.ssh` were untouched. Home is not synced;
Desktop is.

It survived sixteen days because **`pytest` puts the repo root on `sys.path`**, so
every test passed and `./scripts/check.sh` stayed green while the install was dead
for anything run from another directory. Arav would have hit it on his first
script outside the repo root.

- **Fixed at the source** — the repo now lives at `~/dev/Capstonee`, outside the
  synced tree, with the inherited flags cleared and the venv rebuilt. A fresh
  venv comes out clean and `import rlm` works from `/` with no help.
- **Guard made honest** — `scripts/check.sh` probes with `env -u PYTHONPATH`. It
  already ran from `/` so cwd could not mask a dead install, but it inherited the
  `PYTHONPATH` that `.venv/bin/activate` exported, so it reported what the local
  crutch did rather than what a teammate's clone would do. That crutch is gone
  and is not needed.
- **Silent skip removed** — `tests/test_lm_builder.py` used `importorskip`, so a
  broken install turned the only test of the RLM seam into a skip inside a green
  suite. A vendored copy that is present but not importable now loads from the
  vendored tree and the test still runs; only a genuinely un-bootstrapped clone
  skips.

**If this recurs, check the folder before the machine.** Anything under `~/Desktop`
or `~/Documents` on a Mac with iCloud Drive sync will do this to `.venv` and
`.git` — and syncing `.git` risks worse than a broken import.

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

- [x] `plan/` Pydantic models — concept graph, ordered study sequence, rationale.
      `plan/models.py`. Edge direction is named (`prerequisite`/`dependent`) not
      positional, every concept carries a `book_position` so O5 can compare book
      order against plan order without re-parsing, and `extra="forbid"` means an
      unexpected key from Tier 1 is a rejection rather than a silent drop.
- [x] Validation that fails loudly rather than passing a malformed plan to N
      builders. `plan/validation.py`: cycles, dangling edge endpoints, sequence
      that is not a permutation of the graph, a concept taught before its
      prerequisite, placeholder directives, rationale that disagrees with the
      sequence, and a move with no stated reason. Every violation is collected
      rather than the first — the error message is Tier 1's repair prompt.
- [x] Stub builder that eats a hand-written plan. `plan/EXAMPLE_PLAN.json` is the
      worked example (six OSTEP concepts, one real reorder); `orchestrate/` forks
      one brief per step, joins in Master-Plan order regardless of completion
      order, and puts a provenance pointer on every span. `LmBuilder` proves the
      same interface against the RLM library's own `MockLM`, offline, no keys.

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
