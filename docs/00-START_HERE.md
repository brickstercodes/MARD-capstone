# 00 — Start here

**Every fresh session reads this file first.** It is short on purpose.

## The one rule

**Where two documents disagree, the higher-numbered one wins.** This project changed
provider, control library, model pair, budget and evaluation scope inside three weeks, and
the older documents were deliberately left intact with banners rather than rewritten. That
makes the history auditable and makes reading order matter.

Anything genuinely void has been moved to `docs/archive/`. If a file is in `docs/`, it is
either current or carries a banner saying which parts are not.

## Current state, in ten lines

- **Provider:** OpenAI. Vertex/Gemini abandoned 26 Aug (`18`).
- **Model pair:** `gpt-5.2` (Tier 1 / root) + `gpt-5-mini` (Tier 2 / sub-calls) (`22`).
  Rates live in `provider/rates.py` and nowhere else.
- **Control library:** `Zhang_RLM` @ `62acf7b`, vendored at `.vendor/rlm` (`18` §4.2).
  Both arms run on one implementation — the justification is **implementation parity**,
  never rate limits.
- **Money:** out of pocket. `MARD_SPEND_CAP_USD=120`. The old 780 is void everywhere.
- **Primary document:** `introcs`. Front matter excluded, `outline.json` never an input,
  identically for every system (`16` debt item 2, CLOSED).
- **Configurations:** **B1** vanilla RLM (done, 3 runs) · **M** MARD two-pass · **A1**
  envelope removed · **NC** negative control on a structure-ablated `introcs`.
  **B1 and A1 are different runs** (`31` rename banner).
- **The evaluated modality is explanations.** Task score uses learning objectives and
  in-text cross-references; glossary terms are deferred (`23`).
- **A run in which the system behaved badly is a result, not a failed run** (`24` §2).
- **The three baseline repeats produced three different self-authored architectures.**
  156 / 190 / 75 is not dispersion around a mean and must never be averaged (`32` §4).

## Read next, by job

| Doing | Read, in order |
|---|---|
| **Anything** | this file → `18` (state) → `24` (how to interpret a bad run) |
| Building the MARD arm | + `25` (the brief), `31` banner, `30` banners |
| Negative control / groundedness | + `26` (the brief), `24` §5, `23`, `32` (results + the architecture-instability finding) |
| Scoring, figures, the manuscript | + `27` (the brief), `32` (read before writing §4), **`28`** (MARD-arm findings; one figure is `[UNVERIFIED]`), `30`, `23`, `40` |
| Anything touching cost | + `22`, then `provider/rates.py` |

## Before you spend a token

```bash
scripts/preflight.sh
```

It checks the corpus manifest, the spend cap, that exactly one `rlm` is importable and that
it is the pinned one, and that the test suite is green. **If it fails, fix that and nothing
else.** Every failure it reports has cost this project time at least once.

## Writing to `docs/` when other sessions are running

Several sessions run at once and they share this directory. On 28 Aug two of them
independently wrote the same finding into two different files within minutes of each other.
It was caught and reconciled, but two accounts of one finding drifting apart is exactly what
the higher-number-wins rule exists to prevent — and the rule cannot help if both accounts are
written at the same time.

**The rule: create freely, edit almost never.**

- **A numbered doc you create is yours.** Check `ls docs/` first and take the next free
  number. If you find another session took it while you were writing, renumber yours — the
  file that landed first keeps the number.
- **Never restate another session's finding in your own words.** If you are about to write
  something that already exists elsewhere, write a **pointer** to it instead. One account,
  one place.
- **If another session has already written what you were about to, theirs wins when it is
  more complete.** Collapse yours to a pointer and say so. This is a tie-break that needs no
  negotiation, and it is what happened on 28 Aug.
- **Two edits to someone else's doc are always allowed**, because neither can create a
  competing account: fixing a cross-reference that points at the wrong place, and adding a
  "superseded by" or "see also" pointer.
- **Anything else in a doc you did not create: report it, do not edit it.** Including things
  you are confident are wrong.

**`docs/STATE.json` is append-mostly.** Add to `known_traps`, `unverified` and `findings`;
change `status` only for the configuration your own session owns. Do not restructure it.

**`paper/main.tex` has exactly one writer** — the `docs/27` session. No exceptions: two
agents editing one `.tex` produces a conflict nobody has time to resolve.

**When you finish, report every file you touched.** The 28 Aug collision was caught because a
session listed its edits unprompted. That habit is the last line of defence.

### One consequence of running in parallel

`scripts/preflight.sh` runs the **whole** test suite, so a failing test inside another
session's in-progress work will fail *your* preflight. **Read the failure before acting on
it.** If it is outside your footprint, note it and continue; it is not yours to fix and
"fixing" it will collide with the session that owns it.

## Standing rules that override your judgement

- **No number without a logged run** under `runs/`. All seven `docs/30` §1 fields.
- **No citation without a verified row** in `docs/40-LITERATURE_LOG.md`. Only two of the
  manuscript's seventeen references currently have one.
- **3 repeats on every number, variance reported.** Never average away a spread that is
  itself the finding.
- **A null result is publishable**, framed by the O4 boundary. Never tune toward a positive.
- **Mark anything unverifiable `[UNVERIFIED]` and surface it.** Never quietly assert, never
  quietly drop.
- **Escalate rather than invent.** If a decision is not written down, it is not yours.
