"""Seed control.

Three seeds on every number with variance reported is non-negotiable
(CONTEXT.md §3.4), and §1.7 challenge 3 explains why: the standing critique of
this line of work is "your improvement is noise". Seeding has to be a single
call that cannot be half-applied, or one unseeded library turns a variance
result into an anecdote.
"""

from __future__ import annotations

import os
import random
from typing import Any

# Fixed rather than arbitrary so that "seed 0/1/2" means the same thing in every
# table in both manuscripts, including runs re-executed after a machine change.
CAMPAIGN_SEEDS = (11, 23, 42)


def seed_everything(seed: int) -> dict[str, Any]:
    """Seed every RNG the pipeline can reach and report what was actually seeded.

    The return value is written into the run manifest, so a reader can tell the
    difference between "numpy was seeded" and "numpy was not installed" without
    guessing.
    """
    applied: dict[str, Any] = {"seed": seed, "python_random": True}

    random.seed(seed)
    # Hash randomisation is process-level and cannot be changed after start, so
    # record it rather than pretend to set it.
    applied["pythonhashseed_env"] = os.environ.get("PYTHONHASHSEED")

    try:
        import numpy as np
    except ImportError:
        applied["numpy"] = False
    else:
        np.random.seed(seed)
        applied["numpy"] = True

    try:
        import torch
    except ImportError:
        applied["torch"] = False
    else:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            applied["torch_cuda"] = True
        applied["torch"] = True

    return applied


def sampling_params_for(seed: int, temperature: float = 0.0) -> dict[str, Any]:
    """Provider-facing sampling settings for a seeded run.

    Seeding a local RNG does nothing to a hosted model. Passing the seed through
    to the API and pinning temperature is the only lever available, and even then
    provider determinism is best-effort — which is exactly why variance across
    seeds gets reported rather than assumed away.
    """
    return {"seed": seed, "temperature": temperature}
