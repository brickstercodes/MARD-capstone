#!/usr/bin/env python
"""Full MARD run with verbose real-time logging.

One real, fully-logged MARD run on the complete corpus, with live event printing.

    export OPENAI_API_KEY="sk-..."
    export MARD_SPEND_CAP_USD=50
    .venv/bin/python scripts/run_mard_full_verbose.py 42 --document-id axler
    .venv/bin/python scripts/run_mard_full_verbose.py 11 --document-id introcs
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from pathlib import Path

from mard.run import TIER1_REASONING_EFFORT, TIER2_MAX_TOKENS, TIER2_REASONING_EFFORT, run_mard
from provider.rates import build_rate_card
from runlog import CAMPAIGN_SEEDS, RunLogger, SpendCap, SpendLedger

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO_ROOT / "corpus"
TIER1_MODEL = "gpt-5.2"
TIER2_MODEL = "gpt-5-mini"
ESTIMATED_USD = 5.0


def tail_events(run_dir: Path, stop_event: threading.Event) -> None:
    """Print events from events.jsonl as they appear."""
    events_file = run_dir / "events.jsonl"
    last_pos = 0
    event_count = 0
    
    # Wait for file to exist
    while not events_file.exists() and not stop_event.is_set():
        time.sleep(0.1)
    
    if not events_file.exists():
        return
    
    print("\n[=== LIVE EVENTS ===]")
    while not stop_event.is_set():
        try:
            with open(events_file, "r") as f:
                f.seek(last_pos)
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        kind = event.get("kind", "unknown")
                        
                        # Pretty-print key events
                        if kind == "mard_pass0":
                            print(f"  [Pass 0] Topics: {event['topics_accepted']}/{event['topics_requested']}, Skeleton: ~{event['estimated_render_tokens']} tokens")
                        elif kind == "mard_pass1":
                            pct = 100 * event['chapters_explored'] / event['chapters_total']
                            print(f"  [Pass 1] {event['chapters_explored']}/{event['chapters_total']} chapters ({pct:.0f}%): {event['concepts_accepted']} concepts, {event['edges_accepted']} edges")
                        elif kind == "mard_cross_chapter_edges":
                            if event['total_edges'] > 0:
                                rate = event['cross_chapter_edges'] / event['total_edges']
                                print(f"  [Links] {event['cross_chapter_edges']}/{event['total_edges']} edges cross chapters ({rate:.1%})")
                        elif kind == "mard_compile_plan":
                            print(f"  [Plan] {event['concepts']} concepts compiled, {event['moves']} moved to plan order")
                        elif kind == "tier2_fork":
                            print(f"  [Tier 2] Launching {event['builders']} concurrent builders...")
                        elif kind == "tier2_join":
                            print(f"  [Join] Synthesized {len(event['concept_order'])} concepts into final artefact")
                        elif kind == "call_complete":
                            # Show token usage for major calls
                            if "input_tokens" in event:
                                print(f"  [API] {event.get('model', 'unknown')}: {event.get('input_tokens', 0):,} in / {event.get('output_tokens', 0):,} out")
                        
                        event_count += 1
                last_pos = f.tell()
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        time.sleep(0.5)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", type=int, choices=CAMPAIGN_SEEDS)
    parser.add_argument("--ablation", choices=["a1s", "a1f"], default=None)
    parser.add_argument("--document-id", default="introcs")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    system = f"mard_{args.ablation}" if args.ablation else "mard"
    document_id = args.document_id

    cap = SpendCap.from_env()
    ledger = SpendLedger(REPO_ROOT / "runs", cap)
    seed_index = CAMPAIGN_SEEDS.index(args.seed)
    
    print("=" * 72)
    print(f"[mard] Configuration")
    print("=" * 72)
    print(f"[mard] System: {system}")
    print(f"[mard] Document: {document_id}")
    print(f"[mard] Seed: {args.seed} (index {seed_index})")
    print(f"[mard] Spend cap: ${cap.ceiling_usd:.2f}, ${ledger.remaining:.2f} remaining")
    print(f"[mard] Tier 1 (exploration): {TIER1_MODEL}")
    print(f"[mard] Tier 2 (synthesis): {TIER2_MODEL}")
    print()
    
    ledger.check_before_run(ESTIMATED_USD)

    with RunLogger.start(
        runs_root=REPO_ROOT / "runs",
        system=system,
        document_id=document_id,
        seed=args.seed,
        models={"tier1": TIER1_MODEL, "tier2": TIER2_MODEL},
        params={
            "ablation": args.ablation,
            "tier1_reasoning_effort": TIER1_REASONING_EFFORT,
            "tier2_reasoning_effort": TIER2_REASONING_EFFORT,
            "tier2_max_tokens": TIER2_MAX_TOKENS,
        },
        rate_card=build_rate_card(),
    ) as run:
        # Start event printer thread
        stop_event = threading.Event()
        printer = threading.Thread(
            target=tail_events,
            args=(run.run_dir, stop_event),
            daemon=True
        )
        printer.start()
        
        print("[mard] Starting run...")
        result = run_mard(
            CORPUS_DIR,
            document_id,
            tier1_model=TIER1_MODEL,
            tier2_model=TIER2_MODEL,
            logger=run,
            ablation=args.ablation,
        )
        
        stop_event.set()
        printer.join(timeout=1)
        
        run.set_result(
            {
                "compiled": result.compiled,
                "concepts_accepted": result.concepts_accepted,
                "edges_accepted": result.edges_accepted,
                "cross_chapter_edges": result.cross_chapter_edges,
                "never_declared_rejections": result.never_declared_rejections,
            }
        )
        totals = run.totals()
        run_id = run.run_id
        run_dir = run.run_dir

    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    ledger.record(summary)

    print()
    print("=" * 72)
    print(f"[{system}] RUN COMPLETE")
    print("=" * 72)
    print(f"[{system}] run_id: {run_id}")
    print(f"[{system}] tokens in/out: {totals['input_tokens']:,} / {totals['output_tokens']:,}")
    print(f"[{system}] cost: ${totals['cost']:.4f}")
    print(f"[{system}] compiled: {result.compiled}")
    print(f"[{system}] concepts_accepted: {result.concepts_accepted}")
    print(f"[{system}] edges_accepted: {result.edges_accepted}")
    print(f"[{system}] cross_chapter_edges: {result.cross_chapter_edges}")
    print(f"[{system}] never_declared_rejections: {result.never_declared_rejections}")
    if result.artefact is not None:
        print(f"[{system}] artefact saved to {run_dir / 'artefacts' / 'tier2_output.md'}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
