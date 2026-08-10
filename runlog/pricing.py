"""Token cost accounting, with provenance attached to every rate.

CONTEXT.md §4.3 rule 4 exists because third-party pricing aggregators disagreed
by up to 2x for the same model while this project was being prepared, and §2.3
records that a "15-25x cost reduction" claim died with the budget rate it rested
on. So the design decision here is deliberate: a rate cannot be used unless it
carries the date it was read and the URL it was read from, and rates go stale on
purpose rather than silently ageing into the paper.

The cost model is the contribution (O6); the cost number is a measurement. This
module keeps them separable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

# A rate older than this is refused rather than warned about. Frontier and budget
# tier pricing moved month to month through 2026, and a stale rate produces a
# number that looks fine and is wrong — the worst failure mode for this project.
MAX_RATE_AGE = timedelta(days=30)

TOKENS_PER_MILLION = 1_000_000


class StaleRateError(RuntimeError):
    """Raised when a rate is too old to be quoted in a result."""


@dataclass(frozen=True)
class ModelRate:
    """Published price for one model, with the provenance that makes it citable."""

    model: str
    input_per_million: float
    output_per_million: float
    currency: str
    retrieved_on: date
    source_url: str
    """Must be the provider's own pricing page. Aggregators are not sources."""

    def cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * self.input_per_million + output_tokens * self.output_per_million
        ) / TOKENS_PER_MILLION

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "input_per_million": self.input_per_million,
            "output_per_million": self.output_per_million,
            "currency": self.currency,
            "retrieved_on": self.retrieved_on.isoformat(),
            "source_url": self.source_url,
        }


@dataclass(frozen=True)
class RateCard:
    """The set of rates in force for a measurement campaign.

    Deliberately empty by default. Filling it is Track 3's job on the day the
    numbers are taken, from official provider pricing pages (§4.3 item 7 of the
    live verification debt).
    """

    rates: dict[str, ModelRate]

    @classmethod
    def empty(cls) -> RateCard:
        return cls(rates={})

    def with_rate(self, rate: ModelRate) -> RateCard:
        return RateCard(rates={**self.rates, rate.model: rate})

    def cost_for(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        *,
        as_of: date | None = None,
    ) -> float | None:
        """Cost in the rate's currency, or None when no rate has been recorded.

        Returning None rather than 0.0 is the point: an unpriced run must show up
        as unpriced in the summary, not as free.
        """
        rate = self.rates.get(model)
        if rate is None:
            return None
        today = as_of or date.today()
        if today - rate.retrieved_on > MAX_RATE_AGE:
            raise StaleRateError(
                f"Rate for {model!r} was retrieved on {rate.retrieved_on.isoformat()}, "
                f"more than {MAX_RATE_AGE.days} days before {today.isoformat()}. "
                f"Re-read {rate.source_url} and update the rate card before quoting cost."
            )
        return rate.cost(input_tokens, output_tokens)

    def to_dict(self) -> dict[str, Any]:
        return {model: rate.to_dict() for model, rate in self.rates.items()}
