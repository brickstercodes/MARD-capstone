"""Tests for the project's RateCard.

The failure mode that matters here is not "the math is wrong" -- it's "the
rate quietly drifted from what the provider's page actually says today".
These tests pin the two model rates to the values eval.rates documents
reading on 22 Aug 2026, so a future edit that changes a number without
updating the docstring's justification breaks the suite instead of shipping
silently.
"""

from __future__ import annotations

from datetime import date

from eval.rates import TIER1_MODEL, TIER2_MODEL, default_rate_card


def test_tier1_rate_is_the_introductory_price_not_docs12s_figure():
    card = default_rate_card()
    rate = card.rates[TIER1_MODEL]
    # docs/12-MODEL_PAIR.md records $1.50/$7.50 -- that is gemini-3.6-flash's
    # post-introductory rate, effective 1 Jan 2027, after this project ends.
    assert rate.input_per_million == 0.75
    assert rate.output_per_million == 3.75


def test_tier2_rate_matches_docs12_with_no_discrepancy():
    card = default_rate_card()
    rate = card.rates[TIER2_MODEL]
    assert rate.input_per_million == 0.25
    assert rate.output_per_million == 1.50


def test_both_rates_carry_provider_source_and_a_read_date():
    card = default_rate_card()
    for rate in card.rates.values():
        assert rate.source_url.startswith("https://deepmind.google/")
        assert rate.retrieved_on == date(2026, 8, 22)


def test_cost_for_computes_against_the_recorded_rate():
    card = default_rate_card()
    # 1000 in + 1000 out at $0.75/$3.75 per 1M = 0.00075 + 0.00375
    cost = card.cost_for(TIER1_MODEL, input_tokens=1000, output_tokens=1000)
    assert cost == 0.0045
