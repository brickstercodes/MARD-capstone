"""The project's RateCard, built from provider pricing read on the day.

CONTEXT.md §4.3 rule 4 and runlog.pricing's own docstring both say the same
thing: a rate is only usable when it carries the date it was read and the
provider's own URL. This module is that reading.

Two cards, because the project has now measured runs on two providers and both
sets of numbers have to stay quotable:

  - `default_rate_card()` -- OpenAI, the active backend (docs/17).
  - `gemini_rate_card()` -- Vertex, retained so the 122 runs already in `runs/`
    and every figure in docs/16 can still be re-priced. A number you cannot
    reproduce is not a number (CONTEXT.md §3.4).

`rate_card_for()` picks between them off the active backend profile, so a run
can never be priced against the provider it did not use.

## What was read, and the discrepancy found reading it

OpenAI's own pricing page (developers.openai.com/api/docs/pricing), read
25 Aug 2026, gives gpt-5.6-terra at $1.00/$6.00 and gpt-5.6-luna at
$0.10/$0.60 per 1M input/output.

The GPT-5.6 launch coverage from 9 Jul 2026 quotes a materially different set
-- luna $1/$6, terra $2.50/$15, sol $5/$30 -- i.e. terra 2.5x and luna 10x
above what the provider's page states today. Whether that is a July price cut
or launch-day reporting error, this is precisely the up-to-2x aggregator
disagreement §4.3 rule 4 exists to guard against, so the provider page wins and
the discrepancy is recorded here rather than resolved by preference. Anyone
quoting a cost figure in either manuscript should re-read the page that day;
`MAX_RATE_AGE` will force the issue on its own after 30 days.

The page also lists cached-input rates ($0.10/1M for terra, $0.01/1M for luna).
`runlog.ModelRate` has no cached-input field and this module does not add one --
that is Track 2's schema, and a cached rate that silently priced as uncached
would be the exact silent-wrong-number failure `runlog/pricing.py` was built to
prevent. Logged as verification debt in docs/17 instead; it matters for Tier 1's
repeated envelope reads, the same concern docs/12 raised for Vertex caching.
"""

from __future__ import annotations

from datetime import date

from runlog import ModelRate, RateCard

OPENAI_RATES_READ_ON = date(2026, 8, 25)
OPENAI_PRICING_URL = "https://developers.openai.com/api/docs/pricing"

TIER1_MODEL = "gpt-5.6-terra"
TIER2_MODEL = "gpt-5.6-luna"

# --------------------------------------------------------------------- Vertex
# Kept verbatim from the 22 Aug reading that priced every existing run. See
# git history for the full note: docs/12 records $1.50/$7.50 for
# gemini-3.6-flash, which is that model's post-introductory rate effective
# 1 Jan 2027; $0.75/$3.75 is what runs inside the measurement window were
# actually billed, and is therefore what is recorded.

GEMINI_RATES_READ_ON = date(2026, 8, 22)

GEMINI_TIER1_MODEL = "gemini-3.6-flash"
GEMINI_TIER2_MODEL = "gemini-3.1-flash-lite"


def default_rate_card() -> RateCard:
    """The RateCard in force for the active (OpenAI) measurement window.

    Re-read OPENAI_PRICING_URL and rebuild this before OPENAI_RATES_READ_ON +
    30 days (runlog.pricing.MAX_RATE_AGE) -- RateCard.cost_for raises
    StaleRateError on its own once that window passes, so this isn't a silent
    expiry.
    """
    return (
        RateCard.empty()
        .with_rate(
            ModelRate(
                model=TIER1_MODEL,
                input_per_million=1.00,
                output_per_million=6.00,
                currency="USD",
                retrieved_on=OPENAI_RATES_READ_ON,
                source_url=OPENAI_PRICING_URL,
            )
        )
        .with_rate(
            ModelRate(
                model=TIER2_MODEL,
                input_per_million=0.10,
                output_per_million=0.60,
                currency="USD",
                retrieved_on=OPENAI_RATES_READ_ON,
                source_url=OPENAI_PRICING_URL,
            )
        )
    )


def gemini_rate_card() -> RateCard:
    """Vertex rates as read on 22 Aug 2026, for re-pricing the existing runs.

    Note this card goes stale on 21 Sep 2026 by MAX_RATE_AGE. That is correct
    behaviour, not a bug to work around: re-deriving a historical cost after
    that date means re-reading what Google charged at the time, from the
    provider, and saying so.
    """
    return (
        RateCard.empty()
        .with_rate(
            ModelRate(
                model=GEMINI_TIER1_MODEL,
                input_per_million=0.75,
                output_per_million=3.75,
                currency="USD",
                retrieved_on=GEMINI_RATES_READ_ON,
                source_url="https://deepmind.google/models/gemini/flash/",
            )
        )
        .with_rate(
            ModelRate(
                model=GEMINI_TIER2_MODEL,
                input_per_million=0.25,
                output_per_million=1.50,
                currency="USD",
                retrieved_on=GEMINI_RATES_READ_ON,
                source_url="https://deepmind.google/models/gemini/flash-lite/",
            )
        )
    )


def rate_card_for(backend_name: str) -> RateCard:
    """The card matching a backend, so a run cannot be priced off the wrong one."""
    if backend_name == "openai":
        return default_rate_card()
    if backend_name == "gemini":
        return gemini_rate_card()
    raise ValueError(f"No rate card recorded for backend {backend_name!r}.")
