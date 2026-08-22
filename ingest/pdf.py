"""The single place this package touches PyMuPDF's untyped surface.

PyMuPDF ships `py.typed` with inline annotations and no stub files, so what mypy
sees depends on the wheel build. On Python 3.14 with mypy 2.3.0, `pymupdf.Document`
is reported as neither iterable nor a typed constructor; on 3.11 the same version
checks clean. Eleven strict-mode errors across three modules came from that
difference alone.

Two decisions keep it from recurring:

- **Pages are reached by index, never by iterating the document.** `doc[index]` is
  the one access pattern that types identically across builds. `for page in doc` is
  more natural to read and is the reason six of those eleven errors existed.
- **The untyped-constructor exemption lives in `pyproject.toml`, scoped to this
  module**, rather than as inline `# type: ignore` comments. `strict = true` turns on
  `warn_unused_ignores`, so an ignore that a 3.14 toolchain needs becomes an error on
  a 3.11 one — the suppression would break whichever environment did not need it. A
  module-scoped override is version-independent and states its reason in one place.

Nothing here does any parsing. If a function in this file grows logic, it belongs in
`blocks.py` or `quality.py` instead.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pymupdf


def open_document(path: str) -> Any:
    """Open a PDF. Returns Any because the constructor is untyped in some builds."""
    return pymupdf.open(path)


def new_document() -> Any:
    """An empty in-memory document, for building synthetic fixtures in tests."""
    return pymupdf.open()


def save(doc: Any, path: Any) -> None:
    """Write an in-memory document to disk. Test fixtures only."""
    doc.save(path)


def page_count(doc: Any) -> int:
    return int(doc.page_count)


def pages(doc: Any) -> Iterator[tuple[int, Any]]:
    """Yield (1-based page number, page) by index.

    One-based because every page number this project reports — in `SourceSpan`, in the
    `[[page:N]]` markers, in W7's provenance spot-checks — is the number a reader would
    cite. Converting at the boundary means no caller has to remember to add one.
    """
    for index in range(page_count(doc)):
        yield index + 1, doc[index]


def page_heights(path: str) -> dict[int, float]:
    doc = open_document(path)
    return {number: float(page.rect.height) for number, page in pages(doc)}


def raw_text(doc: Any) -> str:
    """Every page's text, joined. Used for extraction-quality measurement only."""
    return "\n".join(str(page.get_text("text")) for _number, page in pages(doc))
