"""Tests for the flat-context negative control (docs/26 Task A).

Two layers: synthetic blocks exercise the shuffle/strip/verify logic in isolation
(fast, no corpus needed), and one integration test runs the real pipeline against
`corpus/introcs` end to end — the actual "did the ablation work" check `docs/26` §2
requires, not a hand-constructed stand-in for it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from envelope.pass0 import run_pass0
from eval.flatten import (
    AblationIncompleteError,
    flatten_blocks,
    flatten_corpus,
    load_blocks,
    load_sections,
    render_text,
    shuffled_sections,
    verify_ablation,
)
from ingest.blocks import Block
from ingest.sections import Section, build_sections

CORPUS_INTROCS = Path(__file__).resolve().parents[1] / "corpus" / "introcs"


def _section(position: int, title: str, block_ids: tuple[str, ...]) -> Section:
    return Section(
        section_id=f"doc.{title.lower().replace(' ', '-')}",
        title=title,
        book_position=position,
        page_start=position + 1,
        page_end=position + 1,
        char_count=sum(len(b) for b in block_ids),
        block_ids=block_ids,
    )


def _heading(block_id: str, text: str, level: int = 1) -> Block:
    return Block(
        block_id=block_id,
        page=1,
        kind="heading",
        level=level,
        role=None,
        text=text,
        bbox=(0.0, 0.0, 1.0, 1.0),
        font_size=16.0,
    )


def _body(block_id: str, text: str) -> Block:
    return Block(
        block_id=block_id,
        page=1,
        kind="body",
        level=None,
        role=None,
        text=text,
        bbox=(0.0, 0.0, 1.0, 1.0),
        font_size=10.0,
    )


def _synthetic_corpus() -> tuple[list[Section], dict[str, Block]]:
    blocks = {
        "b:h1": _heading("b:h1", "Alpha"),
        "b:p1": _body("b:p1", "Alpha body text."),
        "b:h2": _heading("b:h2", "Beta"),
        "b:p2": _body("b:p2", "Beta body text."),
        "b:h3": _heading("b:h3", "Gamma"),
        "b:p3": _body("b:p3", "Gamma body text."),
    }
    sections = [
        _section(0, "Alpha", ("b:h1", "b:p1")),
        _section(1, "Beta", ("b:h2", "b:p2")),
        _section(2, "Gamma", ("b:h3", "b:p3")),
    ]
    return sections, blocks


def test_shuffle_is_deterministic_in_its_seed() -> None:
    sections, _ = _synthetic_corpus()
    a = shuffled_sections(sections, seed=1)
    b = shuffled_sections(sections, seed=1)
    assert [s.section_id for s in a] == [s.section_id for s in b]


def test_shuffle_is_a_permutation_not_a_subset() -> None:
    sections, _ = _synthetic_corpus()
    shuffled = shuffled_sections(sections, seed=7)
    assert {s.section_id for s in shuffled} == {s.section_id for s in sections}
    assert len(shuffled) == len(sections)


def test_different_seeds_can_produce_different_orders() -> None:
    # Not guaranteed for every seed pair with only 3 items, but true for these two —
    # pinned so a regression in shuffle logic (e.g. seed ignored) is caught.
    sections, _ = _synthetic_corpus()
    a = [s.section_id for s in shuffled_sections(sections, seed=1)]
    b = [s.section_id for s in shuffled_sections(sections, seed=4)]
    assert a != b


def test_flatten_blocks_strips_heading_kind_and_level() -> None:
    sections, blocks = _synthetic_corpus()
    flat_blocks, _permutation = flatten_blocks(sections, blocks, seed=1)
    assert all(block.kind != "heading" for block in flat_blocks)
    assert all(block.level is None for block in flat_blocks)


def test_flatten_blocks_keeps_heading_text() -> None:
    sections, blocks = _synthetic_corpus()
    flat_blocks, _permutation = flatten_blocks(sections, blocks, seed=1)
    texts = {block.text for block in flat_blocks}
    assert {"Alpha", "Beta", "Gamma"} <= texts


def test_flatten_blocks_permutation_matches_section_order() -> None:
    sections, blocks = _synthetic_corpus()
    flat_blocks, permutation = flatten_blocks(sections, blocks, seed=1)
    by_id = {s.section_id: s for s in sections}
    expected_block_ids = [
        block_id for section_id in permutation for block_id in by_id[section_id].block_ids
    ]
    assert [b.block_id for b in flat_blocks] == expected_block_ids


def test_render_text_has_no_atx_markers() -> None:
    sections, blocks = _synthetic_corpus()
    flat_blocks, _ = flatten_blocks(sections, blocks, seed=1)
    text = render_text(flat_blocks)
    assert not any(line.startswith("#") for line in text.splitlines())


def test_render_text_has_no_page_markers() -> None:
    sections, blocks = _synthetic_corpus()
    flat_blocks, _ = flatten_blocks(sections, blocks, seed=1)
    text = render_text(flat_blocks)
    assert "[[page:" not in text


def test_verify_ablation_on_stripped_blocks_is_empty_and_degenerate() -> None:
    sections, blocks = _synthetic_corpus()
    flat_blocks, _ = flatten_blocks(sections, blocks, seed=1)
    skeleton, trace = verify_ablation("synthetic", flat_blocks)
    assert skeleton.is_empty
    assert trace["degenerate"] is True


def test_verify_ablation_on_unstripped_blocks_is_not_empty() -> None:
    """Negative control on the test itself: real headings still yield real sections,
    so `verify_ablation`'s emptiness on stripped blocks is the stripping's effect,
    not `build_sections`/`run_pass0` being trivially empty on any input."""
    _sections, blocks = _synthetic_corpus()
    unstripped = list(blocks.values())
    skeleton, trace = verify_ablation("synthetic", unstripped)
    assert not skeleton.is_empty
    assert trace["degenerate"] is False


def test_flatten_corpus_raises_when_stripping_regresses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """If `flatten_blocks` ever stopped stripping heading structure (a regression,
    not a real code path today), `flatten_corpus` must refuse to write a corpus that
    silently isn't flat — `docs/26` §2's "report it; do not paper over it by
    deleting more" applies to the build script itself.
    """
    import eval.flatten as flatten_module

    sections, blocks = _synthetic_corpus()

    def _unstripped_flatten_blocks(
        sections: list[Section], blocks: dict[str, Block], seed: int
    ) -> tuple[list[Block], list[str]]:
        order = [s.section_id for s in sections]
        return list(blocks.values()), order

    monkeypatch.setattr(flatten_module, "load_sections", lambda _path: sections)
    monkeypatch.setattr(flatten_module, "load_blocks", lambda _path: blocks)
    monkeypatch.setattr(flatten_module, "flatten_blocks", _unstripped_flatten_blocks)

    with pytest.raises(AblationIncompleteError):
        flatten_module.flatten_corpus(tmp_path / "source", tmp_path / "target", "synthetic")

    assert not (tmp_path / "target" / "document.txt").exists()


@pytest.mark.skipif(not CORPUS_INTROCS.exists(), reason="corpus/introcs not present")
def test_flatten_corpus_end_to_end_on_real_introcs(tmp_path: Path) -> None:
    target = tmp_path / "introcs_flat"
    manifest = flatten_corpus(CORPUS_INTROCS, target, "introcs_flat", seed=1)

    assert (target / "document.txt").exists()
    assert (target / "manifest.json").exists()
    assert manifest["flatten"]["shuffle_seed"] == 1
    assert manifest["flatten"]["ablation_verified"]["is_empty"] is True
    assert manifest["flatten"]["ablation_verified"]["degenerate"] is True

    text = (target / "document.txt").read_text(encoding="utf-8")
    assert "[[page:" not in text
    # The real corpus's body text legitimately contains lines starting with "#"
    # (C-family `#include`, Python `#` comments in code samples), so a blanket
    # "no line starts with #" check would false-positive on real content. The
    # actual invariant is that a known heading's text survives with no ATX marker
    # immediately in front of it — never "# Chapter Outline", just "Chapter Outline".
    assert "Chapter Outline" in text
    assert not any(re.match(r"^#{1,6}\s+Chapter Outline\s*$", line) for line in text.splitlines())

    # Re-derive sections from the written manifest's own permutation and confirm the
    # real `run_pass0` entry point (not just `verify_ablation`) agrees.
    sections = load_sections(CORPUS_INTROCS / "sections.json")
    blocks = load_blocks(CORPUS_INTROCS / "document.jsonl")
    flat_blocks, _ = flatten_blocks(sections, blocks, seed=1)
    rebuilt_sections = build_sections(flat_blocks, "introcs_flat")
    skeleton, trace = run_pass0("introcs_flat", rebuilt_sections)
    assert skeleton.is_empty
    assert trace["degenerate"] is True


@pytest.mark.skipif(not CORPUS_INTROCS.exists(), reason="corpus/introcs not present")
def test_flatten_corpus_writes_document_jsonl_mard_can_load(tmp_path: Path) -> None:
    """`mard.run._load_blocks` (and `envelope.cli`'s own loader) read
    `document.jsonl`, not `document.txt` — confirmed the hard way (Anugrah, 28 Aug
    2026: `corpus/introcs_flat/` had only `document.txt` and `manifest.json`, so
    the MARD arm's negative-control run would fail immediately with
    `FileNotFoundError`). B1/vanilla only reads `document.txt` and was unaffected,
    which is why this was missed until someone tried the MARD side specifically.
    """
    target = tmp_path / "introcs_flat"
    flatten_corpus(CORPUS_INTROCS, target, "introcs_flat", seed=1)

    jsonl_path = target / "document.jsonl"
    assert jsonl_path.exists()

    import json

    blocks = []
    with jsonl_path.open(encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            payload["bbox"] = tuple(payload["bbox"])
            blocks.append(Block(**payload))  # exactly mard.run._load_blocks's own logic

    assert blocks  # non-empty: the flattened text still has real block content
    assert all(block.kind != "heading" for block in blocks)  # the ablation itself


@pytest.mark.skipif(not CORPUS_INTROCS.exists(), reason="corpus/introcs not present")
def test_flatten_corpus_is_reproducible_for_a_fixed_seed(tmp_path: Path) -> None:
    first = flatten_corpus(CORPUS_INTROCS, tmp_path / "a", "introcs_flat", seed=3)
    second = flatten_corpus(CORPUS_INTROCS, tmp_path / "b", "introcs_flat", seed=3)
    assert first["flatten"]["section_permutation"] == second["flatten"]["section_permutation"]
    assert (tmp_path / "a" / "document.txt").read_bytes() == (
        tmp_path / "b" / "document.txt"
    ).read_bytes()
