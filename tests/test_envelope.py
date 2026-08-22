"""Tests for the envelope, Pass 0, and skeleton fidelity.

The first test in this file is the most important one in the repository. If
`for_child` ever stops carrying the parent's findings, MARD has silently become
vanilla RLM, every O3 number measures nothing, and no other test would notice —
the pipeline would still run and still produce plausible output. See
`docs/01-ENVELOPE_VS_BASE_LIBRARY.md`.
"""

from __future__ import annotations

from envelope.envelope import Envelope, Finding
from envelope.fidelity import score_fidelity
from envelope.pass0 import run_pass0
from envelope.skeleton import Skeleton
from ingest.blocks import Block
from ingest.sections import build_sections, choose_section_level


def _section(index: int, title: str, page_start: int, page_end: int):
    from ingest.sections import Section

    return Section(
        section_id=f"doc.{title.lower().replace(' ', '-')}",
        title=title,
        book_position=index,
        page_start=page_start,
        page_end=page_end,
        char_count=1000 * (page_end - page_start + 1),
        block_ids=(f"doc:p{page_start:04d}:b000",),
    )


def _skeleton(*sections) -> Skeleton:
    return Skeleton.from_sections("doc", list(sections))


def _blocks(headings: list[tuple[int, int, str]], pages: int) -> list[Block]:
    """headings: (page, level, text). Plus one body block per page."""
    blocks = []
    for page, level, text in headings:
        blocks.append(
            Block(
                block_id=f"doc:p{page:04d}:h",
                page=page,
                kind="heading",
                level=level,
                role=None,
                text=text,
                bbox=(72.0, 100.0, 400.0, 120.0),
                font_size=14.0,
            )
        )
    for page in range(1, pages + 1):
        blocks.append(
            Block(
                block_id=f"doc:p{page:04d}:b",
                page=page,
                kind="body",
                level=None,
                role=None,
                text="prose " * 50,
                bbox=(72.0, 200.0, 400.0, 600.0),
                font_size=9.0,
            )
        )
    return sorted(blocks, key=lambda b: (b.page, b.kind != "heading"))


# --- the invariant that carries the whole contribution ----------------------------


def test_child_envelope_carries_parent_findings():
    """MARD's defining behaviour: findings flow DOWN into a child call.

    The base RLM library gives a child a fresh empty logger and root_prompt=None
    (.vendor/rlm/rlm/core/rlm.py:824). If this test fails, MARD is vanilla RLM.
    """
    parent = Envelope.from_skeleton(_skeleton(_section(0, "Intro", 1, 10))).with_findings(
        Finding(section_id="doc.intro", pass_index=1, concepts=("paging",)),
        Finding(section_id="doc.intro", pass_index=1, prerequisites=(("paging", "tlb"),)),
    )

    child = parent.for_child("doc.intro", "Extract prerequisites.")

    assert len(child.findings) == 2
    assert child.skeleton.sections == parent.skeleton.sections
    assert child.directive == "Extract prerequisites."
    assert "paging -> tlb" in child.render()


def test_growth_does_not_mutate_the_parent():
    parent = Envelope.from_skeleton(_skeleton(_section(0, "Intro", 1, 10)))
    grown = parent.with_findings(Finding(section_id="doc.intro", pass_index=1))

    assert parent.findings == ()
    assert len(grown.findings) == 1


def test_stripped_envelope_is_the_a1_ablation():
    """A1 removes the envelope and nothing else — same target section, no structure."""
    full = Envelope.from_skeleton(_skeleton(_section(0, "Intro", 1, 10))).for_child(
        "doc.intro", "Do the thing."
    )

    stripped = full.stripped()

    assert stripped.is_stripped
    assert stripped.render() == ""
    assert stripped.target_section_id == full.target_section_id
    assert stripped.document_id == full.document_id


def test_directive_is_rendered_last():
    envelope = Envelope.from_skeleton(_skeleton(_section(0, "Intro", 1, 10))).for_child(
        "doc.intro", "THE INSTRUCTION"
    )
    rendered = envelope.render()
    assert rendered.index("STRUCTURAL MAP") < rendered.index("YOUR DIRECTIVE")
    assert rendered.rstrip().endswith("THE INSTRUCTION")


def test_finding_window_truncates_and_admits_it():
    envelope = Envelope.from_skeleton(_skeleton(_section(0, "Intro", 1, 10)))
    for index in range(20):
        envelope = envelope.with_findings(
            Finding(section_id="doc.intro", pass_index=1, note=f"note-{index}")
        )

    rendered = envelope.render()
    assert "most recent 12 of 20" in rendered
    assert "note-19" in rendered
    assert "note-0" not in rendered


# --- Pass 0 -----------------------------------------------------------------------


def test_pass0_reports_degeneration_on_an_unstructured_document():
    """The O4 boundary, made checkable: no sections means MARD becomes vanilla RLM."""
    skeleton, trace = run_pass0("flat", [])

    assert skeleton.is_empty
    assert trace["degenerate"] is True
    assert "degenerates to vanilla RLM" in trace["note"]


def test_pass0_drops_section_ids_the_scout_invented():
    sections = [_section(0, "Intro", 1, 10), _section(1, "Middle", 11, 20)]

    class Hallucinating:
        def label(self, prompt, section_ids):
            return {section_ids[0]: "real topic", "doc.not-a-section": "invented"}

    skeleton, trace = run_pass0("doc", sections, Hallucinating())

    assert trace["topics_accepted"] == 1
    assert trace["topics_invented_and_dropped"] == ["doc.not-a-section"]
    assert skeleton.sections[0].topic == "real topic"
    assert skeleton.sections[1].topic is None


def test_pass0_truncates_an_overlong_topic():
    class Verbose:
        def label(self, prompt, section_ids):
            return {section_ids[0]: " ".join(f"word{i}" for i in range(40))}

    skeleton, _trace = run_pass0("doc", [_section(0, "Intro", 1, 10)], Verbose())

    topic = skeleton.sections[0].topic
    assert topic is not None
    assert len(topic.split()) == 12


# --- sections ---------------------------------------------------------------------


def test_source_span_carries_exactly_the_contract_fields():
    """plan.models.SourceSpan forbids extra keys, so this shape has to be exact."""
    span = _section(3, "Paging", 40, 55).to_source_span()
    assert set(span) == {"section_id", "book_position", "page_start", "page_end"}
    assert span["book_position"] == 3
    assert span["page_start"] == 40


def test_section_level_is_chosen_by_resulting_section_length():
    """Regression: a fixed level-1 rule gave University Physics 9 sections of 106 pages.

    Here level 1 would give two 50-page sections and level 2 gives twenty 5-page ones,
    so the chooser must reach past level 1.
    """
    headings = [(1, 1, "Part One"), (51, 1, "Part Two")]
    headings += [(page, 2, f"Section {page}") for page in range(1, 100, 5)]

    assert choose_section_level(_blocks(headings, 100)) == 2


def test_density_is_characters_per_page():
    section = _section(0, "Intro", 10, 19)
    assert section.page_count == 10
    assert section.density == 1000.0


def test_boilerplate_and_front_matter_do_not_extend_a_section_span():
    blocks = _blocks([(5, 1, "Real Section")], 10)
    blocks.append(
        Block(
            block_id="doc:p0009:f",
            page=9,
            kind="front_matter",
            level=None,
            role=None,
            text="contents listing",
            bbox=(72.0, 700.0, 400.0, 720.0),
            font_size=9.0,
        )
    )
    sections = build_sections(blocks, "doc", level=1)

    assert len(sections) == 1
    assert sections[0].page_end == 10  # the front-matter block on p9 did not set it


# --- fidelity ---------------------------------------------------------------------


def test_fidelity_scores_recall_and_boundary_error():
    skeleton = _skeleton(
        _section(0, "Vector Spaces", 5, 20),
        _section(1, "Linear Maps", 21, 40),
        _section(2, "A Heading The Publisher Omitted", 41, 45),
    )
    outline = [
        {"level": 1, "title": "Chapter 1 Vector Spaces", "start_page": 5},
        {"level": 1, "title": "Chapter 2 Linear Maps", "start_page": 22},
        {"level": 1, "title": "Chapter 3 Never Detected", "start_page": 60},
        {"level": 3, "title": "Too deep to count", "start_page": 7},
    ]

    report = score_fidelity(skeleton, outline)

    assert report.outline_entries == 3  # the level-3 entry is out of scope
    assert report.matched == 2
    assert report.recall == round(2 / 3, 3)
    assert report.unmatched_outline_titles == ("Chapter 3 Never Detected",)
    assert report.spurious == 1
    assert report.mean_start_page_error == 0.5  # 0 pages and 1 page
