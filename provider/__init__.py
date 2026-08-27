"""OpenAI provider infrastructure for MARD's own Tier 1/2 calls.

`replm` had no concurrency cap at all (docs/18 §4.2, historical). This package was
built as "what `alexzhang13/rlm` gets for free" for that reason, and that reasoning
now applies to `Zhang_RLM` too — but `Zhang_RLM` has no client-injection seam
(`docs/18` §4.2 addendum, `vanilla/run.py`), so `ThrottledAsyncOpenAI` and `Throttle`
now serve **only MARD's own Tier 1/2 calls** (via `provider/seams.py`), not the
vanilla arm. The vanilla arm relies on `Zhang_RLM`'s own `max_concurrent_subcalls`
for concurrency and `vanilla/openai_logging_bridge.py` for 429/retry visibility.
"""

from provider.openai_client import ThrottledAsyncOpenAI
from provider.rates import build_rate_card
from provider.reasoning import completion_kwargs, is_reasoning_model
from provider.seams import OpenAIChapterExplorer, OpenAILanguageModel, OpenAITopicLabeller
from provider.throttle import RetryExhaustedError, Throttle, ThrottleConfig

__all__ = [
    "ThrottledAsyncOpenAI",
    "Throttle",
    "ThrottleConfig",
    "RetryExhaustedError",
    "is_reasoning_model",
    "completion_kwargs",
    "build_rate_card",
    "OpenAITopicLabeller",
    "OpenAIChapterExplorer",
    "OpenAILanguageModel",
]
