# Parse quality — physics1

Source: `university-physics-volume-1_-_WEB.pdf`
Pages: 959 · body font size: 9.0pt

## Extraction

| Metric | Value |
|---|---|
| Extractable characters | 2,087,384 |
| After boilerplate removal | 2,032,210 |
| Removed as running header/footer | 29,643 |
| Blocks by kind | {'front_matter': 145, 'boilerplate': 1072, 'body': 11207, 'caption': 795, 'heading': 1081} |
| Body begins on page | 17 (145 front-matter blocks held back) |
| Headings by level | {'level_3': 143, 'level_4': 922, 'level_1': 9, 'level_2': 7} |
| Pages with no detected heading | 341 |
| Pages with almost no text | 34 |

## Dropped-formula scars (measured on raw extraction, not on our blocks)

| Metric | Value |
|---|---|
| Raw non-empty lines | 41,581 |
| Orphan-punctuation rate | **113.5/1k lines** (warn above 50) |
| Raw signal counts | {'orphan_punctuation': 4720, 'line_ends_in_operator': 144, 'line_ends_in_connective': 117, 'lone_symbol_line': 688} |

## Structural signals

| Metric | Value |
|---|---|
| PDF outline entries | 198 |
| Outline max depth | 2 |
| Pages outside outline coverage | 0 |
| Ground-truth blocks tagged | {'learning_objectives': 99, 'check_understanding': 170, 'key_terms': 17, 'summary': 19, 'review_questions': 34} |

## Warnings

- Orphan-punctuation rate 113.5/1k lines exceeds the 50/1k calibration threshold. Inline formulae are being dropped by text extraction. Do not use this document for the primary quality comparison: the loss is content, not formatting, and it will masquerade as a difference between systems.

## What these numbers are not

Every figure above is a heuristic over PDF text-extraction output. The orphan-punctuation rate undercounts: a display equation that vanishes without leaving punctuation behind is invisible to it, and its threshold is calibrated against three files, not validated. `pages_with_no_heading` counts pages, not sections, so a long section reads as many headingless pages. Treat all of it as flags for a human to check, not as measurements to report.
