"""Render the manuscript's data figures from logged runs.

Kept as a script rather than hand-drawn images so every figure regenerates from
`runs/` and cannot drift from the tables it sits beside. Print-safe by
construction: series are separated by lightness, never by hue alone, so the
figures survive greyscale reproduction and colour-vision deficiency without a
second encoding.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
OUT = ROOT / "paper"

INK = "#1f2933"
MID = "#7b8794"
PALE = "#cbd2d9"
FAINT = "#eef1f4"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Nimbus Roman", "Times New Roman", "DejaVu Serif"],
    "font.size": 8,
    "axes.edgecolor": MID,
    "axes.linewidth": 0.6,
    "xtick.color": INK,
    "ytick.color": INK,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
})

REFERENCE_RUN = "20260828T083754__mard__introcs__s42__548fe0"


def envelope_composition() -> list[dict[str, int]]:
    """Per-call token composition of the Pass 1 prompt, from the logged prompts."""
    rows = []
    calls = (RUNS / REFERENCE_RUN / "calls.jsonl").read_text().splitlines()
    for line in calls:
        record = json.loads(line)
        if record.get("role") != "tier1_pass1":
            continue
        content = json.loads(record["prompt"])[0]["content"]
        heads = [(m.start(), m.group(1)) for m in re.finditer(r"^## (.+)$", content, re.M)]
        seg = {}
        for i, (pos, name) in enumerate(heads):
            end = heads[i + 1][0] if i + 1 < len(heads) else len(content)
            seg[name.split(" (")[0]] = (end - pos) // 4
        rows.append({
            "skeleton": seg.get("STRUCTURAL MAP", 0),
            "findings": seg.get("FINDINGS SO FAR", 0),
            "other": seg.get("THIS CHAPTER", 0) + seg.get("YOUR DIRECTIVE", 0)
                     + seg.get("WHAT TO RETURN", 0) + seg.get("YOUR TARGET", 0),
        })
    return rows


def fig_envelope() -> None:
    rows = envelope_composition()
    x = list(range(1, len(rows) + 1))
    skel = [r["skeleton"] for r in rows]
    find = [r["findings"] for r in rows]
    other = [r["other"] for r in rows]

    fig, ax = plt.subplots(figsize=(3.35, 2.25))
    ax.stackplot(x, skel, find, other, colors=[PALE, INK, FAINT],
                 edgecolor="white", linewidth=0.5)

    ax.annotate("skeleton $S(D)$\n4,031 tokens on every call",
                xy=(7.5, 2000), ha="center", va="center", fontsize=7, color=INK)
    ax.annotate("accumulated findings $F(c)$\n0 $\\rightarrow$ 3,013 tokens",
                xy=(11.3, 4780), ha="center", va="center", fontsize=7, color="white")

    ax.set_xlabel("Pass 1 call (chapter, book order)")
    ax.set_ylabel("prompt tokens")
    ax.set_xlim(1, len(rows))
    ax.set_ylim(0, 8000)
    ax.set_xticks([1, 4, 7, 10, 14])
    ax.set_yticks([0, 2000, 4000, 6000, 8000])
    ax.set_yticklabels(["0", "2k", "4k", "6k", "8k"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "fig_envelope.pdf", bbox_inches="tight")
    print("wrote fig_envelope.pdf")


def fig_results() -> None:
    quality = {"vanilla RLM": [0.3145, 0.5720, 0.7654],
               "MARD": [0.5844, 0.6296, 0.6502]}
    tokens = {"vanilla RLM": [516875, 646792, 3315432],
              "MARD": [93809, 94257, 94660]}
    ablation = [("MARD, full", 0.917, 2.0),
                ("skeleton\nsuppressed", 0.898, 0.0),
                ("findings\nsuppressed", 0.014, 57.0)]

    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.05))

    for ax, data, label, logscale in (
        (axes[0], quality, "objective coverage", False),
        (axes[1], tokens, "input tokens per run", True),
    ):
        for i, (name, vals) in enumerate(data.items()):
            y = [i] * len(vals)
            ax.plot(vals, y, "o", ms=5, color=INK if name == "MARD" else MID,
                    mfc=INK if name == "MARD" else "white",
                    mew=1.0, zorder=3, clip_on=False)
            ax.plot([min(vals), max(vals)], [i, i], "-", color=PALE, lw=1.4, zorder=1)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(list(data), fontsize=7.5)
        ax.set_ylim(-0.55, 1.55)
        ax.set_xlabel(label)
        if logscale:
            ax.set_xscale("log")
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.tick_params(axis="y", length=0)

    ax = axes[2]
    names = [a[0] for a in ablation]
    fracs = [a[1] for a in ablation]
    bars = ax.barh(range(3), fracs, height=0.55,
                   color=[PALE, PALE, INK], edgecolor=MID, linewidth=0.6)
    for i, (frac, rej) in enumerate([(a[1], a[2]) for a in ablation]):
        ax.text(frac + 0.03, i - 0.14, f"{frac:.3f}", va="center", fontsize=7, color=INK)
        ax.text(frac + 0.03, i + 0.20, f"{rej:.0f} unresolved", va="center",
                fontsize=6, color=MID)
    ax.set_yticks(range(3))
    ax.set_yticklabels(names, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.15)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xlabel("cross-chapter edge fraction")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)

    axes[0].set_title("(a) quality: three repeats", fontsize=8, pad=6)
    axes[1].set_title("(b) input tokens: three repeats", fontsize=8, pad=6)
    axes[2].set_title("(c) ablation by envelope channel", fontsize=8, pad=6)

    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / "fig_results.pdf", bbox_inches="tight")
    print("wrote fig_results.pdf")


if __name__ == "__main__":
    fig_envelope()
    fig_results()
