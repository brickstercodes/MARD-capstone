"""Pass 0 — skeleton extraction, deterministic part and scout part kept apart.

The Tier 1 call is injected as a `TopicLabeller` rather than constructed here, for
two reasons that are about measurement rather than testing fashion. It lets the whole
deterministic half be exercised with no keys, no spend and no network, which is what
`docs/RLM_BASELINE_SURVEY.md` recommends for pre-key work. And it means the ablation
that removes topic labelling is a different argument, not a different code path.

The prompt lives here as a module constant, versioned, because
`docs/30-MEASUREMENT_PROTOCOL.md` section 1 requires a config snapshot to record
"prompt template versions". A prompt built inline from f-strings at the call site
cannot be recorded.
"""

from __future__ import annotations

import json
import re
from typing import Any, Protocol

from envelope.skeleton import Skeleton
from ingest.sections import Section

TOPIC_PROMPT_VERSION = "pass0-topics-v1"

TOPIC_PROMPT = """\
You are the Scout. Below is the structural map of a textbook: one line per section,
with its title, page range and text density.

For each section, write one short phrase (at most 12 words) naming what a learner
would actually learn there. Do not restate the title. Do not add sections.

Return JSON only: an object mapping section_id to the phrase.

{skeleton}

Section ids, in order:
{section_ids}
"""

# A label longer than this is the model summarising the section instead of naming it,
# and every extra word is paid for on every child call that reads the skeleton.
MAX_TOPIC_WORDS = 12


class TopicLabeller(Protocol):
    """Whatever can turn a rendered skeleton into {section_id: topic}."""

    def label(self, prompt: str, section_ids: list[str]) -> dict[str, str]: ...


class NoOpTopicLabeller:
    """Leaves every topic unset — Pass 0 with the scout call switched off.

    Not a test double. This is the honest baseline for "how much of the structural
    map is free", and the skeleton it produces is still valid and still usable.
    """

    def label(self, prompt: str, section_ids: list[str]) -> dict[str, str]:
        return {}


def _clean_topic(raw: str) -> str:
    words = re.sub(r"\s+", " ", raw).strip().split(" ")
    return " ".join(words[:MAX_TOPIC_WORDS])


def build_prompt(skeleton: Skeleton) -> str:
    return TOPIC_PROMPT.format(
        skeleton=skeleton.render(),
        section_ids="\n".join(section.section_id for section in skeleton.sections),
    )


def run_pass0(
    document_id: str,
    sections: list[Section],
    labeller: TopicLabeller | None = None,
) -> tuple[Skeleton, dict[str, Any]]:
    """Produce the structural map. Returns the skeleton and a trace for the run log.

    An empty section list is not an error. It is the O4 boundary: a document with no
    exploitable structure yields an empty skeleton and MARD degenerates to vanilla RLM
    (`CONTEXT.md` line 92). The trace says so explicitly so the run log records
    degeneration as a finding rather than as a missing value.
    """
    skeleton = Skeleton.from_sections(document_id, sections)

    trace: dict[str, Any] = {
        "pass": 0,
        "prompt_version": TOPIC_PROMPT_VERSION,
        "section_count": len(skeleton.sections),
        "provenance": skeleton.provenance,
        "degenerate": skeleton.is_empty,
        "labeller": type(labeller or NoOpTopicLabeller()).__name__,
    }

    if skeleton.is_empty:
        trace["note"] = (
            "Empty skeleton: no sections detected. MARD degenerates to vanilla RLM "
            "on this document (CONTEXT.md line 92, objective O4)."
        )
        return skeleton, trace

    active = labeller or NoOpTopicLabeller()
    prompt = build_prompt(skeleton)
    raw_topics = active.label(prompt, [s.section_id for s in skeleton.sections])

    known_ids = {section.section_id for section in skeleton.sections}
    accepted = {
        section_id: _clean_topic(topic)
        for section_id, topic in raw_topics.items()
        if section_id in known_ids and topic.strip()
    }
    invented = sorted(set(raw_topics) - known_ids)

    labelled = skeleton.with_topics(accepted)

    trace.update(
        {
            "prompt_chars": len(prompt),
            "topics_requested": len(known_ids),
            "topics_accepted": len(accepted),
            "topics_invented_and_dropped": invented,
            "labelled_fraction": labelled.labelled_fraction,
            "estimated_render_tokens": labelled.estimated_render_tokens,
        }
    )
    if invented:
        # A model returning ids that are not in the map answered a different question.
        # plan/models.py forbids extra keys for the same reason; dropping them quietly
        # would hide that, so they are named in the trace.
        trace["note"] = f"Scout returned {len(invented)} unknown section ids; dropped."

    return labelled, trace


def load_trace(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        loaded: dict[str, Any] = json.load(handle)
    return loaded
