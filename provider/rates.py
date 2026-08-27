"""The one place `gpt-5.2` / `gpt-5-mini` prices are written down.

Read live from OpenAI's own pricing page — `developers.openai.com/api/docs/pricing`
(the `openai.com/api/pricing/` and `platform.openai.com/docs/pricing` URLs both
redirect there) — on 27 Aug 2026, the day this module was written. Per
`runlog.pricing.RateCard`'s own discipline (CLAUDE.md's measurement-discipline
section; `docs/18` §5.5/§4.2 addendum), this is the *only* place these numbers should
be typed in: neither the vanilla arm's `Zhang_RLM` nor any per-model cost field on it
is ever fed a price (docs/18 §5.5's "two prices, one goes stale" trap) — cost is
computed once, centrally, from `RunLogger.totals()` calling into the `RateCard` this
module builds.

Re-read the page and update `RETRIEVED_ON` before 26 Sep 2026 — `RateCard.cost_for`
raises `StaleRateError` past the 30-day mark rather than let a stale number ride.
"""

from __future__ import annotations

from datetime import date

from runlog.pricing import ModelRate, RateCard

SOURCE_URL = "https://developers.openai.com/api/docs/pricing"
RETRIEVED_ON = date(2026, 8, 27)

TIER1_MODEL = "gpt-5.2"
TIER2_MODEL = "gpt-5-mini"


def build_rate_card() -> RateCard:
    """`gpt-5.2` (Tier 1 / root) and `gpt-5-mini` (Tier 2 / sub-calls), per docs/18 §7
    item 1's resolution. Cached-input rates ($0.175/1M and $0.025/1M respectively)
    are on the same page but are not wired here: nothing in the pipeline currently
    tracks a cached-vs-uncached token split (`CompletionResult` reports only
    `input_tokens`/`output_tokens`), so recording a cached rate nothing reads from
    would be exactly the kind of unused, silently-stale figure `docs/18` §5.5 warns
    about.
    """
    card = RateCard.empty()
    card = card.with_rate(
        ModelRate(
            model=TIER1_MODEL,
            input_per_million=1.75,
            output_per_million=14.00,
            currency="USD",
            retrieved_on=RETRIEVED_ON,
            source_url=SOURCE_URL,
        )
    )
    card = card.with_rate(
        ModelRate(
            model=TIER2_MODEL,
            input_per_million=0.25,
            output_per_million=2.00,
            currency="USD",
            retrieved_on=RETRIEVED_ON,
            source_url=SOURCE_URL,
        )
    )
    return card
