# 39 — Implementation brief: the negative control, and the axler run for Figure 1

**For the `docs/25` MARD-arm session.** Paste as a new message; you keep your context.

Written 28 Aug 2026. Paper is written Saturday. This is the last set of runs.

---

## 0. Read first

1. `docs/36-PLAN_PROVE_O3.md` — what the paper now claims, and what it has stopped claiming.
2. `docs/30-MEASUREMENT_PROTOCOL.md` banner item 6 — the negative control's definition.
3. `docs/38-DETERMINISM_RESULTS.md` — the results your runs slot beside.

Then `scripts/preflight.sh`.

**Budget:** $9.38 of $120 spent. These runs cost roughly $4. Cost is not a constraint;
wall-clock is. Do not batch-run anything not listed here.

---

## 1. Footprint

**Yours:** `scripts/`, `mard/`, `provider/`, `runs/` (you are the only writer there),
`docs/41-NEGATIVE_CONTROL_RESULTS.md`.

**Read-only:** `eval/`, `corpus/`, `ingest/`.

**Do not touch: `paper/`.** It has one writer and it is not you. Put your numbers in
`docs/41` and they will be lifted into the manuscript from there.

`docs/26`'s session is scoring at the same time and reads `runs/` continuously. Write only
complete run directories; never leave a partial `summary.json` behind.

---

## 2. Task 1 — parameterise the document (do this first)

`scripts/run_vanilla_full.py:33` hardcodes `DOCUMENT_ID = "introcs"`, and
`scripts/run_mard_full.py` takes a seed and an optional ablation but no document. Both need
a `--document-id` argument defaulting to `introcs`, so the existing campaign commands keep
working unchanged.

Verify before running anything expensive: `mard/run.py` derives sections and chapters from
`document.jsonl` at runtime via `build_sections` / `group_into_chapters`, so
`corpus/introcs_flat/` needs only `document.jsonl` and `manifest.json`, both of which exist.
Confirm this with a dry check rather than trusting this paragraph.

---

## 3. Task 2 — the negative control, 6 runs

Corpus: `corpus/introcs_flat/` — same text, section order shuffled, heading markers stripped.
Systems: B1 (vanilla RLM) and MARD full. Seeds: the three campaign seeds. 3 × 2 = 6 runs.

**The prediction is a null difference**, and a null is the claimed outcome here, not a failure
to find an effect. `run_pass0` should record an empty skeleton as `degenerate: true` rather
than raising. If it raises instead, that is a finding about the guard — report it, do not
patch around it to force a run to complete.

Two things to watch, and to record either way:

- **If MARD is measurably *worse* than B1 here**, that is the envelope's overhead with nothing
  to orient against. It is a result and it goes in the paper. Do not soften it.
- **If the skeleton is empty but MARD still produces cross-chapter edges**, something other
  than the skeleton is carrying structure, and the ablation story in `docs/38` needs
  revisiting. Flag it loudly rather than filing it as a curiosity.

Record all seven `docs/30` §1 fields per run, as the campaign already does.

---

## 4. Task 3 — one MARD run on `axler` — BLOCKED, do not work around

Figure 1 panel (c) needs MARD's concept graph for *Linear Algebra Done Right*, because panels
(a) and (b) are that book.

**`corpus/axler/` has no `manifest.json`, and `corpus/SOURCES.json` has axler's `url`,
`pdf_sha256` and `retrieved_on` all null.** `verify_or_raise` will refuse. `SOURCES.json`'s
own rules say a null is "unrecorded, not unknown-forever" and "do not guess one."

So: **do not fabricate a manifest, and do not bypass `verify_or_raise`.** Report what is
missing and stop. If — and only if — someone supplies the actual download URL, the SHA-256 of
the file on disk, and the retrieval date, fill `SOURCES.json` from those, pin the manifest,
and run one MARD full run at seed 11. One run, not three: this is a figure, not a result, and
it must be labelled as a single unreplicated run wherever it appears.

---

## 5. Deliverable

`docs/41-NEGATIVE_CONTROL_RESULTS.md`, containing:

- a table of the 6 runs: system, seed, run id, task score, input/output tokens, calls, cost,
  wall-clock, and for MARD the concept/edge/cross-chapter counts
- the B1-vs-MARD delta and its spread, stated plainly, with the direction called out
- what the skeleton did on the flattened corpus — empty and `degenerate: true`, or not
- the axler status: blocked, and exactly which three fields are missing
- run ids of anything you excluded, and why

Do not compute task scores yourself — `docs/26` owns `eval/`. Emit the runs; say in `docs/41`
that scoring is pending and name the run ids so that session can pick them up.

Report back with the delta and its direction. Unrounded.
