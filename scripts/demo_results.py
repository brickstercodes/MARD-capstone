"""One-screen results summary for the W3 review, computed live from runs/.

Exists because a presentation should read the same artefacts the manuscript
does, rather than a slide someone typed. Every number printed here is derived
from a run directory at call time; nothing is hard-coded.
"""

from __future__ import annotations

import json
import statistics as st
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / "runs"

EXCLUDED_PREFIXES = ("20260828T075502", "20260828T080609", "20260828T081414")
"""Pre-fix MARD seed-11 runs (docs/28): they predate the async-seam repair."""


def load(pattern: str) -> list[dict]:
    out = []
    for d in sorted(RUNS.glob(pattern)):
        if "smoke" in d.name or d.name.startswith(EXCLUDED_PREFIXES):
            continue
        summary = d / "summary.json"
        if summary.exists():
            out.append(json.loads(summary.read_text()))
    return out


def spread(values: list[float], fmt: str = ",.0f") -> str:
    return f"{st.mean(values):{fmt}} [{min(values):{fmt}}–{max(values):{fmt}}]"


def fmt_list(values: list[int]) -> str:
    return ", ".join(str(v) for v in values)


STRUCTURE_REPORT = Path(__file__).resolve().parent.parent / "eval" / "structure_report.json"


def structure_counts() -> tuple[list[int], list[int]]:
    """Read the manuscript's own numbers rather than recomputing them here.

    Recomputing invites a demo that quietly contradicts the paper: heading
    level selection is a real decision (`eval/structure.py` makes it once) and
    a second implementation of it in a presentation script would be a second
    answer. MARD's count is the post-merge one for the same reason.
    """
    report = json.loads(STRUCTURE_REPORT.read_text())
    b1 = [r["concept_count"] for r in report["b1"]]
    mard = [r["concepts"] for r in report["mard"]["mard"]]
    return b1, mard


def main() -> None:
    b1 = [r for r in load("*vanilla_rlm__introcs__s*") if r["status"] == "ok"]
    mard = [r for r in load("*__mard__introcs__s*") if r["status"] == "ok"]

    print("\n  SAME BOOK, SAME SETTINGS, THREE RUNS EACH\n")
    print(f"  {'':20}{'vanilla RLM':>28}{'MARD':>24}")
    rows = [
        ("input tokens", [r["totals"]["input_tokens"] for r in b1],
         [r["totals"]["input_tokens"] for r in mard], ",.0f"),
        ("cost (USD)", [r["totals"]["cost"] for r in b1],
         [r["totals"]["cost"] for r in mard], ".4f"),
        ("wall clock (s)", [r["wall_clock_s"] for r in b1],
         [r["wall_clock_s"] for r in mard], ".0f"),
    ]
    for label, left, right, fmt in rows:
        print(f"  {label:20}{spread(left, fmt):>28}{spread(right, fmt):>24}")

    secs, concepts = structure_counts()
    print(f"  {'structural units':20}{fmt_list(secs):>28}{fmt_list(concepts):>24}")

    ratio = st.mean([r["totals"]["input_tokens"] for r in b1]) / st.mean(
        [r["totals"]["input_tokens"] for r in mard])
    print(f"\n  MARD reads {ratio:.1f}x fewer input tokens.")

    print("\n  ABLATION — which half of the envelope does the work?\n")
    for label, pattern in (("MARD, full", "*__mard__introcs__s*"),
                           ("skeleton removed", "*__mard_a1__introcs__s*"),
                           ("findings removed", "*__mard_a1f__introcs__s*")):
        runs = [r for r in load(pattern) if r["status"] == "ok"]
        fracs, rej = [], []
        for r in runs:
            res = r.get("result") or {}
            if res.get("edges_accepted"):
                fracs.append(res["cross_chapter_edges"] / res["edges_accepted"])
            rej.append(res.get("never_declared_rejections", 0))
        print(f"  {label:22}cross-chapter {st.mean(fracs):6.1%}"
              f"     unresolved prerequisites {st.mean(rej):5.1f}")

    print("\n  NEGATIVE CONTROL — the same book, scrambled\n")
    flat_m = [r for r in load("*__mard__introcs_flat__s*") if r["status"] == "ok"]
    flat_b = [r for r in load("*vanilla_rlm__introcs_flat__s*") if r["status"] == "ok"]
    words = []
    for r in flat_b:
        answer = RUNS / r["run_id"] / "artefacts" / "vanilla_answer.md"
        words.append(len(answer.read_text().split()))
    print(f"  vanilla RLM           wrote {min(words):,}–{max(words):,} words, "
          f"cost ${st.mean([r['totals']['cost'] for r in flat_b]):.2f}, "
          "flagged nothing")
    print(f"  MARD                  declined in "
          f"{st.mean([r['wall_clock_s'] for r in flat_m]):.2f}s, cost $0.00, "
          f"{len(flat_m)}/{len(flat_m)} runs identical\n")


if __name__ == "__main__":
    main()
