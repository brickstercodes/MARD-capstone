#!/usr/bin/env bash
# Install the RLM base library and run its own examples, capturing the output.
#
# Issue #11 asks for the library "running its own examples end-to-end". That is a
# claim about this machine on this day, so it gets evidence rather than a tick:
# everything below is teed into runs/_bootstrap/ and can be attached to the
# issue. If the base library does not work here, that has to surface in W0 —
# Track 3 needs the vanilla RLM control running in W1 and it is built on this.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${REPO_ROOT}/runs/_bootstrap"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="${OUT_DIR}/bootstrap_${STAMP}.log"
RLM_REPO="https://github.com/alexzhang13/rlm"
VENDOR_DIR="${REPO_ROOT}/.vendor/rlm"

mkdir -p "${OUT_DIR}" "${REPO_ROOT}/.vendor"
exec > >(tee -a "${LOG}") 2>&1

echo "=== MARD bootstrap · ${STAMP} ==="
echo "repo root : ${REPO_ROOT}"
echo

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "!! No virtualenv active. Run:"
  echo "     python3 -m venv .venv && source .venv/bin/activate && pip install -e '.[dev]'"
  echo "   Installing into the system interpreter makes the config snapshot"
  echo "   unreproducible, which defeats the point of the run log."
  exit 1
fi

# VIRTUAL_ENV being set is not enough. A venv records absolute paths, so renaming
# the project directory leaves an activated-looking shell whose `python3` has
# quietly fallen through to the system interpreter — and the install then either
# fails on PEP 668 or, worse, succeeds system-wide and poisons the snapshot.
PY="${VIRTUAL_ENV}/bin/python"
if [[ ! -x "${PY}" ]]; then
  echo "!! VIRTUAL_ENV points at ${VIRTUAL_ENV} but there is no interpreter there."
  echo "   The venv is stale — usually because the project folder was renamed."
  echo "   Rebuild it:"
  echo "     deactivate; rm -rf .venv && python3 -m venv .venv"
  echo "     source .venv/bin/activate && pip install -e '.[dev]'"
  exit 1
fi
RESOLVED="$(command -v python3 || true)"
if [[ "${RESOLVED}" != "${VIRTUAL_ENV}/"* ]]; then
  echo "!! python3 resolves to ${RESOLVED}, outside the active venv ${VIRTUAL_ENV}."
  echo "   Using ${PY} explicitly instead."
fi

echo "python    : $("${PY}" --version 2>&1)"
echo "pip       : $("${PY}" -m pip --version)"
echo

echo "--- 1. clone or update the RLM base library ---"
# Vendored as a working copy rather than a pinned pip install because the
# examples live in the repo, and reproducing a base-paper number in W1 means
# reading their eval setup, not just importing the package.
if [[ -d "${VENDOR_DIR}/.git" ]]; then
  git -C "${VENDOR_DIR}" pull --ff-only
else
  git clone "${RLM_REPO}" "${VENDOR_DIR}"
fi
RLM_SHA="$(git -C "${VENDOR_DIR}" rev-parse HEAD)"
echo "RLM commit: ${RLM_SHA}"
echo

echo "--- 2. install it ---"
"${PY}" -m pip install -e "${VENDOR_DIR}"
echo

echo "--- 3. import check ---"
"${PY}" -c "import rlm; print('rlm imported from', rlm.__file__)"
echo

echo "--- 4. list the examples we are expected to run ---"
find "${VENDOR_DIR}" -maxdepth 2 \( -name 'example*' -o -name 'examples' -o -name 'demo*' \) -print
echo
echo "Run each one manually and paste the result below this line in the log."
echo "An example that needs an API key will fail until keys are provisioned —"
echo "record that as blocked, not as broken."
echo

echo "--- 5. record what was installed ---"
"${PY}" -m pip freeze > "${OUT_DIR}/pip_freeze_${STAMP}.txt"
cat > "${OUT_DIR}/rlm_${STAMP}.json" <<EOF
{
  "rlm_repo": "${RLM_REPO}",
  "rlm_commit": "${RLM_SHA}",
  "captured_at": "${STAMP}",
  "python": "$("${PY}" --version 2>&1)"
}
EOF

echo
echo "Done. Evidence in ${OUT_DIR}"
echo "Attach ${LOG} to issue #11 before ticking the box."
