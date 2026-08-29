#!/usr/bin/env python
"""Smoke test with verbose real-time logging so prof can see progress.

One cheap MARD smoke run: Pass 0 on the full skeleton, Pass 1 restricted to the
first chapter only. Prints live progress to console.

    export OPENAI_API_KEY="sk-..."
    export MARD_SPEND_CAP_USD=50
    .venv/bin/python scripts/smoke_mard_verbose.py
"""

from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

from mard.run import TIER1_REASONING_EFFORT, TIER2_MAX_TOKENS, TIER2_REASONING_EFFORT, run_mard
from provider.rates import build_rate_card
from runlog import RunLogger, SpendCap, SpendLedger

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / "corpus"
DOCUMENT_ID = "introcs"
TIER1_MODEL = "gpt-5.2"
TIER2_MODEL = "gpt-5-mini"
MAX_CHAPTERS = 1
ESTIMATED_USD = 2.0


def tail_events(run_dir: Path, stop_event: threading.Event) -> None:
    """Print events from events.jsonl as they appear."""
    events_file = run_dir / "events.jsonl"
    last_pos = 0
    
    # Wait for file to exist
    while not events_file.exists() and not stop_event.is_set():
        time.sleep(0.1)
    
    if not events_file.exists():
        return
    
    print("\n[live events]")
    while not stop_event.is_set():
        try:
            with open(events_file, "r") as f:
                f.seek(last_pos)
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        kind = event.get("kind", "unknown")
                        at = event.get("at", "")
                        
                        # Pretty-print key events
                        if kind == "mard_pass0":
                            print(f"  ✓ Pass 0: {event['topics_accepted']} topics accepted")
                        elif kind == "mard_pass1":
                            print(f"  ✓ Pass 1: {event['concepts_accepted']} concepts, {event['edges_accepted']} edges ({event['chapters_explored']}/{event['chapters_total']} chapters)")
                        elif kind == "mard_compile_plan":
                            print(f"  ✓ Compile: {event['concepts']} concepts → {event['plan_order']}")
                        elif kind == "tier2_fork":
                            print(f"  ✓ Tier 2: Launching {event['builders']} builders")
                        elif kind == "tier2_join":
                            print(f"  ✓ Join: {len(event['concept_order'])} concepts synthesized")
                last_pos = f.tell()
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        time.sleep(0.5)


def main() -> int:
    cap = SpendCap.from_env()
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    print(f"[smoke] spend cap ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")
    ledger.check_before_run(ESTIMATED_USD)

    run_dir_ref = {"run_dir": None}
    
    with RunLogger.start(
        runs_root=REPO_ROOT / "runs",
        system="mard_smoke",
        document_id=DOCUMENT_ID,
        seed=0,
        models={"tier1": TIER1_MODEL, "tier2": TIER2_MODEL},
        params={
            "max_chapters": MAX_CHAPTERS,
            "smoke": True,
            "tier1_reasoning_effort": TIER1_REASONING_EFFORT,
            "tier2_reasoning_effort": TIER2_REASONING_EFFORT,
            "tier2_max_tokens": TIER2_MAX_TOKENS,
        },
        rate_card=build_rate_card(),
    ) as run:
        run_dir_ref["run_dir"] = run.run_dir
        
        # Start event printer thread
        stop_event = threading.Event()
        printer = threading.Thread(
            target=tail_events,
            args=(run.run_dir, stop_event),
            daemon=True
        )
        printer.start()
        
        print(f"[smoke] Starting MARD run...")
        print(f"[smoke] Tier 1 (Pass 0 + Pass 1): {TIER1_MODEL}")
        print(f"[smoke] Tier 2 (synthesis): {TIER2_MODEL}")
        
        result = run_mard(
            CORPUS_DIR,
            DOCUMENT_ID,
            tier1_model=TIER1_MODEL,
            tier2_model=TIER2_MODEL,
            logger=run,
            max_chapters=MAX_CHAPTERS,
        )
        
        stop_event.set()
        printer.join(timeout=1)
        
        run.set_result(
            {
                "concepts_accepted": result.concepts_accepted,
                "edges_accepted": result.edges_accepted,
                "compiled": result.compiled,
            }
        )
        totals = run.totals()
        run_id = run.run_id
        run_dir = run.run_dir

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    ledger.record(summary)

    print()
    print("=" * 72)
    print(f"[smoke] RUN COMPLETE")
    print("=" * 72)
    print(f"[smoke] run_id: {run_id}")
    print(f"[smoke] tokens in/out: {totals['input_tokens']:,} / {totals['output_tokens']:,}")
    print(f"[smoke] cost: ${totals['cost']:.4f}")
    print(f"[smoke] concepts_accepted: {result.concepts_accepted}")
    print(f"[smoke] edges_accepted: {result.edges_accepted}")
    print(f"[smoke] compiled: {result.compiled}")
    for trace in result.pass1_traces:
        rejected = trace["rejected"]
        flag = " <-- FIX NOT WORKING" if any("explorer returned" in r for r in rejected) else ""
        print(
            f"[smoke] chapter {trace['chapter_id']}: envelope "
            f"{trace['envelope']['rendered_chars']} chars, "
            f"{trace['concepts_accepted']} concepts, rejected={rejected}{flag}"
        )
    print(f"[smoke] full trace: {run_dir / 'events.jsonl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
