#!/usr/bin/env bash
# Format, lint, type-check, test. Run before every commit.
#
# One script rather than four remembered commands, because the failure this
# guards against is a freeze-week commit that breaks a teammate's imports.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

STATUS=0
run() {
  echo
  echo "=== $* ==="
  "$@" || STATUS=1
}

run ruff format --check .
run ruff check .
run mypy runlog
run pytest -q

echo
if [[ ${STATUS} -eq 0 ]]; then
  echo "All checks passed."
else
  echo "Checks failed. Fix before committing."
fi
exit ${STATUS}
