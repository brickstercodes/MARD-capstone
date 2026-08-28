# 30 — Measurement protocol

> ### ⚠️ AMENDED — 26 Aug 2026 (protocol still frozen; two rows changed)
>
> The provider switch to OpenAI ([`18-PROVIDER_MIGRATION.md`](18-PROVIDER_MIGRATION.md))
> changes exactly three things here. Everything else — the seven required fields, the
> ground-truth source, the explanations-only constraint, the matrices, the freezes —
> stands unchanged.
>
> 1. **§1 "Cost"** — read "same-day published **OpenAI** rate", not Vertex. Same
>    discipline, same 30-day staleness rule.
> 2. **§1 "Seed"** — `replm` has **no `seed` parameter**, and reasoning-model endpoints
>    reject `temperature` outright. "3 seeds" is operationally **3 repeat runs at default
>    sampling, variance reported across repeats**; `CAMPAIGN_SEEDS` remain run
>    *identifiers*. `TRACK3_HANDOFF.md` already anticipated this. See `18` §5.4.
> 3. **§1 "Config snapshot"** — depth must be logged as an
>    **`(enable_sub_calls, max_recursion_depth)` pair**, never one integer, or the A4
>    depth-0 row is a silent duplicate of depth-1. See `18` §5.1.
> 6. **§5's Manuscript A matrix substitutes the negative control.** The frozen OOLONG
>    subset (n=50, `eval/frozen_subsets/`) is **deferred to Manuscript B**: at 150–800 s per
>    run, ×2 systems ×3 seeds, it is days of wall-clock. Manuscript A's flat-context control
>    is instead a **structure-ablated variant of the primary document** — same text, section
>    order shuffled, heading markers stripped. This holds content constant and varies only
>    structure, so it is a manipulation rather than a change of corpus, and `run_pass0`
>    already records the resulting empty skeleton as `degenerate: true` rather than as an
>    error. **This is a scope deferral, not an edit to a frozen subset** — nothing in
>    `eval/frozen_subsets/` is touched, per that directory's own immutability rule. See
>    the MARD-arm implementation brief.
> 5. **§4 gains a failed-run definition, and §1 gains groundedness fields** — see
>    [`24-GROUNDEDNESS_AND_SEED42.md`](24-GROUNDEDNESS_AND_SEED42.md) §6. A run is
>    re-runnable only if the **protocol did not execute** (harness fault, provider fault,
>    unverified corpus). A run in which the *system under test* behaved badly is a **result**
>    and is reported. Systems producing per-concept output additionally record a
>    **groundedness rate**, a **regeneration count**, and where derivable a **mis-sourced
>    count**.
> 4. **§6 is replaced.** The Google MRCR v2 reproduction is void. Track 3 instead
>    reproduces a **base-paper** number (arXiv:2512.24601), which is what §6 always wanted
>    and could not have while the pair was Gemini. See `18` §6.

**Status:** Frozen W0 (2 Aug 2026) · Owner: Track 1 · **This is the document Track 3 builds its scorers and matrix runner against** (`CONTEXT.md` §3.6 dependency map, W0 edge T1 → T3). Track 3: read this fully before starting the W1 vanilla-RLM-control task.

Anything not nailed down here is exactly the kind of ambiguity `CONTEXT.md` Part 0 rule 3 warns about — four sessions each filling the gap with a "sensible default" produces four incomparable numbers. If something you need isn't specified below, escalate to Track 1; do not infer it.

## 1. What gets measured, per run

Every run of any system (MARD, vanilla RLM / A1, any baseline, any other ablation) on any document, for any seed, must record:

| Field | Definition |
|---|---|
| **Task score** | Output quality metric — see §2. Depends on evaluated output modality: **explanations only** (`CONTEXT.md` §2.1). Never flashcards/quizzes/diagrams. |
| **Tokens consumed** | Input + output tokens, summed across every model call in the run (Tier 1 scout + all Tier 2 builders). Split input/output separately in the log; report the sum in tables. |
| **Calls issued** | Count of model API calls, split by tier (Tier 1 call count, Tier 2 call count, total). |
| **Cost** | `tokens × same-day published OpenAI rate`, from `provider.rates.build_rate_card()` (`docs/18` §1/§10 — `docs/12-MODEL_PAIR.md` is void). Never a cached/aggregator rate — `CONTEXT.md` §4.3 item 4: "third-party aggregators disagreed by up to 2× for the same model during preparation." |
| **Wall-clock latency** | End-to-end run time. Fork-join means this is `max(builder latency)`, not `Σ(builder latency)` — report both so the parallelism claim is checkable, not asserted. |
| **Seed** | Which of the 3 seeds this run used. See §4. |
| **Config snapshot** | Full run configuration — model IDs, prompt template versions, depth setting, which ablation (if any) is active, document ID. |

A number that cannot be traced back to all seven fields above, from a logged run, is not a number (`CONTEXT.md` §3.4).

## 2. Task score — output quality

Evaluated output modality is **explanations only**. Score against **document-native ground truth** (`CONTEXT.md` §1.5 glossary): glossary terms, per-chapter learning objectives, in-text cross-references, forward-reference positions — all extracted programmatically by Track 4, never expert-annotated. No ethics approval is implied or needed because no human subjects are involved on this axis.

Exact scoring function (e.g. precision/recall against glossary terms, alignment scoring against learning objectives) is Track 3's implementation detail, not frozen here — but the **ground-truth source** and the **explanations-only modality constraint** are frozen, and Track 3's scorer must be built against document-native ground truth as it is extracted by Track 4 (`CONTEXT.md` §3.3 Track 4 W2), not against any other reference.

## 3. O5 dependency-ordering score — separate from task score

O5 (dependency-ordered artefact) is scored independently of §2's explanation-quality score, on **2 of the 4 documents** (`CONTEXT.md` §2.1). Metric: **forward-reference violations, counted before vs. after reordering** — i.e., count how many times the generated sequence places a concept before something the document itself declares as a prerequisite, comparing book order against Master-Plan order. This is the same metric `docs/31-ABLATIONS.md` A3 uses; O5's full-matrix version and A3's ablation version are the same measurement, run on different document subsets (O5: 2 docs, full baseline set; A3: whichever documents the main matrix covers).

Book order is a real ordering, not a null baseline — `CONTEXT.md` §2.4 is explicit that this is not a straw man.

## 4. Seed policy

**3 seeds on every number, variance reported. Non-negotiable** (`CONTEXT.md` §2.1, §3.4). "Seed" here means: same document, same system, same config — re-run with a different random seed controlling any stochastic decoding (temperature > 0 sampling) and, for MARD/RLM specifically, any non-deterministic ordering in async fork-join execution if that affects output. Variance is reported as spread (e.g., min/max/std across the 3 runs) alongside the central value — never a single run presented as *the* number, and never seeds cherry-picked or dropped after the fact (`CONTEXT.md` §3.4: "never tune toward a positive result after the fact").

If variance swamps an effect, that is reported as the finding, not hidden (Risk #6, `CONTEXT.md` §3.7).

## 5. The matrix, by manuscript

**Manuscript A (W3, locked 27 Aug):** 1 primary document × systems {vanilla RLM (=A1) · MARD full · negative control on flat-context document (OOLONG) · ablation A2 (plan withheld — chosen in `docs/31-ABLATIONS.md`)} × 3 seeds. Front-load the longest run — W3 is 4 days with no recovery room (`CONTEXT.md` §3.3, §3.5).

**Manuscript B (W6, locked 13 Sep):** 4 documents × 5 systems (4 first-hand baselines + MARD) × 3 seeds, plus the full ablation grid (A1–A4, with A4 as the depth sweep) and O5 scoring on 2 of the 4 documents.

The 5 systems for B, named exactly (`CONTEXT.md` §2.1, §2.2 item 2): full-context · naive chunking · embedding RAG · vanilla RLM · MARD. "Single-tier without the plan" is **not** a 6th system — it is ablation A2, already counted above.

## 6. Sanity check before trusting any MARD number

Per `docs/12-MODEL_PAIR.md`, the original plan to reproduce a base-paper GPT-5 number is unavailable (base paper and SRLM are GPT-5-family only; our pair is Gemini). **Replacement, assigned to Track 3, before W1 sign-off:** reproduce Google's own GDM-MRCR v2 (8-needle) number for `gemini-3.6-flash` directly against the Vertex AI endpoint, using the released dataset at `github.com/google-deepmind/eval_hub/tree/master/eval_hub/mrcr_v2`, and confirm it lands near the published 91.8%/54.0% figures in `docs/12-MODEL_PAIR.md`. If it doesn't reproduce, that is a signal about our harness before it's a signal about anything else — stop and diagnose before running the real matrix.

## 7. Logging requirements

Every run logged: envelope state (for MARD runs), full transcripts, token counts, config snapshot, seed (`CONTEXT.md` §3.4). This lives under `runs/` per the intended repo shape in `CONTEXT.md` §4.1. Track 2 owns the logging harness itself (`CONTEXT.md` §3.3 Track 2 W0: "structured logging + config-snapshot harness — Track 3 depends on this existing in W0"); this protocol defines *what* must be captured, Track 2 defines *how*.

## 8. Freeze interaction

**Feature freezes (23 Aug / 13 Sep) are absolute** — a pipeline change invalidates every number measured before it (`CONTEXT.md` §3.4). This protocol document itself is frozen as of today; if it needs to change after Track 3 has built against it, that is a protocol change requiring Track 1 sign-off and, if past a feature freeze, is out of scope for the manuscript the freeze protects.

**Results freezes (27 Aug / 20 Sep):** after these, numbers are written up, never re-run. A wrong result gets a limitations paragraph, not a re-run (`CONTEXT.md` §3.4).

## 9. What this protocol deliberately does not specify

- The exact BrowseComp-Plus query subset and OOLONG negative-control subset — these are Track 3's W0 task to fix and never change once written down (`CONTEXT.md` §3.3 Track 3 W0). This protocol requires that they be written down and frozen; it does not choose them.
- The internal implementation of the task-quality scorer (§2) beyond its ground-truth source and modality constraint.
- Model pair, budget ceiling, provider — see `docs/12-MODEL_PAIR.md`.
- Ablation definitions — see `docs/31-ABLATIONS.md`.
