"""The whole point of `provider/sync_seams.py`: prove the adapters return concrete
values, not coroutines, and that `run_pass0`/`run_pass1` accept them cleanly.

Without this module, handing `OpenAITopicLabeller`/`OpenAIChapterExplorer` (both
`async def`) straight to `run_pass0`/`run_pass1` (both synchronous call sites)
produces an unawaited coroutine that `run_pass1`'s `isinstance(raw, dict)` check
silently rejects for every chapter — zero concepts, no exception (`docs/25` §2).
These tests are the guard against that regressing.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass

from envelope.envelope import Envelope
from envelope.pass0 import run_pass0
from envelope.pass1 import run_pass1
from envelope.skeleton import Skeleton
from ingest.chapters import Chapter
from ingest.sections import Section
from provider.seams import OpenAIChapterExplorer, OpenAITopicLabeller
from provider.sync_seams import SyncChapterExplorer, SyncTopicLabeller
from provider.throttle import Throttle


@dataclass
class _FakeMessage:
    content: str


@dataclass
class _FakeChoice:
    message: _FakeMessage


@dataclass
class _FakeUsage:
    prompt_tokens: int
    completion_tokens: int


@dataclass
class _FakeResponse:
    choices: list[_FakeChoice]
    usage: _FakeUsage


class _FakeCompletions:
    def __init__(self, content: str) -> None:
        self._content = content

    async def create(self, **kwargs: object) -> _FakeResponse:
        return _FakeResponse(
            choices=[_FakeChoice(message=_FakeMessage(content=self._content))],
            usage=_FakeUsage(prompt_tokens=10, completion_tokens=5),
        )


class _FakeChat:
    def __init__(self, content: str) -> None:
        self.completions = _FakeCompletions(content)


class _FakeRawClient:
    """A stand-in for `openai.AsyncOpenAI` that never touches the network."""

    def __init__(self, content: str) -> None:
        self.chat = _FakeChat(content)


def _client(content: str):
    from provider.openai_client import ThrottledAsyncOpenAI

    return ThrottledAsyncOpenAI(Throttle(), raw_client=_FakeRawClient(content))  # type: ignore[arg-type]


def _chapter() -> Chapter:
    return Chapter(
        chapter_id="doc.ch01",
        number=1,
        title="Chapter 1",
        book_position=0,
        page_start=1,
        page_end=10,
        char_count=1000,
        section_ids=("doc.sec-a", "doc.sec-b"),
    )


def _sections() -> list[Section]:
    return [
        Section(
            section_id="doc.sec-a",
            title="1.1 Section A",
            book_position=0,
            page_start=1,
            page_end=5,
            char_count=500,
            block_ids=("b1",),
        ),
        Section(
            section_id="doc.sec-b",
            title="1.2 Section B",
            book_position=1,
            page_start=6,
            page_end=10,
            char_count=500,
            block_ids=("b2",),
        ),
    ]


def test_sync_topic_labeller_returns_a_dict_not_a_coroutine():
    labeller = SyncTopicLabeller(
        inner=OpenAITopicLabeller(client=_client('{"doc.sec-a": "topic a"}'), model="gpt-5.2")
    )
    result = labeller.label("prompt", ["doc.sec-a"])

    assert not inspect.iscoroutine(result)
    assert isinstance(result, dict)
    assert result == {"doc.sec-a": "topic a"}


def test_sync_chapter_explorer_returns_a_dict_not_a_coroutine():
    explorer = SyncChapterExplorer(
        inner=OpenAIChapterExplorer(
            client=_client('{"concepts": [], "prerequisites": []}'), model="gpt-5.2"
        )
    )
    result = explorer.explore("prompt", _chapter())

    assert not inspect.iscoroutine(result)
    assert isinstance(result, dict)
    assert result == {"concepts": [], "prerequisites": []}


def test_run_pass0_accepts_the_sync_labeller_with_no_coroutine_rejection():
    sections = _sections()
    labeller = SyncTopicLabeller(
        inner=OpenAITopicLabeller(
            client=_client('{"doc.sec-a": "topic a", "doc.sec-b": "topic b"}'),
            model="gpt-5.2",
        )
    )
    skeleton, trace = run_pass0("doc", sections, labeller=labeller)

    assert trace["topics_accepted"] == 2
    assert skeleton.labelled_fraction == 1.0


def test_run_pass1_accepts_the_sync_explorer_with_no_coroutine_rejection():
    sections = _sections()
    chapter = _chapter()
    section_titles = {s.section_id: s.title for s in sections}
    skeleton = Skeleton.from_sections("doc", sections)
    envelope = Envelope.from_skeleton(skeleton)

    concept_json = (
        '{"concepts": [{"id": "doc.ch01.c1", "section_id": "doc.sec-a", '
        '"label": "Concept One", "directive": "Explain concept one in full detail."}], '
        '"prerequisites": []}'
    )
    explorer = SyncChapterExplorer(
        inner=OpenAIChapterExplorer(client=_client(concept_json), model="gpt-5.2")
    )

    result = run_pass1(envelope, [chapter], section_titles, explorer=explorer)

    assert len(result.concepts) == 1
    assert result.traces[0]["rejected"] == []
    for trace in result.traces:
        assert "explorer returned" not in "".join(trace["rejected"])
