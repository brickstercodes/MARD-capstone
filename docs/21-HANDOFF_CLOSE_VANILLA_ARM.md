# Implementation brief — vendor `Zhang_RLM`, wire it to `ingest`, close the vanilla arm

**Paste this whole file as the first message of a fresh Claude Code session opened in
`~/Desktop/Capstone/MARD-capstone`.**

Written 27 Aug 2026. Every fact below was verified first-hand against this repo,
`corpus/introcs/`, and `github.com/FalseAdvertising/Zhang_RLM` @ `62acf7b`. Anything
unverified is marked as such.

**Goal of this session:** one logged vanilla-RLM run on `introcs` that reads the
ingested corpus, performs the real task, and records all seven measurement fields.
That closes the A1 / O3 control arm.

---

## 0. Read first, in this order

1. `docs/18-W3_PROVIDER_SWITCH.md` — the current state of provider, control library,
   model pair and cost. Where it and any other doc disagree, `18` wins. **§4.2 changes
   in this session — see §2 below.**
2. `docs/31-ABLATIONS.md` — what A1 toggles. Read the banner.
3. `docs/30-MEASUREMENT_PROTOCOL.md` — the seven fields. Read the banner.
4. `docs/16-PRIMARY_DOCUMENT.md` — the two structural confounds and why `introcs` is
   primary. **Its verification-debt item 2 blocks this work; see §3.**
5. `ingest/manifest.py` — corpus provenance pinning, added 27 Aug.
6. `docs/TRACK3_HANDOFF.md` — the `runlog` API you will wrap runs in.

`docs/12-MODEL_PAIR.md` and `docs/15-VERTEX_GEMINI_CLIENT_PATCH.md` are **void** —
the project left Vertex/Gemini for OpenAI on 26 Aug. History only.

---

## 1. Why the last run produced garbage — two causes, neither the library's fault

The 30-iteration run on *Introduction to Computer Science* returned 78 "headings" that
were mostly table-of-contents lines and mid-sentence fragments. Both causes are in
`run_file.py`, and both are one-line fixes.

**Cause 1 — it read the raw PDF, not the ingested corpus.** `load_pages()` calls
`pypdf` directly on the PDF. That reintroduces the printed table of contents, which is
**confound #2** in `docs/16`: *"`introcs` prints its full chapter list on page 7; a
model reading the first pages gets the skeleton for free."* `ingest/` exists to strip
it. Proof: `PART 1 PROBLEM SOLVING`, `Introduction 9` and `Chapter Review 33` all
appear in the run output and occur **zero** times in `corpus/introcs/document.txt`.

`pypdf` is also simply worse than this project's own extractor — `ingest/` uses PyMuPDF
and produces 2,432,812 cleaned characters with **0 warnings**, 1,403 detected headings,
and verified page mapping (1,199 of 1,200 sampled blocks).

**Cause 2 — the prompt literally asked for a table of contents.**

```python
DEFAULT_PROMPT = (
    "Give me a chapter-by-chapter table of contents: for each chapter/major "
    "section you can identify, list its title and a 1-2 sentence summary of "
    "what it covers."
)
```

The model did exactly what it was asked. Nothing malfunctioned. The output was a
correct answer to the wrong question, on the wrong input.

### The good news: half the integration already exists

`run_file.py` already handles this project's own text format:

> *"If the file carries `[[page:N]]` markers (e.g. from our own PDF->txt converter),
> split on them to recover the same per-page structure a PDF would give us."*

`ingest/cli.py` writes exactly those markers (`PAGE_MARKER = "[[page:{page}]]"`).
Verified on the real corpus:

| Check on `corpus/introcs/document.txt` | Value |
|---|---|
| `[[page:N]]` markers | **937** (page 3 → 939) |
| Non-empty page chunks after split | **916** |
| Chars per chunk, mean / median / max | 2,682 / 2,760 / 4,826 |
| ATX heading markers surviving the split | **1,487** |

So the hook works. It was pointed at the wrong file.

Also keep in mind, `run_file.py`'s two other choices are **good** and should survive:
passing `prompt=pages` as a `list[str]` (the library natively supports this and its own
system prompt iterates pages), and using `root_prompt=question` so the task stays
anchored in the root's fixed message instead of being buried in a multi-million-character
context. Do not undo either.

---

## 2. The control library changes to `Zhang_RLM` — and this *strengthens* the argument

`docs/18` §4.2 currently names Arav's **`replm`** fork (`Vanilla_RLM_Python`) as the
control, justified on **implementation parity**. The library changes; the justification
does not, and it gets better.

`orchestrate/lm_builder.py`'s docstring says its `LanguageModel` protocol is declared
structurally *"rather than imported from the RLM library on purpose"*, and that
**`rlm.clients.base_lm.BaseLM` satisfies it** — MARD's Tier 2 was designed against
Zhang's client layer from the start. Meanwhile `replm`'s `OpenAIAdapter.acomplete(model,
messages, temperature, max_tokens, ...)` does **not** satisfy that protocol at all.

So: using `Zhang_RLM` means **both arms share Zhang's client layer**, which is stronger
parity than `replm` would have given. Same argument, better instantiation.

**Task: update `docs/18` §4.2, `docs/19`, `docs/20` and `paper/main.tex` to name
`Zhang_RLM` @ `62acf7b`.** And note what becomes obsolete, because a lot does — see §6.

**The rate-limit justification remains forbidden.** `docs/18` §4.2 explains why it is
factually backwards. Do not put it in a comment, a commit message, or the paper.

---

## 3. Decisions — 3.1 and 3.2 are ANSWERED; 3.3 is still open

Anugrah answered the first two on 27 Aug. **3.3 remains open and is not yours to
decide** — escalate and wait if it still blocks you.

### 3.1 ANSWERED 27 Aug — the task both arms are given

**Anugrah's decision: study-guide explanations.** Not a plan, not a table of contents.
The vanilla arm is asked for the same *end artefact* as MARD and reaches it however RLM
reaches it — being told to build a concept graph first would hand vanilla RLM MARD's
architecture and stop it being vanilla.

**The frozen `root_prompt`, verbatim:**

```text
Using the textbook available in `context`, write a study guide for a learner
meeting this material for the first time. Identify the concepts the textbook
teaches and, for each one, write an explanation the learner can study from.
Order the guide so that a concept is explained only after anything it depends
on has been explained. Output the study guide itself, with no commentary about
your process.
```

Three things in it are load-bearing, so do not paraphrase it:

- *"write an explanation the learner can study from"* — `docs/30` §2 fixes the evaluated
  modality as **explanations only**. Anything else is unscoreable.
- *"Order the guide so that a concept is explained only after anything it depends on"* —
  MARD achieves this structurally, by joining in Master Plan order. Vanilla must be
  **given the same instruction** or the ordering comparison is unfair to it. How it
  complies is its own business.
- *"no commentary about your process"* — the last run returned ~15 entries reading
  *"Content not provided in excerpt, please paste the text."* This closes that door.

This string is now paper content. **It cannot change after a measured run**
(`CONTEXT.md` §3.4). If it must, that is a re-run of the whole matrix, decided by
Anugrah and nobody else.

### 3.2 ANSWERED 27 Aug — both arms read the identical cleaned text

**Anugrah's decision: yes to both halves of `docs/16` verification-debt item 2**, now
marked CLOSED there.

- Every system reads `corpus/<doc>/document.txt` — front matter excluded, so the printed
  table of contents never reaches a model.
- `outline.json` remains the **yardstick** skeleton fidelity is scored against and is
  **never an input** to Pass 0, to the vanilla arm, or to anything else.
- Identical for both arms. No exceptions.

The reason, for the paper: this is the only configuration in which the skeleton is
derived rather than copied from the publisher, and the 82.2% recall at 0.0 pages
boundary error was measured under it. Any other choice invalidates that number.

### 3.3 Related, already escalated — the A1 reading

`docs/19` §3 records an open ambiguity: `docs/31` says A1 *"is architecturally vanilla
RLM"* and that A1 and the control are *"the same run"*, but vanilla RLM (root REPL +
flat sub-calls) and MARD (Pass 0/1 → plan → 120 builders) are different architectures,
not one boolean. If Anugrah has not answered this yet, ask again — it determines whether
what you build here is A1 itself or a separate baseline.

---

## 4. Tasks

### T1 — Vendor `Zhang_RLM`, and resolve the package collision first

**Critical:** `.vendor/rlm` currently holds `alexzhang13/rlm`, installed editable, and
`Zhang_RLM` is a **fork of the same package** — both provide `import rlm`. Installing
both editable means the last install silently wins and you will not be able to tell
which code ran. **Replace, do not add.**

Follow the established pattern in `scripts/bootstrap_rlm.sh` and
`scripts/bootstrap_replm.sh` (read both; they are careful about things that have already
cost this project a day):

- Repoint `bootstrap_rlm.sh` at `https://github.com/FalseAdvertising/Zhang_RLM`, **pinned
  at `62acf7b`** — pinned, not `pull --ff-only`, because a moving control library makes
  every measured number unattributable.
- Keep the venv guards, the `chflags nohidden` fix for the editable-`.pth`, and the
  import check run from `/` rather than the repo root. Each of those exists because of a
  real incident recorded in the script's own comments.
- `pip uninstall rlms` and remove the stale `.vendor/rlm` working copy before
  reinstalling, so there is exactly one `rlm` on the path. Verify:
  `cd / && python -c "import rlm; print(rlm.__file__)"` must point into the new vendor
  directory.
- Record the pinned SHA in `runs/_bootstrap/` as the existing script does.
- Leave `.vendor/replm` alone but note in `docs/18` that it is no longer the control.

**Do not copy `rlm/` source into this repo.** `.vendor/` is gitignored and vendoring as a
working copy is the deliberate existing pattern — the fork's own tests and examples matter,
not just the importable package.

### T2 — Verify the corpus before spending a token

```bash
python -m ingest.manifest corpus --document-id introcs   # added 27 Aug; must pass
cat corpus/introcs/parse_quality.md                       # must show 0 warnings
```

If `manifest.json` does not exist, the corpus predates provenance pinning — regenerate
with `scripts/fetch_corpus.sh introcs`, which fetches, verifies the source hash, parses,
and pins. Note `corpus/SOURCES.json` currently has `url`, `pdf_sha256` and
`retrieved_on` as `null`; the script prints the hash on first fetch and refuses to parse
until they are recorded. **Record them, commit, re-run.** Do not guess any of the three.

These three greps are the direct test for the bug that broke the last run:

```bash
grep -c "PART 1 PROBLEM SOLVING"     corpus/introcs/document.txt   # must be 0
grep -c "Introduction 9"             corpus/introcs/document.txt   # must be 0
grep -cE '^#{1,6} .*Chapter Outline' corpus/introcs/document.txt   # must be 14
```

**If any is wrong, stop.** Front-matter exclusion is broken and every downstream number
would be measuring the table of contents again.

### T3 — Write the vanilla arm as a module, not a script

Retire `run_file.py` as the entry point — it is a useful prototype, not a measured
harness. Add `eval/vanilla_rlm.py` (or extend `eval/`, which already holds
`frozen_subsets`) exposing something like:

```python
def run_vanilla(
    corpus_dir: Path,
    document_id: str,
    *,
    task_prompt: str,          # frozen, from §3.1
    model: str,
    max_iterations: int,
    max_concurrent_subcalls: int,
    seed_label: int,           # a run identifier, not a decoding seed
) -> VanillaResult: ...
```

It must:

1. **Call `ingest.manifest.verify_or_raise(corpus_dir / document_id)` first.** A measured
   run against an unverified corpus is not a measured run.
2. Read `corpus/<doc>/document.txt` — **never** the PDF, never `document.jsonl`, never
   `outline.json`.
3. Split on `[[page:N]]` into a `list[str]` and pass it as `prompt=pages`. Reuse
   `run_file.py`'s regex; do not re-invent chunking. Assert the chunk count is > 1 —
   silently falling back to one giant chunk is how this becomes a full-context baseline
   wearing an RLM label.
4. Pass the frozen task as `root_prompt`, as `run_file.py` already does.
5. Return the answer plus the usage numbers the library already provides.

### T4 — Wrap every run in `runlog`

All seven `docs/30` §1 fields, or it is not a number: task score, tokens in/out
separately, calls issued split by tier, cost, wall-clock (**both `max` and `Σ` over
sub-calls**), run identity, and a full config snapshot — model IDs, prompt-template
version, depth setting, active ablation, document, and the **vendored library's pinned
SHA**.

Zhang's library gives you most of this for free:
`on_subcall_start` / `on_subcall_complete` / `on_iteration_start` /
`on_iteration_complete` callbacks all carry depth, and `get_usage_summary()` returns
per-model call counts and token totals. Wire the callbacks into `RunLogger.log_call`
rather than reconstructing timings.

`RunLogger` writes `summary.json` with `status: "failed"` and a traceback on a crash.
Keep that: a hole in the matrix should explain itself.

### T5 — Cost, and the spend cap

`RLMConfig`-style cost fields default to zero in these libraries, so an unconfigured run
reports a cost of `0.0` that looks like a measurement. Feed rates from
`runlog.pricing.RateCard`, which refuses a rate older than 30 days. `runlog` reports cost
as `null`, never `0.0`, for an unpriced model — keep that asymmetry.

Export `MARD_SPEND_CAP_USD` or `SpendCap.from_env()` refuses to run. **The old `$780` is
void** — those were free Vertex credits, now stranded, and all money is out of pocket.
Use **`MARD_SPEND_CAP_USD=60`** for Phase A.

Cost calibration from the failed run: 359,498 input / 120,850 output tokens ≈ **$3.86**
at Sol rates. Output came in roughly **ten times** the projection in `docs/18` §10.
**Report your real token counts** so that section can be corrected with measured figures.

### T6 — Depth and concurrency

- **Depth:** Zhang's parameter is `max_depth`, default `1`, meaning root RLM + flat
  sub-calls. That is the base paper's primary reported condition and what the control
  runs at. Note this differs from `replm`'s `max_recursion_depth` — see §6.
- **Concurrency:** Zhang's library ships `max_concurrent_subcalls` (default `4`),
  threaded through the environment and semaphore-gated. **Use it. Do not hand-roll a
  throttle** — the last attempt at that produced incomplete responses and was
  reimplementing this parameter.
- Run at **≤70%** of the measured per-minute ceiling (`RATE_LIMIT_BUDGET.md` §3);
  retries draw from the same bucket as first attempts. Honour `Retry-After`; jittered
  backoff. **Log every 429** with its timestamp — a 429 is data, not noise.
- `max_iterations`: the failed run hit `30`, the library default, so it terminated on
  budget exhaustion rather than completion. If a clean run still hits the ceiling, that
  is a **finding to report**, not a number to raise quietly.

### T7 — Smoke, then measure

1. **Smoke:** ~20 pages of `document.txt`, one run, real model, verbose. Read the
   trajectory. Confirm no TOC lines, no mid-sentence titles, no "please paste the text"
   responses.
2. **One full run** on `introcs`, logged.
3. **Three repeats.** `CAMPAIGN_SEEDS = (11, 23, 42)` are run *identifiers*; variance
   comes from genuine repeats, because these endpoints do not expose deterministic
   decoding.

---

## 5. Traps

1. **Two packages named `rlm`.** T1. This is the one that will waste a day if missed —
   the failure is silent and the tests stay green.
2. **`root_prompt` is the objection a reviewer already has queued.**
   `RLM_BASELINE_SURVEY.md` §2.3 and `docs/01-ENVELOPE_VS_BASE_LIBRARY.md` both record
   that the library has a downward-injection slot and passes `root_prompt=None` to
   children, so expect *"you just used `root_prompt`."* Using it for the **root's task
   statement** is exactly what it is documented for and is fine. **MARD must never use
   `root_prompt` to carry the envelope** — that would collapse the upward/downward
   distinction the entire contribution rests on. Keep the envelope in the child prompt
   where `envelope/pass1.py` already puts it.
3. **Chunking silently collapsing to one chunk.** `run_file.py` falls back to `[text]`
   when it finds fewer than two page markers. On `document.txt` that would make the
   "vanilla RLM" arm a full-context baseline with an RLM label. Assert, don't hope.
4. **Reasoning-model parameters.** GPT-5-family endpoints require
   `max_completion_tokens` rather than `max_tokens` and **reject `temperature`**. Zhang's
   `_normalize_sampling_args` already renames the former, and `sampling_args` defaults to
   `{}` so temperature is never sent unless you add it. **Do not add it.** If you do,
   `RLMConfig.temperature` becomes dead config recorded in the manifest as though it
   applied, which corrupts the config snapshot.
5. **Windows/UTF-8.** `62acf7b` fixes missing `encoding="utf-8"` in the REPL's context
   loading across `local_repl.py`, `ipython_repl.py` and `docker_repl.py`. `document.txt`
   contains em-dashes and page markers, so on Windows the unfixed version crashes. This
   is why the fork is pinned at `62acf7b` and not at upstream.
6. **Truncation is a failure, not a low score.** `join_in_plan_order` already validates
   non-empty `span.text` per plan step and raises `IncompleteArtefactError`. Do not
   regress it and do not catch it to keep a run alive.
7. **`pypdf` vs PyMuPDF.** `run_file.py` imports `pypdf`. The corpus path does not need
   it. Do not let a PDF-reading code path survive in the measured harness at all — its
   existence is what caused the last failure.

---

## 6. What becomes obsolete — clean these up

Switching the control from `replm` to `Zhang_RLM` retires a list of hazards. Update the
docs so nobody defends against a trap that no longer exists:

| Recorded for `replm` | Status under `Zhang_RLM` |
|---|---|
| `max_recursion_depth=0` silently equals `1` (`sub_caller.py:96`) | **Gone.** Zhang's `max_depth=0` is meaningful — the root itself falls back to a plain LM (`rlm/core/rlm.py:350`) |
| Batched sub-calls bypass recursion before `a0ca553` | **Gone.** `_rlm_query_batched` (`local_repl.py:335`) routes through the same `subcall_fn` as single `rlm_query` |
| No `seed` parameter anywhere | **Gone.** `sampling_args` accepts `seed` (`base_lm.py:26`), verified carried through |
| No concurrency cap at all | **Gone.** `max_concurrent_subcalls=4` by default |
| `LanguageModel` protocol not satisfied by the client | **Gone.** `BaseLM` satisfies it — that is why `lm_builder.py` declared it structurally |
| Log depth as an `(enable_sub_calls, max_recursion_depth)` pair | **Superseded.** Zhang's equivalents are `max_depth` and `orchestrator` / sub-call settings — establish the correct pair and record what you find |

`docs/18` §5 and §5.1–§5.3, `docs/19` §5–§6 and `docs/20` §5 all describe `replm`
behaviour. Mark them as historical rather than deleting them — they are the record of
why the control library changed.

**Also still open, and unaffected by this switch:** the MARD↔library depth-numbering
off-by-one in `docs/18` §5.2 is `[UNVERIFIED]`, derived from documentation rather than
from `envelope/pass1.py`'s call structure. Re-derive it for Zhang's `max_depth` and
report what you find. Do not assume the `replm` mapping transfers.

---

## 7. Acceptance criteria

- [ ] §3.1 task string drafted and **signed off by Anugrah** before any matrix run.
- [ ] §3.2 answered on the record; §3.3 chased if still open.
- [ ] Exactly one `rlm` package importable; `cd / && python -c "import rlm; print(rlm.__file__)"`
      resolves into the new vendor directory. Pinned SHA `62acf7b` recorded in
      `runs/_bootstrap/`.
- [ ] `python -m ingest.manifest corpus --document-id introcs` passes.
- [ ] `parse_quality.md` shows **0 warnings**; all three greps in T2 return the expected
      values.
- [ ] `corpus/SOURCES.json` has a real `url`, `pdf_sha256` and `retrieved_on` for
      `introcs`.
- [ ] The harness reads `document.txt` only. **No PDF-reading code path exists in it.**
- [ ] Page split asserted `> 1` chunk; run log records the chunk count (expect ~916).
- [ ] Task passed via `root_prompt`; envelope **not** passed via `root_prompt` anywhere.
- [ ] Zero output titles carry a trailing page number or begin mid-sentence; zero
      responses ask a human to supply text.
- [ ] The output is explanations per `docs/30` §2 — not heading summaries, not a table
      of contents.
- [ ] `max_concurrent_subcalls` set from config and present in the run manifest; 429s
      logged with `Retry-After`.
- [ ] Cost non-zero and sourced from `RateCard`; `MARD_SPEND_CAP_USD` exported.
- [ ] Three logged runs under `runs/` with all seven `docs/30` §1 fields populated,
      variance reported across them.
- [ ] Real token counts reported back so `docs/18` §10 can be corrected from measurement
      rather than assumption.
- [ ] `ruff check`, `ruff format --check`, `mypy` clean; all existing tests pass; new
      code has tests.
- [ ] `docs/18` §4.2, `docs/19`, `docs/20`, `paper/main.tex` updated to name
      `Zhang_RLM` @ `62acf7b`; §6's obsolete traps marked historical.
- [ ] Nothing anywhere attributes the library choice to rate limits.

---

## 8. Rules that override your judgement

- **Feature freeze A was 23 Aug; results freeze A is 27 Aug.** A pipeline change
  invalidates every number measured before it. If you want to change a prompt, the
  Master Plan schema, or `ingest/`'s behaviour — **stop and ask Anugrah.**
- **3 repeats on every number, variance reported.** Non-negotiable.
- **A null result is publishable**, framed by the O4 structure-dependence boundary.
  Never tune toward a positive after the fact.
- **No number without a logged run. No citation without a verified row in
  `docs/40-LITERATURE_LOG.md`.** Mark anything unverifiable `[UNVERIFIED]` and surface
  it — never quietly assert it, never quietly drop it.
- **Escalate rather than invent.** Four workstreams run in parallel; a decision invented
  here becomes three different decisions elsewhere.
- **Report findings, instinct and options.** Anugrah wants everything surfaced, including
  things that look like your own mistakes. The last run's root causes were a default
  prompt string and a `pypdf` call — both invisible until someone read the file and said
  so out loud.
