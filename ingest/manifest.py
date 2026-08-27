"""Corpus provenance: what document was parsed, by what code, into what bytes.

This module exists because `.gitignore` excludes `corpus/*/document.*` — the parsed
text every measured number is computed from is not in the repository, and until now
the only record of its origin was a bare filename in `parse_quality.json`. That makes
"regenerate the corpus" and "reproduce the corpus" different operations, and nothing
could tell them apart.

Two ways a regenerated corpus silently stops matching the measured one:

  1. The upstream PDF changes. OpenStax reissues books at the same URL; a revision
     shifts pagination, which shifts section spans, which shifts the skeleton, which
     shifts every score. Skeleton fidelity measured against different pagination is
     not a number.
  2. `ingest/` changes. Three heading-detection defects were fixed in a single day
     during W1, one of which moved `introcs` from 7 detected headings to 1,403.
     `CONTEXT.md` §3.4 makes a pipeline change an invalidation of every prior number.

So the manifest records the source hash, the pipeline commit, and the hash of every
artefact produced. Verification compares and **raises** — the same discipline
`runlog.pricing.RateCard` already applies to model prices, applied to the input those
prices are spent on.

Deliberately not reusing `runlog.ConfigSnapshot`: it is run-shaped (it requires a
run_id, a system and a seed) and a corpus artefact has none of those. Eight lines of
duplicated `git` plumbing is cheaper than bending a type into two jobs.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MANIFEST_FILENAME = "manifest.json"

INGEST_CONTRACT_VERSION = 1
"""Bump when `ingest/` changes what its artefacts *mean*, not merely how it is written.

A bump invalidates every corpus generated under the previous version, which is the
point: verification reports a version mismatch as a discrepancy rather than letting a
semantically different parse pass a byte comparison it was never going to fail.
"""

HASHED_ARTEFACTS = (
    "document.jsonl",
    "document.txt",
    "outline.json",
    "sections.json",
    "chapters.json",
    "parse_quality.json",
)
"""Artefacts whose bytes are pinned.

`document.*` because they are the untracked input to everything downstream.
`outline.json` because it is the yardstick skeleton fidelity is scored against, so a
change there moves a reported number without touching the text. The `.md` renderings
are excluded: they are derived from `parse_quality.json` and would only add a second
thing to keep in sync.
"""

READ_CHUNK_BYTES = 1 << 20


class ManifestMismatchError(RuntimeError):
    """A corpus on disk does not match the manifest that describes it.

    Raised rather than warned. A stale corpus produces plausible numbers against the
    wrong document, and a warning in a log nobody reads is not a control.
    """

    def __init__(self, doc_id: str, discrepancies: list[str]) -> None:
        self.doc_id = doc_id
        self.discrepancies = discrepancies
        detail = "\n  - ".join(discrepancies)
        super().__init__(
            f"Corpus '{doc_id}' does not match its manifest:\n  - {detail}\n"
            "Regenerate with `python -m ingest.cli <pdf> --doc-id "
            f"{doc_id}`, or if the change is intended, delete "
            f"{MANIFEST_FILENAME} and re-ingest to re-pin."
        )


def sha256_file(path: Path) -> str:
    """Hash a file in chunks, because the corpus contains 2.5 MB text and 940-page PDFs."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(READ_CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def _git(*args: str) -> str | None:
    """Return git output, or None when git is unavailable or this is not a repo."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None if result.returncode == 0 else None


@dataclass(frozen=True)
class SourceRecord:
    """Where the document came from. `url` and `retrieved_on` come from SOURCES.json."""

    file_name: str
    sha256: str
    bytes: int
    page_count: int | None = None
    url: str | None = None
    retrieved_on: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_name": self.file_name,
            "sha256": self.sha256,
            "bytes": self.bytes,
            "page_count": self.page_count,
            "url": self.url,
            "retrieved_on": self.retrieved_on,
        }


def _pipeline_record() -> dict[str, Any]:
    status = _git("status", "--porcelain")
    return {
        "contract_version": INGEST_CONTRACT_VERSION,
        "git_commit": _git("rev-parse", "HEAD"),
        "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_dirty": bool(status),
    }


def _artefact_records(target: Path) -> dict[str, dict[str, Any]]:
    """Hash the artefacts that exist. A missing one is recorded as absent, not skipped.

    Absence is meaningful: `sections.json` and `chapters.json` are written by a later
    stage than `ingest.cli`, so a manifest written at ingest time legitimately has them
    null. Recording null distinguishes "not produced yet" from "produced and unhashed".
    """
    records: dict[str, dict[str, Any]] = {}
    for name in HASHED_ARTEFACTS:
        path = target / name
        if not path.exists():
            records[name] = {"sha256": None, "bytes": None}
            continue
        records[name] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    return records


def write_manifest(
    target: Path,
    doc_id: str,
    source: SourceRecord,
) -> dict[str, Any]:
    """Pin the corpus at `target`. Returns the manifest it wrote."""
    manifest = {
        "doc_id": doc_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": source.to_dict(),
        "pipeline": _pipeline_record(),
        "artefacts": _artefact_records(target),
    }
    (target / MANIFEST_FILENAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def load_manifest(target: Path) -> dict[str, Any]:
    path = target / MANIFEST_FILENAME
    if not path.exists():
        raise FileNotFoundError(
            f"No {MANIFEST_FILENAME} in {target}. This corpus predates provenance "
            "pinning; re-ingest to create one."
        )
    loaded: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def verify(target: Path, *, strict_pipeline: bool = False) -> list[str]:
    """Compare the corpus on disk against its manifest. Returns discrepancies.

    Returns rather than raises so a caller can report all of them at once; use
    `verify_or_raise` for the loud-failure path. `strict_pipeline` additionally
    requires the ingest commit to match, which is correct after a results freeze and
    too strict during development.
    """
    manifest = load_manifest(target)
    problems: list[str] = []

    recorded_version = manifest.get("pipeline", {}).get("contract_version")
    if recorded_version != INGEST_CONTRACT_VERSION:
        problems.append(
            f"ingest contract version {recorded_version} != {INGEST_CONTRACT_VERSION} "
            "— the parse means something different now"
        )

    if strict_pipeline:
        recorded_commit = manifest.get("pipeline", {}).get("git_commit")
        current_commit = _git("rev-parse", "HEAD")
        if recorded_commit != current_commit:
            problems.append(f"ingest commit {recorded_commit} != working tree {current_commit}")
        if manifest.get("pipeline", {}).get("git_dirty"):
            problems.append("manifest was written from a dirty working tree")

    for name, recorded in manifest.get("artefacts", {}).items():
        path = target / name
        expected = recorded.get("sha256")
        if expected is None:
            continue
        if not path.exists():
            problems.append(f"{name}: pinned in manifest but missing on disk")
            continue
        actual = sha256_file(path)
        if actual != expected:
            problems.append(f"{name}: sha256 {actual[:12]} != pinned {expected[:12]}")

    return problems


def verify_or_raise(target: Path, *, strict_pipeline: bool = False) -> None:
    """Verify, and fail loudly on any discrepancy. Use this before a measured run."""
    problems = verify(target, strict_pipeline=strict_pipeline)
    if problems:
        manifest = load_manifest(target)
        raise ManifestMismatchError(manifest.get("doc_id", target.name), problems)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify a parsed corpus against its provenance manifest."
    )
    parser.add_argument("corpus_dir", type=Path)
    parser.add_argument("--document-id", required=True)
    parser.add_argument(
        "--strict-pipeline",
        action="store_true",
        help="Also require the ingest commit to match. Correct after a results freeze.",
    )
    args = parser.parse_args()

    target = args.corpus_dir / args.document_id
    verify_or_raise(target, strict_pipeline=args.strict_pipeline)
    manifest = load_manifest(target)
    source = manifest["source"]
    print(
        f"{args.document_id}: OK — source sha256 {source['sha256'][:12]}, "
        f"ingest {(manifest['pipeline']['git_commit'] or 'unknown')[:12]}, "
        f"{sum(1 for a in manifest['artefacts'].values() if a['sha256'])} artefacts pinned"
    )


if __name__ == "__main__":
    main()
