# Handoff — Track 3: why the `introcs` run produced garbage, and how to re-run it

**For:** Arav Sharma (@FalseAdvertising), Track 3 · **Paste this whole file as the
first message of a fresh Claude Code session opened in the repo root.**

Written 27 Aug 2026. Every claim below was checked first-hand against the repo,
the corpus artefacts and the run output on 27 Aug.

---

## 0. First: the run failed, and it was not your fault

The 30-iteration run on *Introduction to Computer Science* returned 78 "headings"
that are mostly **table-of-contents lines and mid-sentence body fragments**. The
root cause is structural, not carelessness:

> **`corpus/*/document.*` is in `.gitignore` (line 15).** On a fresh clone of this
> repository, `corpus/introcs/document.txt` **does not exist.** There was nothing
> correct to point the RLM at, so it got pointed at the raw PDF.

The ingestion pipeline exists precisely to prevent what happened. Running without
it is running without the method.

### The proof, so you can confirm it yourself

Three headings from your output do not occur anywhere in the cleaned corpus:

| String from the run | Occurrences in `corpus/introcs/document.txt` |
|---|---|
| `PART 1 PROBLEM SOLVING` | **0** |
| `Introduction 9` | **0** |
| `Chapter Review 33` | **0** |

They exist only in the raw PDF's printed table of contents, which `ingest/`
deliberately strips. This is **confound #2**, recorded in
`docs/16-PRIMARY_DOCUMENT.md` before the run happened: *"`introcs` prints its full
chapter list on page 7; a model reading the first pages gets the skeleton for
free."*

### Everything else in the output follows from that one cause

- **Page numbers welded into titles** — `Chapter 9 285`, `Chapter 347`,
  `Introduction 39`, `Appendix A ... 911 A`. TOC lines, not headings. Most of the
  iteration budget went on summarising the table of contents.
- **Mid-sentence fragments as titles** — *"conclusion that 'Socrates is
  mortal.'"*, *"chapter, rather than focusing on the programming details..."*,
  *"section of code. A critical section is..."*. Body text mistaken for headings.
  `ingest/` already fixed this class of bug (three of them, each with a regression
  test — see `docs/16`).
- **~15 entries reading "Content not provided in excerpt. Please paste the
  text"** — the model asking a human for input it should have sliced out of the
  REPL. This is the dangerous failure mode: it looks like output and is not.
- **Confident fabrication where there was nothing** — e.g. *"no content is
  provided in the excerpt, but such reviews typically recap key concepts."* One
  entry reuses another's phrasing about OS abstraction for an unrelated
  architecture chapter.
- **30 iterations is Zhang's `max_iterations` default.** The run terminated on
  budget exhaustion, not completion. 359k input tokens against a 617k-token book
  means most of the document was never read.

### One result worth keeping

Seven separate `Chapter Outline` entries (#33, 47, 51, 58, 63, 70, 75) all
received the **identical** summary — Chapter 4's four sections. `Chapter Outline`
legitimately occurs 14 times in the corpus, once per chapter. The model found
several and could not tell which chapter any of them belonged to.

That is *exactly* the blindness MARD claims to fix, demonstrated on our own
primary document. **Keep the transcript.** It is a good qualitative figure for the
paper. It is **not** a baseline number, because the input was wrong.

---

## 1. Before you start — the repo is not pushed

As of 27 Aug the working copy is **ahead 2 commits** of `origin/main`, with eight
modified and five untracked files not committed. **You may be looking at a stale
clone.** Sync with Anugrah before doing anything, and specifically confirm these
exist for you:

- `docs/18-W3_PROVIDER_SWITCH.md` — **the current state** of provider, control
  library, model pair and cost. Where it and any other doc disagree, `18` wins.
- `docs/19-HANDOFF_MARD_ON_FORK.md` — the MARD-arm implementation brief.
- `paper/main.tex`

If they are missing, ask for them rather than proceeding from `CONTEXT.md` alone:
the project **left Vertex/Gemini for OpenAI on 26 Aug**, and `docs/12-MODEL_PAIR.md`
and `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md` are both void.

---

## 2. Regenerate the corpus — this is step one, not optional

The PDF is also not in the repo (`corpus/raw/` is ignored: *"source PDFs are
fetched, not vendored, so licence provenance stays with the upstream
distributor"*). So:

```bash
# 1. Fetch the PDF from OpenStax directly. CC BY 4.0 at the book level --
#    confirmed against OpenStax's own book-level licensing page, NOT the
#    CC BY-NC-SA that some individual chapter footers state.
#    Put it under corpus/raw/ (already gitignored).

# 2. Regenerate the parse artefacts.
python -m ingest.cli corpus/raw/introcs.pdf --doc-id introcs

# 3. Regenerate the skeleton and passes.
python -m envelope.cli corpus --document-id introcs
```

### Then verify the parse before you spend a single token

```bash
cat corpus/introcs/parse_quality.md
```

You must see, per `docs/16-PRIMARY_DOCUMENT.md`:

| Check | Expected for `introcs` |
|---|---|
| Warnings raised | **0** |
| Characters after cleaning | ~2,432,812 |
| Headings detected | ~1,403 |
| Learning-objective blocks | 61 |
| Key-terms blocks | 14 |
| Orphan punctuation per 1k lines | ~30.3 |

And these sanity greps, which are the direct test for the bug that broke the last
run:

```bash
grep -c "PART 1 PROBLEM SOLVING" corpus/introcs/document.txt   # must be 0
grep -c "Introduction 9"          corpus/introcs/document.txt   # must be 0
grep -cE '^#{1,6} .*Chapter Outline' corpus/introcs/document.txt # must be 14
```

**If any of those three is wrong, stop.** Front-matter exclusion is not working
and every downstream number would be measuring the table of contents again.

---

## 3. The two structural controls, and why both arms need them

Both concern document structure reaching a model without that model having derived
it. If structure arrives by another route, we report the publisher's work as MARD's.

1. **The publisher's bookmark outline** lives in `corpus/introcs/outline.json`
   with an explicit provenance field. It is the **yardstick** for skeleton
   quality. **It is never an input.** Do not read it into any prompt.
2. **The printed table of contents** is inside the body text. `ingest/` tags it
   `kind: front_matter`, keeps it in `document.jsonl`, and **excludes it from
   `document.txt`**. Use `document.txt`. Never feed `document.jsonl` or the raw
   PDF to a model.

**Both controls apply identically to the vanilla-RLM arm and the MARD arm.** If
the arms get different inputs, the comparison isolates nothing and ablation A1 is
void. This is the single most important sentence in this document.

---

## 4. The task was also wrong

"Summarise the headings" is not the task. Per `docs/30-MEASUREMENT_PROTOCOL.md`
§2, the evaluated output modality is **explanations only** — never flashcards,
quizzes or diagrams, and not heading summaries either.

- **The MARD arm** emits a **Master Plan**: a concept graph plus an ordered study
  sequence plus reordering rationale, validated against `plan/models.py` and
  `plan/validation.py`. A malformed plan must **fail loudly**, not dispatch N
  subtly wrong builders. Tier 2 then generates one explanation per section and the
  spans are joined in **Master Plan order**, not book order.
- **The vanilla arm** must be given the *same task* on the *same input*, without
  the envelope. Not a different task, and not a summarisation task.

`envelope/pass1.py`'s `directive_for()` and `PASS1_PROMPT` already define the real
Pass 1 task. Read them before writing any prompt. **Do not modify them** — feature
freeze A was 23 Aug and a prompt change is a re-run of the whole matrix.

---

## 5. Run configuration

- **Control library:** Arav's fork `FalseAdvertising/Vanilla_RLM_Python`, pinned
  **`a0ca553`**. Both arms run on this one implementation — see `docs/18` §4.2. The
  justification is **implementation parity**, never rate limits; `docs/18` §4.2
  explains why the rate-limit reasoning is factually backwards and must not appear
  anywhere.
- **Depth:** `max_recursion_depth=1`, `enable_sub_calls=True`. Library default and
  the base paper's primary reported condition.
- **`max_recursion_depth=0` is a trap.** The guard at `sub_caller.py:96` is
  `self._depth + 1 < max_recursion_depth`; the root starts at `_depth=0`, so 0 and
  1 take the *same* branch. Setting 0 does **not** disable sub-calls and the trace
  is indistinguishable. The real no-sub-calls condition is
  `enable_sub_calls=False`. **Log depth as an
  `(enable_sub_calls, max_recursion_depth)` pair**, never one integer.
- **Concurrency:** `replm` has **no concurrency cap** — bare `asyncio.gather`, no
  semaphore anywhere in `src/`. You must supply one, shared across both arms.
  Run at ≤70% of the measured per-minute ceiling; honour `Retry-After`; jittered
  backoff; bounded attempts then **fail the run loudly**. Log every 429 with its
  timestamp — a 429 is data, not noise.
- **Reasoning models:** send `max_completion_tokens`, not `max_tokens`, and do not
  send `temperature` — GPT-5-family endpoints reject it. Both fixes are already in
  `a0ca553`'s `client.py`. `RLMConfig.temperature` becomes **dead config**: omit it
  from the manifest or mark it not-applied, because recording a value that was
  never sent corrupts the config snapshot.
- **Cost:** `cost_per_input_token` defaults to `0.0`, so an unconfigured run
  reports a cost of `0.0` that looks like a measurement. Feed rates from
  `runlog.pricing.RateCard`. Export `MARD_SPEND_CAP_USD` or `SpendCap.from_env()`
  refuses to run. **The old $780 is void** — those were free Vertex credits, now
  stranded. All money is out of pocket. Use `MARD_SPEND_CAP_USD=60`.
- **Repeats:** three runs, variance reported. `replm` has no `seed` parameter at
  all; `CAMPAIGN_SEEDS = (11, 23, 42)` are run *identifiers*, and the variance
  comes from genuine repeats.
- **Iterations:** the last run hit the 30-iteration ceiling. If a clean run still
  hits it, that is a finding to report, not a number to raise quietly.

### Cost calibration from your run

Your 359,498 input / 120,850 output tokens cost roughly **$3.86** at Sol rates,
**$2.17** at Terra. Output tokens came in about **ten times** the projection in
`docs/18` §10, so Manuscript A is more like **$25–35** than the $9 estimated there.
Please report your real token counts so that section can be corrected with
measured figures instead of assumptions.

---

## 6. Log every run

All seven fields from `docs/30` §1, or it is not a number: task score, tokens
in/out separately, calls issued split by tier, cost, wall-clock (**both `max` and
`Σ` over builders**), run identity, and a full config snapshot including model IDs,
prompt-template versions, the depth pair, active ablation, document, and the
**fork's** git SHA. `docs/TRACK3_HANDOFF.md` shows the `RunLogger` API.

A crashed run still writes `summary.json` with `status: "failed"` and a traceback.
That is deliberate: a hole in the matrix should explain itself rather than be
absent.

**Truncation is a failure, not a low score.** `join_in_plan_order` already
validates non-empty `span.text` per plan step and raises `IncompleteArtefactError`.
Do not regress that, and do not catch it to keep a run alive — a throttled run
producing empty responses would otherwise yield an artefact short by a section
with every identity check satisfied and a complete-looking log.

---

## 7. Definition of done

- [ ] `corpus/introcs/parse_quality.md` shows **0 warnings** and the table in §2
      matches.
- [ ] All three sanity greps in §2 return the expected values.
- [ ] The vanilla arm reads `corpus/introcs/document.txt` — **never** the PDF,
      `document.jsonl`, or `outline.json`.
- [ ] Zero output titles contain a trailing page number or begin mid-sentence.
- [ ] Zero output entries ask a human to supply text.
- [ ] The output is the assigned task, not heading summaries.
- [ ] Depth logged as an `(enable_sub_calls, max_recursion_depth)` pair; fork SHA
      recorded.
- [ ] A shared concurrency limiter is in place; 429s logged with `Retry-After`.
- [ ] Cost is non-zero and sourced from `RateCard`.
- [ ] One logged run under `runs/` with all seven `docs/30` §1 fields populated.
- [ ] Real token counts reported back so `docs/18` §10 can be corrected.

---

## 8. Rules that override your judgement

- **Feature freeze A was 23 Aug; results freeze A is 27 Aug.** A pipeline change
  invalidates every number measured before it. If you want to change a prompt, the
  Master Plan schema, or `ingest/`'s behaviour — **stop and ask Anugrah.** Those
  are re-runs of the whole matrix.
- **No number without a logged run.** A figure that cannot be traced to all seven
  fields is not admissible.
- **A null result is publishable**, framed by the O4 structure-dependence
  boundary. Never tune toward a positive after the fact.
- **Escalate rather than invent.** Four workstreams run in parallel; a decision
  invented here becomes three different decisions elsewhere. Mark anything
  unverifiable `[UNVERIFIED]` and surface it — never quietly assert it, never
  quietly drop it.
- **Report findings, instinct and options.** Anugrah wants everything surfaced,
  including things that look like your own mistakes. The last run's root cause was
  a `.gitignore` line, which is exactly the kind of thing that stays invisible
  until someone says it out loud.
