"""Running header and footer removal, by page position rather than by regex.

Position beats pattern matching here for a reason worth recording: a regex tuned to
one book's footer ("Access for free at openstax.org") silently fails on the next
book and leaves 900 copies of a URL in the text a model is charged tokens to read.
Position generalises — a running header sits in the same narrow band at the top or
bottom of most pages, whatever it says.

Page numbers are normalised to a digit placeholder before counting repeats, because
"Chapter 3 | 141" and "Chapter 3 | 142" are the same header and must be recognised
as one repeated string, not 900 unique ones.
"""

from __future__ import annotations

import re
from collections import defaultdict

from ingest.blocks import Block

# Fraction of page height at the top and bottom treated as header/footer territory.
BAND_FRACTION = 0.08

# A string has to repeat on at least this many pages to count as running furniture.
#
# An absolute floor rather than only a share of the book, because running headers are
# often chapter-scoped: "32 1 - Introduction to Computer Science" repeats on the ~24
# pages of its chapter, which is 2.5% of a 939-page book. A fraction-only rule set
# high enough to protect real headings let every one of those through. Position in the
# header/footer band is what makes the low absolute floor safe: body headings do not
# sit in the top or bottom 8% of the page.
MIN_REPEAT_PAGES = 8
MIN_PAGE_FRACTION = 0.005

# Real content is rarely this short; long strings in the band are usually a
# paragraph that overflowed into it, and dropping them would lose content.
MAX_BOILERPLATE_CHARS = 120

DIGITS = re.compile(r"\d+")


def _normalise(text: str) -> str:
    return DIGITS.sub("#", text).strip().lower()


def _edge_block_ids(blocks: list[Block], page_heights: dict[int, float]) -> set[str]:
    """Ids of the single topmost and bottommost text block on each page, when in band.

    Being *in* the header band is not enough on its own. University Physics sets
    "Solution" and "Significance" as short blocks that often land inside the top or
    bottom 8% of a page, and a band-only rule deleted 400+ of them — real content
    headings, silently removed. A running header is not merely near the edge, it is
    the outermost block on the page. Requiring both conditions fixed that without
    losing the chapter-scoped headers the band rule was added to catch.
    """
    first_by_page: dict[int, Block] = {}
    last_by_page: dict[int, Block] = {}

    for block in blocks:
        current_first = first_by_page.get(block.page)
        if current_first is None or block.bbox[1] < current_first.bbox[1]:
            first_by_page[block.page] = block

        current_last = last_by_page.get(block.page)
        if current_last is None or block.bbox[3] > current_last.bbox[3]:
            last_by_page[block.page] = block

    edge_ids: set[str] = set()
    for page, height in page_heights.items():
        top_block = first_by_page.get(page)
        if top_block and top_block.bbox[1] <= height * BAND_FRACTION:
            edge_ids.add(top_block.block_id)

        bottom_block = last_by_page.get(page)
        if bottom_block and bottom_block.bbox[3] >= height * (1 - BAND_FRACTION):
            edge_ids.add(bottom_block.block_id)

    return edge_ids


def mark_boilerplate(blocks: list[Block], page_heights: dict[int, float]) -> list[Block]:
    """Re-label running headers and footers as kind='boilerplate'.

    Blocks are marked rather than deleted so the parse-quality report can state how
    much was removed and from where. A silent drop is unauditable, and
    ingest/__init__.py is explicit that this module's output is evidence.
    """
    edge_block_ids = _edge_block_ids(blocks, page_heights)

    occurrences: dict[str, set[int]] = defaultdict(set)
    for block in blocks:
        if block.block_id in edge_block_ids and len(block.text) <= MAX_BOILERPLATE_CHARS:
            occurrences[_normalise(block.text)].add(block.page)

    page_count = len(page_heights) or 1
    threshold = max(MIN_REPEAT_PAGES, page_count * MIN_PAGE_FRACTION)
    repeated = {key for key, pages in occurrences.items() if len(pages) >= threshold}

    marked: list[Block] = []
    for block in blocks:
        is_furniture = (
            block.block_id in edge_block_ids
            and len(block.text) <= MAX_BOILERPLATE_CHARS
            and _normalise(block.text) in repeated
        )
        if is_furniture:
            marked.append(
                Block(
                    block_id=block.block_id,
                    page=block.page,
                    kind="boilerplate",
                    level=None,
                    role=None,
                    text=block.text,
                    bbox=block.bbox,
                    font_size=block.font_size,
                )
            )
        else:
            marked.append(block)

    return marked
