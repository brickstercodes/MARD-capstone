"""Tests for corpus provenance pinning.

The behaviour that matters is the *loud failure*: a corpus that has drifted from its
manifest must raise, not warn. A warning would let a measured run proceed against the
wrong document, which is the exact failure this module exists to prevent.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ingest.manifest import (
    INGEST_CONTRACT_VERSION,
    MANIFEST_FILENAME,
    ManifestMismatchError,
    SourceRecord,
    load_manifest,
    sha256_file,
    verify,
    verify_or_raise,
    write_manifest,
)

SOURCE = SourceRecord(
    file_name="book.pdf",
    sha256="0" * 64,
    bytes=1234,
    page_count=939,
    url="https://example.invalid/book.pdf",
    retrieved_on="2026-08-27",
)


def _corpus(tmp_path: Path) -> Path:
    target = tmp_path / "introcs"
    target.mkdir()
    (target / "document.txt").write_text("# Chapter One\nbody text\n", encoding="utf-8")
    (target / "document.jsonl").write_text('{"block_id": "b1"}\n', encoding="utf-8")
    (target / "outline.json").write_text('{"entries": []}', encoding="utf-8")
    return target


def test_sha256_file_matches_hashlib(tmp_path: Path) -> None:
    import hashlib

    path = tmp_path / "f.bin"
    payload = b"x" * (3 << 20)  # larger than one read chunk, so chunking is exercised
    path.write_bytes(payload)
    assert sha256_file(path) == hashlib.sha256(payload).hexdigest()


def test_write_manifest_pins_present_artefacts_and_nulls_absent(tmp_path: Path) -> None:
    target = _corpus(tmp_path)
    manifest = write_manifest(target, "introcs", SOURCE)

    assert manifest["doc_id"] == "introcs"
    assert manifest["source"]["sha256"] == "0" * 64
    assert manifest["source"]["url"] == "https://example.invalid/book.pdf"
    assert manifest["pipeline"]["contract_version"] == INGEST_CONTRACT_VERSION

    assert manifest["artefacts"]["document.txt"]["sha256"] is not None
    # sections.json was not written by this stage. Recorded as null so that "not
    # produced yet" stays distinguishable from "produced and unhashed".
    assert manifest["artefacts"]["sections.json"]["sha256"] is None
    assert (target / MANIFEST_FILENAME).exists()


def test_verify_passes_on_an_untouched_corpus(tmp_path: Path) -> None:
    target = _corpus(tmp_path)
    write_manifest(target, "introcs", SOURCE)
    assert verify(target) == []
    verify_or_raise(target)  # must not raise


def test_a_single_changed_byte_is_caught(tmp_path: Path) -> None:
    target = _corpus(tmp_path)
    write_manifest(target, "introcs", SOURCE)

    # The realistic drift: ingest changes and document.txt comes out slightly different.
    (target / "document.txt").write_text("# Chapter One\nbody texu\n", encoding="utf-8")

    problems = verify(target)
    assert len(problems) == 1
    assert "document.txt" in problems[0]

    with pytest.raises(ManifestMismatchError) as caught:
        verify_or_raise(target)
    # The message has to tell the reader how to get out of the hole, not just that
    # they are in one.
    assert "python -m ingest.cli" in str(caught.value)


def test_a_deleted_artefact_is_caught(tmp_path: Path) -> None:
    target = _corpus(tmp_path)
    write_manifest(target, "introcs", SOURCE)
    (target / "document.jsonl").unlink()

    problems = verify(target)
    assert any("document.jsonl" in p and "missing" in p for p in problems)


def test_a_contract_version_bump_invalidates_an_old_corpus(tmp_path: Path) -> None:
    """The case a byte comparison alone would pass.

    If ingest's output means something different, an untouched corpus is still wrong.
    """
    target = _corpus(tmp_path)
    write_manifest(target, "introcs", SOURCE)

    path = target / MANIFEST_FILENAME
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["pipeline"]["contract_version"] = INGEST_CONTRACT_VERSION - 1
    path.write_text(json.dumps(manifest), encoding="utf-8")

    problems = verify(target)
    assert any("contract version" in p for p in problems)


def test_strict_pipeline_flags_a_dirty_working_tree(tmp_path: Path) -> None:
    target = _corpus(tmp_path)
    write_manifest(target, "introcs", SOURCE)

    path = target / MANIFEST_FILENAME
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["pipeline"]["git_dirty"] = True
    manifest["pipeline"]["git_commit"] = "deadbeef"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    assert verify(target, strict_pipeline=False) == []
    problems = verify(target, strict_pipeline=True)
    assert any("dirty" in p for p in problems)
    assert any("commit" in p for p in problems)


def test_a_corpus_with_no_manifest_says_so_usefully(tmp_path: Path) -> None:
    target = _corpus(tmp_path)
    with pytest.raises(FileNotFoundError) as caught:
        load_manifest(target)
    assert "re-ingest" in str(caught.value)
