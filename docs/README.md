# Supplementary record

This directory is the supplementary results log referenced by the manuscript in
`../paper/`. It holds the measurement protocol, the decision records that fixed
that protocol *before* any result existed, and the results themselves.

Every number in the paper traces to a run directory under `../runs/`. These
documents say what was measured, how, and what was decided in advance. They were
written as the work happened rather than reconstructed afterwards, which is why
some record decisions that later turned out to be wrong — those are kept, with
the correction recorded in place, rather than quietly edited out.

## Results

| Document | Backs |
|---|---|
| [`28-MARD_ARM_FINDINGS.md`](28-MARD_ARM_FINDINGS.md) | The MARD campaign: nine runs, the ablation ladder, the async-seam and token-budget defects found during it |
| [`35-SCORING_RESULTS.md`](35-SCORING_RESULTS.md) | Task scores, tokens and cost, MARD vs vanilla RLM (paper Table VI) |
| [`38-DETERMINISM_RESULTS.md`](38-DETERMINISM_RESULTS.md) | Structural stability, fidelity and provenance; per-chapter coverage (paper Table VII) |
| [`32-GROUNDEDNESS_RESULTS_AND_ARCHITECTURAL_INSTABILITY.md`](32-GROUNDEDNESS_RESULTS_AND_ARCHITECTURAL_INSTABILITY.md) | Groundedness of generated content; the vanilla arm's run-to-run instability (paper Table IX) |
| [`41-NEGATIVE_CONTROL_RESULTS.md`](41-NEGATIVE_CONTROL_RESULTS.md) | The structure-ablated negative control (paper Table XI) |
| [`44-SECOND_DOCUMENT_RESULTS.md`](44-SECOND_DOCUMENT_RESULTS.md) | Replication on a second document (paper Table VIII) |
| [`43-BASE_PAPER_HARNESS_CHECK.md`](43-BASE_PAPER_HARNESS_CHECK.md) | The bounded OOLONG harness check — explicitly **not** a reproduction |

## Protocol and design, fixed before results

| Document | Contents |
|---|---|
| [`00-CLAIM.md`](00-CLAIM.md) | The claim as registered, including what a null result would look like |
| [`30-MEASUREMENT_PROTOCOL.md`](30-MEASUREMENT_PROTOCOL.md) | The seven fields every run must record; seed policy; what counts as a re-runnable failure |
| [`31-ABLATIONS.md`](31-ABLATIONS.md) | The frozen ablation set and what each manipulation isolates |
| [`23-GROUNDTRUTH_SPEC.md`](23-GROUNDTRUTH_SPEC.md) | How document-native ground truth is extracted, and why LLM-generated ground truth was rejected |
| [`24-GROUNDEDNESS_AND_SEED42.md`](24-GROUNDEDNESS_AND_SEED42.md) | The seed-42 grounding anomaly and the rule that kept it in the results |
| [`16-PRIMARY_DOCUMENT.md`](16-PRIMARY_DOCUMENT.md) | Choice of primary document and the corpus's known limits |
| [`01-ENVELOPE_VS_BASE_LIBRARY.md`](01-ENVELOPE_VS_BASE_LIBRARY.md) | What the base library's metadata already does, and what the envelope adds |

## Infrastructure decisions

| Document | Contents |
|---|---|
| [`18-PROVIDER_MIGRATION.md`](18-PROVIDER_MIGRATION.md) | The mid-project provider change, what it invalidated, and what it made possible |
| [`22-MODEL_PAIR_OPENAI.md`](22-MODEL_PAIR_OPENAI.md) | The model pair, and the honest statement that no published benchmark justifies it |
| [`40-LITERATURE_LOG.md`](40-LITERATURE_LOG.md) | Every cited work, verified first-hand against its primary record |
| [`RLM_BASELINE_SURVEY.md`](RLM_BASELINE_SURVEY.md) | Survey of candidate baselines and why the vanilla-RLM isolation baseline was chosen |

## Reading these documents

**Numbering is historical.** Gaps are documents that were internal to building
the system — implementation briefs, task assignments, project bookkeeping — and
are not part of the public record. Numbers were not reassigned, so a reference
in one document still points where it did when it was written.

**Vocabulary.** `W0`–`W5` are project week milestones; `W0` is planning and `W3`
is the measurement campaign. `Track 1`–`Track 4` were parallel workstreams
(design, orchestration, evaluation, ingestion). `O1`–`O6` are the research
objectives, listed with the outcome each returned in Table I of the
manuscript (Section 1.3, *Objectives, and what each returned*). `O6` is
deferred: only the vanilla-RLM isolation baseline was run.

**Amendment banners.** Several documents open with a banner recording that a
figure below was later corrected. Those are deliberate: three measurement
defects were found by re-deriving published numbers by hand, and the record of
each correction is kept where the original claim was made.
