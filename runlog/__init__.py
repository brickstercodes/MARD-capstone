"""Run logging and reproducibility for the MARD capstone.

Owned by Track 2, consumed by all four tracks. It exists as a top-level package
rather than living inside `orchestrate/` because Track 1's envelope work, Track
3's measurement and Track 4's ground-truth extraction all need to log runs, and
none of them should have to import the orchestrator to do it.
"""

from runlog.budget import (
    BudgetExceededError,
    SpendCap,
    SpendLedger,
    UnsetSpendCapError,
)
from runlog.config import ConfigSnapshot
from runlog.pricing import ModelRate, RateCard, StaleRateError
from runlog.run import RunLogger, load_run
from runlog.seeds import CAMPAIGN_SEEDS, sampling_params_for, seed_everything

__all__ = [
    "CAMPAIGN_SEEDS",
    "BudgetExceededError",
    "ConfigSnapshot",
    "ModelRate",
    "RateCard",
    "RunLogger",
    "SpendCap",
    "SpendLedger",
    "StaleRateError",
    "UnsetSpendCapError",
    "load_run",
    "sampling_params_for",
    "seed_everything",
]
