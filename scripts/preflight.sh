#!/usr/bin/env bash
# Run before spending a token. Every check here has cost this project time at least once.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
FAIL=0
ok(){ printf '  \033[32mOK\033[0m   %s\n' "$1"; }
bad(){ printf '  \033[31mFAIL\033[0m %s\n' "$1"; FAIL=1; }

echo "== preflight =="

# 1. venv active, and it is THIS project's venv.
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  bad "no virtualenv active - run: source .venv/bin/activate"
else
  ok "venv active: ${VIRTUAL_ENV}"
fi
PY="${VIRTUAL_ENV:-.venv}/bin/python"

# 2. Exactly one importable rlm, and it is the pinned vendored one.
#    A second editable install wins silently and you cannot tell which code ran.
RLM_PATH="$(cd / && "$PY" -c 'import rlm; print(rlm.__file__)' 2>/dev/null || true)"
if [[ -z "$RLM_PATH" ]]; then
  bad "import rlm failed - run scripts/bootstrap_rlm.sh"
elif [[ "$RLM_PATH" != *".vendor/rlm/"* ]]; then
  bad "rlm resolves to $RLM_PATH, not .vendor/rlm - a stale install is shadowing it"
else
  ok "rlm -> $RLM_PATH"
fi

# 3. The pinned SHA. A moving control library makes every number unattributable.
SHA="$(git -C .vendor/rlm rev-parse --short HEAD 2>/dev/null || echo none)"
[[ "$SHA" == 62acf7b* ]] && ok "vendored rlm @ $SHA" || bad "vendored rlm @ $SHA, expected 62acf7b"

# 4. Spend cap. SpendCap.from_env() refuses to run without it; 780 is the void figure.
CAP="${MARD_SPEND_CAP_USD:-unset}"
if [[ "$CAP" == "unset" ]]; then bad "MARD_SPEND_CAP_USD unset"
elif [[ "$CAP" == "780" ]]; then bad "MARD_SPEND_CAP_USD=780 - that is the VOID stranded-credit figure (docs/22)"
else ok "MARD_SPEND_CAP_USD=$CAP"; fi

# 5. API key present but never printed.
[[ -n "${OPENAI_API_KEY:-}" ]] && ok "OPENAI_API_KEY set" || bad "OPENAI_API_KEY unset"

# 6. Corpus provenance. A measured run against an unverified corpus is not a measured run.
if "$PY" -m ingest.manifest corpus --document-id introcs >/dev/null 2>&1; then
  ok "corpus manifest verified (introcs)"
else
  bad "corpus manifest FAILED - see ingest/manifest.py"
fi

# 7. Front-matter exclusion. This is the bug that produced a whole garbage run once.
T=corpus/introcs/document.txt
if [[ -f "$T" ]]; then
  A=$(grep -c "PART 1 PROBLEM SOLVING" "$T" || true)
  B=$(grep -cE '^#{1,6} .*Chapter Outline' "$T" || true)
  { [[ "$A" == "0" ]] && [[ "$B" == "14" ]]; } \
    && ok "front matter excluded (toc-leak=0, chapter-outlines=14)" \
    || bad "structure check: toc-leak=$A (want 0), chapter-outlines=$B (want 14)"
else
  bad "$T missing - run scripts/fetch_corpus.sh introcs"
fi

# 8. Quality gates.
"$PY" -m pytest -q >/dev/null 2>&1 && ok "tests pass" || bad "tests FAILING"
command -v ruff >/dev/null && { ruff check . >/dev/null 2>&1 && ok "ruff clean" || bad "ruff check FAILING"; }

echo
[[ $FAIL -eq 0 ]] && echo "preflight PASSED - clear to run." \
  || { echo "preflight FAILED - fix the above and nothing else."; exit 1; }
