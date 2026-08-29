# MARD Demo Checklist

Verify setup in 5 minutes before presenting.

## Setup (One-Time)

- [ ] OpenAI key obtained
- [ ] .venv created and .env file with OPENAI_API_KEY=sk-...
- [ ] Dependencies: pip install -e .
- [ ] Clean ledger: rm -f runs/_ledger.json
- [ ] Spending cap: export MARD_SPEND_CAP_USD=50

## 5-Minute Pre-Demo Test

```bash
cd ~/Desktop/Capstone/MARD-capstone
source .venv/bin/activate

python3 -c "import mard; print('OK')"
grep "OPENAI_API_KEY" .env
python scripts/smoke_mard_verbose.py
```

Expected: Completes in ~60 sec with live output.

## During Demo

Quick demo (60 sec):
```bash
python scripts/smoke_mard_verbose.py
```

Full demo (3-5 min):
```bash
python scripts/run_mard_full_verbose.py 42 --document-id axler
```

After run:
```bash
cat runs/mard-42-*/summary.json | python3 -m json.tool
head -50 runs/mard-42-*/artefacts/tier2_output.md
python scripts/demo_results.py
```

## Quick Fixes

- Import error: pip install -e .
- No API key: cat .env
- Spend cap exceeded: export MARD_SPEND_CAP_USD=100
- Timeout: Wait 2 min, API can be slow

## Success

- Smoke test runs without errors
- Live events print in real-time
- Cost under budget
- Concepts/edges found
- Artefact generated

You're ready!
