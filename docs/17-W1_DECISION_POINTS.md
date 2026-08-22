# 17 — W1 decision points: the 16 Aug and 19 Aug triggers, resolved

**Status:** Decided 22 Aug 2026 · Decision owner: Anugrah Shetty (Track 1) · Type: ADR-style, per global `CLAUDE.md` Part 7 · Closes: `CONTEXT.md` line 322 and Risk #3 (line 452) · Read by: Track 2 and Track 3 before Feature freeze A

## Two triggers, not one

`CONTEXT.md` pre-authorised the same fallback twice, on two different conditions and two different dates. They have been conflated in conversation, and resolving them together is what makes tomorrow's freeze holdable.

| | Condition | Date | Status |
|---|---|---|---|
| **Trigger A** | "if Pass 0 is not producing a usable skeleton" → cut Pass 2, ship two-pass MARD in A (line 322) | Sun 16 Aug | **Resolved: Pass 0 is usable. Proceed.** |
| **Trigger B** | "Pass 1 concept/prerequisite extraction unreliable" → two-pass MARD for A, restore Pass 2 in W5 for B (Risk #3, line 452) | Wed 19 Aug | **Fires. Two-pass MARD for Manuscript A.** |

Both dates passed without the decision being made. This document makes them, six and three days late respectively, and records what the decision rests on.

## Trigger A — Pass 0 is usable

Decided on measured evidence, produced 22 Aug by `envelope/pass0.py` and scored by `envelope/fidelity.py`. The derived skeleton is compared against the PDF bookmark outline, which is used as **ground truth for grading, never as an input** — see `docs/16-PRIMARY_DOCUMENT.md`.

| Document | Sections | Recall vs outline | Mean start-page error |
|---|---|---|---|
| **`introcs` (primary)** | 120 | **82.2%** | **0.0 pages** |
| `physics1` | 143 | 67.7% | 0.06 pages |
| `axler` | 17 | 0.0% | — |

82.2% of the publisher's own chapter and section entries recovered from the document's text alone, with page boundaries agreeing exactly. That is a usable skeleton by any reading of the condition, and it is a number the paper can report rather than a claim it has to assume.

Three qualifications, stated because the decision rests on the first document only:

- **`axler`'s 0% is a real failure, left visible.** Its front-matter detection fell back to page 1, so its "skeleton" is the printed contents page. Stripping trailing page numbers in the fidelity matcher would have raised the score while hiding that. Not done: `CONTEXT.md` §3.4 forbids tuning toward a positive, and a metric adjusted until it flatters the thing it measures is worse than a bad score.
- **Most of Pass 0 is not a model call.** Titles, page ranges and the density estimate are arithmetic over Track 4's parse. Only *topic per section* needs Tier 1, and it is one call over the whole skeleton. Pass 0 is therefore cheaper and more reproducible than the plan assumed — a re-run changes the topics and nothing else.
- **The skeleton was over its stated budget at section granularity.** `CONTEXT.md` line 74 prices Pass 0's envelope at ~500 tokens; the 120-section skeleton renders at ~1,970. See the granularity decision below, which is what brings it back inside the budget.

## Trigger B — two-pass MARD for Manuscript A

**Pass 2, the targeted deep dive into concept-dense regions, is out of scope for Manuscript A. It returns in W5 for Manuscript B, where it was always scheduled.**

The condition asks whether Pass 1's extraction is reliable. As of 22 Aug that question is unanswerable, because Pass 1 was written today. Building it and freezing it on the same day means the answer arrives during W3's measurement week — where `docs/30-MEASUREMENT_PROTOCOL.md` §8 forbids changing the pipeline, so the answer could not be acted on. A trigger whose evidence cannot exist before the freeze should fire on the conservative side.

**What this costs, and what it does not.** Manuscript A's measurement matrix is untouched: one document × {vanilla RLM (=A1) · MARD full · flat-context negative control · A2 plan withheld} × 3 seeds, exactly as `docs/30-MEASUREMENT_PROTOCOL.md` §5 specifies. What changes is what "MARD full" *is* for Manuscript A — a two-pass configuration rather than three. That has to be stated in §3 and in the results table caption; reporting a two-pass run as three-pass would be the overclaim `CONTEXT.md` §4.3 exists to prevent.

The configuration is already a named condition rather than an improvisation. `docs/31-ABLATIONS.md` A4 defines depth 0 as "Pass 0 + Pass 1 only (no targeted deep dive) — a 'two-pass MARD' run, directly reusable if Track 1's 16 Aug decision point triggers the two-pass fallback." Manuscript A's MARD arm is A4's depth-0 cell. When W5 restores Pass 2, A's number remains a valid point on B's depth curve rather than becoming an orphan.

**Consequence for Feature freeze A:** it holds. The pipeline scope loses Pass 2 — pre-authorised — and the measurement scope loses nothing.

## Pass 1 granularity: chapters, not sections

**Pass 1 runs one call per chapter.** `introcs` has 14 numbered chapters against 120 sections.

`CONTEXT.md` line 75 prices Pass 1 at "~200 tokens/chapter", so chapters is what the plan costed. The section-granular alternative is 8.6× the call count, and — because the envelope carries the skeleton into every recursive call — 8.6× the envelope's own token cost, on every call. Sections remain the unit **Tier 2 dispatches on**, so builders still get fine-grained targets; only exploration is coarser.

Measured effect on the envelope: chapter-level renders at roughly 300 tokens against line 74's ~500 budget, where section-level rendered at ~1,970.

Two findings came out of implementing this, both on real documents, both recorded because each would have distorted a cost number:

- **The chapter count is not the outline's level-1 entry count.** I first assumed `introcs` had 18 chapters, from 18 level-1 bookmark entries. It has **14**; the other four are the contents, preface, "About OpenStax" and back matter.
- **`physics1` prints its Answer Key as a second "Chapter 1" to "Chapter 17"** on pp.895–959, after real content ends at p.895. Ungrouped, that gave 34 chapters for a 17-chapter book and would have doubled Pass 1's call volume on answers rather than exposition. `Chapter.is_repeat` marks a chapter whose number an earlier chapter already used; `content_chapters()` excludes them, and the excluded page ranges stay in `chapters.json` so the judgement is checkable. Current counts: `introcs` 14 of 15 explored, `physics1` 17 of 34, `axler` 9 of 10.

## What was built to these decisions

| Module | What it does |
|---|---|
| `ingest/sections.py` | Sections carrying the four `SourceSpan` fields PR #48 requires |
| `ingest/chapters.py` | Chapters from the sections' own numbering, with repeat-run detection |
| `envelope/skeleton.py` | Pass 0's structural map, with provenance as a field |
| `envelope/envelope.py` | The envelope, its growth semantics, and `stripped()` = ablation A1 |
| `envelope/pass0.py` | Skeleton extraction: deterministic half separate from the scout call |
| `envelope/pass1.py` | Chapter-by-chapter exploration, envelope carried into each call |
| `envelope/compile_plan.py` | Findings → Master Plan, sequenced and with reorder notes |
| `envelope/fidelity.py` | The derived skeleton scored against the PDF outline |

54 tests pass; `ruff check`, `ruff format --check` and `mypy` are clean.

**The single most important test in the repository** is `tests/test_pass1.py::test_a_later_chapters_prompt_contains_an_earlier_chapters_findings`, with `tests/test_envelope.py::test_child_envelope_carries_parent_findings` behind it. If the envelope stops flowing downward, MARD is vanilla RLM, every O3 number measures nothing, and **no other test would fail** — the pipeline would still run and still produce plausible output. `docs/01-ENVELOPE_VS_BASE_LIBRARY.md` is the argument; those two tests are the guard.

## Two things Pass 1 and the compiler deliberately refuse to do

**Pass 1 does not repair the model's output.** A concept naming a section outside its own chapter, an edge pointing at an undeclared concept, a `cross_reference` with no quote, a directive too short for the tier boundary — each is dropped and named in `pass1_trace.json`. Demoting an unsupported cross-reference to `inferred` would be the tempting fix and is the worst one: it launders an unfalsifiable claim into a plausible one, and `evidence` exists precisely so Track 3 can score document-asserted edges separately from model-inferred ones.

**The compiler refuses a cyclic graph rather than breaking it.** Which edge to drop is a judgement about the document; making it silently would put a fabricated dependency claim into the artefact O5 is scored on. `UnsequenceablePlanError` names the concepts involved.

## Consequences

### Positive
- Feature freeze A holds with Manuscript A's matrix intact.
- A's MARD arm is a defined cell of B's depth sweep, so the number survives into B.
- Pass 0's fidelity is now a reported measurement rather than an assumption.
- The envelope is inside its stated token budget at the granularity the plan costed.

### Negative — stated plainly
- **Manuscript A's headline claim is weaker than the design intended.** Two-pass MARD tests whether the envelope helps *exploration*; it does not test whether targeted deep dives pay for themselves. That was O3's more interesting half and it moves to B.
- **Pass 1 will be frozen the day it was written.** No soak time, no reliability evidence. If its extraction turns out unreliable, W3 measures an unreliable extractor and the finding is a limitations paragraph, not a fix.
- **The sequence is the lexicographically smallest topological order, not the minimum-displacement one.** Both are valid; they can differ in move count, and O5 counts moves. `envelope/compile_plan.py` documents this and it belongs in §3 rather than being left implicit.

### Risks
- `axler` cannot currently carry a usable skeleton. It is not the primary document and its O5 use is unaffected, but W5's corpus expansion has one fewer working candidate than the plan assumes.
- Chapter numbering is a heuristic over section titles. It fits `introcs` and `physics1` and partly fits `axler`. A W5 document that numbers differently will need the rule extended, and that is a pipeline change — after Feature freeze A it is out of scope for the manuscript the freeze protects.

## Verification debt opened

| # | Item | Status |
|---|---|---|
| 1 | Pass 1's reliability — the question Trigger B could not answer | [UNVERIFIED] — measured in W3, reported as a limitation if poor |
| 2 | `tests/test_compile_plan.py` restates `plan/validation.py`'s rules locally because `plan/` arrives with PR #48. Replace with a real `validate_master_plan` call the day it merges | Open — one line, and the local restatement rots the moment the boundary changes |
| 3 | `envelope/pass1.py::CONCEPT_ID` duplicates `plan.models.ConceptId`. A drift test guards it; an import would remove the need | Open, same trigger as #2 |
| 4 | Whether the lexicographic ordering choice materially changes O5's move count against a displacement-minimising order | [UNVERIFIED] — cheap to check once real plans exist |
| 5 | Two-pass framing written into §3 and every A results caption | Not started — Track 1, before the 3 Sep draft |
