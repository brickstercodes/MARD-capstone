"""Run the Track 1 W1 pipeline over a parsed document. Thin by design.

Two-pass MARD, per `docs/17-W1_DECISION_POINTS.md`: Pass 0 builds the structural map,
Pass 1 explores chapter by chapter growing the envelope, and the findings compile into
a Master Plan. Pass 2 is out of scope for Manuscript A by decision, not by omission.

Artefacts written next to the parse, under `corpus/<doc_id>/`:

  sections.json           Sections, with the four SourceSpan fields PR #48 requires
  chapters.json           Chapters, the unit Pass 1 runs at
  skeleton.json           Pass 0's structural map
  pass0_trace.json        Pass 0's run record
  skeleton_fidelity.*     The derived skeleton scored against the PDF outline
  pass1_trace.json        One record per chapter, with the envelope it was given
  master_plan.json        The compiled plan, ready for the tier boundary
  master_plan_trace.json  What moved, and why, in machine-readable form

With no explorer configured, Pass 0 and Pass 1 both run with their model call switched
off. That is a real configuration and not a dry run: everything deterministic still
lands, and `master_plan.json` comes out empty rather than fabricated.

Usage:
    python -m envelope.cli corpus/introcs --document-id introcs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from envelope.compile_plan import UnsequenceablePlanError, compile_master_plan
from envelope.envelope import Envelope
from envelope.fidelity import render_markdown, score_fidelity
from envelope.pass0 import run_pass0
from envelope.pass1 import run_pass1
from envelope.skeleton import Skeleton
from ingest.blocks import Block
from ingest.chapters import content_chapters, group_into_chapters
from ingest.sections import build_sections


def _load_blocks(corpus_dir: Path) -> list[Block]:
    blocks = []
    with (corpus_dir / "document.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            payload["bbox"] = tuple(payload["bbox"])
            blocks.append(Block(**payload))
    return blocks


def _write(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _score_against_outline(corpus_dir: Path, skeleton: Skeleton) -> str:
    outline_path = corpus_dir / "outline.json"
    if not outline_path.exists():
        return "no outline to score against"

    entries = json.loads(outline_path.read_text(encoding="utf-8"))["entries"]
    report = score_fidelity(skeleton, entries)
    _write(corpus_dir / "skeleton_fidelity.json", report.to_dict())
    (corpus_dir / "skeleton_fidelity.md").write_text(render_markdown(report), encoding="utf-8")
    return f"recall {report.recall:.1%}, mean start-page error {report.mean_start_page_error}"


def run_w1(corpus_dir: Path, document_id: str) -> None:
    blocks = _load_blocks(corpus_dir)
    sections = build_sections(blocks, document_id)
    all_chapters = group_into_chapters(sections, document_id)
    chapters = content_chapters(all_chapters)

    skeleton, pass0_trace = run_pass0(document_id, sections)
    envelope = Envelope.from_skeleton(skeleton)

    section_titles = {section.section_id: section.title for section in sections}
    pass1 = run_pass1(envelope, chapters, section_titles)

    _write(
        corpus_dir / "sections.json",
        {
            "document_id": document_id,
            "source_spans": [section.to_source_span() for section in sections],
            "sections": [section.to_dict() for section in sections],
        },
    )
    _write(
        corpus_dir / "chapters.json",
        {
            "document_id": document_id,
            "chapter_count": len(all_chapters),
            "explored_by_pass1": len(chapters),
            "excluded_unnumbered": [c.chapter_id for c in all_chapters if c.number is None],
            "excluded_as_repeat": [
                {"chapter_id": c.chapter_id, "pages": [c.page_start, c.page_end]}
                for c in all_chapters
                if c.is_repeat
            ],
            "chapters": [chapter.to_dict() for chapter in all_chapters],
        },
    )
    _write(corpus_dir / "skeleton.json", skeleton.to_dict())
    _write(
        corpus_dir / "pass0_trace.json",
        {**pass0_trace, "envelope": envelope.to_dict()},
    )
    _write(
        corpus_dir / "pass1_trace.json",
        {
            "document_id": document_id,
            "chapters_explored": len(pass1.traces),
            "concepts_accepted": len(pass1.concepts),
            "edges_accepted": len(pass1.edges),
            "final_envelope": pass1.envelope.to_dict(),
            "chapters": pass1.traces,
        },
    )

    fidelity = _score_against_outline(corpus_dir, skeleton)

    if not pass1.concepts:
        # No concepts is not an error: it is what the pipeline produces with the scout
        # call switched off, and writing an empty plan would look like a failed run.
        _write(
            corpus_dir / "master_plan_trace.json",
            {
                "compiled": False,
                "reason": "Pass 1 accepted no concepts; nothing to compile.",
            },
        )
        print(
            f"{document_id}: {len(sections)} sections, {len(chapters)} of "
            f"{len(all_chapters)} chapters explored, {fidelity}; no concepts, so no plan compiled"
        )
        return

    try:
        compiled = compile_master_plan(document_id, pass1.concepts, pass1.edges, sections)
    except UnsequenceablePlanError as err:
        _write(
            corpus_dir / "master_plan_trace.json",
            {"compiled": False, "reason": str(err)},
        )
        print(f"{document_id}: plan could not be sequenced - {err}")
        return

    _write(corpus_dir / "master_plan.json", compiled.plan)
    _write(corpus_dir / "master_plan_trace.json", {"compiled": True, **compiled.trace})
    print(
        f"{document_id}: {len(sections)} sections, {len(chapters)} of "
        f"{len(all_chapters)} chapters explored, {fidelity}; "
        f"plan has {compiled.trace['concepts']} concepts, "
        f"{compiled.trace['edges']} edges, {compiled.trace['moves']} moves"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Pass 0 and Pass 1 on a parsed document.")
    parser.add_argument("corpus_dir", type=Path)
    parser.add_argument("--document-id", required=True)
    args = parser.parse_args()

    run_w1(args.corpus_dir, args.document_id)


if __name__ == "__main__":
    main()
