#!/usr/bin/env bash
# Format, lint, type-check, test. Run before every commit.
#
# One script rather than four remembered commands, because the failure this
# guards against is a freeze-week commit that breaks a teammate's imports.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

# Bare `ruff`/`mypy`/`pytest` outside a venv print "command not found" and exit
# non-zero, which this script then reports as "Checks failed" — a setup mistake
# wearing the costume of a lint failure. Resolve the tools from the venv and
# fail with the fix instead.
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "!! No virtualenv active. Run:"
  echo "     python3 -m venv .venv && source .venv/bin/activate && pip install -e '.[dev]'"
  exit 1
fi

# VIRTUAL_ENV being set is not enough. A venv records absolute paths, so
# renaming the project directory leaves an activated-looking shell whose tools
# have quietly fallen through to whatever is next on PATH.
VENV_BIN="${VIRTUAL_ENV}/bin"
if [[ ! -x "${VENV_BIN}/python" ]]; then
  echo "!! VIRTUAL_ENV points at ${VIRTUAL_ENV} but there is no interpreter there."
  echo "   The venv is stale — usually because the project folder was renamed."
  echo "   Rebuild it:"
  echo "     deactivate; rm -rf .venv && python3 -m venv .venv"
  echo "     source .venv/bin/activate && pip install -e '.[dev]'"
  exit 1
fi

# A venv without the dev extras fails identically to no venv at all. It is the
# likelier mistake on a fresh clone, so name it separately.
MISSING=()
for tool in ruff mypy pytest; do
  [[ -x "${VENV_BIN}/${tool}" ]] || MISSING+=("${tool}")
done
if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "!! Not installed in ${VIRTUAL_ENV}: ${MISSING[*]}"
  echo "   The dev extras are missing. Run:"
  echo "     pip install -e '.[dev]'"
  exit 1
fi

STATUS=0
run() {
  # Headers name the tool, not its absolute path in the venv.
  echo
  echo "=== $(basename "$1") ${*:2} ==="
  "$@" || STATUS=1
}

run "${VENV_BIN}/ruff" format --check .
run "${VENV_BIN}/ruff" check .
run "${VENV_BIN}/mypy" runlog
run "${VENV_BIN}/pytest" -q

echo
if [[ ${STATUS} -eq 0 ]]; then
  echo "All checks passed."
else
  echo "Checks failed. Fix before committing."
fi
exit ${STATUS}
