"""Stemmed token-set overlap scorer for document-native ground truth.

docs/23-GROUNDTRUTH_SPEC.md §4: matching a learning objective ("Define computer
science") against a generated explanation needs a decision, because the objective
will not appear verbatim. Stemmed token-set overlap against a stated threshold is
the option recommended there — cheap, deterministic, and re-runnable by a reviewer
with no API key, unlike embedding similarity, which would put a second model inside
the measurement (the same hazard docs/23 §1 rejects for concept/prerequisite ground
truth, in more respectable clothing).

`DEFAULT_THRESHOLD` is a placeholder pending Track 3 sign-off — §4 explicitly marks
the scoring-function choice as Track 3's decision, not Track 1's. Whatever threshold
is used, report `ScoreResult.matched_tokens` / `reference_tokens` alongside it, so
the reported number survives a reviewer who disagrees with the threshold.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

DEFAULT_THRESHOLD = 0.6
"""Recall threshold. Placeholder, not signed off — see module docstring."""

_WORD_PATTERN = re.compile(r"[a-z]+")

_MIN_TOKEN_CHARS = 3

_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "as",
        "at",
        "be",
        "by",
        "can",
        "for",
        "from",
        "has",
        "have",
        "in",
        "into",
        "is",
        "it",
        "its",
        "of",
        "on",
        "or",
        "over",
        "such",
        "than",
        "that",
        "the",
        "their",
        "this",
        "to",
        "was",
        "well",
        "were",
        "what",
        "which",
        "will",
        "with",
        "you",
        "your",
    }
)

# Longest suffix first: `_SUFFIXES` is scanned in order and the first match wins,
# so a longer suffix must precede any shorter suffix it contains (e.g. "ing" before
# "s" would be irrelevant here, but "ational" must still precede "s").
_SUFFIXES = (
    "ational",
    "ization",
    "fulness",
    "ousness",
    "iveness",
    "edly",
    "ally",
    "ized",
    "ised",
    "ing",
    "ment",
    "ness",
    "ies",
    "ied",
    "ion",
    "ers",
    "er",
    "ed",
    "es",
    "ly",
    "s",
)


def stem(word: str) -> str:
    """Strip the first matching suffix. A lightweight approximation, not Porter's.

    Collides inflections of the same word with each other ("defines"/"defining"/
    "defined" all -> "defin") well enough for a coverage check on this project's
    vocabulary. It is not a general-purpose NLP component: unlike Porter's algorithm
    it has no final-"e" recoding step, so a bare root ("define") is not guaranteed
    to collide with its own inflections.
    """
    for suffix in _SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= _MIN_TOKEN_CHARS:
            return word[: -len(suffix)]
    return word


def token_set(text: str) -> set[str]:
    words = _WORD_PATTERN.findall(text.lower())
    return {
        stem(word) for word in words if word not in _STOPWORDS and len(word) >= _MIN_TOKEN_CHARS
    }


@dataclass(frozen=True)
class ScoreResult:
    reference_tokens: int
    matched_tokens: int
    overlap: float
    threshold: float
    covered: bool


def score_overlap(
    reference_text: str,
    candidate_text: str,
    *,
    threshold: float = DEFAULT_THRESHOLD,
) -> ScoreResult:
    """Recall of `reference_text`'s stemmed tokens inside `candidate_text`.

    Recall against the (short) reference, not Jaccard or precision against the
    (long) candidate: a generated explanation covering one objective is expected to
    contain far more tokens than the objective statement itself, so precision would
    punish thoroughness rather than measure coverage.
    """
    reference_tokens = token_set(reference_text)
    if not reference_tokens:
        return ScoreResult(0, 0, 0.0, threshold, False)

    candidate_tokens = token_set(candidate_text)
    matched = reference_tokens & candidate_tokens
    overlap = len(matched) / len(reference_tokens)
    return ScoreResult(
        len(reference_tokens), len(matched), overlap, threshold, overlap >= threshold
    )
