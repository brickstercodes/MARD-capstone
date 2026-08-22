# Parse quality — introcs

Source: `Introduction_To_Computer_Science_-_WEB.pdf`
Pages: 939 · body font size: 9.0pt

## Extraction

| Metric | Value |
|---|---|
| Extractable characters | 2,507,564 |
| After boilerplate removal | 2,432,812 |
| Removed as running header/footer | 44,983 |
| Blocks by kind | {'front_matter': 216, 'boilerplate': 1178, 'caption': 574, 'heading': 1403, 'body': 7315} |
| Body begins on page | 19 (216 front-matter blocks held back) |
| Headings by level | {'level_1': 120, 'level_4': 902, 'level_3': 378, 'level_2': 3} |
| Pages with no detected heading | 323 |
| Pages with almost no text | 25 |

## Dropped-formula scars (measured on raw extraction, not on our blocks)

| Metric | Value |
|---|---|
| Raw non-empty lines | 34,772 |
| Orphan-punctuation rate | **30.3/1k lines** (warn above 50) |
| Raw signal counts | {'orphan_punctuation': 1052, 'line_ends_in_operator': 385, 'line_ends_in_connective': 13, 'lone_symbol_line': 462} |

## Structural signals

| Metric | Value |
|---|---|
| PDF outline entries | 129 |
| Outline max depth | 2 |
| Pages outside outline coverage | 6 |
| Ground-truth blocks tagged | {'learning_objectives': 61, 'key_terms': 14, 'review_questions': 28, 'references': 1, 'summary': 1} |

## Warnings

None raised by the checks in `ingest/quality.py`.

## What these numbers are not

Every figure above is a heuristic over PDF text-extraction output. The orphan-punctuation rate undercounts: a display equation that vanishes without leaving punctuation behind is invisible to it, and its threshold is calibrated against three files, not validated. `pages_with_no_heading` counts pages, not sections, so a long section reads as many headingless pages. Treat all of it as flags for a human to check, not as measurements to report.
