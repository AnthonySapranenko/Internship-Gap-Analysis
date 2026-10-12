"""Extract skill requirements from an internship description.

Works line by line. Section headings ("Minimum Qualifications:", "Nice to have") set the
level for the lines under them, and a cue in the same sentence ("... is a plus",
"... required") overrides the section.
"""

import re
from collections.abc import Iterator

from gap_analyzer.engine.catalog import SkillCatalog
from gap_analyzer.models import Mention, Requirement, RequirementLevel


def _words(*phrases: str) -> re.Pattern[str]:
    return re.compile(r"\b(?:" + "|".join(phrases) + r")\b", re.IGNORECASE)


# Cues that can appear anywhere, in a heading or inside a sentence.
PREFERRED_CUES = _words(
    "preferred",
    r"nice[- ]to[- ]haves?",
    "a plus",
    "pluses",
    "bonus",
    "desired",
    "desirable",
    "ideally",
)
REQUIRED_CUES = _words("required", "must")

# Words that only signal a section when they are in a heading. Inside a sentence
# ("... to meet product requirements") they say nothing about the skills mentioned.
REQUIRED_HEADINGS = _words(
    "requirements",
    "qualifications",
    "must[- ]haves?",
    r"what you(?:['’]ll)? need",
    "what you bring",
    "who you are",
    "you have",
    r"what we['’]re looking for",
    "skills",
)
OTHER_HEADINGS = _words(
    "responsibilities",
    r"what you['’]ll do",
    "about",
    "benefits",
    "perks",
    "compensation",
    "overview",
    "the role",
    "the team",
    "who we are",
    "location",
    "salary",
    "pay",
)

BULLET = re.compile(r"^\s*(?:[-*•▪◦·]|\d+[.)])\s+")
SENTENCE_END = re.compile(r"(?<=[.!?;])\s+")

MAX_HEADING_WORDS = 6  # "Preferred Qualifications", "What you'll need to succeed"
MAX_EVIDENCE_CHARS = 240
# Every character str.splitlines() treats as a line boundary.
LINE_BREAKS = "\r\n\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029"

LEVEL_STRENGTH = {
    RequirementLevel.UNSPECIFIED: 0,
    RequirementLevel.PREFERRED: 1,
    RequirementLevel.REQUIRED: 2,
}


def _sentence_level(sentence: str) -> RequirementLevel | None:
    if PREFERRED_CUES.search(sentence):
        return RequirementLevel.PREFERRED
    if REQUIRED_CUES.search(sentence):
        return RequirementLevel.REQUIRED
    return None


def _heading_level(heading: str) -> RequirementLevel | None:
    # Preferred first: "Preferred Qualifications" also contains "qualifications".
    if PREFERRED_CUES.search(heading):
        return RequirementLevel.PREFERRED
    if REQUIRED_CUES.search(heading) or REQUIRED_HEADINGS.search(heading):
        return RequirementLevel.REQUIRED
    return None


def _is_known_heading(text: str) -> bool:
    return _heading_level(text) is not None or bool(OTHER_HEADINGS.search(text))


def _split_heading(line: str, catalog: SkillCatalog) -> tuple[str | None, str]:
    """Split a line into (heading, content). The heading is None for ordinary lines."""
    if BULLET.match(line):
        return None, BULLET.sub("", line)

    # "Requirements:" or "Nice to have: Docker, AWS", but not "Proficiency in one of: Java".
    head, colon, rest = line.partition(":")
    if (
        colon
        and len(head.split()) <= MAX_HEADING_WORDS
        and (_is_known_heading(head) or not rest.strip())
        and not catalog.find_in_text(head)
    ):
        return head, rest

    short = len(line.split()) <= MAX_HEADING_WORDS and not line.rstrip().endswith((".", ","))
    if short and _is_known_heading(line) and not catalog.find_in_text(line):
        return line, ""  # "Preferred Qualifications"

    return None, line


def _evidence(sentence: str) -> str:
    sentence = " ".join(sentence.split())
    if len(sentence) > MAX_EVIDENCE_CHARS:
        sentence = sentence[: MAX_EVIDENCE_CHARS - 1].rstrip() + "…"
    return sentence


def _sentences(content: str) -> Iterator[tuple[int, str]]:
    """Split like SENTENCE_END.split, but also yield where each sentence starts."""
    start = 0
    for match in SENTENCE_END.finditer(content):
        yield start, content[start : match.start()]
        start = match.end()
    yield start, content[start:]


def extract(text: str, catalog: SkillCatalog) -> tuple[list[Requirement], list[Mention]]:
    """Return the requirements, plus every place in `text` where a skill is mentioned.

    One requirement per skill, in the order skills first appear. If a skill is mentioned
    more than once, the strongest level wins (required over preferred over unspecified),
    with the evidence from that mention. Mention offsets index into `text` as given.
    """
    section: RequirementLevel | None = None
    found: dict[str, Requirement] = {}
    mentions: list[Mention] = []

    line_start = 0
    for raw_line in text.splitlines(keepends=True):
        offset, line_start = line_start, line_start + len(raw_line)
        line = raw_line.rstrip(LINE_BREAKS)
        if not line.strip():
            continue

        heading, content = _split_heading(line, catalog)
        content_offset = offset + len(line) - len(content)  # content is a suffix of line
        # Keep an inline heading in the evidence: "Nice to have: Docker", not just "Docker".
        prefix = ""
        if heading is not None:
            section = _heading_level(heading)
            prefix = f"{heading.strip()}: "

        for sentence_offset, sentence in _sentences(content):
            level = _sentence_level(sentence) or section or RequirementLevel.UNSPECIFIED
            for start, end, skill in catalog.find_in_text(sentence):
                base = content_offset + sentence_offset
                mentions.append(Mention(skill=skill.name, start=base + start, end=base + end))

                existing = found.get(skill.name)
                if existing and LEVEL_STRENGTH[existing.level] >= LEVEL_STRENGTH[level]:
                    continue
                # Replacing a dict entry keeps its position, so first-mention order holds.
                found[skill.name] = Requirement(
                    skill=skill.name, level=level, evidence=_evidence(prefix + sentence)
                )

    return list(found.values()), mentions


def extract_requirements(text: str, catalog: SkillCatalog) -> list[Requirement]:
    return extract(text, catalog)[0]
