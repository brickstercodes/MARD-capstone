"""The project's RateCard, built from provider pricing read on the day.

CONTEXT.md §4.3 rule 4 and runlog.pricing's own docstring both say the same
thing: a rate is only usable when it carries the date it was read and the
provider's own URL. This module is that one-time reading, done for the W1
vanilla-RLM control and every run after it until MAX_RATE_AGE forces a
re-read.

Docs/12-MODEL_PAIR.md records $1.50/$7.50 per 1M in/out for gemini-3.6-flash.
Reading deepmind.google/models/gemini/flash/ directly on 22 Aug 2026 found
that figure is the model's *post-introductory* rate, effective 1 Jan 2027 --
the page states an introductory rate of $0.75/$3.75 applies until then. This
project's measurement window (W1-W6) closes 13 Sep 2026, entirely inside the
introductory period, so $0.75/$3.75 is what a real run is actually billed at
today, and that is the rate recorded below -- not docs/12's figure. Flagged
to Track 1/Anugrah as a correction to that doc's cost projection, not
silently substituted.

gemini-3.1-flash-lite's $0.25/$1.50 matched docs/12-MODEL_PAIR.md exactly on
the same read, no discrepancy there.
"""

from __future__ import annotations

from datetime import date

from runlog import ModelRate, RateCard

RATES_READ_ON = date(2026, 8, 22)

TIER1_MODEL = "gemini-3.6-flash"
TIER2_MODEL = "gemini-3.1-flash-lite"


def default_rate_card() -> RateCard:
    """The RateCard in force for the current measurement window.

    Re-read both source pages and rebuild this before RATES_READ_ON + 30 days
    (runlog.pricing.MAX_RATE_AGE) -- RateCard.cost_for raises StaleRateError
    on its own once that window passes, so this isn't a silent expiry.
    """
    return (
        RateCard.empty()
        .with_rate(
            ModelRate(
                model=TIER1_MODEL,
                input_per_million=0.75,
                output_per_million=3.75,
                currency="USD",
                retrieved_on=RATES_READ_ON,
                source_url="https://deepmind.google/models/gemini/flash/",
            )
        )
        .with_rate(
            ModelRate(
                model=TIER2_MODEL,
                input_per_million=0.25,
                output_per_million=1.50,
                currency="USD",
                retrieved_on=RATES_READ_ON,
                source_url="https://deepmind.google/models/gemini/flash-lite/",
            )
        )
    )
