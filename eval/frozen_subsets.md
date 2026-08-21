# Frozen Evaluation Subsets — BrowseComp-Plus & OOLONG

**Status: FROZEN.** Track 3 W0 deliverable, issue #19. Per the project's
evidence-discipline rule (CONTEXT.md §4.3): the method and seed were fixed
before any result exists, and what these steps produced is the canonical,
immutable version — it is not revisited or re-run to get a "nicer" sample,
even though this run's hashes don't (and are not expected to) bit-match any
other run of the same steps on a different machine/library version.

Both files under `eval/frozen_subsets/` are immutable **as of the commit that
adds them**. Any future change to either file's contents is a new,
separately-named subset (e.g. `_v2`) — never an edit to these two.

---

## 1. OOLONG negative-control subset (`trec_coarse`, n=50)

**Source:** Bertsch et al., *Oolong: Evaluating long context reasoning and
aggregation capabilities*, arXiv:2511.02817. `trec_coarse` split, 131,072-token
context length (matches the RLM base paper's Table 1 OOLONG setting).
OOLONG is the project's negative control (flat context, no exploitable
hierarchy) — see CONTEXT.md glossary and O4.

**Method:** the benchmark's own `generate_dataset.py` (from
`github.com/abertsch72/oolong`, `src/data_gen/oolong-synth/`) regenerates the
real task pool deterministically from its human-labeled source corpus, then a
seeded downsample selects 50 of the generated instances. The benchmark's own
`subsample.py` was deliberately **not** used — it is a hardcoded,
un-seeded, multi-dataset research script, not independently reproducible even
by its own authors.

**Commands actually run** (Python 3.12.10 — the repo's `EvalContextWindow.py`
uses a backslash inside an f-string expression, which only parses on 3.12+):

```bash
git clone https://github.com/abertsch72/oolong.git
cd oolong/src/data_gen/oolong-synth
pip install torch transformers datasets tiktoken litellm jsonlines python-dateutil anthropic google-genai
python freeze_oolong.py   # see script below
```

```python
import random, sys, json, pickle
sys.path.insert(0, '.')
from generate_dataset import generate_dataset

SEED = 42
random.seed(SEED)
generate_dataset("trec_coarse", repeats=1, context_lens=[17])  # 2**17 = 131072

with open("oolong-synth-datagen/trec_coarse.pkl", "rb") as f:
    d = pickle.load(f)

n = len(d["id"])
records = [{k: d[k][i] for k in d} for i in range(n)]
records = sorted(records, key=lambda r: r["id"])

random.seed(SEED)  # re-seed independently for the downsample step
chosen = sorted(random.sample(records, 50), key=lambda r: r["id"])
# ... write context window + task metadata, see repo history for full script
```

This run generated **139** raw task instances at 131K context, then
downsampled 50 of them with `random.seed(42)`.

**Files:**
- `eval/frozen_subsets/oolong_trec_coarse_50_frozen_tasks.jsonl` — 50 task
  records (question, answer, task type, etc.), one per line.
- `eval/frozen_subsets/oolong_context_window_131k.txt` — the single shared
  131K-token context window all 50 tasks are asked against.

**sha256 (this run, actually produced):**
```
b6c451e183e348cd35d168c9830e28b435f002e12367e0ee01672c907d34c085  oolong_trec_coarse_50_frozen_tasks.jsonl
80747454c9c293d13a39eb0c6f453b05fdc0c74f6439493dcd49bb12d2ce9089  oolong_context_window_131k.txt
```

**Note on reproducibility:** a different `transformers`/`torch` version can
change how many internal random calls are consumed before the seed reaches
the downsample step, so a re-run elsewhere is not expected to bit-match these
hashes. That is fine and expected — these hashes are the frozen record for
this project, not a target to reproduce.

**OOLONG-Pairs is explicitly excluded from this freeze.** It is a separate,
harder, paper-fixed 20-task benchmark (pairwise aggregation, quadratic
scaling), already fully enumerated in the RLM paper's own Appendix D.1 —
nothing to generate or sample for it.

---

## 2. BrowseComp-Plus subset (n=20)

**Source:** Patel et al., *BrowseComp-Plus: A more fair and transparent
evaluation benchmark of deep-research agents*, arXiv:2508.06600. Decrypted
from the gated `Tevatron/browsecomp-plus` HF dataset (830 real queries total,
each with gold/negative/evidence documents as full text).

**Method:** `random.seed(42); random.sample(records, 20)` over the full,
real, decrypted 830-query set, sorted by `query_id` before and after
sampling. N=20 follows the RLM paper's own Appendix D.2 precedent (20-of-150
queries), applied here to the full real dataset since the RLM authors' exact
150-query pre-sample was never published and cannot be reproduced by anyone
outside that paper. **This is our own legitimate seed-42 sample of the real
benchmark, following the RLM paper's methodology — it is not, and is not
claimed to be, a reproduction of the RLM paper authors' literal instances.**

**Commands actually run:**

```bash
pip install datasets huggingface_hub
huggingface-cli login   # HF access token, read scope; gate accepted at
                         # huggingface.co/datasets/Tevatron/browsecomp-plus

git clone https://github.com/texttron/BrowseComp-Plus.git
cd BrowseComp-Plus
python scripts_build_index/decrypt_dataset.py \
  --output data/browsecomp_plus_decrypted.jsonl \
  --generate-tsv topics-qrels/queries.tsv
python freeze_browsecomp_plus_subset.py   # see script below
```

```python
import argparse, hashlib, json, random
from collections import defaultdict

SEED = 42
N = 20

def load_qrels(path):
    out = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            qid, _, docid = parts[0], parts[1], parts[2]
            out[qid].append(docid)
    return out

records = [json.loads(l) for l in open("data/browsecomp_plus_decrypted.jsonl", encoding="utf-8") if l.strip()]

def sort_key(r):
    qid = str(r.get("query_id", ""))
    return (0, int(qid)) if qid.isdigit() else (1, qid)

records = sorted(records, key=sort_key)
random.seed(SEED)
chosen = sorted(random.sample(records, N), key=sort_key)

golds = load_qrels("topics-qrels/qrel_golds.txt")
evidence = load_qrels("topics-qrels/qrel_evidence.txt")
# each chosen record gets gold_docids / evidence_docids attached, then written
# to browsecomp_plus_frozen_20.jsonl -- see repo history for full script
```

This run loaded **830** real decrypted queries and sampled 20.

**Frozen query IDs (n=20):**
```
1022, 1071, 1169, 1177, 1179, 149, 159, 174, 186, 235, 362, 371, 408, 464, 50, 55, 58, 682, 864, 942
```

**File:** `eval/frozen_subsets/browsecomp_plus_frozen_20.jsonl` — 20 real
queries, each with `query`, `answer`, `gold_docs`/`negative_docs`/
`evidence_docs` (full document text) and `gold_docids`/`evidence_docids`
(from `topics-qrels/qrel_golds.txt` / `qrel_evidence.txt`). ~57MB, since full
document text is embedded per query (not a bug — this is the actual QA
context).

**sha256 (canonical ID-based hash, printed by the freeze script — not a
raw-file hash, so it stays stable across cosmetic JSON re-serialization):**
```
c2d944883115fc8ca75db2a9f5fa134ded25bdfa2b0a0eea6575abeb413e1e87  (bcp_w0_20_real|total=830|n=20|seed=42|method=random.sample|<sorted query IDs>)
```

**Note on Windows encoding:** the freeze script's `open()` calls were changed
to explicit `encoding="utf-8"` (vs. the platform default) to run on Windows,
where some document text in the corpus isn't valid cp1252. This is an I/O
fix only — it does not touch sampling, seeding, or output content.

---

## 3. Not part of this freeze

- **OOLONG-Pairs** — separate, paper-fixed 20-task benchmark (RLM paper
  Appendix D.1), fully enumerated already, nothing to generate.
- Final subset *size* (BrowseComp-Plus N=20, OOLONG N=50-of-generated-pool)
  may still need revisiting once Anugrah's model-pair/budget-ceiling decision
  lands — the *selection method and seed* are locked now regardless, per
  CONTEXT.md §4.3.
