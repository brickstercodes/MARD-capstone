"""Entry point: one PDF in, four artefacts out, under corpus/<doc_id>/.

Kept thin on purpose (global CLAUDE.md Part 4: "keep entry points thin") — it wires
the four steps together and owns the output layout, nothing else.

Artefacts, and why each exists separately rather than as one bundle:

  document.jsonl      Page-mapped blocks. The machine-readable parse. One JSON object
                      per line so a 900-page book can be streamed rather than loaded.
  document.txt        The same content as a single marked-up stream, for Pass 0 to
                      read and for a human to eyeball. Headings carry ATX markers and
                      every page break is stamped, so provenance survives in plain text.
  outline.json        The publisher's bookmark tree. SEPARATE FILE, with a provenance
                      field, because feeding it to Pass 0 would mean reporting the
                      publisher's table of contents as MARD's derived skeleton. See
                      ingest/outline.py for the full argument.
  parse_quality.json  The evidence report, plus a .md rendering of it.
  parse_quality.md

Usage:
    python -m ingest.cli <pdf-path> --doc-id introcs --out-dir corpus
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pymupdf

from ingest.blocks import Block, extract_blocks
from ingest.boilerplate import mark_boilerplate
from ingest.outline import first_content_page, read_outline
from ingest.quality import build_report, render_markdown

PAGE_MARKER = "[[page:{page}]]"

EXCLUDED_FROM_TEXT_STREAM = frozenset({"boilerplate", "front_matter"})


def _mark_front_matter(blocks: list[Block], content_start_page: int) -> list[Block]:
    """Re-label everything before the first chapter as front matter.

    Marked rather than deleted, and excluded from document.txt rather than dropped
    from document.jsonl, because the front matter contains the printed table of
    contents — see ingest/outline.first_content_page for why that is a confound and
    not just noise. Someone may legitimately want it back; nobody should get it by
    default without noticing.
    """
    if content_start_page <= 1:
        return blocks

    return [
        Block(
            block_id=block.block_id,
            page=block.page,
            kind="front_matter",
            level=None,
            role=None,
            text=block.text,
            bbox=block.bbox,
            font_size=block.font_size,
        )
        if block.page < content_start_page and block.kind != "boilerplate"
        else block
        for block in blocks
    ]


def _page_heights(path: str) -> dict[int, float]:
    doc = pymupdf.open(path)
    return {index + 1: page.rect.height for index, page in enumerate(doc)}


def _render_text_stream(blocks: list[Block]) -> str:
    """Blocks to a single marked-up string, boilerplate dropped, pages stamped.

    Page markers are emitted even for pages whose text was entirely boilerplate, so
    the marker sequence is gapless and a reader can always tell which page a line
    came from by scanning backwards.
    """
    parts: list[str] = []
    current_page = None

    for block in blocks:
        if block.page != current_page:
            parts.append(f"\n{PAGE_MARKER.format(page=block.page)}\n")
            current_page = block.page

        if block.kind in EXCLUDED_FROM_TEXT_STREAM:
            continue
        if block.kind == "heading":
            marker = "#" * (block.level or 1)
            role = f" <!-- role:{block.role} -->" if block.role else ""
            parts.append(f"\n{marker} {block.text}{role}\n")
        else:
            parts.append(block.text)

    return "\n".join(parts).strip() + "\n"


def ingest_document(pdf_path: str, doc_id: str, out_dir: Path) -> None:
    blocks, body_size = extract_blocks(pdf_path, doc_id)
    blocks = mark_boilerplate(blocks, _page_heights(pdf_path))
    outline = read_outline(pdf_path)
    content_start_page = first_content_page(outline)
    blocks = _mark_front_matter(blocks, content_start_page)

    doc = pymupdf.open(pdf_path)
    page_count = doc.page_count
    raw_text = "\n".join(page.get_text("text") for page in doc)

    report = build_report(
        doc_id=doc_id,
        source_file=Path(pdf_path).name,
        page_count=page_count,
        body_font_size=body_size,
        blocks=blocks,
        outline=outline,
        raw_text=raw_text,
        content_start_page=content_start_page,
    )

    target = out_dir / doc_id
    target.mkdir(parents=True, exist_ok=True)

    with (target / "document.jsonl").open("w", encoding="utf-8") as handle:
        for block in blocks:
            handle.write(json.dumps(block.to_dict(), ensure_ascii=False) + "\n")

    (target / "document.txt").write_text(_render_text_stream(blocks), encoding="utf-8")

    (target / "outline.json").write_text(
        json.dumps(
            {
                "doc_id": doc_id,
                "provenance": "pdf_bookmark_outline",
                "warning": (
                    "Publisher metadata, not a derived skeleton. Feeding this to Pass 0 "
                    "would report the publisher's table of contents as MARD's output. "
                    "Track 1 owns that decision; see ingest/outline.py."
                ),
                "entries": [entry.to_dict() for entry in outline],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    (target / "parse_quality.json").write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (target / "parse_quality.md").write_text(render_markdown(report), encoding="utf-8")

    print(
        f"{doc_id}: {page_count} pages, {report.chars_after_cleaning:,} chars kept, "
        f"{len(report.warnings)} warning(s) -> {target}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a PDF into corpus artefacts.")
    parser.add_argument("pdf_path")
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--out-dir", default="corpus", type=Path)
    args = parser.parse_args()

    ingest_document(args.pdf_path, args.doc_id, args.out_dir)


if __name__ == "__main__":
    main()
