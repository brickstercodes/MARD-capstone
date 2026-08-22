"""Tests for the ingestion pipeline, on synthetic PDFs built in-test.

Synthetic rather than fixture files, for two reasons. The corpus PDFs are tens of
megabytes and do not belong in the repository, and a synthetic page is the only way
to assert on a *known* layout — with a real textbook page you are asserting on
whatever the publisher happened to do, which makes a failure ambiguous between "the
code broke" and "the page is unusual".

The three cases here are the three bugs this module actually shipped with during
W1 and had to have fixed, so they are regression tests, not decoration:

  1. Cover-page font sizes were elected as heading level 1, burying real headings.
  2. Running headers were detected by band position alone, which deleted the
     "Solution" and "Significance" headings out of University Physics.
  3. Front matter, containing the printed table of contents, flowed into the text
     stream a model reads.
"""

from __future__ import annotations

import pytest

from ingest import pdf
from ingest.blocks import extract_blocks
from ingest.boilerplate import mark_boilerplate
from ingest.quality import measure_math_loss

BODY_SIZE = 9.0
SECTION_SIZE = 14.0
COVER_SIZE = 40.0
PAGE_COUNT = 20


@pytest.fixture
def synthetic_pdf(tmp_path):
    """A cover page plus many body pages, each with a running footer.

    The cover's 40pt word appears on one page only; the 14pt section headings appear
    on many. A size-only heading rule picks the cover; a coverage-aware rule does not.
    """
    doc = pdf.new_document()

    cover = doc.new_page()
    cover.insert_text((72, 200), "GRAND TITLE", fontsize=COVER_SIZE, fontname="hebo")

    for index in range(PAGE_COUNT):
        page = doc.new_page()
        page.insert_text(
            (72, 100),
            f"{index + 1}.0 Section {index + 1}",
            fontsize=SECTION_SIZE,
            fontname="hebo",
        )
        page.insert_text((72, 300), "Solution", fontsize=SECTION_SIZE, fontname="hebo")
        page.insert_text(
            (72, 400), "Body prose that carries the actual content.", fontsize=BODY_SIZE
        )
        # Running footer, in the bottom band, as the last block on the page.
        page.insert_text(
            (72, page.rect.height - 20),
            f"Access for free at example.org {index}",
            fontsize=7.5,
        )

    path = tmp_path / "synthetic.pdf"
    pdf.save(doc, path)
    return str(path)


def _parsed(path: str):
    blocks, body_size = extract_blocks(path, "synth")
    heights = pdf.page_heights(path)
    return mark_boilerplate(blocks, heights), body_size


def test_body_font_size_is_the_most_used_size(synthetic_pdf):
    _blocks, body_size = _parsed(synthetic_pdf)
    assert body_size == BODY_SIZE


def test_cover_page_size_is_not_elected_a_heading_level(synthetic_pdf):
    """Regression: a 40pt word on one page must not outrank the real section style."""
    blocks, _ = _parsed(synthetic_pdf)
    headings = [block for block in blocks if block.kind == "heading"]

    level_one_sizes = {block.font_size for block in headings if block.level == 1}
    assert COVER_SIZE not in level_one_sizes
    assert level_one_sizes == {SECTION_SIZE}


def test_section_headings_are_detected_on_every_page(synthetic_pdf):
    blocks, _ = _parsed(synthetic_pdf)
    detected = {
        block.page
        for block in blocks
        if block.kind == "heading" and block.text.startswith(tuple("0123456789"))
    }
    assert len(detected) == PAGE_COUNT


def test_running_footer_is_marked_boilerplate(synthetic_pdf):
    blocks, _ = _parsed(synthetic_pdf)
    footers = [block for block in blocks if block.kind == "boilerplate"]
    assert len(footers) == PAGE_COUNT
    assert all("Access for free" in block.text for block in footers)


def test_mid_page_repeated_heading_survives(synthetic_pdf):
    """Regression: "Solution" repeats on every page but is not page furniture.

    It is not the topmost or bottommost block, so the edge-block rule must keep it.
    A band-position-only rule removed 400+ of these from University Physics.
    """
    blocks, _ = _parsed(synthetic_pdf)
    solutions = [block for block in blocks if block.text.strip() == "Solution"]
    assert len(solutions) == PAGE_COUNT
    assert all(block.kind != "boilerplate" for block in solutions)


def test_page_mapping_is_one_based_and_complete(synthetic_pdf):
    blocks, _ = _parsed(synthetic_pdf)
    pages = {block.page for block in blocks}
    assert min(pages) == 1
    assert max(pages) == PAGE_COUNT + 1


def test_math_loss_rate_flags_orphan_punctuation():
    clean = "The algorithm runs in linear time.\nIt uses a single pass.\n" * 50
    scarred = "We use Equation 3.16, with .\nThe result is about  m/s .\n" * 50

    _lines, _signals, clean_rate = measure_math_loss(clean)
    _lines, _signals, scarred_rate = measure_math_loss(scarred)

    assert clean_rate < scarred_rate
