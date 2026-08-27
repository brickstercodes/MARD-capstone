# How to set up the @Capstone project board

> **Why this is a manual doc.** GitHub does not expose ProjectV2 *view* mutations in its
> public API, so view layouts, grouping, slicing and filters cannot be scripted.
> `scripts/configure_board.sh` sets every **field value** (Track, Phase, Block,
> Priority, Status, Start date, End date); the steps below turn those fields into
> views. Budget about five minutes.

## 0. Before anything else

**Clear the search box.** The board currently has `pr` typed into it, which is why only
13 of 46 cards are visible. Click the ✕ at the right of the search bar.

**Then run the field script:**

```bash
cd ~/Desktop/Capstone/MARD-capstone
PROJECT_NUMBER=2 DRY_RUN=1 ./scripts/configure_board.sh   # inspect
PROJECT_NUMBER=2 ./scripts/configure_board.sh             # apply
```

It creates four single-select fields (`Track`, `Phase`, `Block`, `Priority`) and two
date fields (`Start date`, `End date`), then fills them on all 45 plan items.

**Raise the Backlog WIP limit.** The column reads `12 / 5` — a limit of 5 on a backlog
column will sit permanently red and stop meaning anything. Column `···` → *Set limit* →
clear it, or set it on **In progress** instead, where a WIP limit actually does work.

---

## 1. Five views to build

Rename the existing views rather than adding more — five tabs is already the practical
maximum before the tab bar stops being scannable.

### View 1 — "Now" (board) · the default tab

The only view anyone should need on a normal day.

| Setting | Value |
|---|---|
| Layout | **Board** |
| Column field | **Status** |
| Slice by | **Track** |
| Filter | `block:W0,W1 -status:Done` |
| Sort | `Priority` ascending |

Slicing by Track puts a left-hand panel on the board: click a track and the board shows
only that person's cards. Nobody has to read 45 titles to find their four.

**Why filter to W0/W1:** a board showing all nine weeks is a document, not a board.
Widen the filter one block at a time as you move through the plan.

### View 2 — "By track" (board) · who owns what

| Setting | Value |
|---|---|
| Layout | **Board** |
| Column field | **Track** |
| Filter | `-status:Done` |
| Sort | `Block` ascending |

Five columns, one per track plus Gates & Decisions, each in week order. This is the view
for "am I clear on my lane for the next month."

### View 3 — "Sprint" (table) · Friday gate review

| Setting | Value |
|---|---|
| Layout | **Table** |
| Group by | **Block** |
| Visible fields | Title · Assignees · Track · Status · Priority · End date |
| Filter | `-status:Done` |
| Sort | `Track` ascending |

Grouped by week, so the Friday 45-minute gate review is literally "open this view, read
the W*n* group, close the gate or escalate."

### View 4 — "Roadmap" · the calendar

| Setting | Value |
|---|---|
| Layout | **Roadmap** |
| Date fields | Start = **Start date**, Target = **End date** |
| Group by | **Track** |
| Markers | **Milestones** |
| Zoom | **Month** |

This is the view that was blank before — Roadmap needs date fields, and every item's
were empty. With `Markers: Milestones` on you get the W0–W9 milestone lines drawn over
the bars, so the freezes are visible as vertical marks.

Two things you should be able to *see* here once it renders:

- **W4 overlapping W5** — the Manuscript A bar runs underneath the start of Phase B.
  That overlap is how the extended W0 was paid for (Timeline V2 §2.1).
- **W3 as the short bar** — 4 days against everything else's 7. That is the block with
  no recovery room.

### View 5 — "Gates" (table) · the dates that do not move

| Setting | Value |
|---|---|
| Layout | **Table** |
| Filter | `label:gate,decision` |
| Sort | `End date` ascending |
| Visible fields | Title · Assignees · End date · Status |

Ten rows: four freezes, two deliveries, four W0 decisions. Pin this tab. Everything else
on the board can slip a day; nothing here can.

---

## 2. Field reference

Set by `scripts/configure_board.sh`, derived from issue titles and
`Timeline_and_Workload.md` V2 §2.

| Field | Values | Meaning |
|---|---|---|
| **Track** | T1 · Core & Paper · T2 · Orchestration · T3 · Evaluation · T4 · Corpus & Production · ⚑ Gates & Decisions | Owner lane |
| **Phase** | A · Pipeline & Manuscript A · B · Hardening & Manuscript B | Which manuscript this serves |
| **Block** | W0 … W9 | Sprint block; spans are filed under their *start* week |
| **Priority** | P0 · Now (W0–W1) · P1 · Next (W2–W4) · P2 · Later (W5–W9) | How soon, not how important — everything here is important |
| **Start / End date** | per block | Drives Roadmap. Spans cover the whole range (e.g. T2 · W7–W9 runs 14–30 Sep) |
| **Status** | Ready (W0) · Backlog (everything else) | Only the current block is Ready, so *Ready* keeps its meaning |

**Estimate is deliberately left empty.** Filling it from block length would encode
"days available" as "effort," which is not the same number and would quietly mislead the
Friday review. Set it yourselves during planning if you want it.

## 3. Re-running

`configure_board.sh` is idempotent — existing fields are detected and reused, values are
overwritten with the same derivation. Re-run it after adding issues, or after a timeline
revision (update `block_dates()` in the script first, and the milestone due dates in
`seed_github_issues.sh` to match).

## 4. Weekly hygiene

- Move **Status → Ready** for the incoming block each Monday, and widen View 1's filter.
- The four **decision** tickets should close in W0. If any is still open on 9 Aug, it is
  blocking someone — check the issue body for who.
- **Gate tickets close last**, after every checklist box in them is ticked. A gate closed
  early is a gate that did not happen.
