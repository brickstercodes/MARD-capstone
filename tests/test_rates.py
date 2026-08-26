"""Tests for the project's RateCards.

The failure mode that matters here is not "the math is wrong" -- it's "the
rate quietly drifted from what the provider's page actually says today".
These tests pin each model rate to the value eval.rates documents reading, so
a future edit that changes a number without updating the docstring's
justification breaks the suite instead of shipping silently.

Both cards are covered, not just the active one. The Gemini card is what
re-prices the 122 Vertex runs already on disk; if it drifts, historical
figures in docs/16 stop reconciling and nothing would otherwise notice.
"""

from __future__ import annotations

from datetime import date

import pytest

from eval.rates import (
    GEMINI_TIER1_MODEL,
    GEMINI_TIER2_MODEL,
    TIER1_MODEL,
    TIER2_MODEL,
    default_rate_card,
    gemini_rate_card,
    rate_card_for,
)


def test_tier1_rate_is_openais_own_page_not_the_launch_coverage():
    card = default_rate_card()
    rate = card.rates[TIER1_MODEL]
    # Launch coverage from 9 Jul 2026 quotes $2.50/$15.00 for terra -- 2.5x
    # these figures. The provider's own page wins (CONTEXT.md §4.3 rule 4).
    assert rate.input_per_million == 1.00
    assert rate.output_per_million == 6.00


def test_tier2_rate_matches_the_same_reading():
    card = default_rate_card()
    rate = card.rates[TIER2_MODEL]
    assert rate.input_per_million == 0.10
    assert rate.output_per_million == 0.60


def test_openai_rates_carry_provider_source_and_a_read_date():
    card = default_rate_card()
    for rate in card.rates.values():
        assert rate.source_url.startswith("https://developers.openai.com/")
        assert rate.retrieved_on == date(2026, 8, 25)


def test_gemini_card_still_prices_the_historical_runs():
    card = gemini_rate_card()
    tier1 = card.rates[GEMINI_TIER1_MODEL]
    tier2 = card.rates[GEMINI_TIER2_MODEL]
    # The introductory rate the existing runs were actually billed at, not
    # docs/12's $1.50/$7.50 post-introductory figure.
    assert (tier1.input_per_million, tier1.output_per_million) == (0.75, 3.75)
    assert (tier2.input_per_million, tier2.output_per_million) == (0.25, 1.50)
    for rate in card.rates.values():
        assert rate.source_url.startswith("https://deepmind.google/")
        assert rate.retrieved_on == date(2026, 8, 22)


def test_cost_for_computes_against_the_recorded_rate():
    card = default_rate_card()
    # 1000 in + 1000 out at $1.00/$6.00 per 1M = 0.001 + 0.006
    cost = card.cost_for(TIER1_MODEL, input_tokens=1000, output_tokens=1000)
    assert cost == pytest.approx(0.007)


def test_the_two_cards_do_not_price_each_others_models():
    """The whole point of rate_card_for: a run can't be priced off the wrong
    provider. An OpenAI model must be unpriced (None) on the Gemini card
    rather than silently borrowing a Gemini rate."""
    assert gemini_rate_card().cost_for(TIER1_MODEL, 1000, 1000) is None
    assert default_rate_card().cost_for(GEMINI_TIER1_MODEL, 1000, 1000) is None


def test_rate_card_for_dispatches_and_refuses_the_unknown():
    assert rate_card_for("openai").rates.keys() == {TIER1_MODEL, TIER2_MODEL}
    assert rate_card_for("gemini").rates.keys() == {GEMINI_TIER1_MODEL, GEMINI_TIER2_MODEL}
    with pytest.raises(ValueError, match="No rate card"):
        rate_card_for("anthropic")
