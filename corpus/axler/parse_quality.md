# Parse quality — axler

Source: `LADR4e.pdf`
Pages: 404 · body font size: 10.5pt

## Extraction

| Metric | Value |
|---|---|
| Extractable characters | 770,296 |
| After boilerplate removal | 737,844 |
| Removed as running header/footer | 32,452 |
| Blocks by kind | {'body': 8819, 'boilerplate': 607, 'heading': 17, 'caption': 1} |
| Body begins on page | 1 (0 front-matter blocks held back) |
| Headings by level | {'level_1': 17} |
| Pages with no detected heading | 398 |
| Pages with almost no text | 0 |

## Dropped-formula scars (measured on raw extraction, not on our blocks)

| Metric | Value |
|---|---|
| Raw non-empty lines | 19,990 |
| Orphan-punctuation rate | **87.8/1k lines** (warn above 50) |
| Raw signal counts | {'orphan_punctuation': 1756, 'line_ends_in_operator': 402, 'line_ends_in_connective': 0, 'lone_symbol_line': 681} |

## Structural signals

| Metric | Value |
|---|---|
| PDF outline entries | 168 |
| Outline max depth | 3 |
| Pages outside outline coverage | 0 |
| Ground-truth blocks tagged | {} |

## Warnings

- Orphan-punctuation rate 87.8/1k lines exceeds the 50/1k calibration threshold. Inline formulae are being dropped by text extraction. Do not use this document for the primary quality comparison: the loss is content, not formatting, and it will masquerade as a difference between systems.
- No learning-objective or key-terms blocks found. docs/30-MEASUREMENT_PROTOCOL.md section 2 scores task quality against document-native ground truth of exactly this kind, so this document cannot carry the primary task-score measurement.
- Front matter not detected, so the printed table of contents (if any) is still in document.txt. A model reading it receives the publisher's chapter list without exploring — see ingest/outline.first_content_page.

## What these numbers are not

Every figure above is a heuristic over PDF text-extraction output. The orphan-punctuation rate undercounts: a display equation that vanishes without leaving punctuation behind is invisible to it, and its threshold is calibrated against three files, not validated. `pages_with_no_heading` counts pages, not sections, so a long section reads as many headingless pages. Treat all of it as flags for a human to check, not as measurements to report.
