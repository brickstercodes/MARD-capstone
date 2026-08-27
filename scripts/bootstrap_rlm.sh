#!/usr/bin/env bash
# Vendor the RLM control library — Arav's Zhang_RLM fork (docs/18-W3_PROVIDER_SWITCH.md
# §4.2, reversed 27 Aug 2026) — pinned at 62acf7b, and install it editable.
#
# Pinned rather than pulled to latest: a moving control library makes every measured
# number unattributable. Same vendor-as-working-copy rationale as before (the fork's
# own tests and examples matter, not just the importable package), same iCloud
# hidden-.pth fix, same "run from /" import check — each exists because of a real
# incident recorded here and in this script's own history.
#
# `replm` (FalseAdvertising/Vanilla_RLM_Python) is retired — no longer the control,
# and no longer vendored at all (scripts/bootstrap_replm.sh and .vendor/replm/ are
# both deleted; see docs/18 §4.2's superseded-not-erased record).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${REPO_ROOT}/runs/_bootstrap"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="${OUT_DIR}/bootstrap_${STAMP}.log"
RLM_REPO="https://github.com/FalseAdvertising/Zhang_RLM"
PINNED_SHA="62acf7b9fb70baf78b899213fec5aea9951c8341"
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

echo "--- 1. remove any prior rlm install/vendor copy ---"
# Zhang_RLM is a fork of alexzhang13/rlm and installs under the same distribution
# name (rlms), importable as `rlm`. Installing both editable means the last install
# silently wins and there is no way to tell which code ran — replace, don't add.
"${PY}" -m pip uninstall -y rlms >/dev/null 2>&1 || true
rm -rf "${VENDOR_DIR}"
echo "cleared prior rlms install and ${VENDOR_DIR}"
echo

echo "--- 2. clone and pin ${PINNED_SHA} ---"
git clone "${RLM_REPO}" "${VENDOR_DIR}"
git -C "${VENDOR_DIR}" checkout "${PINNED_SHA}"
RLM_SHA="$(git -C "${VENDOR_DIR}" rev-parse HEAD)"
echo "RLM commit: ${RLM_SHA}"
if [[ "${RLM_SHA}" != "${PINNED_SHA}" ]]; then
  echo "!! Resolved SHA ${RLM_SHA} does not match the pinned ${PINNED_SHA}. Aborting."
  exit 1
fi
echo

echo "--- 3. install it ---"
"${PY}" -m pip install -e "${VENDOR_DIR}"

# An editable install resolves through a .pth file, and CPython 3.14's
# site.addpackage skips any .pth carrying the macOS hidden flag — silently, with
# no warning and a zero exit. It happened here between 3 and 4 Aug 2026 and cost
# a day: `import rlm` was dead while the whole test suite stayed green, because
# pytest puts the repo root on sys.path. Clearing the flag is idempotent and
# cheap; diagnosing it a second time is not.
SITE_PACKAGES="$("${PY}" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
if command -v chflags >/dev/null 2>&1; then
  chflags nohidden "${SITE_PACKAGES}"/__editable__* 2>/dev/null || true
fi
echo

echo "--- 4. import check ---"
# From / rather than here: run in the repo root, this passes on sys.path[0]
# alone and proves nothing about the install.
(cd / && "${PY}" -c "import rlm; print('rlm imported from', rlm.__file__)")
echo

echo "--- 5. record what was installed ---"
"${PY}" -m pip freeze > "${OUT_DIR}/pip_freeze_${STAMP}.txt"
cat > "${OUT_DIR}/rlm_${STAMP}.json" <<EOF
{
  "rlm_repo": "${RLM_REPO}",
  "rlm_commit": "${RLM_SHA}",
  "pinned_sha": "${PINNED_SHA}",
  "captured_at": "${STAMP}",
  "python": "$("${PY}" --version 2>&1)"
}
EOF

echo
echo "Done. Evidence in ${OUT_DIR}"
echo "Vendored at ${VENDOR_DIR}, pinned to ${RLM_SHA}."
