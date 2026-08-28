# 34 — Implementation brief: scoring (O3 quality, forward-reference violations, groundedness over MARD)

**This file is for the session that already built `eval/`** — the `docs/26` agent. Paste it
as a new message into that session; it keeps its context and its ownership of `eval/`.

Written 28 Aug 2026. Deadline: the manuscript is written Saturday 29 Aug. Everything here
must be a logged, re-runnable number by Friday night.

---

## 0. Read first

1. `docs/00-START_HERE.md` — the higher-number-wins rule and the concurrent-writing protocol.
2. `docs/30-MEASUREMENT_PROTOCOL.md` §2 (task score) and §3 (forward-reference violations).
3. `docs/23-GROUNDTRUTH_SPEC.md` §7 — what you already built, and the "blocked" note at the
   end of it. **That block has cleared** (see §3 below).
4. `docs/28-MARD_ARM_FINDINGS.md` — the campaign that produced the runs you are about to score.

Then run `scripts/preflight.sh`. If it fails, read the failure; another session's failing
test is not yours to fix.

---

## 1. Footprint — the MARD session is running at the same time

**Yours to create:** anything new under `eval/`, `tests/test_*` for it, and `docs/35+`.

**Read-only, absolutely:** `runs/`. The `docs/25` session is writing negative-control runs
into `runs/` while you work. Read run directories, never write into them. Your outputs go to
`eval/` (JSON) and `docs/35-SCORING_RESULTS.md` (prose).

**Do not touch:** `mard/`, `envelope/`, `orchestrate/`, `provider/`, `plan/`, `paper/`,
`.vendor/`, and any file under `eval/frozen_subsets/`.

If you need a change outside your footprint, stop and report it.

---

## 2. Task A — O3 quality score: B1 vs MARD

**This is the paper's headline number.** O3 is "isolate the contribution — MARD vs vanilla
RLM on output quality and tokens consumed" (`CONTEXT.md` objective table).

### The comparable artefacts

| System | File in each run dir | Runs |
|---|---|---|
| B1 (vanilla RLM) | `artefacts/vanilla_answer.md` | the three `*__vanilla_rlm__introcs__s{11,23,42}__*` |
| MARD full | `artefacts/tier2_output.md` | the three `*__mard__introcs__s{11,23,42}__*` (use the **last** s11 run; the earlier s11 runs are pre-fix and are not results) |

Ablation runs (`mard_a1`, `mard_a1f`) are scored too, on the same scorer, so §3 of the paper
can show the ablation ladder on the same axis. `mard_a1f` has five run dirs for two seeds —
take the last completed run per seed and say in your doc which run ids you used.

### The reference

Document-native ground truth only, per `docs/30` §2 — `ingest/groundtruth.py`
`extract_learning_objectives` over `corpus/introcs/document.jsonl`. 61 objectives. Never an
LLM-generated reference (`docs/23` §1).

### The metric

`eval/groundtruth_scoring.py` `score_overlap`, recall-based, as built. Report per run:

- **objectives covered** — count and fraction, at `DEFAULT_THRESHOLD`
- **the same fraction at two other thresholds** (say 0.5 and 0.7), so the number survives a
  reviewer who disagrees with 0.6, exactly as your own module docstring demands
- `matched_tokens` / `reference_tokens` retained per objective in the JSON

Then per configuration: **mean and min–max across the three seeds.** Never a single run as
*the* number (`docs/30` §4).

### One constraint you must not break

**The cross-chapter-edge fraction is MARD-internal and can never be presented as an O3
comparison.** B1 emits no concept graph at all — verified: `result` is `null` in all three
vanilla run summaries. There is no B1 number to compare 91.7% against. That figure belongs
to the ablation ladder (MARD vs A1s vs A1f) and nowhere else. If you find yourself writing
"MARD 91.7% vs vanilla —", stop.

### Also report, from `summary.json`, no new measurement needed

Tokens (input/output split), calls, cost, wall-clock, per configuration, mean and spread.
The token story is half of O3 and it is already logged. B1 s42 alone spent 3.3M input tokens
and $1.60; MARD s42 spent 94.7K input and $0.58. That contrast wants a table.

---

## 3. Task B — forward-reference violations (docs/30 §3)

`docs/23` §7 recorded this as blocked because no Master Plan existed for `introcs`. **It is
no longer blocked.** Every MARD run now writes `artefacts/master_plan.json` — 84 concepts,
133 edges, in the s42 full run.

The metric is a before/after count, on the same document:

- **before** = book order. You already have this half — `extract_cross_references` classifies
  in-text `Chapter N` mentions as forward / backward / same-chapter against page order.
- **after** = Master Plan order. Take the compiled plan's concept sequence, map concepts to
  their source chapters, and count how many times the plan places a concept before something
  the document declares as its prerequisite.

Report before and after, per seed, mean and spread. If the plan does not reduce violations,
**that is the result** — report it. `docs/00-CLAIM.md` explicitly budgets for a null result
here.

Note the mapping step honestly: concepts carry `aliases` after the duplicate-id merge, so a
concept can belong to more than one chapter. Say in your doc how you resolved that, and
report the count both ways if the choice moves the number.

---

## 4. Task C — groundedness over the MARD runs

Your `eval/groundedness.py` has only been run over the vanilla arm
(`eval/groundedness_report_vanilla.json`). Run `score_run` over every MARD-arm run
(`mard`, `mard_a1`, `mard_a1f`) and write `eval/groundedness_report_mard.json`.

What matters for the paper: the seed-42 grounding failure recorded in `docs/32` was found in
the vanilla arm. **Does MARD's envelope change the grounded / ungrounded / regenerated /
`root_authored` split, and does the s42 anomaly reappear?** That question is the third axis —
faithfulness and auditability — and a clean answer to it is worth a subsection.

If the detector needs a shape change to read MARD call logs (the call structure differs —
99 calls across two tiers, not 2), make it in `eval/`, keep the vanilla report re-runnable,
and add a test.

---

## 5. Order of work

Task A first, all of it, before touching B or C. If Friday runs out, the paper can survive
without B and C; it cannot survive without A.

## 6. Definition of done

- `eval/scoring_report.json` — every run, every configuration, all seven `docs/30` §1 fields
  plus the quality score, traceable to a run id
- `eval/groundedness_report_mard.json`
- `docs/35-SCORING_RESULTS.md` — the tables the paper will lift, each with run ids, the
  threshold used, and spread across seeds; and an explicit note of anything you could not
  measure and why
- tests for anything new; `scripts/preflight.sh` no worse than you found it
- **no writes anywhere in `runs/`**

Report back with the headline: covered-objective fraction for B1 and for MARD, mean and
range, and the token/cost contrast. Do not round in your report — give the figures.
