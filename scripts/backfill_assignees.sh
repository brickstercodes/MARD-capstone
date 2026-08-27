#!/usr/bin/env bash
#
# Backfill issue assignees from track labels.
#
# This exists because GitHub's REST API silently drops assignees who lack push
# access to the repo: the issue is created successfully, the assignee is simply
# ignored, and nothing in the response says so. Teammates invited as
# collaborators are NOT assignable until they accept the invitation.
#
# So the seeding run creates correct issues with empty assignees, and this
# script fills them in afterwards, deriving the owner from the track:* label
# rather than re-deriving it from the plan.
#
# Order of operations
#   1. ./scripts/backfill_assignees.sh --check      (who is assignable today?)
#   2. Invite anyone missing, and have them ACCEPT the emailed invitation
#   3. ./scripts/backfill_assignees.sh              (assign everything)
#
set -euo pipefail

OWNER="${OWNER:-brickstercodes}"
REPO="${REPO:-MARD-capstone}"
REPO_SLUG="$OWNER/$REPO"

T1_USER="${T1_USER:-brickstercodes}"
T2_USER="${T2_USER:-parthparu}"
T3_USER="${T3_USER:-FalseAdvertising}"
T4_USER="${T4_USER:-Tanz101-tech}"

# Issues with no track:* label (gates, deliveries, decisions) fall to T1.
DEFAULT_USER="$T1_USER"

DRY_RUN="${DRY_RUN:-0}"

user_for_track() {
  case "$1" in
    track:1-core-paper)        echo "$T1_USER" ;;
    track:2-orchestration)     echo "$T2_USER" ;;
    track:3-evaluation)        echo "$T3_USER" ;;
    track:4-corpus-production) echo "$T4_USER" ;;
    *)                         echo "$DEFAULT_USER" ;;
  esac
}

# WHY a dedicated check mode: the failure this script fixes is invisible, so the
# diagnosis has to be explicit rather than inferred from a silent no-op.
check_assignable() {
  echo "Repo: $REPO_SLUG"
  echo
  echo "== Collaborators (accepted) =="
  gh api "repos/$REPO_SLUG/collaborators" --jq '.[] | "  \(.login)  [\(.permissions.push | if . then "push" else "NO PUSH" end)]"' 2>/dev/null \
    || echo "  (could not read - need admin access)"
  echo
  echo "== Pending invitations (NOT yet assignable) =="
  local pending
  pending="$(gh api "repos/$REPO_SLUG/invitations" --jq '.[] | "  \(.invitee.login)  invited \(.created_at)"' 2>/dev/null || true)"
  [[ -n "$pending" ]] && echo "$pending" || echo "  (none)"
  echo
  echo "== Assignable users (this is the list that actually matters) =="
  local assignable
  assignable="$(gh api "repos/$REPO_SLUG/assignees" --jq '.[].login' 2>/dev/null || true)"
  echo "$assignable" | sed 's/^/  /'
  echo
  echo "== Verdict per track =="
  local t u
  for t in "T1:$T1_USER" "T2:$T2_USER" "T3:$T3_USER" "T4:$T4_USER"; do
    u="${t#*:}"
    if [[ -z "$u" ]]; then
      printf "  %-3s %-22s NOT SET\n" "${t%%:*}" "-"
    elif grep -Fxq "$u" <<<"$assignable"; then
      printf "  %-3s %-22s OK - assignable\n" "${t%%:*}" "$u"
    elif gh api "users/$u" --jq .login >/dev/null 2>&1; then
      printf "  %-3s %-22s BLOCKED - user exists but has no push access (invite, and have them accept)\n" "${t%%:*}" "$u"
    else
      printf "  %-3s %-22s BAD USERNAME - no such GitHub user\n" "${t%%:*}" "$u"
    fi
  done
  echo
  echo "To invite:  gh api -X PUT repos/$REPO_SLUG/collaborators/<user> -f permission=push"
  echo "They must ACCEPT the emailed invitation before assignment will stick."
}

backfill() {
  local assignable
  assignable="$(gh api "repos/$REPO_SLUG/assignees" --jq '.[].login')"

  local assigned=0 skipped=0 blocked=0

  while IFS=$'\t' read -r num track current; do
    local want
    want="$(user_for_track "$track")"

    [[ -z "$want" ]] && { skipped=$((skipped+1)); continue; }

    if [[ "$current" == *"$want"* ]]; then
      skipped=$((skipped+1))
      continue
    fi

    if ! grep -Fxq "$want" <<<"$assignable"; then
      echo "  #$num  BLOCKED - '$want' is not assignable on this repo"
      blocked=$((blocked+1))
      continue
    fi

    if [[ "$DRY_RUN" == "1" ]]; then
      echo "  [dry-run] #$num -> $want  ($track)"
    else
      gh issue edit "$num" -R "$REPO_SLUG" --add-assignee "$want" >/dev/null
      echo "  #$num -> $want  ($track)"
    fi
    assigned=$((assigned+1))
  done < <(
    gh issue list -R "$REPO_SLUG" --state open --limit 300 \
      --json number,labels,assignees \
      --jq '.[] | [
              (.number|tostring),
              ([.labels[].name] | map(select(startswith("track:"))) | first // "none"),
              ([.assignees[].login] | join(","))
            ] | @tsv'
  )

  echo
  echo "Assigned: $assigned   Already correct/skipped: $skipped   Blocked: $blocked"
  [[ "$blocked" -gt 0 ]] && echo "Run with --check to see why the blocked ones failed."
}

case "${1:-}" in
  --check|-c) check_assignable ;;
  *)          backfill ;;
esac
