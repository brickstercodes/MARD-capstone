# 16 — Primary document selection and W1 ingestion

**Status:** Decided 22 Aug 2026 · Decision owner: Anugrah Shetty (Track 1, acting on Track 4's W1) · Type: ADR-style, per global `CLAUDE.md` Part 7 · Closes: issue #29 definition-of-done items 1–3 · Supersedes: nothing

## Decision

**`introcs` — OpenStax *Introduction to Computer Science* — is the primary document for Manuscript A.**

`physics1` (OpenStax *University Physics Volume 1*) and `axler` (*Linear Algebra Done Right*, 4e) are parsed and retained for W5's corpus expansion, but **neither may carry the primary task-score measurement.** Reasons below.

Track 4's W1 work was executed by Track 1 on 22 Aug because Track 4 could not complete it, and #29 is a hard blocker on Pass 0. This is a resourcing exception, recorded so it is not mistaken for a change of ownership.

## Context

`CONTEXT.md` line 178 fixes the corpus as openly licensed only and names OpenStax, OSTEP and Axler, partly because "OpenStax titles carry machine-readable learning objectives, glossaries and answer keys". `docs/30-MEASUREMENT_PROTOCOL.md` §2 then makes those signals load-bearing: task quality is scored against document-native ground truth — glossary terms, per-chapter learning objectives, in-text cross-references — extracted programmatically, never expert-annotated.

So the primary document is not a free choice. It must actually contain those signals, and it must survive PDF text extraction without losing content.

## Evidence

All figures produced by `ingest/` on 22 Aug 2026 and reproducible with `python -m ingest.cli <pdf> --doc-id <id>`. Full per-document reports are in `corpus/<doc_id>/parse_quality.md`.

| | `introcs` | `physics1` | `axler` |
|---|---|---|---|
| Pages | 939 | 959 | 404 |
| Characters kept after cleaning | 2,432,812 | 2,032,210 | 737,844 |
| PDF outline entries / max depth | 129 / 2 | 198 / 2 | 168 / 3 |
| Headings detected | 1,403 | 1,081 | 17 |
| Learning-objective blocks | **61** | **99** | 0 |
| Key-terms blocks | **14** | **17** | 0 |
| Review-question blocks | 28 | 34 | 0 |
| Orphan-punctuation rate (per 1k lines) | **30.3** | **113.5** | **87.8** |
| Warnings raised | **0** | 1 | 3 |

**No OCR is needed on any of the three.** Every page carries a text layer; the three books yield 2.6M, 2.1M and 0.74M extractable characters respectively. This closes the question of whether to introduce PaddleOCR or an equivalent: it would replace perfect text with imperfect text, and — decisively — OCR errors in glossary terms would corrupt the reference set that §2's task score is measured against, silently and unfixably after Feature Freeze A.

### Why `physics1` is disqualified as primary

Its orphan-punctuation rate is 113.5 per 1,000 lines against `introcs`'s 30.3. That metric counts punctuation left stranded where a formula used to be, and the qualitative reading confirms what it implies. From page 141 of the source:

> "To find the time when the position is −98 m, we use Equation 3.16, with ."

The equation is gone. This is content loss, not formatting loss, and it is not uniform across systems under test — a condition that reads more of the document encounters more of the damage. Left as primary, it would manufacture a difference between MARD and vanilla RLM that has nothing to do with either.

### Why `axler` is disqualified as primary

Two independent reasons. It carries **no** learning objectives and no key-terms sections, so §2's ground truth cannot be extracted from it at all. And its orphan-punctuation rate is 87.8/1k. It remains the strongest candidate for the **O5 dependency-ordering case study** — a 3-level outline and 135 numbered theorem and definition labels give it the most explicit prerequisite structure of the three — but O5 is scored separately from task quality (`docs/30-MEASUREMENT_PROTOCOL.md` §3), so that use is unaffected.

## Two confounds this work surfaced — Track 1 decisions, not closed here

Both are cases where structure reaches a model without the model having derived it. `docs/00-CLAIM.md` claims that a metadata envelope built from reading roughly 3–5% of a document makes exploration structure-aware. If the structure arrives by another route, the paper reports the publisher's work as MARD's.

**1. The PDF bookmark outline.** All three books ship one (129/198/168 entries). It is a ready-made chapter and section tree. `ingest/` writes it to a **separate** `outline.json` with an explicit `provenance: pdf_bookmark_outline` field and never merges it into the text stream, precisely so that using it has to be a decision. **Open: may Pass 0 read `outline.json`?** If yes, vanilla RLM (A1) must receive the identical input or the O3 comparison is not isolated.

**2. The printed table of contents, which is inside the body text.** Subtler and easier to miss, because it arrives through the ordinary text channel. `introcs` prints its full chapter list on page 7; a model reading the first pages gets the skeleton for free. `ingest/` detects front matter via the first numbered chapter entry, marks those blocks `kind: front_matter`, keeps them in `document.jsonl`, and **excludes them from `document.txt`**. `axler` has no numbered chapter entry, so front-matter detection falls back to page 1 and raises a warning rather than guessing. **Open: confirm that excluding front matter is what Track 1 wants, and that A1 gets the same treatment.**

## What was produced

Per document, under `corpus/<doc_id>/`:

| Artefact | Contents |
|---|---|
| `document.jsonl` | One block per line: `block_id`, `page`, `kind`, `level`, `role`, `text`, `bbox`, `font_size` |
| `document.txt` | Single marked-up stream — ATX heading markers, `<!-- role:… -->` tags, `[[page:N]]` stamps, boilerplate and front matter excluded |
| `outline.json` | Publisher bookmark tree with page spans and a provenance warning |
| `parse_quality.json` / `.md` | The evidence report |

Code in `ingest/` (`blocks`, `boilerplate`, `outline`, `quality`, `cli`), tests in `tests/test_ingest.py`.

**Verification performed:** 1,200 randomly sampled blocks across the three documents were checked to appear on the page they claim. 1,199 passed; the single failure is a symbol-index line in `axler` where whitespace normalisation differs, not a mapping error. `ruff check`, `ruff format --check` and `mypy` are clean; 7 tests pass.

Three defects were found and fixed during the day, and each has a regression test, because each would have degraded results silently rather than failing loudly:

1. Cover-page font sizes were elected heading level 1, burying the real section style — only 7 headings were detected in a 939-page book. Fixed by requiring a heading size to appear on a minimum number of pages and to be predominantly bold.
2. Running-header removal keyed on page-band position alone, which deleted 417 `Solution` and `Significance` headings from `physics1` — real content. Fixed by additionally requiring the block to be the topmost or bottommost on its page.
3. Front matter, including the printed table of contents, flowed into the text stream (confound 2 above).

## Consequences

### Positive
- `introcs` raises zero parse warnings, which is a cleaner starting position than the plan assumed.
- 61 learning-objective and 14 key-terms blocks are already located and tagged, so Track 4's W2 ground-truth extraction starts from marked boundaries rather than re-deriving them.
- Page mapping is verified, satisfying #29 DoD item 2 and W7's provenance spot-checks.

### Negative — stated plainly
- **The corpus is now effectively two usable documents plus one restricted one**, against `CONTEXT.md` §2.2's four. W5's expansion to four documents needs two more openly licensed candidates that pass the same checks, and formula-dense texts are likely to fail them. This should be sized before W5, not discovered in it.
- The orphan-punctuation threshold (50/1k lines) is calibrated against these three files only. It is a flag for a human, not a validated measurement, and the report says so.
- Heading levels are not semantically uniform: in `introcs`, level 1 covers both chapter and section titles, and level 4 is contaminated with contents-page lines. Usable as markers; not usable as a semantic hierarchy without further work.

### Risks
- `axler` yields 17 headings across 404 pages, so any structural marker on it is weak. If it becomes an O5 document, its structure must come from the outline (confound 1) and that dependency must be stated in the paper.
- Committing ~16 MB of derived corpus artefacts to git is a repository-hygiene decision nobody has made. The files are on disk; whether they are tracked, git-lfs'd, or regenerated from a checksum manifest is open.

## Verification debt opened

| # | Item | Status |
|---|---|---|
| 1 | Two further openly licensed documents that pass the parse-quality checks, needed for W5 | Not started |
| 2 | Whether excluding front matter and withholding `outline.json` is what Pass 0 should see, and that A1 is treated identically | **Open — Track 1, blocks Pass 0** |
| 3 | Whether the 50/1k orphan-punctuation threshold generalises beyond these three files | [UNVERIFIED] |
| 4 | Whether `introcs` level-4 headings should be reclassified before Track 3 builds against the markers | Open — cheap now, expensive after Feature Freeze A |
