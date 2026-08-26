"""Tests for the backend switch.

Two things here are worth a test rather than a careful reading.

The first is that OpenAI is the default. The pivot's whole safety property is
that nothing reaches Vertex unless someone asks for it on purpose, and that
property lives in one `os.environ.get` default -- easy to invert in a hurry
and invisible until a bill arrives.

The second is that `temperature` is dropped for OpenAI. It is dropped because
GPT-5-family reasoning models reject it with a hard 400, so getting this wrong
does not degrade a run, it kills every call in a campaign at the first request.
"""

from __future__ import annotations

import dataclasses

import pytest

from eval.backends import BACKEND_ENV, GEMINI_VERTEX, OPENAI, active_profile


def test_openai_is_the_default_backend(monkeypatch):
    monkeypatch.delenv(BACKEND_ENV, raising=False)
    assert active_profile() is OPENAI


def test_vertex_requires_asking_for_it(monkeypatch):
    monkeypatch.setenv(BACKEND_ENV, "gemini")
    assert active_profile() is GEMINI_VERTEX


def test_unknown_backend_fails_loudly(monkeypatch):
    monkeypatch.setenv(BACKEND_ENV, "bedrock")
    with pytest.raises(ValueError, match="not a known backend"):
        active_profile()


def test_openai_sampling_drops_temperature_and_pins_reasoning_effort():
    params = OPENAI.sampling_params(seed=11)
    assert "temperature" not in params
    assert params["seed"] == 11
    assert params["reasoning_effort"] == "medium"


def test_gemini_sampling_keeps_temperature_and_adds_nothing():
    params = GEMINI_VERTEX.sampling_params(seed=11)
    assert params == {"seed": 11, "temperature": 0.0}


def test_backend_kwargs_carry_provider_specific_arguments():
    assert OPENAI.backend_kwargs() == {"model_name": "gpt-5.6-terra"}
    assert GEMINI_VERTEX.backend_kwargs() == {
        "model_name": "gemini-3.6-flash",
        "use_vertex": True,
    }
    assert OPENAI.backend_kwargs("gpt-5.6-luna")["model_name"] == "gpt-5.6-luna"


def test_each_backend_gets_its_own_ledger():
    """Vertex spend is redeemable credit against a INR75,000 cap; OpenAI spend
    is cash against a different one. One ledger holding both would produce a
    total that means nothing and a cap that guards nothing."""
    assert OPENAI.runs_root == "runs-openai"
    assert GEMINI_VERTEX.runs_root == "runs"
    assert OPENAI.runs_root != GEMINI_VERTEX.runs_root


def test_profiles_are_frozen():
    """A profile mutated at runtime would desync the rate card from the run."""
    with pytest.raises(dataclasses.FrozenInstanceError):
        OPENAI.tier1_model = "gpt-5.6-sol"  # type: ignore[misc]
