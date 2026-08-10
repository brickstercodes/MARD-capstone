# Working in this repo

Read `../CONTEXT.md` first. It is the single source of truth and it overrides
anything inferred from the code.

## Three rules that override anything you infer

1. **The deliverable is two manuscripts.** Working code is a means, not the
   goal. A change that makes the code nicer but invalidates a measured number is
   a net loss.
2. **No claim, citation, figure or number enters any artefact without a
   first-hand source.** A July 2026 audit of this project's own materials found
   three misattributed citations and four wrong figures, all carried confidently
   from one document to the next.
3. **There are four parallel workstreams.** Inventing a decision that belongs to
   another track produces four incompatible answers. Escalate instead.

## Do not decide these — escalate to Anugrah

- Track → person assignment
- The model pair (one frontier, one budget)
- Compute / API budget ceiling
- Venue, and whether Manuscript A goes to an archival venue (faculty's call)
- Whether the paper softens the Pareto-sweep framing

If work is blocked on one of these, say so and stop.

## Dead claims — never reintroduce

- "15–25× cost reduction" — rests on a rate that no longer exists. Present the
  cost *model*; the number arrives with the results.
- "No system supports uploading an entire textbook" — false in 2026. The gap is
  **ordering**, not ingestion.
- "40% accuracy loss beyond 128K" attributed to *Lost in the Middle* — that
  paper reports no such figure.
- Named 2024-era models (Gemini 1.5 Pro, Claude 3.5 Sonnet, Llama 3.1, Mistral
  7B). Say "frontier tier" and "budget tier"; name models only at selection time.
- Kendall's τ curriculum alignment against external syllabi — cut permanently.

## Code conventions

- Comments explain **why**, never what.
- Every module gets a file-level docstring explaining why it exists.
- Single responsibility. Rule of Three before abstracting.
- Named constants over magic values.
- Dependencies flow inward.
- `ruff format` · `ruff check` · `mypy` before committing.

## Measurement discipline

- Every run goes through `runlog.RunLogger`. No exceptions.
- Three seeds on every number (`runlog.CAMPAIGN_SEEDS`), variance reported.
- Model rates come from the provider's own pricing page, on the day, with the
  URL recorded. `RateCard` refuses rates older than 30 days.
- If a figure cannot be verified first-hand, mark it `[UNVERIFIED]` and surface
  it. Do not quietly drop it and do not quietly assert it.
