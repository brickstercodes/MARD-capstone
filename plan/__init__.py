"""The Master Plan contract between Tier 1 and Tier 2. Owned by Track 2.

Its own package rather than part of `orchestrate/` because the schema is a
contract that Track 1 writes to and Track 3 scores against. A malformed plan
must fail loudly at this boundary — the alternative is N builders producing
subtly wrong sections that nobody notices until the results are in.
"""

from pathlib import Path

from plan.models import (
    SCHEMA_VERSION,
    Concept,
    ConceptEdge,
    ConceptGraph,
    ConceptId,
    EdgeEvidence,
    MasterPlan,
    ReorderNote,
    SourceSpan,
    StudyStep,
)
from plan.validation import (
    MasterPlanError,
    PlanViolation,
    check_master_plan,
    load_master_plan,
    parse_master_plan,
    validate_master_plan,
)

EXAMPLE_PLAN_PATH = Path(__file__).parent / "EXAMPLE_PLAN.json"
"""A hand-written plan that satisfies every boundary rule.

The worked example of the contract: Track 1 writes toward it, Track 3 scores
against its shape, and Tier 2 can be exercised end-to-end without a model. The
document it describes is illustrative — which document is primary is Track 4's
call, not this fixture's.
"""

__all__ = [
    "EXAMPLE_PLAN_PATH",
    "SCHEMA_VERSION",
    "Concept",
    "ConceptEdge",
    "ConceptGraph",
    "ConceptId",
    "EdgeEvidence",
    "MasterPlan",
    "MasterPlanError",
    "PlanViolation",
    "ReorderNote",
    "SourceSpan",
    "StudyStep",
    "check_master_plan",
    "load_master_plan",
    "parse_master_plan",
    "validate_master_plan",
]
