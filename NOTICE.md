# Third-party material

This repository's own source is MIT licensed (see `LICENSE`). It incorporates
and depends on material under other terms, recorded here so that a reader does
not have to infer them.

## Vendored code

`.vendor/rlm/` — the reference implementation of *Recursive Language Models*
(Zhang, Kraska & Khattab, arXiv:2512.24601), **MIT licensed**. It is not
committed to this repository; `scripts/bootstrap_rlm.sh` fetches it at the
pinned commit. The vendored copy retains its own `LICENSE`.

## Corpus documents

Source PDFs are **not redistributed here**. `corpus/SOURCES.json` records, for
each document, the publisher's own book-level licence, the URL it was retrieved
from, the SHA-256 of the exact file retrieved, and the retrieval date;
`scripts/fetch_corpus.sh` reproduces the corpus from the publishers and refuses
to parse on a hash mismatch.

| Document | Publisher | Licence |
|---|---|---|
| *Introduction to Computer Science* | OpenStax / Rice University | CC BY 4.0 |
| *Linear Algebra Done Right*, 4th ed. | Sheldon Axler | CC BY-NC |
| *University Physics* Volume 1 | OpenStax | CC BY-NC-SA 4.0 |

Licences are read from each publisher's book-level page, never from a chapter
footer — `introcs` is the live example of why: its book-level page states
CC BY 4.0 while individual chapter footers state CC BY-NC-SA.

## Evaluation subsets

`eval/frozen_subsets/` contains subsets derived from OOLONG (Bertsch et al.,
arXiv:2511.02817) and BrowseComp-Plus, under those benchmarks' own terms. See
`eval/frozen_subsets.md` for how each was generated and frozen.
