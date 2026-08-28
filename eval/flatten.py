"""The flat-context negative control: a structure-ablated `introcs`.

`docs/30` §5 amendment item 6 substitutes this for the frozen OOLONG subset in
Manuscript A's matrix (days of wall-clock, deferred to Manuscript B). The control
holds content constant and varies only structure — same text, section order
shuffled, heading markers stripped — so it is a manipulation of the primary
document rather than a change of corpus, and it parallels ablation A1 one level
lower: A1 removes the structure the *system* accumulates, this removes the
structure the *document* supplies.

**Why block-level, not text-level, stripping.** `ingest.sections.build_sections`
groups content by `Block.kind == "heading"` and `Block.level`, both derived from
PDF font metrics (`ingest/blocks.py`) — it never re-parses `document.txt`'s ATX
markers. Stripping only the rendered `#` characters would leave every block's real
`kind`/`level` untouched, and the ablation would be a no-op the moment anything
re-derives sections from blocks instead of from the text a human reads. So this
module relabels heading blocks (`kind="body"`, `level=None`) at the source the
pipeline actually reads, using `corpus/introcs/document.jsonl` — the parsed blocks
`corpus/introcs/sections.json`'s `source_spans` already carries `block_ids` for, so
section boundaries come from that recorded structure rather than from guessing at
the text. `document.txt` is then rendered from those same relabelled blocks, so the
human-readable artefact and the machine-verifiable one cannot drift apart.

**The `[[page:N]]` decision: dropped.** Page numbers are positional structure in
the same sense heading levels are — a model can reconstruct original reading order
from a page sequence even after sections are shuffled and headings are stripped,
which would leave the ablation incomplete in exactly the way `docs/26` §2 warns
about. They are omitted from the flattened `document.txt` entirely.

**Both `document.txt` and `document.jsonl` are written.** The vanilla arm
(`vanilla.run.run_vanilla_rlm`) reads only `document.txt`, so an earlier version of
this module wrote only that — but the MARD arm's own ingestion
(`mard.run._load_blocks`, `envelope.cli`'s loader) reads `document.jsonl`
unconditionally, the same as it would for any other corpus, and has no path that
falls back to `document.txt` alone. Without the `.jsonl` file the MARD arm's
negative-control run fails immediately with `FileNotFoundError`, before it ever
reaches the degenerate-skeleton behaviour this module exists to produce (confirmed
the hard way, 28 Aug 2026). `flat_blocks` is already the exact block list both
arms need; this just persists it in the shape `mard.run`/`envelope.cli` expect,
one JSON object per line, the same as `ingest.cli.ingest_document` writes for a
freshly-parsed corpus.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import replace
from pathlib import Path
from typing import Any

from envelope.pass0 import run_pass0
from envelope.skeleton import Skeleton
from ingest.blocks import Block
from ingest.manifest import SourceRecord, sha256_file, write_manifest
from ingest.sections import Section, build_sections

# Distinct from `runlog.seeds.CAMPAIGN_SEEDS` (11, 23, 42), which identify *system*
# runs. This seed controls exactly one thing — the section-order permutation — and
# is fixed so the control is reproducible without being confused with a run seed.
FLATTEN_SHUFFLE_SEED = 20260827


class AblationIncompleteError(RuntimeError):
    """The flattened corpus still yields a non-empty skeleton.

    Raised rather than warned, same discipline as `ingest.manifest.ManifestMismatchError`:
    `docs/26` §2 is explicit that an incomplete ablation must be reported and
    investigated, never papered over by deleting more text until the symptom
    disappears.
    """


def load_sections(sections_path: Path) -> list[Section]:
    """Reconstruct `Section` objects from a pinned `sections.json`.

    Drops `page_count`/`density` — computed properties `Section.to_dict()` adds,
    not constructor fields — and restores `block_ids` to a tuple.
    """
    payload = json.loads(sections_path.read_text(encoding="utf-8"))
    return [
        Section(
            section_id=entry["section_id"],
            title=entry["title"],
            book_position=entry["book_position"],
            page_start=entry["page_start"],
            page_end=entry["page_end"],
            char_count=entry["char_count"],
            block_ids=tuple(entry["block_ids"]),
        )
        for entry in payload["sections"]
    ]


def load_blocks(document_jsonl_path: Path) -> dict[str, Block]:
    """Read the page-mapped blocks, keyed by `block_id` for `Section.block_ids` lookup."""
    blocks: dict[str, Block] = {}
    with document_jsonl_path.open(encoding="utf-8") as handle:
        for line in handle:
            entry = json.loads(line)
            blocks[entry["block_id"]] = Block(
                block_id=entry["block_id"],
                page=entry["page"],
                kind=entry["kind"],
                level=entry["level"],
                role=entry["role"],
                text=entry["text"],
                bbox=tuple(entry["bbox"]),
                font_size=entry["font_size"],
            )
    return blocks


def shuffled_sections(sections: list[Section], seed: int) -> list[Section]:
    """Book order, permuted. Deterministic in `seed`, nothing else."""
    ordered = sorted(sections, key=lambda section: section.book_position)
    shuffled = list(ordered)
    random.Random(seed).shuffle(shuffled)
    return shuffled


def _strip_heading(block: Block) -> Block:
    """Remove a block's structural signal while keeping its text.

    This is the ablation's core operation — see the module docstring's "why
    block-level" note. Non-heading blocks (body, caption, role-marker) pass through
    unchanged; they carry no structural signal to strip.
    """
    if block.kind != "heading":
        return block
    return replace(block, kind="body", level=None)


def flatten_blocks(
    sections: list[Section], blocks: dict[str, Block], seed: int
) -> tuple[list[Block], list[str]]:
    """Shuffle section order, strip heading structure, return blocks and the permutation.

    The permutation is the shuffled sections' ids, book order, so it can be recorded
    in the manifest and the shuffle audited independently of re-running it.
    """
    order = shuffled_sections(sections, seed)
    flat_blocks = [
        _strip_heading(blocks[block_id]) for section in order for block_id in section.block_ids
    ]
    return flat_blocks, [section.section_id for section in order]


def render_text(flat_blocks: list[Block]) -> str:
    """Plain text: one block's text per paragraph, no heading markers, no page markers."""
    return "\n\n".join(block.text for block in flat_blocks).strip() + "\n"


def verify_ablation(document_id: str, flat_blocks: list[Block]) -> tuple[Skeleton, dict[str, Any]]:
    """Run the real section-boundary algorithm and the real Pass 0 against the ablated
    blocks — not a hand-constructed empty list. `ingest.sections.build_sections` finds
    zero heading blocks (every one was relabelled `body`), so `choose_section_level`
    falls through to its no-candidate-qualifies branch and every block fails the
    `starts_section` test; `sections` comes out `[]` by the same code path a real
    corpus goes through, not by assertion.
    """
    sections = build_sections(flat_blocks, document_id)
    return run_pass0(document_id, sections)


def flatten_corpus(
    source_dir: Path,
    target_dir: Path,
    document_id: str,
    seed: int = FLATTEN_SHUFFLE_SEED,
) -> dict[str, Any]:
    """Build the flattened corpus on disk and pin it. Returns the written manifest.

    Raises `AblationIncompleteError` before writing anything if the ablation did not
    empty the skeleton — `docs/26` §2's "stop and report" applies to a build script
    exactly as it applies to a person reading the trace by hand.
    """
    sections = load_sections(source_dir / "sections.json")
    blocks = load_blocks(source_dir / "document.jsonl")
    flat_blocks, permutation = flatten_blocks(sections, blocks, seed)

    skeleton, trace = verify_ablation(document_id, flat_blocks)
    if not skeleton.is_empty or not trace["degenerate"]:
        raise AblationIncompleteError(
            f"Flattening {source_dir} did not empty the skeleton: "
            f"is_empty={skeleton.is_empty}, degenerate={trace['degenerate']}, "
            f"{len(skeleton.sections)} section(s) survived. Something is still "
            "carrying structure; find it before running anything against this corpus."
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "document.txt").write_text(render_text(flat_blocks), encoding="utf-8")
    with (target_dir / "document.jsonl").open("w", encoding="utf-8") as handle:
        for block in flat_blocks:
            handle.write(json.dumps(block.to_dict(), ensure_ascii=False) + "\n")

    source_document_txt = source_dir / "document.txt"
    manifest = write_manifest(
        target_dir,
        document_id,
        SourceRecord(
            file_name=f"{source_dir.name}/document.txt",
            sha256=sha256_file(source_document_txt),
            bytes=source_document_txt.stat().st_size,
        ),
    )
    manifest["flatten"] = {
        "shuffle_seed": seed,
        "source_corpus": source_dir.name,
        "section_permutation": permutation,
        "page_markers": "dropped",
        "ablation_verified": {
            "is_empty": skeleton.is_empty,
            "degenerate": trace["degenerate"],
        },
    }
    (target_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the flat-context negative control corpus (docs/26 Task A)."
    )
    parser.add_argument("--source-dir", default=Path("corpus/introcs"), type=Path)
    parser.add_argument("--target-dir", default=Path("corpus/introcs_flat"), type=Path)
    parser.add_argument("--document-id", default="introcs_flat")
    parser.add_argument("--seed", default=FLATTEN_SHUFFLE_SEED, type=int)
    args = parser.parse_args()

    manifest = flatten_corpus(args.source_dir, args.target_dir, args.document_id, args.seed)
    ablation = manifest["flatten"]["ablation_verified"]
    print(
        f"{args.document_id}: flattened from {args.source_dir} (seed {args.seed}), "
        f"ablation verified degenerate={ablation['degenerate']} -> {args.target_dir}"
    )


if __name__ == "__main__":
    main()
