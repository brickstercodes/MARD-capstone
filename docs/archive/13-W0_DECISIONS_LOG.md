# 13 — W0 decisions log: what was decided, what's still open, what's needed

**Status:** Living document as of 2 Aug 2026 · Branch: `Track1-W0` · Owner: Track 1 (Anugrah Shetty)

This is the single place that answers three questions for anyone picking up this project mid-W0: what did Track 1 already decide, what is still genuinely open and whose call is it, and what does Track 1 need from someone else before the next thing can move. It exists because `CONTEXT.md` Part 0 rule 3 warns that undocumented decisions get reinvented differently by four parallel sessions — this log is the guard against that specific failure for W0.

---

## 1. Decided this W0 — frozen, written into `docs/`

| # | Decision | Where it lives | Closes |
|---|---|---|---|
| 1 | Claim sentence — one sentence, disjunctive (quality and/or tokens), O4 stated as a prediction not a hedge | `docs/00-CLAIM.md` | DoD item 1 |
| 2 | Ablation set — 4 ablations, operationally parameterised (A1 envelope removed = the vanilla-RLM control itself; A2 plan withheld — chosen as Manuscript A's single ablation; A3 reordering disabled; A4 depth sweep {0,1,2,3}) | `docs/31-ABLATIONS.md` | DoD item 2 |
| 3 | Measurement protocol — metrics, seed policy (3 seeds, variance reported, non-negotiable), the matrix definition per manuscript, logging requirements, freeze interaction | `docs/30-MEASUREMENT_PROTOCOL.md` | DoD item 3 (protocol exists; "Track 3 has read it" is not something Track 1 can close alone — see §3 below) |
| 4 | Model pair — **Gemini 3.6 Flash (Tier 1) + Gemini 3.1 Flash-Lite (Tier 2)**, Vertex AI only, cited against GDM-MRCR v2 (official DeepMind pages, vendor-self-reported, flagged as such). Overturns the deck's "3.1 Pro = frontier" framing — 3.6 Flash beats 3.1 Pro on long-context retrieval (91.8/54.0 vs 84.9/26.3) at lower cost | `docs/12-MODEL_PAIR.md` | `CONTEXT.md` §4.2 item 2 |
| 5 | Pareto-sweep framing softened — paper says "we select from published benchmarks and report the cost frontier for our chosen pair," per `CONTEXT.md` §2.2 item 3, with an optional reduced 2×2 in W5 if slack | `docs/12-MODEL_PAIR.md` §"Why Gemini 3.1 Flash-Lite," last paragraph | `CONTEXT.md` §4.2 item 7 |
| 6 | Budget ceiling — **₹75,000 maximum**, spendable only from Anugrah's existing ~₹90,000 Google Cloud credit balance, Vertex AI only (no AI Studio / Gemini Developer API path) | `docs/12-MODEL_PAIR.md` header | `CONTEXT.md` §4.2 item 3 |
| 7 | Where W0 artefacts land in the (currently empty, zero-commit) repo — `docs/` only, no source tree, so Track 2's W0 scaffolding job doesn't conflict with anything Track 1 wrote | This commit itself | Resolves the `CONTEXT.md` §4.1 tension between "claim sentence written into the repo" (my DoD) and "scaffolding the repo is Track 2's W0 job, do not scaffold it if you are not Track 2" |

---

## 2. Still open — not Track 1's to decide, escalate rather than infer

Straight from `CONTEXT.md` §4.2, restated here with current status so this log doesn't drift out of sync with the source of truth.

| # | Open decision | Owner | Deadline | Status as of 10 Aug |
|---|---|---|---|---|
| 1 | Track → person assignment for Tracks 2–4 | Anugrah | W0 | **Closed, 10 Aug.** Track 1 = Anugrah Shetty. Track 2 = Parth. Track 3 = Arav (GitHub: falseadverstising). Track 4 = Tanish ("Tanz"). No longer a suggestion — this is the confirmed roster; all track-scoped docs and issue assignments should use these names going forward. |
| 4 | Venue | Faculty (Dr. Sweta) | at review | Open. Deadline table exists (`CONTEXT.md` §3.1); not yet raised with her. |
| 5 | Whether Manuscript A goes to an archival venue | Faculty | before A is submitted | Open. Flagged as urgent in `CONTEXT.md` §3.1 — costs nothing to ask now, expensive to discover in October. |
| 6 | Guide review windows | Dr. Sweta's availability | — | Assumed Mon 31 Aug–Tue 1 Sep (A) and Wed 23 Sep (B); not confirmed. If she needs longer, **A's scope gets cut, not the date.** |

Items 2, 3, 7 from `CONTEXT.md` §4.2 (model pair, budget ceiling, Pareto framing) are now closed — see §1 above. Item 1 (track assignment) closed 10 Aug — see row above.

---

## 3. What Track 1 needs from someone else before the next thing moves

This is the part `CONTEXT.md` doesn't have yet, because these are blockers this W0 session's research surfaced, not ones anticipated in the original plan.

### 3a. From Anugrah personally

- **The working Vertex AI Gemini client code from your other project.** The reference RLM library (`github.com/alexzhang13/rlm`) has no Vertex AI path — its `GeminiClient` is hardcoded to the direct API-key flow (`GEMINI_API_KEY` via `google-genai`), not `vertexai=True`/project/location. You said you have a prior project with working Vertex Gemini code. **This needs to actually be handed to Track 2** — pointed at, pasted, or the repo shared — before Track 2 can port it into a patched `GeminiClient`. Nothing further can happen on the orchestration side without it. If it turns out that code doesn't transfer cleanly (different SDK version, different auth flow), Track 2 needs to know that early, not discover it in W1.
- **Confirmation that the ₹75,000 figure is a hard ceiling Track 2 can build a spend-cap against**, not a soft target — `docs/12-MODEL_PAIR.md` treats it as hard. If there's any flex, say so before Track 2 sizes W6's run volume against it.

### 3b. From Track 2 (Parth)

- **Port the Vertex Gemini client** described above. This is now a concrete W0/W1 task, not an assumption — sized and confirmed feasible before end of W0 if possible, since it blocks "RLM library installed and running its own examples" (`CONTEXT.md` §3.3 Track 2 W0).
- **Structured logging + config-snapshot harness**, as already assigned in `CONTEXT.md` §3.3 — `docs/30-MEASUREMENT_PROTOCOL.md` §7 now specifies *what* must be captured (envelope state, transcripts, token counts, config snapshot, seed); Track 2 still owns *how*.

### 3c. From Track 3 (Arav)

- **Read `docs/30-MEASUREMENT_PROTOCOL.md` in full** — this is the literal DoD item still open ("Track 3 has read it"). Track 1 cannot close this alone; it needs a confirmation back.
- **Reproduce the GDM-MRCR v2 (8-needle) number for `gemini-3.6-flash` directly on Vertex** as the new sanity check (replaces the now-unreachable GPT-5 base-paper reproduction — see `docs/12-MODEL_PAIR.md` "Consequences → Negative," item 1). Do this before trusting any MARD-specific measurement.
- **Fix and write down the exact BrowseComp-Plus query subset and OOLONG negative-control subset** — unchanged from `CONTEXT.md` §3.3, restated here because it's still outstanding.

### 3d. From Track 4 (Tanish)

- Nothing new surfaced this session beyond what `CONTEXT.md` §3.3 already assigns (licensing confirmation, deadline table, LaTeX repo setup).

### 3e. Verification debt this session opened (per `CONTEXT.md` §4.3 discipline — surfaced, not silently dropped)

| # | Item | Status |
|---|---|---|
| 1 | No independent (non-Google) long-context benchmark found comparing Gemini 3.6 Flash vs 3.1 Pro — everything in `docs/12-MODEL_PAIR.md` is vendor self-reported | [UNVERIFIED] — re-check before Manuscript A draft, 28 Aug |
| 2 | Whether Track 2's ported Vertex client preserves the RLM library's existing retry/backend-abstraction behaviour | Not yet attempted |
| 3 | Cache-storage pricing for Vertex context caching (relevant to Tier 1's repeated envelope reads) — current pricing page has no storage-per-hour line item, but that silence isn't confirmed as "free" | [UNVERIFIED] — check before W6 cost modelling |

---

## 4. Repo-state note

The `MARD-capstone` local repo had a stale `.git/index.lock` (and a related `HEAD.lock`) left over from an earlier session that the sandbox environment's filesystem bridge would not let this session unlink. The `docs/` commit on `main` (and this branch) was made via git plumbing (`write-tree` / `commit-tree` + direct ref write) to work around it rather than fighting the lock. **If you open this repo on your own machine and git complains about a stale lock, that is this same leftover file** — safe to delete normally there, since your machine doesn't have the sandbox's permission quirk.

Nothing in this branch or on `main` has been pushed to `origin` (`https://github.com/brickstercodes/MARD-capstone.git`). That remains your call.
