"""Config snapshots.

A run's numbers are only defensible if the exact conditions that produced them
can be reconstructed months later. CONTEXT.md §3.4 puts it plainly: a number you
cannot reproduce on 29 Sep is not a number. This module captures those
conditions once, at run start, so no part of the pipeline has to remember to
record them later.

Kept separate from `run` because the snapshot is also useful on its own — for
instance when Track 3 wants to diff two runs that disagree.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib import metadata
from typing import Any

# Recording every installed package makes the diff between two runs unreadable.
# These are the ones that can actually change a result.
TRACKED_PACKAGES = (
    "pydantic",
    "numpy",
    "openai",
    "anthropic",
    "vllm",
    "transformers",
    "pymupdf",
    "pdfplumber",
)


def _git(*args: str) -> str | None:
    """Return git output, or None when git is unavailable or the repo is bare."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in TRACKED_PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return versions


@dataclass(frozen=True)
class ConfigSnapshot:
    """Everything needed to explain why a run produced the numbers it did."""

    run_id: str
    system: str
    """Which system was measured: mard, vanilla_rlm, full_context, naive_chunk, rag."""

    document_id: str
    seed: int
    models: dict[str, str]
    """Role to model identifier, e.g. {"tier1": "...", "tier2": "..."}."""

    params: dict[str, Any] = field(default_factory=dict)
    """Anything else that changes behaviour: depth, chunk size, temperature, top_k."""

    # Captured automatically. Present as fields so they land in the manifest
    # verbatim rather than being recomputed at read time.
    git_commit: str | None = field(default=None)
    git_branch: str | None = field(default=None)
    git_dirty: bool = field(default=False)
    python_version: str = field(default="")
    platform_id: str = field(default="")
    packages: dict[str, str] = field(default_factory=dict)
    captured_at: str = field(default="")

    @classmethod
    def capture(
        cls,
        *,
        run_id: str,
        system: str,
        document_id: str,
        seed: int,
        models: dict[str, str],
        params: dict[str, Any] | None = None,
    ) -> ConfigSnapshot:
        """Build a snapshot from the caller's intent plus the ambient environment."""
        status = _git("status", "--porcelain")
        return cls(
            run_id=run_id,
            system=system,
            document_id=document_id,
            seed=seed,
            models=dict(models),
            params=dict(params or {}),
            git_commit=_git("rev-parse", "HEAD"),
            git_branch=_git("rev-parse", "--abbrev-ref", "HEAD"),
            git_dirty=bool(status),
            python_version=sys.version.split()[0],
            platform_id=platform.platform(),
            packages=_package_versions(),
            captured_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "system": self.system,
            "document_id": self.document_id,
            "seed": self.seed,
            "models": self.models,
            "params": self.params,
            "git": {
                "commit": self.git_commit,
                "branch": self.git_branch,
                "dirty": self.git_dirty,
            },
            "environment": {
                "python": self.python_version,
                "platform": self.platform_id,
                "packages": self.packages,
            },
            "captured_at": self.captured_at,
        }
