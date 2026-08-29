# MARD Live Demo Setup

Quick walkthrough for running MARD with **live verbose logging** so your professor sees real-time progress.

## What You Need
- OpenAI API key (from https://platform.openai.com/api/keys)
- Python 3.10+
- ~$1-3 budget for the demo

## 60-Second Setup

```bash
cd ~/Desktop/Capstone/MARD-capstone
source .venv/bin/activate

# Create .env with your API key (one-time)
cat > .env << 'ENVFILE'
OPENAI_API_KEY=sk-YOUR_KEY_HERE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project"}
ENVFILE

# Clean ledger for fresh demo (one-time)
rm -f runs/_ledger.json

# Set spending limit
export MARD_SPEND_CAP_USD=50
```

## Run the Demo (With Live Logging)

**Quick test (60 sec, $0.50) — Shows all real-time events:**
```bash
python scripts/smoke_mard_verbose.py
```

**Full demo (3-5 min, $1.50) — Shows live progress on full corpus:**
```bash
python scripts/run_mard_full_verbose.py 42 --document-id axler
```

Or for the full paper corpus (longer):
```bash
python scripts/run_mard_full_verbose.py 11 --document-id introcs
```

## What Your Professor Will See

As the script runs, you'll see **live events** printed in real-time:
- Pass 0 extracting topics from skeleton
- Pass 1 exploring chapters and finding concepts/edges
- Plan reordering concepts based on dependencies
- Tier 2 synthesizing into final narrative

With cost, tokens, and metrics updating live.

## After the Run Completes

Show the results:

```bash
# Show summary metrics
cat runs/mard-42-*/summary.json | python3 -m json.tool

# Show generated synthesis
cat runs/mard-42-*/artefacts/tier2_output.md

# Compare to baseline (paper table)
python scripts/demo_results.py
```

## Verify Reproducibility with SHA-256

Prove the corpus hasn't changed:

```bash
cd corpus/axler
find . -name "*.md" -type f -exec sha256sum {} \; | sort > checksums.txt
sha256sum -c checksums.txt  # All should show: OK
```

## Test Corpora (Pick One)

| Corpus | Chapters | Time | Cost |
|--------|----------|------|------|
| axler | 5 | 45s | $0.50 |
| introcs | 16 | 3-5m | $1.50 |
| physics1 | 8 | 1-2m | $0.75 |

Start with axler for a quick demo.

## What MARD Demonstrates

1. **Metadata Envelope:** Structural metadata threads through recursive calls
2. **Cross-Chapter Links:** Finds 0.917 rate vs 0.014 without envelope
3. **Efficiency:** 15.8x token reduction vs vanilla RLM
4. **Reproducibility:** SHA-256 hashes prove corpus immutability

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Import error | pip install -e . |
| No API key | cat .env and verify |
| Spend cap exceeded | export MARD_SPEND_CAP_USD=100 |

---

Tip: Run smoke_mard_verbose.py once before demo!
