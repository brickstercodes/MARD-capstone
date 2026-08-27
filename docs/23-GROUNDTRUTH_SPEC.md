# 23 — Document-native ground truth: what to extract, and what it costs

**Status:** Costed 27 Aug 2026 against `corpus/introcs/` · Owner: Track 1 (Anugrah Shetty,
now holding both arms) · **Implements** `docs/30-MEASUREMENT_PROTOCOL.md` §2 and §3

`docs/30` §2 freezes two things and leaves one open. Frozen: the ground-truth **source**
(document-native, extracted programmatically, never expert-annotated) and the evaluated
**modality** (explanations only). Open, and explicitly Track 3's: the scoring function.

This document costs each source against the real corpus so the scope decision is made on
measurement rather than on how the week feels.

---

## 1. Why not LLM-generated ground truth

Considered and **rejected** 27 Aug: giving the textbook to three fresh frontier-model
sessions, extracting concepts and prerequisites from each, and majority-voting the result.

Three reasons, in order of severity.

**It is circular.** The system under test is a language model extracting concepts and
prerequisite relations from a textbook. That proposal makes the *reference* a language
model extracting concepts and prerequisite relations from the same textbook. Agreement
between them measures model–model agreement, not correctness, and any bias the two share
inflates the score invisibly. It is the first thing a reviewer attacks and there is no
recovery from it.

**Majority voting does not rescue it.** Voting reduces error only when errors are
*independent*. Three samples from one model share training data, architecture and prompt,
so they fail in the same places — the same implicit prerequisites missed, the same
over-weighting of explicitly-headed material. Correlated errors reinforce under a vote
rather than cancelling, and high agreement then reads as high accuracy with no way to
distinguish the two.

**It costs the sentence that makes the evaluation credible.** `docs/30` §2's whole
argument is *"extracted programmatically by Track 4, never expert-annotated. No ethics
approval is implied or needed."* `CONTEXT.md` §2.1 cut expert Likert evaluation
**permanently** for that reason. Model-generated ground truth is non-reproducible
(non-deterministic, closed model, versions move), is annotation by an unauditable judge,
and is not document-native in any sense — it is model-native.

**The legitimate version**, if a second signal is wanted: a **blind pairwise preference
study**. Twenty matched explanation pairs, one per arm, identifying markers stripped, sides
shuffled, a judge picks the better one. Reported as an *LLM-judge preference*, never as
ground truth, with the judge's model family disclosed alongside the system's. The blinding
is what makes it admissible; without it there is nothing there.

---

## 2. What is already on disk

Verified 27 Aug by reading `corpus/introcs/document.jsonl`. `docs/16` was right that
extraction "starts from marked boundaries rather than re-deriving them":

| `role` tag | Blocks | Content shape |
|---|---|---|
| `learning_objectives` | **61** | Marker block, then `•`-delimited bullets in following body blocks |
| `key_terms` | **14** | Marker block, then a **run-on glossary with no delimiters** |
| `review_questions` | 28 | Marker block, then questions |
| `summary` | 1 | — |
| `references` | 1 | — |

The tagged block is the **heading only** — e.g. `"Learning Objectives By the end of this
section, you will be able to:"`. The items live in the untagged body blocks that follow,
up to the next heading or role marker.

---

## 3. Source by source

### 3.1 Learning objectives — **do this one**

Effort **30–45 min**. Confidence **high**.

Walk forward from each of the 61 markers, collecting body blocks until the next heading or
role marker, then split on `•`. Observed content:

```
• Discuss the history that led to the creation of computer science as a field
• Define computer science
• Assess what computer science can do, as well as what it should not do
```

This becomes the task-score reference set for Manuscript A.

### 3.2 Cross-references — **do this one**

Effort **45–60 min**. Confidence **high**.

Regex over `document.txt` for in-text references — *"as we saw in Chapter N"*, *"see
Chapter N"*, *"in Section N.M"* — classified forward or backward by comparing the target's
page range (from `chapters.json` / `sections.json`) against the citing page.

Produces `docs/30` §3's metric: **forward-reference violations**, counted for book order
and for Master Plan order.

**Score against references extracted from the text, never against the edges the model
emitted.** The latter is circular in the same way §1 is.

### 3.3 Key terms — **defer**

Effort **1.5–2.5 h**. Confidence **medium**, with one unverified dependency.

The glossary is run-on, term and definition concatenated with no separator:

> `adversarial attack sample input (e.g., an image) that is designed to cause a system to
> behave problematically algorithm sequence of precise instructions artificial intelligence
> (AI) development of computer functions to perform tasks…`

It **is** strictly alphabetical, which makes alphabetical segmentation tempting.
**It does not work.** Greedy splitting fails immediately: after `algorithm`, the next word
`sequence` is also alphabetically later, so the boundary is ambiguous. A dynamic program
with priors on term and definition length would do better — but it is a heuristic that
**cannot be validated without ground truth**, which is the problem being solved. Do not
take this route.

**Take the bold-span route instead.** Glossary terms are typeset bold, definitions are not.
PyMuPDF is already a dependency and `ingest/pdf.py` is already the single place that
touches it; `page.get_text("dict")` exposes font per span, so within the key-terms page
ranges the terms are the bold spans. Verifiable — bold is bold — and roughly 40 lines.

> **[UNVERIFIED] · 10-minute check.** The PDF is not on disk (`corpus/raw/` is gitignored),
> so this could not be confirmed: **does the OpenStax PDF use a distinct bold font face for
> glossary terms, rather than a synthesised weight?** Almost certainly yes, but check it the
> moment the PDF is re-fetched. It decides whether this source costs 1.5 h or is abandoned.

### 3.4 Review questions — not in scope

28 blocks, but `docs/30` §2 fixes the modality as explanations. Questions are neither a
reference set for explanation coverage nor an evaluated output. Manuscript B, if ever.

---

## 4. The scoring function — Track 3's decision, and it costs the most

Effort **1–1.5 h** once chosen. The choice matters more than the implementation.

`"Define computer science"` will not appear verbatim in a generated explanation, so
matching needs a decision:

| Option | Trade |
|---|---|
| Keyword overlap | Crude. Defensible if stated plainly |
| **Stemmed token-set overlap, stated threshold** | **Recommended.** Cheap, deterministic, and a reviewer can re-run it with no API key |
| Embedding similarity | Better recall, but it puts a **second model inside the measurement** — the same hazard as §1 in more respectable clothing |

Whatever is chosen, **report raw counts alongside the threshold** so the number survives a
reviewer who disagrees with the threshold.

---

## 5. Totals, and where this sits in the schedule

| Scope | Effort |
|---|---|
| Objectives + cross-references + scorer + tests | **3–4 h** |
| …plus key terms via bold spans | **5–6.5 h** |

**The schedule cost is close to zero**, because the extractor does not compete with the
runs. The measurement matrix is wall-clock bound — twelve runs, mostly waiting — and
scoring happens against artefacts already on disk. So:

- **Cross-references** — Friday evening, alongside the O5 metric it produces.
- **Objectives + scorer** — Saturday morning, written while the matrix executes.
- **Key terms** — only if the §3.3 check passes and Saturday afternoon has slack.

---

## 6. What §4 of the paper must say

A restriction stated is fine; a restriction implied is not. The Experimental Setup section
must name **which of `docs/30` §2's ground-truth sources were used and which were not** —
learning objectives and in-text cross-references yes, glossary terms deferred — and give the
matching function and threshold explicitly. Anything less reads as though the full reference
set was scored.

---

## 7. What landed, 27 Aug 2026

Implemented per §5's Friday/Saturday scope. 189 tests pass; `ruff format`, `ruff check` and
`mypy` clean repo-wide.

- **`ingest/groundtruth.py`**
  - `extract_learning_objectives` (§3.1) — walks forward from each `learning_objectives`
    marker, stopping at the first heading, role marker, **or unbulleted body block**. That
    last guard fixes a real corpus bug caught during the build: bullet blocks are immediately
    followed by plain prose, which would otherwise have leaked in as bogus objectives. A
    corpus-shape regression test now covers it.
  - `extract_cross_references` (§3.2) — regexes `document.txt` for in-text `Chapter N`
    mentions, classifying forward / backward / same-chapter **against book order only**.
- **`eval/groundtruth_scoring.py`** — stemmed token-set overlap (§4), recall-based against the
  short reference. `DEFAULT_THRESHOLD` is commented as a **placeholder pending Track 3
  sign-off**, since §4 makes the scoring-function choice Track 3's call.
- **Tests** for both, plus the corpus-shape regression test.

### Blocked, and what it blocks

**Master Plan order cannot be classified yet.** `corpus/introcs/master_plan_trace.json`
reports `compiled: false` — no plan has been compiled for `introcs`, so there is nothing to
compare book order against. **`docs/30` §3's before/after forward-reference violation metric
therefore depends on the MARD arm producing a validated Master Plan first.** Until then only
the book-order baseline half of the metric exists. This is a sequencing dependency, not a
defect: it clears the moment Pass 1 runs end-to-end.

**Key terms (§3.3) remains deferred**, still blocked on the `[UNVERIFIED]` bold-face check
against a PDF that is not on disk.
