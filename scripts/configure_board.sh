#!/bin/bash
#
# Populate GitHub Projects v2 field values for the MARD backlog.
#
# Needs bash 4+ for associative arrays. macOS ships bash 3.2 as /bin/bash and
# `bash` on PATH, so plain "bash script.sh" silently runs the wrong one even
# after `brew install bash` - the system bash shadows Homebrew's on PATH.
# The self-exec below finds a real bash 4+ (checking common Homebrew
# locations first) and re-execs into it, so callers do not have to remember
# the full path themselves.
if [ -z "${BASH_VERSINFO:-}" ] || [ "${BASH_VERSINFO[0]}" -lt 4 ]; then
  for candidate in /opt/homebrew/bin/bash /usr/local/bin/bash bash; do
    found="$(command -v "$candidate" 2>/dev/null || true)"
    if [ -n "$found" ]; then
      ver="$("$found" -c 'echo "${BASH_VERSINFO[0]}"' 2>/dev/null || echo 0)"
      if [ "$ver" -ge 4 ] 2>/dev/null; then
        exec "$found" "$0" "$@"
      fi
    fi
  done
  echo "FATAL: could not find bash 4+. Run: brew install bash" >&2
  echo "       Then invoke directly: /opt/homebrew/bin/bash $0 $*" >&2
  exit 1
fi
#
# The board is unreadable out of the box because every custom field is empty:
# Roadmap has no dates to draw, there is nothing to group columns by except
# Status, and 45 identical-looking cards sit in one Backlog column.
#
# Labels cannot fix this. Projects v2 will not group a board by Labels, because
# labels are multi-valued. Grouping requires a single-select field, so this
# script creates Track / Phase / Block fields and derives their values from the
# issue titles, which are deterministic (see seed_github_issues.sh).
#
# It also sets Start/End dates per block so the Roadmap view renders, and
# Priority so "what is urgent right now" is visible without reading 45 cards.
#
# View LAYOUTS cannot be scripted - GitHub does not expose ProjectV2 view
# mutations in its public API. See docs/BOARD_SETUP.md for those steps.
#
# Usage
#   PROJECT_NUMBER=2 DRY_RUN=1 ./scripts/configure_board.sh
#   PROJECT_NUMBER=2 ./scripts/configure_board.sh
#
set -euo pipefail

OWNER="${OWNER:-brickstercodes}"
PROJECT_NUMBER="${PROJECT_NUMBER:-2}"
DRY_RUN="${DRY_RUN:-0}"

# Field names. Changing these is safe; the script creates whatever is missing.
F_TRACK="Track"
F_PHASE="Phase"
F_BLOCK="Block"
F_START="Start date"
F_END="End date"
F_PRIORITY="Priority"
F_STATUS="Status"

TRACK_OPTS="T1 · Core & Paper,T2 · Orchestration,T3 · Evaluation,T4 · Corpus & Production,⚑ Gates & Decisions"
PHASE_OPTS="A · Pipeline & Manuscript A,B · Hardening & Manuscript B"
BLOCK_OPTS="W0,W1,W2,W3,W4,W5,W6,W7,W8,W9"
PRIORITY_OPTS="P0 · Now,P1 · Next,P2 · Later"

PROJECT_ID=""
declare -A FIELD_ID
declare -A OPT_ID     # key: "<field name>|<option name>"

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

preflight() {
  [[ "${BASH_VERSINFO[0]}" -lt 4 ]] && {
    echo "FATAL: bash 4+ required for associative arrays. You have bash ${BASH_VERSION}." >&2
    echo "       If running via direnv, confirm which bash is being used:" >&2
    echo "       direnv exec ~/ which bash && bash --version" >&2
    exit 1
  }

  command -v gh >/dev/null || { echo "FATAL: gh not found." >&2; exit 1; }
  command -v jq >/dev/null || { echo "FATAL: jq not found. brew install jq" >&2; exit 1; }

  local login
  login="$(gh api user --jq .login 2>/dev/null || true)"
  [[ "$login" == "$OWNER" ]] || {
    echo "FATAL: authenticated as '${login:-<none>}', expected '$OWNER'." >&2
    echo "       Run from ~/Desktop/Capstone so direnv loads .envrc." >&2
    exit 1
  }

  PROJECT_ID="$(gh project view "$PROJECT_NUMBER" --owner "$OWNER" --format json --jq .id 2>/dev/null || true)"
  [[ -n "$PROJECT_ID" ]] || {
    echo "FATAL: cannot read project #$PROJECT_NUMBER for $OWNER." >&2
    echo "       Missing scope? gh auth refresh -s project,repo" >&2
    exit 1
  }
  echo "Project #$PROJECT_NUMBER ($PROJECT_ID) as $login"
}

# ---------------------------------------------------------------------------
# Fields
# ---------------------------------------------------------------------------

load_fields() {
  local json
  json="$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json --limit 100)"

  local name id
  while IFS=$'\t' read -r name id; do
    FIELD_ID["$name"]="$id"
  done < <(jq -r '.fields[] | [.name, .id] | @tsv' <<<"$json")

  local fname oname oid
  while IFS=$'\t' read -r fname oname oid; do
    OPT_ID["$fname|$oname"]="$oid"
  done < <(jq -r '.fields[] | select(.options != null) | .name as $f | .options[] | [$f, .name, .id] | @tsv' <<<"$json")
}

# ensure_single_select <field-name> <comma-separated-options>
ensure_single_select() {
  local name="$1" opts="$2"
  if [[ -n "${FIELD_ID[$name]:-}" ]]; then
    echo "  field exists: $name"
    return
  fi
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "  [dry-run] create single-select field: $name [$opts]"
    return
  fi
  gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
    --name "$name" --data-type SINGLE_SELECT --single-select-options "$opts" >/dev/null
  echo "  created field: $name"
}

ensure_date_field() {
  local name="$1"
  if [[ -n "${FIELD_ID[$name]:-}" ]]; then
    echo "  field exists: $name"
    return
  fi
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "  [dry-run] create date field: $name"
    return
  fi
  gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" \
    --name "$name" --data-type DATE >/dev/null
  echo "  created field: $name"
}

seed_fields() {
  echo "== Fields =="
  ensure_single_select "$F_TRACK"    "$TRACK_OPTS"
  ensure_single_select "$F_PHASE"    "$PHASE_OPTS"
  ensure_single_select "$F_BLOCK"    "$BLOCK_OPTS"
  ensure_single_select "$F_PRIORITY" "$PRIORITY_OPTS"
  ensure_date_field    "$F_START"
  ensure_date_field    "$F_END"
  [[ "$DRY_RUN" == "1" ]] || load_fields   # pick up newly created ids
}

# ---------------------------------------------------------------------------
# Derivation from issue title
#
# Titles are deterministic - seed_github_issues.sh writes them in exactly these
# shapes, so parsing them is more reliable than round-tripping labels through
# the Projects API (which does not expose labels as a groupable field anyway).
# ---------------------------------------------------------------------------

# Block dates track Timeline_and_Workload.md V2 section 2. W4 deliberately
# overlaps W5 - that overlap is how the extended W0 was funded.
block_dates() {
  case "$1" in
    W0) echo "2026-07-29 2026-08-09" ;;
    W1) echo "2026-08-10 2026-08-16" ;;
    W2) echo "2026-08-17 2026-08-23" ;;
    W3) echo "2026-08-24 2026-08-27" ;;
    W4) echo "2026-08-28 2026-09-03" ;;
    W5) echo "2026-08-31 2026-09-06" ;;
    W6) echo "2026-09-07 2026-09-13" ;;
    W7) echo "2026-09-14 2026-09-20" ;;
    W8) echo "2026-09-21 2026-09-27" ;;
    W9) echo "2026-09-28 2026-09-30" ;;
    *)  echo "" ;;
  esac
}

# Priority is "how soon", not "how important" - everything here is important.
# P0 is the current and next block, so the board answers "what now?" at a glance.
priority_for_block() {
  case "$1" in
    W0|W1)       echo "P0 · Now" ;;
    W2|W3|W4)    echo "P1 · Next" ;;
    *)           echo "P2 · Later" ;;
  esac
}

phase_for_block() {
  case "$1" in
    W0|W1|W2|W3|W4) echo "A · Pipeline & Manuscript A" ;;
    *)              echo "B · Hardening & Manuscript B" ;;
  esac
}

# Status: only the current block is Ready. Everything else stays in Backlog so
# the Ready column means something.
status_for_block() {
  case "$1" in
    W0) echo "Ready" ;;
    *)  echo "Backlog" ;;
  esac
}

# derive <title> -> "<track>\t<first-block>\t<last-block>"
#
# Spans ("T2 · W7–W9 · ...") get a first and last block so the Roadmap bar
# covers the whole span while the Block field still groups it under its start.
derive() {
  local t="$1" track="" first="" last=""

  case "$t" in
    "T1 · "*) track="T1 · Core & Paper" ;;
    "T2 · "*) track="T2 · Orchestration" ;;
    "T3 · "*) track="T3 · Evaluation" ;;
    "T4 · "*) track="T4 · Corpus & Production" ;;
    *)        track="⚑ Gates & Decisions" ;;
  esac

  if [[ "$t" == T[1-4]\ ·\ W* ]]; then
    # second " · "-delimited segment is "W6" or "W8–W9"
    local seg
    seg="$(awk -F ' · ' '{print $2}' <<<"$t")"
    first="$(grep -oE 'W[0-9]+' <<<"$seg" | head -1 || true)"
    last="$(grep -oE 'W[0-9]+' <<<"$seg" | tail -1 || true)"
  else
    case "$t" in
      *"Feature freeze A"*) first="W2" ;;
      *"Results freeze A"*) first="W3" ;;
      *"Manuscript A"*)     first="W4" ;;
      *"Feature freeze B"*) first="W6" ;;
      *"Results freeze B"*) first="W7" ;;
      *"Manuscript B"*)     first="W9" ;;
      "DECISION · "*)       first="W0" ;;
      *)                    first="" ;;
    esac
    last="$first"
  fi

  printf '%s\t%s\t%s\n' "$track" "$first" "$last"
}

# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------

set_select() {
  local item="$1" field="$2" option="$3"
  # WHY: under DRY_RUN, seed_fields() never creates the fields, so FIELD_ID/
  # OPT_ID are legitimately empty here - that is the dry run working, not a
  # fault. Only warn about a missing id on a REAL run, where it means the
  # field or option genuinely failed to create.
  if [[ "$DRY_RUN" == "1" ]]; then
    return
  fi
  local fid="${FIELD_ID[$field]:-}" oid="${OPT_ID[$field|$option]:-}"
  [[ -n "$fid" && -n "$oid" ]] || { echo "      ! no field/option id for $field=$option"; return; }
  gh project item-edit --id "$item" --project-id "$PROJECT_ID" \
    --field-id "$fid" --single-select-option-id "$oid" >/dev/null
}

set_date() {
  local item="$1" field="$2" value="$3"
  if [[ "$DRY_RUN" == "1" ]]; then
    return
  fi
  local fid="${FIELD_ID[$field]:-}"
  [[ -n "$fid" ]] || { echo "      ! no field id for $field"; return; }
  gh project item-edit --id "$item" --project-id "$PROJECT_ID" \
    --field-id "$fid" --date "$value" >/dev/null
}

apply_items() {
  echo "== Items =="
  local json
  json="$(gh project item-list "$PROJECT_NUMBER" --owner "$OWNER" --format json --limit 200)"

  local n=0 skipped=0
  local id title track first last start end _ignore
  while IFS=$'\t' read -r id title; do
    IFS=$'\t' read -r track first last < <(derive "$title")

    if [[ -z "$first" ]]; then
      echo "  skip (not a plan item): $title"
      skipped=$((skipped+1))
      continue
    fi

    read -r start _ignore  < <(block_dates "$first")
    read -r _ignore end    < <(block_dates "$last")

    set_select "$id" "$F_TRACK"    "$track"
    set_select "$id" "$F_PHASE"    "$(phase_for_block "$first")"
    set_select "$id" "$F_BLOCK"    "$first"
    set_select "$id" "$F_PRIORITY" "$(priority_for_block "$first")"
    set_select "$id" "$F_STATUS"   "$(status_for_block "$first")"
    set_date   "$id" "$F_START"    "$start"
    set_date   "$id" "$F_END"      "$end"

    printf '  %-4s %-6s %-26s %-11s %s\n' \
      "$first" "$start" "$track" "$(priority_for_block "$first")" "${title:0:46}"
    n=$((n+1))
  done < <(jq -r '.items[] | select(.content.title != null) | [.id, .content.title] | @tsv' <<<"$json")

  echo
  echo "Configured: $n   Skipped: $skipped"
}

main() {
  [[ "$DRY_RUN" == "1" ]] && echo "*** DRY RUN - no writes ***"
  preflight
  load_fields
  seed_fields
  load_fields
  apply_items
  echo
  echo "Field values are set. View LAYOUTS cannot be scripted - GitHub does not"
  echo "expose ProjectV2 view mutations. Follow docs/BOARD_SETUP.md (5 minutes)."
}

main "$@"
