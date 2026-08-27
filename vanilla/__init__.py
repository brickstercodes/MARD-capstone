"""The vanilla-RLM control arm — Zhang_RLM's own root-REPL-loop architecture.

`docs/18-W3_PROVIDER_SWITCH.md` §4.2 (reversed 27 Aug 2026): both arms run on
`FalseAdvertising/Zhang_RLM @ 62acf7b`, vendored at `.vendor/rlm`, and the
vanilla-RLM control is Zhang's own `rlm.core.rlm.RLM`, not MARD's own pipeline
with `Envelope.stripped()`. See `run_vanilla_rlm` for the fixed configuration
(`max_depth=1`) this arm runs at.
"""

from vanilla.run import FROZEN_STUDY_GUIDE_PROMPT, run_vanilla_rlm, split_pages, zhang_rlm_fork_sha

__all__ = ["FROZEN_STUDY_GUIDE_PROMPT", "run_vanilla_rlm", "split_pages", "zhang_rlm_fork_sha"]
