"""Tests for the stemmed token-set overlap scorer (docs/23-GROUNDTRUTH_SPEC.md §4)."""

from __future__ import annotations

from eval.groundtruth_scoring import DEFAULT_THRESHOLD, score_overlap, stem, token_set


def test_stem_collapses_common_inflections():
    # A bare-root form ("define") is not guaranteed to collapse to the same stem as
    # its inflections — this stemmer skips Porter's final-"e" recoding on purpose
    # (module docstring). What matters is that the inflections collide with each other.
    assert stem("defines") == stem("defining") == stem("defined")
    assert stem("algorithms") == stem("algorithm")


def test_stem_leaves_short_words_alone_to_avoid_over_stripping():
    # "as" minus "s" would be a 1-char stem; the length floor stops that.
    assert stem("as") == "as"


def test_token_set_drops_stopwords_and_short_tokens():
    tokens = token_set("Define what computer science is and is not.")
    assert "comput" in tokens  # stemmed form of "computer"
    assert "science" in tokens
    assert "is" not in tokens
    assert "what" not in tokens
    assert "and" not in tokens


def test_score_overlap_full_coverage():
    reference = "Define computer science"
    candidate = (
        "In this section we define computer science as the study of computation "
        "and its applications."
    )
    result = score_overlap(reference, candidate, threshold=DEFAULT_THRESHOLD)

    assert result.reference_tokens == 3  # "define", "computer", "science"
    assert result.matched_tokens == result.reference_tokens
    assert result.overlap == 1.0
    assert result.covered is True


def test_score_overlap_below_threshold_is_not_covered():
    reference = "Discuss the history that led to the creation of computer science"
    candidate = "This paragraph is entirely about something unrelated to that topic."

    result = score_overlap(reference, candidate, threshold=0.5)

    assert result.overlap < 0.5
    assert result.covered is False


def test_score_overlap_empty_reference_is_never_covered():
    result = score_overlap("", "any candidate text here", threshold=0.0)
    assert result.reference_tokens == 0
    assert result.covered is False


def test_score_overlap_is_case_and_order_insensitive():
    a = score_overlap("Computer Science", "science computer basics", threshold=1.0)
    b = score_overlap("computer science", "SCIENCE COMPUTER basics", threshold=1.0)
    assert a == b
    assert a.covered is True
