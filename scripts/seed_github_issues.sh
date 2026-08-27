#!/usr/bin/env bash
#
# Seed the MARD capstone backlog into GitHub Issues + Projects.
#
# This script exists because the sprint plan lives in a markdown document
# (Timeline_and_Workload.md V2, 1 Aug 2026) that nobody looks at during a
# standup. Every issue below traces to a specific section of that document,
# cited in the issue body, so the board and the plan cannot silently diverge.
#
# It is idempotent: existing labels, milestones and issue titles are skipped,
# so re-running after editing the plan only adds what is new.
#
# Prerequisites
#   - Run from inside /Users/giant02/Desktop/Capstone so direnv loads .envrc
#     and gh authenticates as @brickstercodes.
#   - gh needs the 'project' scope for the Projects board step:
#       gh auth refresh -s project,repo
#
# Usage
#   DRY_RUN=1 ./scripts/seed_github_issues.sh     # print, create nothing
#   PROJECT_NUMBER=1 ./scripts/seed_github_issues.sh
#
set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OWNER="${OWNER:-brickstercodes}"
REPO="${REPO:-MARD-capstone}"

# Projects (v2) board number, from the board URL:
#   https://github.com/users/brickstercodes/projects/<N>
# Leave empty to create issues without adding them to a board.
PROJECT_NUMBER="${PROJECT_NUMBER:-}"

# GitHub usernames per track. Blank means the issue is created unassigned.
T1_USER="${T1_USER:-brickstercodes}"   # Anugrah Shetty  - MARD Core & Paper Lead
T2_USER="${T2_USER:-}"                 # Parth Sangani   - Orchestration & Tier 2
T3_USER="${T3_USER:-}"                 # Arav Sharma     - Evaluation & Measurement
T4_USER="${T4_USER:-}"                 # Tanish Sharma   - Corpus & Manuscript Production

DRY_RUN="${DRY_RUN:-0}"

REPO_SLUG="$OWNER/$REPO"
PLAN_DOC="Timeline_and_Workload.md V2 (1 Aug 2026)"

created_count=0
skipped_count=0

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

preflight() {
  command -v gh >/dev/null 2>&1 || {
    echo "FATAL: gh not found. Install GitHub CLI first." >&2
    exit 1
  }

  # WHY: a wrong-identity run creates 45 issues under the personal work account
  # and there is no bulk delete in the GitHub UI. Fail before writing anything.
  local login
  login="$(gh api user --jq .login 2>/dev/null || true)"
  if [[ -z "$login" ]]; then
    echo "FATAL: gh is not authenticated. Run this from ~/Desktop/Capstone so direnv loads .envrc." >&2
    exit 1
  fi
  echo "Authenticated as: $login  (GH_CONFIG_DIR=${GH_CONFIG_DIR:-<default>})"
  if [[ "$login" != "$OWNER" ]]; then
    echo "FATAL: expected to be authenticated as '$OWNER' but got '$login'." >&2
    echo "       cd into ~/Desktop/Capstone and confirm 'direnv: loading .envrc' appeared." >&2
    exit 1
  fi

  gh repo view "$REPO_SLUG" >/dev/null 2>&1 || {
    echo "FATAL: cannot see repo $REPO_SLUG." >&2
    exit 1
  }

  # WHY: GitHub's REST API silently DROPS assignees who lack push access - the
  # issue is created, the assignee is ignored, and the response says nothing.
  # Without this warning the run looks like a complete success and the board
  # comes out unassigned. /assignees is the authoritative list.
  local assignable t u
  assignable="$(gh api "repos/$REPO_SLUG/assignees" --jq '.[].login' 2>/dev/null || true)"
  for t in "T1:$T1_USER" "T2:$T2_USER" "T3:$T3_USER" "T4:$T4_USER"; do
    u="${t#*:}"
    [[ -z "$u" ]] && { echo "NOTE: ${t%%:*} has no username set - its issues will be unassigned."; continue; }
    if ! grep -Fxq "$u" <<<"$assignable"; then
      echo "WARN: '$u' (${t%%:*}) is NOT assignable on $REPO_SLUG - assignment will be silently ignored."
      echo "      Fix: gh api -X PUT repos/$REPO_SLUG/collaborators/$u -f permission=push"
      echo "      They must ACCEPT the invitation, then run ./scripts/backfill_assignees.sh"
    fi
  done

  if [[ -n "$PROJECT_NUMBER" ]]; then
    if ! gh project view "$PROJECT_NUMBER" --owner "$OWNER" >/dev/null 2>&1; then
      echo "FATAL: cannot read project #$PROJECT_NUMBER for owner $OWNER." >&2
      echo "       Missing scope? Run: gh auth refresh -s project,repo" >&2
      exit 1
    fi
  else
    echo "NOTE: PROJECT_NUMBER unset - issues will be created but not added to a board."
  fi
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXISTING_TITLES_FILE=""

load_existing_titles() {
  EXISTING_TITLES_FILE="$(mktemp)"
  gh issue list -R "$REPO_SLUG" --state all --limit 500 --json title --jq '.[].title' \
    > "$EXISTING_TITLES_FILE" 2>/dev/null || true
  trap 'rm -f "$EXISTING_TITLES_FILE"' EXIT
}

ensure_label() {
  local name="$1" color="$2" desc="$3"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] label: $name ($color)"
    return
  fi
  gh label create "$name" -R "$REPO_SLUG" --color "$color" --description "$desc" 2>/dev/null \
    || gh label edit "$name" -R "$REPO_SLUG" --color "$color" --description "$desc" >/dev/null
}

ensure_milestone() {
  local title="$1" due="$2" desc="$3"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] milestone: $title (due $due)"
    return
  fi
  local existing
  existing="$(gh api "repos/$REPO_SLUG/milestones?state=all&per_page=100" \
    --jq ".[] | select(.title == \"$title\") | .number" 2>/dev/null || true)"
  if [[ -n "$existing" ]]; then
    return
  fi
  gh api "repos/$REPO_SLUG/milestones" -X POST \
    -f title="$title" \
    -f description="$desc" \
    -f due_on="${due}T23:59:59Z" >/dev/null
}

# mk_issue <title> <milestone> <labels-csv> <assignee-or-empty>   ... body on stdin
mk_issue() {
  local title="$1" milestone="$2" labels="$3" assignee="${4:-}"
  local body
  body="$(cat)"

  if grep -Fxq "$title" "$EXISTING_TITLES_FILE" 2>/dev/null; then
    echo "  skip (exists): $title"
    skipped_count=$((skipped_count + 1))
    return
  fi

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] issue: $title"
    echo "            milestone=$milestone labels=$labels assignee=${assignee:-<none>}"
    created_count=$((created_count + 1))
    return
  fi

  local args=(issue create -R "$REPO_SLUG"
              --title "$title"
              --body "$body"
              --milestone "$milestone"
              --label "$labels")
  [[ -n "$assignee" ]] && args+=(--assignee "$assignee")

  local url
  url="$(gh "${args[@]}")"
  echo "  created: $url  $title"
  created_count=$((created_count + 1))

  if [[ -n "$PROJECT_NUMBER" ]]; then
    gh project item-add "$PROJECT_NUMBER" --owner "$OWNER" --url "$url" >/dev/null
  fi
}

# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

seed_labels() {
  echo "== Labels =="
  ensure_label "track:1-core-paper"        "B60205" "Track 1 - MARD Core & Paper Lead (Anugrah)"
  ensure_label "track:2-orchestration"     "D93F0B" "Track 2 - Orchestration & Tier 2 Execution (Parth)"
  ensure_label "track:3-evaluation"        "FBCA04" "Track 3 - Evaluation Harness & Measurement (Arav)"
  ensure_label "track:4-corpus-production" "0E8A16" "Track 4 - Corpus, Ground Truth & Manuscript Production (Tanish)"
  ensure_label "phase:A"                   "1D76DB" "Phase A - pipeline exists, first result measured (W0-W4)"
  ensure_label "phase:B"                   "5319E7" "Phase B - harden, scale, full paper (W5-W9)"
  ensure_label "gate"                      "000000" "Hard freeze or delivery gate - date does not move"
  ensure_label "deliverable"               "0052CC" "Manuscript or artefact delivery"
  ensure_label "decision"                  "C2E0C6" "Decision Anugrah owns, on a date"
  ensure_label "blocker"                   "E11D21" "Blocks another track - slipping this slips someone else"
  ensure_label "writing"                   "BFD4F2" "Manuscript prose, not code"
}

# ---------------------------------------------------------------------------
# Milestones - dates from Timeline_and_Workload.md V2 section 2 (Calendar)
#
# V2 absorbs a 7-day W0 overrun without moving any Phase B date. The recovery
# comes from compressing W3 (7 days -> 4) and overlapping W4 with W5, NOT from
# spending the ~3 days of W8-W9 slack, which is held in reserve as contingency.
# ---------------------------------------------------------------------------

seed_milestones() {
  echo "== Milestones =="
  ensure_milestone "W0" "2026-08-09" "Wed 29 Jul - Sun 9 Aug (EXTENDED to 12 days in V2). Gate: scope frozen, repo + API keys live, eval protocol written, corpus licensing confirmed, deadline table to faculty."
  ensure_milestone "W1" "2026-08-16" "Mon 10 - Sun 16 Aug. Gate: ingestion + Pass 0 skeleton on 1 doc, Master Plan schema validating, vanilla RLM control running, paper 1-3 drafted."
  ensure_milestone "W2" "2026-08-23" "Mon 17 - Sun 23 Aug. Gate: end-to-end doc to joined output. FEATURE FREEZE A on Sun 23 Aug."
  ensure_milestone "W3" "2026-08-27" "Mon 24 - Thu 27 Aug (COMPRESSED 7 days -> 4 in V2; no recovery room). Gate: Manuscript A measurement matrix complete. RESULTS FREEZE A on Thu 27 Aug."
  ensure_milestone "W4" "2026-09-03" "Fri 28 Aug - Thu 3 Sep (OVERLAPS W5 in V2). Guide review Mon 31 Aug - Tue 1 Sep, revisions Wed 2 Sep. Gate: Manuscript A submission-ready, delivered Thu 3 Sep."
  ensure_milestone "W5" "2026-09-06" "Mon 31 Aug - Sun 6 Sep (UNCHANGED - T2/T3/T4 start this under W4's guide-review window). Gate: feature thaw, corpus to 4 docs, 3 remaining baselines, seed/variance harness."
  ensure_milestone "W6" "2026-09-13" "Mon 7 - Sun 13 Sep (UNCHANGED). Gate: full matrix 4 docs x 5 systems x 3 seeds + ablation grid. FEATURE FREEZE B on Sun 13 Sep."
  ensure_milestone "W7" "2026-09-20" "Mon 14 - Sun 20 Sep (UNCHANGED). Gate: remaining runs + O5 scoring on 2 docs. RESULTS FREEZE B on Sun 20 Sep."
  ensure_milestone "W8" "2026-09-27" "Mon 21 - Sun 27 Sep (UNCHANGED; holds ~3 days of reserve slack). Gate: full manuscript assembled, all figures, limitations, appendices, guide review by Wed 23 Sep."
  ensure_milestone "W9" "2026-09-30" "Mon 28 - Wed 30 Sep (UNCHANGED). Gate: Manuscript B ready Wed 30 Sep."
}

# ---------------------------------------------------------------------------
# Track 1 - MARD Core & Paper Lead (Anugrah Shetty)
# ---------------------------------------------------------------------------

seed_track1() {
  echo "== Track 1 - MARD Core & Paper Lead =="

  mk_issue "T1 · W0 · Freeze the claim, ablation set and measurement protocol; decide the model pair" \
    "W0" "track:1-core-paper,phase:A,blocker" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W0 · Wed 29 Jul – Sun 9 Aug 2026

### Work
- Freeze the claim MARD is making, in one sentence, in writing.
- Freeze the ablation set: envelope removed · plan withheld from Tier 2 · reordering disabled · depth swept.
- Freeze the measurement protocol that Track 3 builds against.
- Decide the model pair: one frontier + one budget model, selected on published benchmarks.

### Why this blocks others
Track 3 cannot fix its subsets or write its scorers against a protocol that is still moving. This is the W0 → T3 edge in the dependency map.

### Definition of done
- [ ] Claim sentence written into the repo (not just discussed)
- [ ] Ablation set enumerated and frozen
- [ ] Measurement protocol document exists and Track 3 has read it
- [ ] Model pair named, with the published benchmark used to pick them cited

### Note on scope
Deck slide 13 currently frames model selection as a 3×3 Pareto sweep — a *result*, not an assumption. The plan recommends softening this to "we select from published benchmarks and report the cost frontier for our chosen pair," with an optional reduced 2×2 sweep in W5 if there is slack. Overclaiming a sweep we did not run is the kind of thing reviewers catch.

_Source: §1 Scope decision · §2 Calendar W0 · §3 Track 1 · §4 Dependency map · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W1 · Pass 0 skeleton extraction + envelope data structure; draft §1–§3" \
    "W1" "track:1-core-paper,phase:A,writing,blocker" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W1 · Mon 10 – Sun 16 Aug 2026

### Work
- Pass 0 skeleton extraction: headings / TOC / index → structural map.
- Envelope data structure + growth semantics.
- Draft §1 Introduction, §2 Related Work, §3 Method.

### Blocked by
- T4 · W1 · parsed primary document. Pass 0 has nothing to run on until that lands.

### Blocks
- T2 · W2 fork-join and the first end-to-end output — everything downstream is shaped by the envelope's output shape.

### ⚠️ Decision you own, on a date — Sun 16 Aug
If Pass 0 is **not** producing a usable skeleton by **Sun 16 Aug**, cut Pass 2 and ship two-pass MARD in Manuscript A, restoring Pass 2 in W5 for Manuscript B.

Make that call on **16 Aug**, not 24 Aug. Slipping the decision is worse than making it early.

### Definition of done
- [ ] Pass 0 produces a structural map on the primary document
- [ ] Envelope data structure implemented with growth semantics
- [ ] §1, §2, §3 exist in draft (results-independent — no excuse to defer)
- [ ] Pass 2 go/no-go decision recorded on 16 Aug

_Source: §3 Track 1 W1 · §4 Dependency map W1 · §2 Hard rules (writing runs continuously from W1) · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W2 · Pass 1 + Pass 2 exploration; envelope → Master Plan compilation" \
    "W2" "track:1-core-paper,phase:A,blocker" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W2 · Mon 17 – Sun 23 Aug 2026

### Work
- Pass 1 enriched exploration: concepts, prerequisites, forward dependencies.
- Pass 2 targeted deep dive (unless cut by the 16 Aug decision).
- Tier 1 scout prompt engineering.
- Envelope → Master Plan compilation.

### Blocks
- T2 · W2 fork-join. The first end-to-end run needs a real Master Plan out of this.

### 🔒 Freeze
**Feature freeze A · Sun 23 Aug.** Anything not landed by end of this block is not in Manuscript A. A change to the pipeline after this date invalidates every number measured before it.

### Definition of done
- [ ] Pass 1 extracts concepts / prerequisites / forward deps on the primary doc
- [ ] Pass 2 landed or formally cut per the 16 Aug decision
- [ ] Envelope compiles to a Master Plan that validates against T2's schema
- [ ] End-to-end run completes: doc → envelope → plan → N builders → joined output

_Source: §3 Track 1 W2 · §2 Calendar W2 · §4 Dependency map W2 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W3 · Interpret Manuscript A results as they land; write §5" \
    "W3" "track:1-core-paper,phase:A,writing" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W3 · Mon 24 – Thu 27 Aug 2026

### Work
- Interpret results as they land from Track 3.
- Write §5 Results for Manuscript A.
- Diagnose anything contradicting the claim **before** it reaches the paper.

### The rule that matters here
If the effect is null or negative (risk #1, trigger date 24 Aug): publish it as a negative result framed by the O4 boundary. That is *why* O4 is an objective. A clean, well-measured null against a stated precondition is a publishable finding.

**Do not tune toward a positive after the fact.**

### 🔒 Freeze
**Results freeze A · Thu 27 Aug.** After this, numbers are written up, never re-run. A wrong result gets a limitation paragraph, not a re-run.

### Definition of done
- [ ] Every number from T3's matrix interpreted, not just reported
- [ ] §5 drafted against real numbers
- [ ] Any claim-contradicting result diagnosed and its treatment decided before 27 Aug

_Source: §3 Track 1 W3 · §2 Calendar W3 + Hard rules · §5 Risks #1 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W4 · Assemble Manuscript A; §6 Discussion incl. the O4 boundary" \
    "W4" "track:1-core-paper,phase:A,writing,deliverable" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W4 · Fri 28 Aug – Thu 3 Sep 2026

### Work
- Assemble Manuscript A (4–8 pages).
- Write §6 Discussion including the O4 degeneration boundary.
- Guide review Mon 31 Aug – Tue 1 Sep · revisions Wed 2 Sep · final Thu 3 Sep.

### ⚠️ V2 overlap — you are double-booked
W4 now runs **on top of W5**. Tracks 2–4 begin Phase B on Mon 31 Aug while you are in guide review. From Wed 2 Sep you are doing A's revisions *and* W5 envelope hardening at the same time.

This is where the compression's cost lands, and it lands on the track the plan says has no slack. If something has to give this week, it is W5 envelope hardening — not Manuscript A, and not the 3 Sep date.

### Claim being made
MARD beats vanilla RLM on a structured benchmark; degenerates gracefully on flat context.
Evidence: 1 primary doc · vanilla RLM control · 1 ablation.

### Definition of done
- [ ] Manuscript A assembled and internally consistent
- [ ] O4 boundary stated as a *prediction* in the framing, not discovered as an excuse
- [ ] Guide review completed and responses incorporated
- [ ] **Delivered Thu 3 Sep**

### Open item to raise before submission
If Manuscript A goes to an archival venue, that can restrict where B can go afterwards (prior-publication rules at most main conferences; journals are usually more permissive about extended versions). Raise this with faculty *before* A is submitted, not after.

_Source: §0 Shape of the plan · §3 Track 1 W4 · §5 Risks #2 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W5 · Envelope hardening across documents 2–4; prompt robustness" \
    "W5" "track:1-core-paper,phase:B" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W5 · Mon 31 Aug – Sun 6 Sep 2026

> **V2 note:** this block starts *during* W4. Manuscript A is still in guide review Mon 31 Aug – Tue 1 Sep and delivers Thu 3 Sep. Phase B work starts anyway — that overlap is how the extended W0 was paid for.

### Work
- Envelope hardening: fix whatever broke on documents 2–4.
- Prompt robustness across domains (OpenStax / OSTEP / Axler are not the same kind of document).
- Restore Pass 2 if it was cut on 16 Aug.

### Blocked by
- T4 · W5 · documents 2–4 parsed and cleaned, with the structural-marker quality report. You need to know which documents are structurally weak — that is the O4 story.

### Definition of done
- [ ] Envelope runs clean on all 4 documents
- [ ] Prompt failures per document catalogued, not just patched
- [ ] Pass 2 restored if previously cut
- [ ] Structurally-weak documents identified and their O4 relevance written down

_Source: §3 Track 1 W5 · §4 Dependency map W5 · §5 Risks #3 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W6 · Support the full measurement matrix; extend §3 for Manuscript B" \
    "W6" "track:1-core-paper,phase:B,writing" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W6 · Mon 7 – Sun 13 Sep 2026

### Work
- Support the measurement matrix — you are the one who knows why a run looks wrong.
- Begin extending §3 Method for Manuscript B.

### 🔒 Freeze
**Feature freeze B · Sun 13 Sep.** Absolute. Cut features, never the freeze.

### Definition of done
- [ ] Every anomalous run in the 4×5×3 matrix triaged with a stated cause
- [ ] §3 extended to cover the hardened method
- [ ] No pipeline changes after 13 Sep

_Source: §3 Track 1 W6 · §2 Calendar W6 + Hard rules · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W7 · Write §4 Setup, §5 Results, §6 Discussion for Manuscript B" \
    "W7" "track:1-core-paper,phase:B,writing" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W7 · Mon 14 – Sun 20 Sep 2026

### Work
Write §4 Experimental Setup, §5 Results, §6 Discussion **against real numbers**.

### 🔒 Freeze
**Results freeze B · Sun 20 Sep.** After this, numbers are written up, never re-run.

### What §5 must contain
- 4 docs × 5 systems × 3 seeds, **variance reported on every number** — this is the paper's spine
- Full ablation grid: envelope removed · plan withheld from Tier 2 · reordering disabled · depth swept
- O5 dependency ordering scored on 2 documents against document-native ground truth
- O6 cost model with measured token counts and same-day published rates

### Reviewer threat this section answers
Reference [3] — SRLM, arXiv:2603.15653 — argues in print that RLM's gains are not primarily driven by recursion. A reviewer who knows that paper attacks MARD on exactly one axis: *your improvement is noise, or prompt luck, not the envelope.* What defends against it is variance across seeds, a negative control, and the O4 boundary stated up front as a prediction.

### Definition of done
- [ ] §4, §5, §6 drafted against frozen numbers
- [ ] Variance reported everywhere, no bare point estimates
- [ ] SRLM's objection explicitly addressed in the text

_Source: §1 Scope decision (in for B) · §3 Track 1 W7 · §2 Hard rules · Timeline_and_Workload.md V2_
EOF

  mk_issue "T1 · W8–W9 · Full assembly, limitations, guide-review response, final polish" \
    "W9" "track:1-core-paper,phase:B,writing,deliverable" "$T1_USER" <<'EOF'
**Track 1 — MARD Core & Paper Lead · Anugrah Shetty**
**Block:** W8–W9 · Mon 21 – Wed 30 Sep 2026

### Work
- Full manuscript assembly (8–12 pages + appendices).
- Limitations section.
- Respond to guide review (assumed Wed 23 Sep).
- Final polish.

### Must appear in limitations
Everything cut from scope, stated as a limitation rather than omitted:
- Expert Likert evaluation and student A/B test — out, ethics approval and scheduling do not fit nine weeks
- Kendall's τ curriculum alignment against OCW syllabi — cut deliberately; external syllabi are noisy, inconsistently structured, unbounded in collection effort, and weakly interpretable even when favourable
- Multi-document synthesis and non-text modalities — out of scope in the proposal

### Definition of done
- [ ] Manuscript B assembled, 8–12 pages + appendices
- [ ] Limitations written honestly, including the deliberate cuts above
- [ ] Guide review responses incorporated
- [ ] **Delivered Wed 30 Sep**

_Source: §0 Shape of the plan · §1 Out, permanently · §3 Track 1 W8–W9 · §6 Open item 3 · Timeline_and_Workload.md V2_
EOF
}

# ---------------------------------------------------------------------------
# Track 2 - Orchestration & Tier 2 Execution (Parth Sangani)
# ---------------------------------------------------------------------------

seed_track2() {
  echo "== Track 2 - Orchestration & Tier 2 Execution =="

  mk_issue "T2 · W0 · Repo scaffolding, RLM library running, API keys + spend cap, logging harness" \
    "W0" "track:2-orchestration,phase:A,blocker" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W0 · Wed 29 Jul – Sun 9 Aug 2026

### Work
- Repo scaffolding.
- RLM library installed and running its own examples end-to-end.
- API keys, rate-limit budget, spend cap.
- Structured logging + config-snapshot harness.

### Why this blocks others
**Track 3 depends on the logging harness existing in W0.** Every run must be logged — envelope state, transcripts, token counts, config snapshot, seed. A number you cannot reproduce on 29 Sep is not a number.

### Definition of done
- [ ] Repo scaffolded and pushed
- [ ] RLM library runs its own examples successfully
- [ ] API keys provisioned, rate-limit budget documented, spend cap set
- [ ] Logging harness captures: envelope state, transcript, token count, config snapshot, seed
- [ ] Track 3 has confirmed the harness meets their needs

### Blocked by
Compute and API budget ceiling — needs a number from Anugrah in W0 before the spend cap can be set (§6 open item 4).

_Source: §3 Track 2 W0 · §2 Hard rules (every run logged) · §4 Dependency map W0 · §6 Open item 4 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W1 · Master Plan Pydantic schema, loud-failing validation, stub Tier 2 builder" \
    "W1" "track:2-orchestration,phase:A" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W1 · Mon 10 – Sun 16 Aug 2026

### Work
- Master Plan schema in Pydantic.
- Loud-failing validation at the tier boundary — a malformed plan must stop the run, not degrade quietly.
- **Stub Tier 2 builder consuming a hand-written plan.**

### Why the stub matters
It fixes the contract *before* Track 1 can generate a real plan, so you are never blocked waiting on the envelope. This is the deliberate decoupling in the W1 dependency map.

### Definition of done
- [ ] Pydantic schema for Master Plan committed
- [ ] Validation fails loudly and specifically at the tier boundary
- [ ] Stub builder consumes a hand-written plan and produces output
- [ ] Contract documented so Track 1 knows what shape to emit

_Source: §3 Track 2 W1 · §4 Dependency map W1 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W2 · asyncio worker pool, fork-join, retry, failure isolation, provenance pointers" \
    "W2" "track:2-orchestration,phase:A" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W2 · Mon 17 – Sun 23 Aug 2026

### Work
- asyncio bounded worker pool.
- Fork-join across N builders.
- Per-builder retry.
- Failure isolation — one builder dying must not take the run with it.
- Provenance pointers on every generated span.
- Join in Master Plan order.

### Why provenance is not optional
It is what the hallucination-rate measurement is spot-checked against in W7 (Track 4).

### 🔒 Freeze
**Feature freeze A · Sun 23 Aug.** The first end-to-end output — doc → envelope → plan → N builders → joined output — must exist by the end of this block.

### Definition of done
- [ ] Bounded worker pool with configurable concurrency
- [ ] Fork-join produces output joined in Master Plan order
- [ ] Per-builder retry and failure isolation verified by deliberately failing a builder
- [ ] Every generated span carries a provenance pointer
- [ ] End-to-end run completes on the primary document

_Source: §3 Track 2 W2 · §2 Calendar W2 · §4 Dependency map W2 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W3 · Keep runs alive through Manuscript A measurement week" \
    "W3" "track:2-orchestration,phase:A,blocker" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W3 · Mon 24 – Thu 27 Aug 2026

### Work
Keep runs alive through measurement week — rate limits, timeouts, partial failures.

**The plan describes this as effectively full-time.** Do not schedule other work into this block.

### 🔒 Freeze
**Results freeze A · Thu 27 Aug.** If a run has not completed by then it does not appear in Manuscript A.

### Definition of done
- [ ] Every run in T3's Manuscript A matrix completed or explicitly recorded as failed
- [ ] Rate-limit and timeout incidents logged, not silently retried into invisibility
- [ ] No partial-failure output silently entered the results

_Source: §3 Track 2 W3 · §2 Calendar W3 + Hard rules · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W4 · Architecture and pipeline figures for Manuscript A; reproducibility notes" \
    "W4" "track:2-orchestration,phase:A,writing" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W4 · Fri 28 Aug – Thu 3 Sep 2026

### Work
- Architecture figure and pipeline figure for Manuscript A.
- Reproducibility notes.

### Definition of done
- [ ] Architecture figure produced in publication quality
- [ ] Pipeline figure produced in publication quality
- [ ] Reproducibility notes cover: config snapshot format, seed handling, how to re-run a logged run
- [ ] Figures handed to Track 4 in time for the Thu 3 Sep delivery

_Source: §3 Track 2 W4 · §2 Calendar W4 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W5 · Scale orchestrator to 4 docs: concurrency, seed plumbing, resumable runs, cost telemetry" \
    "W5" "track:2-orchestration,phase:B" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W5 · Mon 31 Aug – Sun 6 Sep 2026

> **V2 note:** this block starts *during* W4. Manuscript A is still in guide review Mon 31 Aug – Tue 1 Sep and delivers Thu 3 Sep. Phase B work starts anyway — that overlap is how the extended W0 was paid for.

### Work
- Scale the orchestrator: 4 documents, concurrent runs.
- Seed plumbing — seeds must reach every stochastic component, verifiably.
- Resumable runs — W6 is too expensive to restart from zero.
- Cost telemetry per run.

### Why resumability is load-bearing
W6 executes 4 docs × 5 systems × 3 seeds plus an ablation grid and a depth sweep. A non-resumable failure late in that week costs the block.

### Definition of done
- [ ] Orchestrator handles 4 documents concurrently within the rate-limit budget
- [ ] Seed plumbing verified: same seed reproduces the same run
- [ ] A killed run resumes without re-executing completed work
- [ ] Per-run cost telemetry feeds the O6 cost model

_Source: §3 Track 2 W5 · §1 In for Manuscript B (O6 cost model) · §5 Risks #5 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W6 · Keep the full matrix alive (4 docs × 5 systems × 3 seeds + ablation grid)" \
    "W6" "track:2-orchestration,phase:B,blocker" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W6 · Mon 7 – Sun 13 Sep 2026

### Work
Keep the full matrix alive. The plan's words: *this is the week the orchestrator earns its keep.*

### Risk in play
**#5 · API cost or rate limits throttle W6.** Response already decided: vLLM + open weights for ablation sweeps (already in the stack, deck slide 13); frontier model reserved for final tables. Spend cap was set in W0 and is checked weekly.

### 🔒 Freeze
**Feature freeze B · Sun 13 Sep.**

### Definition of done
- [ ] Full matrix executed or every gap explicitly recorded
- [ ] Cost stayed inside the W0 spend cap, or the overrun was escalated the same day
- [ ] No orchestrator changes after 13 Sep

_Source: §3 Track 2 W6 · §2 Calendar W6 · §5 Risks #5 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T2 · W7–W9 · Deterministic replay verification, code cleanup, public artefact, figures for B" \
    "W9" "track:2-orchestration,phase:B,deliverable" "$T2_USER" <<'EOF'
**Track 2 — Orchestration & Tier 2 Execution · Parth Sangani**
**Block:** W7–W9 · Mon 14 – Wed 30 Sep 2026

### Work
- Deterministic replay verification — pick logged runs at random and reproduce them.
- Code cleanup.
- Public code artefact.
- Figures for Manuscript B.
- Reproducibility appendix.

### The standard being met
*A number you cannot reproduce on 29 Sep is not a number.* This block is where that rule is tested rather than asserted.

### Definition of done
- [ ] Randomly sampled logged runs replay deterministically
- [ ] Code cleaned and documented to release quality
- [ ] Public artefact packaged (with Track 4)
- [ ] All Manuscript B figures delivered
- [ ] Reproducibility appendix written

_Source: §3 Track 2 W7–W9 · §2 Hard rules · §1 In for Manuscript B · Timeline_and_Workload.md V2_
EOF
}

# ---------------------------------------------------------------------------
# Track 3 - Evaluation Harness & Measurement (Arav Sharma)
# ---------------------------------------------------------------------------

seed_track3() {
  echo "== Track 3 - Evaluation Harness & Measurement =="

  mk_issue "T3 · W0 · Fix and freeze the BrowseComp-Plus and OOLONG evaluation subsets" \
    "W0" "track:3-evaluation,phase:A,blocker" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W0 · Wed 29 Jul – Sun 9 Aug 2026

### Work
- Read the base paper's evaluation setup closely.
- Fix the BrowseComp-Plus query subset.
- Fix the OOLONG negative-control subset.

### The non-negotiable part
**Write the exact subsets down and never change them.** A subset that drifts mid-project makes every earlier number incomparable, and the drift is usually invisible until someone asks in review.

### Blocked by
- T1 · W0 · frozen claim and measurement protocol.
- T2 · W0 · structured logging harness.

### Definition of done
- [ ] Base paper eval setup summarised in writing
- [ ] BrowseComp-Plus subset enumerated, committed, hash-stamped
- [ ] OOLONG negative-control subset enumerated, committed, hash-stamped
- [ ] Both marked immutable in the repo

_Source: §3 Track 3 W0 · §4 Dependency map W0 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W1 · Get vanilla RLM control running end-to-end; cost accounting; reproduce a published number" \
    "W1" "track:3-evaluation,phase:A,blocker" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W1 · Mon 10 – Sun 16 Aug 2026

### Work
- **Get vanilla RLM running end-to-end.**
- Token / call / cost accounting wrapper.
- Reproduce one published base-paper number as a sanity check.

### Why this is the highest-value task of W1
The plan is explicit: *the control must work before MARD does — this is the single most valuable thing anyone does in W1.* The vanilla RLM control feeds **every comparison in both papers**. If it is wrong, both manuscripts are wrong and nobody finds out until review.

### Definition of done
- [ ] Vanilla RLM runs end-to-end on the fixed subsets
- [ ] Token, call and cost accounting captured per run
- [ ] One published base-paper number reproduced within a stated tolerance
- [ ] Discrepancy, if any, documented rather than rounded away

_Source: §3 Track 3 W1 · §4 Dependency map W1 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W2 · Scorers, ablation runner, dry-run the matrix on a tiny document" \
    "W2" "track:3-evaluation,phase:A" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W2 · Mon 17 – Sun 23 Aug 2026

### Work
- Scorers: task score, tokens consumed, calls issued, cost.
- Ablation runner (envelope removed).
- Dry-run the matrix on a tiny document.

### Blocked by
- T4 · W2 · document-native ground truth (glossary, learning objectives, cross-references, forward-reference positions) feeds these scorers.

### Why the dry run is in scope
W3 is measurement week and it was compressed from 7 days to 4 in V2. There is no recovery room at all. Discovering a broken scorer on 26 Aug costs the Manuscript A results freeze outright — this dry run is now load-bearing, not prudent.

### Definition of done
- [ ] All four scorers implemented and unit-tested
- [ ] Ablation runner executes the envelope-removed condition
- [ ] Full matrix dry-run completes on a tiny document
- [ ] Every scorer output traces to a logged run

_Source: §3 Track 3 W2 · §4 Dependency map W2 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W3 · Execute Manuscript A measurement matrix" \
    "W3" "track:3-evaluation,phase:A,blocker" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W3 · Mon 24 – Thu 27 Aug 2026 · **4 days (compressed from 7 in V2)**

### ⚠️ V2 compression — read this first
This block lost 3 days to fund the extended W0. There is **no recovery room**. A run that fails on Wed 26 Aug cannot be re-run before the freeze. Front-load: start the longest-running configuration Monday morning, not Tuesday.

### Work
Execute Manuscript A's matrix:
- MARD vs vanilla RLM on the structured benchmark
- Negative control on flat context
- One ablation

### 🔒 Freeze
**Results freeze A · Thu 27 Aug.** Locked. After this, numbers are written up, never re-run. If a result is wrong it gets a limitation paragraph.

### Definition of done
- [ ] MARD vs vanilla comparison complete on the frozen subset
- [ ] Negative control on flat context complete
- [ ] One ablation complete
- [ ] Every number traceable to a logged run with config snapshot and seed
- [ ] Results handed to Track 1 in time to interpret before 27 Aug

_Source: §3 Track 3 W3 · §2 Calendar W3 + Hard rules · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W4 · Results tables and plots for Manuscript A; per-number audit" \
    "W4" "track:3-evaluation,phase:A,writing" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W4 · Fri 28 Aug – Thu 3 Sep 2026

### Work
- Results tables and plots for Manuscript A.
- **Verify every number traces to a logged run.**

### Why the audit is a named task, not an assumption
*A reviewer kills this submission on measurement sloppiness faster than on a modest effect size.* The audit is the cheapest insurance in the project.

### Definition of done
- [ ] All Manuscript A tables produced
- [ ] All Manuscript A plots produced
- [ ] Every reported number mapped to a run ID, config snapshot and seed
- [ ] Audit result recorded — including any number that could *not* be traced

_Source: §3 Track 3 W4 and "Why third" · §2 Hard rules · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W5 · Implement the 3 remaining baselines first-hand; seed control and variance harness" \
    "W5" "track:3-evaluation,phase:B,blocker" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W5 · Mon 31 Aug – Sun 6 Sep 2026

> **V2 note:** this block starts *during* W4. Manuscript A is still in guide review Mon 31 Aug – Tue 1 Sep and delivers Thu 3 Sep. Phase B work starts anyway — that overlap is how the extended W0 was paid for.

### Work
Implement first-hand:
- Full-context baseline
- Naive chunking baseline
- Embedding RAG baseline

Plus seed control and variance reporting.

### Why first-hand, not cited
Citing the base paper's Table 1 is acceptable for a short paper, **not for a full one.** All four baselines (these three plus vanilla RLM from W1) must be run by us for Manuscript B.

### Why variance is the spine
3 seeds on every number, variance reported. Non-negotiable — this is what answers SRLM's (arXiv:2603.15653) published objection that RLM's gains are not primarily driven by recursion.

### Definition of done
- [ ] Full-context baseline implemented and validated
- [ ] Naive chunking baseline implemented and validated
- [ ] Embedding RAG baseline implemented and validated
- [ ] Seed control verified end-to-end with Track 2's plumbing
- [ ] Variance reporting produces spread, not just means

_Source: §1 In for Manuscript B · §3 Track 3 W5 · §4 Dependency map W5 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W6 · Execute the full matrix: 4 docs × 5 systems × 3 seeds + ablation grid + depth sweep" \
    "W6" "track:3-evaluation,phase:B,blocker" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W6 · Mon 7 – Sun 13 Sep 2026

### Work
Execute the full measurement matrix:
- 4 documents × 5 systems × 3 seeds
- Ablation grid: envelope removed · plan withheld from Tier 2 · reordering disabled · depth swept

### 🔒 Freeze
**Feature freeze B · Sun 13 Sep.**

### Risk in play
**#6 · Variance swamps the effect across 3 seeds** (trigger 13 Sep). Response already decided: report it. An effect that vanishes under seed variance *is* the finding, and it is better to publish that than to report a single lucky run.

### Definition of done
- [ ] 60 primary runs (4 × 5 × 3) executed or gaps explicitly recorded
- [ ] Full ablation grid executed
- [ ] Depth sweep executed
- [ ] Variance computed per cell
- [ ] Any variance-swamping outcome escalated to Track 1 on 13 Sep, not later

_Source: §1 In for Manuscript B · §3 Track 3 W6 · §2 Calendar W6 · §5 Risks #6 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W7 · O5 scoring with Track 4; significance treatment appropriate to 3 seeds" \
    "W7" "track:3-evaluation,phase:B" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W7 · Mon 14 – Sun 20 Sep 2026

### Work
- Finish O5 dependency-ordering scoring with Track 4, on 2 documents, against document-native ground truth.
- Significance treatment appropriate to 3 seeds — **report spread honestly, do not over-test.**

### The statistical judgement being made
Three seeds does not support heavy significance machinery. Reporting spread honestly is more defensible than a p-value computed on n=3, and a reviewer will notice the difference.

### 🔒 Freeze
**Results freeze B · Sun 20 Sep.**

### Definition of done
- [ ] O5 scored on 2 documents against glossary / learning objectives / cross-references / forward-reference counts
- [ ] Spread reported per number
- [ ] No significance test applied beyond what n=3 supports
- [ ] Numbers frozen 20 Sep

_Source: §1 In for Manuscript B (O5) · §3 Track 3 W7 · §2 Calendar W7 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T3 · W8–W9 · Final tables, plots, and per-number audit against logs" \
    "W9" "track:3-evaluation,phase:B,deliverable" "$T3_USER" <<'EOF'
**Track 3 — Evaluation Harness & Measurement · Arav Sharma**
**Block:** W8–W9 · Mon 21 – Wed 30 Sep 2026

### Work
- Final tables and plots for Manuscript B.
- Per-number audit against logs.

### Definition of done
- [ ] All Manuscript B tables final
- [ ] All Manuscript B plots final
- [ ] Every number in the manuscript mapped to a run ID, config snapshot and seed
- [ ] Audit signed off before 30 Sep

_Source: §3 Track 3 W8–W9 · §2 Hard rules · Timeline_and_Workload.md V2_
EOF
}

# ---------------------------------------------------------------------------
# Track 4 - Corpus, Ground Truth & Manuscript Production (Tanish Sharma)
# ---------------------------------------------------------------------------

seed_track4() {
  echo "== Track 4 - Corpus, Ground Truth & Manuscript Production =="

  mk_issue "T4 · W0 · Confirm corpus licensing; compile the deadline table for faculty; set up LaTeX repo" \
    "W0" "track:4-corpus-production,phase:A,blocker" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W0 · Wed 29 Jul – Sun 9 Aug 2026

### Work
- Confirm licensing on OpenStax / OSTEP / Axler.
- **Compile the deadline + page-limit + archival-status table for faculty** so the venue decision is informed.
- Set up the LaTeX repo and bibliography.

### Why the deadline table is a blocker
Venue selection is the faculty's decision, and they cannot make it without this table. It is the W0 → faculty edge in the dependency map.

### Starting point (verified 29 Jul 2026 — re-verify before sending)
| Venue | Deadline | Note |
|---|---|---|
| ARR August cycle | 3 Aug 2026 | Closed for practical purposes. Feeds EACL 2027. |
| **ARR October cycle** | **12 Oct 2026** | Feeds NAACL 2027 / COLING 2027. 12 days after B is ready. |
| EMNLP 2026 workshops (Budapest, 24–29 Oct) | Direct submission late Jul–Aug, notification late Aug–Sep | Fastest path to an actual decision. Deadlines are per-workshop. |
| ICLR 2027 | Abstract 19 Sep, paper 24 Sep 2026 — **aggregator-sourced, UNVERIFIED against iclr.cc** | Lands 6 days before B is ready. |
| AAAI-27 | 28 Jul 2026 | Closed. |
| AIED 2027 / EDM 2027 | ~Feb 2027 (predicted) | Beyond this semester. |
| IJAIED · Computers & Education: AI | Rolling | Review takes months. |
| AIET 2026 | Held 29–31 Jul 2026 | Closed. |

### ⚠️ Must be resolved before the table goes out
ICLR 2027's dates came from aggregators only. **iclr.cc returned no content on 29 Jul 2026.** Do not hand faculty an unverified deadline without marking it as such.

### Also flag to faculty
If Manuscript A goes to an archival venue, prior-publication rules at most main conferences can restrict where B goes afterwards. Journals are usually more permissive about extended versions. Cheap to ask now, expensive to discover in October.

### Definition of done
- [ ] Licensing confirmed in writing for OpenStax, OSTEP and Axler
- [ ] Deadline table compiled with page limits and archival status per venue
- [ ] ICLR 2027 dates verified against iclr.cc or explicitly marked unverified
- [ ] Archival-status constraint on A→B surfaced to faculty
- [ ] LaTeX repo and bibliography initialised

_Source: §0 (archival note) · §2 Calendar W0 · Deadline reference table · §3 Track 4 W0 · §4 Dependency map W0 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W1 · PDF → text with structural markers and page mapping; clean the primary document" \
    "W1" "track:4-corpus-production,phase:A,blocker" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W1 · Mon 10 – Sun 16 Aug 2026

### Work
- PDF → text + structural markers + page mapping (PyMuPDF / pdfplumber).
- Clean the primary document.

### ⚠️ Hard blocker
**This is a hard W1 blocker for Track 1.** Pass 0 skeleton extraction has nothing to run on until this lands. The plan says it directly: *"lightest" does not mean "starts late."*

Track 1 also owns a go/no-go decision on Pass 2 dated **Sun 16 Aug** — that decision depends on Pass 0 having had a real document to run against.

### Definition of done
- [ ] Primary document parsed to text with structural markers preserved
- [ ] Page mapping retained (needed for provenance spot-checks in W7)
- [ ] Document cleaned and committed
- [ ] Track 1 confirms it is usable for Pass 0 — **early in the week, not on Sunday**

_Source: §3 Track 4 W1 · §3 Track 1 W1 decision · §4 Dependency map W1 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W2 · Extract document-native ground truth programmatically" \
    "W2" "track:4-corpus-production,phase:A,blocker" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W2 · Mon 17 – Sun 23 Aug 2026

### Work
Extract programmatically from the primary document:
- Glossary terms
- Per-chapter learning objectives
- In-text cross-references
- Forward-reference positions

### Why document-native, not external
Kendall's τ curriculum alignment against OCW syllabi was cut deliberately: external syllabi are noisy, inconsistently structured, unbounded in collection effort, and weakly interpretable even when the result is favourable. Document-native ground truth is the stronger claim and it is already in scope.

### Blocks
- T3 · W2 · scorers consume this directly.

### Definition of done
- [ ] Glossary terms extracted
- [ ] Per-chapter learning objectives extracted
- [ ] In-text cross-references extracted
- [ ] Forward-reference positions extracted
- [ ] Output format agreed with Track 3 and delivered to their scorers

_Source: §1 Out, permanently (Kendall's τ) · §3 Track 4 W2 · §4 Dependency map W2 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W3 · Hand-verify the dependency-ordering case study on the primary document" \
    "W3" "track:4-corpus-production,phase:A" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W3 · Mon 24 – Thu 27 Aug 2026

### Work
- Hand-verify the dependency-ordering case study on the primary document.
- Count forward-reference violations before vs after reordering.

### Why by hand
This is the O5 evidence. An automated count that nobody checked is exactly the kind of number a reviewer probes first.

### 🔒 Freeze
**Results freeze A · Thu 27 Aug.**

### Definition of done
- [ ] Dependency ordering hand-verified on the primary document
- [ ] Forward-reference violations counted before reordering
- [ ] Forward-reference violations counted after reordering
- [ ] Disagreements between hand count and automated count documented, not reconciled silently

_Source: §1 In for Manuscript B (O5) · §3 Track 4 W3 · §2 Calendar W3 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W4 · Manuscript A production; verify refs [14] and [15] against the ACM record" \
    "W4" "track:4-corpus-production,phase:A,writing,deliverable" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W4 · Fri 28 Aug – Thu 3 Sep 2026

### Work
- Manuscript A production: template, formatting compliance, bibliography, submission mechanics.
- **Verify references [14] and [15] author lists against the ACM record — currently marked unverified in the deck.**

### Why [14] and [15] are called out by name
They are the only two references in the deck flagged as unverified. Shipping a manuscript with a wrong author list on a cited work is a credibility cost out of all proportion to the effort of checking.

### Definition of done
- [ ] Template applied, formatting compliant with the target venue's requirements
- [ ] Bibliography complete and consistent
- [ ] **Ref [14] author list verified against the ACM Digital Library record**
- [ ] **Ref [15] author list verified against the ACM Digital Library record**
- [ ] Every other reference spot-checked
- [ ] Submission mechanics confirmed — **delivered Thu 3 Sep**

_Source: §3 Track 4 W4 · §2 Calendar W4 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W5 · Parse and clean documents 2–4; structural-marker quality report per document" \
    "W5" "track:4-corpus-production,phase:B,blocker" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W5 · Mon 31 Aug – Sun 6 Sep 2026

> **V2 note:** this block starts *during* W4. Manuscript A is still in guide review Mon 31 Aug – Tue 1 Sep and delivers Thu 3 Sep. Phase B work starts anyway — that overlap is how the extended W0 was paid for.

### Work
- Parse and clean documents 2–4 (OSTEP, Axler, and the pilot document).
- **Structural-marker quality report per document.**

### Why the quality report matters more than the parsing
Track 1 needs to know which documents are structurally weak — *that is the O4 story.* MARD is predicted to degenerate gracefully on flat context, and the O4 boundary is stated as a prediction rather than discovered as an excuse. That framing only works if we know, in advance, which documents are weak.

### Corpus rationale
4 documents: enough to show the effect is not document-specific; not so many that W6 becomes a compute-management exercise.

### Blocks
- T1 · W5 · envelope hardening
- T3 · W5–W6 · baselines and the full matrix

### Definition of done
- [ ] Documents 2, 3 and 4 parsed with structural markers and page mapping
- [ ] Per-document structural-marker quality report written
- [ ] Structurally weak documents identified and flagged to Track 1 with reasoning

_Source: §1 In for Manuscript B (4 documents) · §3 Track 4 W5 · §4 Dependency map W5 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W6 · Ground-truth extraction for the 2 documents used in O5 scoring" \
    "W6" "track:4-corpus-production,phase:B" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W6 · Mon 7 – Sun 13 Sep 2026

### Work
Ground-truth extraction for the 2 documents used in O5 dependency-ordering scoring: glossary, learning objectives, in-text cross-references, forward-reference positions.

### 🔒 Freeze
**Feature freeze B · Sun 13 Sep.**

### Definition of done
- [ ] Both O5 documents have complete document-native ground truth extracted
- [ ] Format matches what Track 3's scorers consume
- [ ] Delivered in time for T3 · W7 scoring

_Source: §1 In for Manuscript B (O5 on 2 documents) · §3 Track 4 W6 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W7 · Hand-verify dependency edges on the second document; provenance spot-checks" \
    "W7" "track:4-corpus-production,phase:B" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W7 · Mon 14 – Sun 20 Sep 2026

### Work
- Hand-verification of dependency edges on the second document.
- Provenance spot-checks for the hallucination-rate measurement.

### Depends on
Track 2's provenance pointers, attached to every generated span since W2.

### 🔒 Freeze
**Results freeze B · Sun 20 Sep.**

### Definition of done
- [ ] Dependency edges hand-verified on document 2
- [ ] Provenance spot-check sample drawn and checked against source pages
- [ ] Hallucination rate reported with the spot-check sample size stated
- [ ] Any unresolvable provenance pointer recorded as a finding

_Source: §1 In for Manuscript B (O5) · §3 Track 2 W2 (provenance) · §3 Track 4 W7 · Timeline_and_Workload.md V2_
EOF

  mk_issue "T4 · W8–W9 · Manuscript B production, appendices, camera-ready checklist, artefact packaging" \
    "W9" "track:4-corpus-production,phase:B,writing,deliverable" "$T4_USER" <<'EOF'
**Track 4 — Corpus, Ground Truth & Manuscript Production · Tanish Sharma**
**Block:** W8–W9 · Mon 21 – Wed 30 Sep 2026

### Work
- Manuscript B production (8–12 pages + appendices).
- Appendices.
- Camera-ready checklist.
- Artefact packaging (with Track 2).

### Definition of done
- [ ] Manuscript B formatted to the target venue's template
- [ ] Appendices assembled, including the reproducibility appendix from Track 2
- [ ] Camera-ready checklist completed item by item
- [ ] Code and data artefact packaged and linked
- [ ] Bibliography final and every reference verified
- [ ] **Delivered Wed 30 Sep**

_Source: §0 Shape of the plan · §3 Track 4 W8–W9 · §2 Calendar W9 · Timeline_and_Workload.md V2_
EOF
}

# ---------------------------------------------------------------------------
# Gates and deliverables - these dates do not move
# ---------------------------------------------------------------------------

seed_gates() {
  echo "== Gates & deliverables =="

  mk_issue "🔒 GATE · Feature freeze A · Sun 23 Aug" \
    "W2" "gate,phase:A" "$T1_USER" <<'EOF'
**Feature freeze A — Sun 23 August 2026. Absolute.**

A change to the pipeline invalidates every number measured before it. **Cut features, never the freeze.**

### Must be true before this closes
- [ ] End-to-end run works: doc → envelope → plan → N builders → joined output
- [ ] T1: envelope + Master Plan compilation landed
- [ ] T2: worker pool, fork-join, retry, failure isolation, provenance landed
- [ ] T3: scorers and ablation runner dry-run clean on a tiny document
- [ ] T4: document-native ground truth delivered to T3

### After this date
No pipeline changes until the W5 feature thaw. Anything not landed is not in Manuscript A.

_Source: §2 Calendar W2 · §2 Hard rules · §4 Dependency map · Timeline_and_Workload.md V2_
EOF

  mk_issue "🔒 GATE · Results freeze A · Thu 27 Aug" \
    "W3" "gate,phase:A" "$T1_USER" <<'EOF'
**Results freeze A — Thu 27 August 2026.**

After this, numbers are written up, never re-run. **If a result is wrong, it gets a limitation paragraph, not a re-run.**

### Must be true before this closes
- [ ] T3: MARD vs vanilla on the structured benchmark complete
- [ ] T3: negative control on flat context complete
- [ ] T3: one ablation complete
- [ ] T4: dependency-ordering case study hand-verified
- [ ] T1: results interpreted, contradictions diagnosed

### Risk trigger dated 24 Aug
**Risk #1 — effect size null or negative.** If MARD does not beat vanilla RLM: publish it as a negative result framed by the O4 boundary. Do not tune toward a positive after the fact.

_Source: §2 Calendar W3 · §2 Hard rules · §5 Risks #1 · Timeline_and_Workload.md V2_
EOF

  mk_issue "🚀 DELIVERY · Manuscript A submission-ready · Thu 3 Sep" \
    "W4" "gate,deliverable,phase:A" "$T1_USER" <<'EOF'
**Manuscript A — submission-ready Thu 3 Sepust 2026.**

4–8 pages. Claim: *MARD beats vanilla RLM on a structured benchmark; degenerates gracefully on flat context.*
Evidence: 1 primary document · vanilla RLM control · 1 ablation.

### Schedule inside the block
- Fri 28 Aug: assemble draft off the frozen numbers
- Mon 31 Aug – Tue 1 Sep: guide review (Dr. Soni Sweta) — **W5 starts in parallel for Tracks 2–4**
- Wed 2 Sep: revisions
- Thu 3 Sep: final

### ⚠️ V2: this date moved, B's did not
Originally Fri 28 Aug. Slipped 6 days to fund the extended W0. **Manuscript B holds at Wed 30 Sep**, as do both Phase B freezes.

Cost of the slip: the EMNLP 2026 workshop path (direct submission late Jul–Aug) is likely gone. ARR October (12 Oct) is unaffected and was always the more realistic target given B's date. Confirm with faculty rather than assuming.

### Checklist
- [ ] T1: manuscript assembled, §6 Discussion incl. O4 boundary
- [ ] T2: architecture + pipeline figures, reproducibility notes
- [ ] T3: tables, plots, per-number audit against logs
- [ ] T4: template, formatting compliance, bibliography, refs [14]/[15] verified against ACM

### Raise before submission, not after
Archival status of A can restrict where B goes (risk #2). Faculty's call — but the question has to be asked before A is submitted.

### What A is for
Not a throwaway. It is the forcing function that gets the pipeline running four weeks before it would otherwise be ready, and its results are a strict subset of B's.

_Source: §0 Shape of the plan · §2 Calendar W4 · §5 Risks #2 · §6 Open item 3 · Timeline_and_Workload.md V2_
EOF

  mk_issue "🔒 GATE · Feature freeze B · Sun 13 Sep" \
    "W6" "gate,phase:B" "$T1_USER" <<'EOF'
**Feature freeze B — Sun 13 September 2026. Absolute.**

**Cut features, never the freeze.**

### Must be true before this closes
- [ ] T4: documents 2–4 parsed, quality-reported; O5 ground truth extracted
- [ ] T1: envelope hardened across all 4 documents
- [ ] T2: orchestrator scaled — concurrency, seeds, resumability, cost telemetry
- [ ] T3: all 4 baselines implemented first-hand; full matrix executed (4 docs × 5 systems × 3 seeds) + ablation grid + depth sweep

### Risk trigger dated 13 Sep
**Risk #6 — variance swamps the effect across 3 seeds.** Report it. An effect that vanishes under seed variance is the finding, and it is better to publish that than to report a single lucky run.

_Source: §2 Calendar W6 · §2 Hard rules · §5 Risks #6 · Timeline_and_Workload.md V2_
EOF

  mk_issue "🔒 GATE · Results freeze B · Sun 20 Sep" \
    "W7" "gate,phase:B" "$T1_USER" <<'EOF'
**Results freeze B — Sun 20 September 2026.**

After this, numbers are written up, never re-run.

### Must be true before this closes
- [ ] T3: all remaining runs complete
- [ ] T3 + T4: O5 dependency ordering scored on 2 documents against document-native ground truth
- [ ] T3: significance treatment appropriate to 3 seeds — spread reported honestly, not over-tested
- [ ] T4: dependency edges hand-verified on document 2; provenance spot-checks done
- [ ] T1: §4–§6 written against real numbers

_Source: §2 Calendar W7 · §2 Hard rules · §3 Tracks 1/3/4 W7 · Timeline_and_Workload.md V2_
EOF

  mk_issue "🚀 DELIVERY · Manuscript B ready · Wed 30 Sep" \
    "W9" "gate,deliverable,phase:B" "$T1_USER" <<'EOF'
**Manuscript B — ready Wed 30 September 2026.**

8–12 pages + appendices. The real technical contribution.

Claim, hardened: multi-document · all baselines first-hand · variance reported · dependency-ordering result included.
Evidence: 4 docs · 4 baselines · full ablation grid · 3 seeds · O5 scored on 2 documents.

### Checklist
- [ ] T1: full assembly, limitations, guide-review response (review assumed Wed 23 Sep), final polish
- [ ] T2: deterministic replay verified, code cleanup, public artefact, figures, reproducibility appendix
- [ ] T3: final tables, plots, per-number audit against logs
- [ ] T4: production, appendices, camera-ready checklist, artefact packaging

### Downstream date, for context
**ARR October cycle closes 12 Oct 2026** — 12 days after B is ready. Feeds NAACL 2027 / COLING 2027. Venue selection is the faculty's decision; this ticket produces the paper, not the submission.

### The standard
*A number you cannot reproduce on 29 Sep is not a number.*

_Source: §0 Shape of the plan · §2 Calendar W9 · Deadline reference table · §2 Hard rules · Timeline_and_Workload.md V2_
EOF
}

# ---------------------------------------------------------------------------
# Open items - decisions Anugrah owns, all dated W0 (section 6)
# ---------------------------------------------------------------------------

seed_open_items() {
  echo "== Open items (decisions) =="

  mk_issue "DECISION · Confirm Track 2/3/4 name assignment" \
    "W0" "decision,phase:A" "$T1_USER" <<'EOF'
**Open item 1 · §6 · owned by Anugrah**

The Track 2/3/4 allocation in the plan is a **suggestion**. You know the team's actual strengths.

### Guidance from the plan
- **Track 2 (Orchestration)** needs the strongest async/systems person.
- **Track 3 (Evaluation)** needs the most meticulous one — *a reviewer kills this submission on measurement sloppiness faster than on a modest effect size.*
- Track 4 is lightest technically but owns two hard blockers (W1 parsing, W2 ground truth) and all submission mechanics.

### Current suggested split
| Track | Suggested |
|---|---|
| T1 · MARD Core & Paper Lead | Anugrah Shetty (fixed — the envelope is the novelty) |
| T2 · Orchestration & Tier 2 | Parth Sangani |
| T3 · Evaluation & Measurement | Arav Sharma |
| T4 · Corpus & Production | Tanish Sharma |

### Definition of done
- [ ] Assignment confirmed or changed
- [ ] GitHub usernames collected for all four and applied to every open issue

_Source: §3 Track headers · §6 Open item 1 · Timeline_and_Workload.md V2_
EOF

  mk_issue "DECISION · Model pair selection, and whether to soften slide 13's Pareto-sweep framing" \
    "W0" "decision,phase:A" "$T1_USER" <<'EOF'
**Open item 2 · §6 · owned by Anugrah**

### Decision
Pick one frontier and one budget model in W0, on **published benchmarks**.

### The framing problem
Deck slide 13 claims model selection is a *result, not an assumption* — a 3×3 Pareto sweep across three pilot documents. That is honest, but it does not fit in nine weeks.

**Recommendation in the plan:** run a reduced 2×2 sweep in W5 if there is slack, and soften slide 13's framing in the paper to *"we select from published benchmarks and report the cost frontier for our chosen pair."*

**Overclaiming a sweep we did not run is the kind of thing that gets caught.**

### Definition of done
- [ ] Frontier model chosen, with the published benchmark cited
- [ ] Budget model chosen, with the published benchmark cited
- [ ] Slide 13 framing decision made and recorded
- [ ] W5 2×2 sweep marked as optional-if-slack, not planned-as-required

_Source: §1 On model selection · §6 Open item 2 · Timeline_and_Workload.md V2_
EOF

  mk_issue "DECISION · Confirm guide review windows with Dr. Soni Sweta" \
    "W0" "decision,phase:A" "$T1_USER" <<'EOF'
**Open item 3 · §6 · owned by Anugrah**

### Assumed windows
- **Manuscript A:** Mon 31 Aug – Tue 1 Sep 2026
- **Manuscript B:** Wed 23 Sep 2026

### The rule if she needs longer
**The results freezes move left, not the delivery dates.** Delivery dates (3 Sep, 30 Sep) are fixed.

### Definition of done
- [ ] Dr. Sweta has confirmed both windows, or given alternatives
- [ ] If longer is needed, new results-freeze dates set and communicated to all four tracks
- [ ] Milestone due dates updated on this board to match

_Source: §2 Calendar W4/W8 · §6 Open item 3 · Timeline_and_Workload.md V2_
EOF

  mk_issue "DECISION · Set the compute and API budget ceiling" \
    "W0" "decision,phase:A,blocker" "$T1_USER" <<'EOF'
**Open item 4 · §6 · owned by Anugrah**

### Decision needed
A **number**, in W0, before Track 2 sets the spend cap.

### Why it is a blocker
T2's W0 task cannot close without it, and risk #5 (API cost or rate limits throttle W6) has a mitigation — vLLM + open weights for ablation sweeps, frontier model reserved for final tables — that only works if there is a cap to check against weekly.

### Definition of done
- [ ] Ceiling agreed as a specific figure
- [ ] Handed to Track 2 for the spend cap
- [ ] Weekly check added to the Friday gate review agenda

_Source: §3 Track 2 W0 · §5 Risks #5 · §6 Open item 4 · Timeline_and_Workload.md V2_
EOF
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
  echo "Seeding backlog into $REPO_SLUG from $PLAN_DOC"
  [[ "$DRY_RUN" == "1" ]] && echo "*** DRY RUN - nothing will be created ***"
  echo

  preflight
  load_existing_titles
  echo

  seed_labels
  seed_milestones
  echo

  seed_track1
  seed_track2
  seed_track3
  seed_track4
  seed_gates
  seed_open_items

  echo
  echo "Done. Created: $created_count   Skipped (already existed): $skipped_count"
  if [[ -z "$PROJECT_NUMBER" ]]; then
    echo "Issues were NOT added to a Projects board. Re-run with PROJECT_NUMBER=<n> to add them."
  fi
}

main "$@"
