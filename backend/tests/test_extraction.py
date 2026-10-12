from gap_analyzer.engine import DEFAULT_CATALOG, extract, extract_requirements
from gap_analyzer.models import RequirementLevel

REQUIRED = RequirementLevel.REQUIRED
PREFERRED = RequirementLevel.PREFERRED
UNSPECIFIED = RequirementLevel.UNSPECIFIED

POSTING = """\
Software Engineering Intern — Summer 2027

About the team
We build internal tools with React and TypeScript.

Responsibilities
- Write and maintain REST APIs in Python
- Participate in code reviews

Minimum Qualifications:
- Currently pursuing a degree in Computer Science
- Experience with Python or Java
- Familiarity with Git
Strong communication skills

Preferred Qualifications
- Experience with SQL and PostgreSQL
- Docker
"""


def levels(text: str) -> dict[str, RequirementLevel]:
    return {r.skill: r.level for r in extract_requirements(text, DEFAULT_CATALOG)}


def test_sections_set_requirement_levels():
    assert levels(POSTING) == {
        "React": UNSPECIFIED,
        "TypeScript": UNSPECIFIED,
        "REST APIs": UNSPECIFIED,
        "Python": REQUIRED,  # first seen under Responsibilities, upgraded by the requirements
        "Java": REQUIRED,
        "Git": REQUIRED,
        "SQL": PREFERRED,
        "PostgreSQL": PREFERRED,
        "Docker": PREFERRED,
    }


def test_preserves_first_mention_order():
    names = [r.skill for r in extract_requirements(POSTING, DEFAULT_CATALOG)]

    assert names[:4] == ["React", "TypeScript", "REST APIs", "Python"]


def test_evidence_comes_from_the_mention_that_set_the_level():
    by_skill = {r.skill: r for r in extract_requirements(POSTING, DEFAULT_CATALOG)}

    assert by_skill["Python"].evidence == "Experience with Python or Java"
    assert by_skill["Docker"].evidence == "Docker"


def test_unbulleted_line_does_not_end_section():
    text = "Requirements:\nStrong communication skills\nGit experience"

    assert levels(text) == {"Git": REQUIRED}


def test_inline_heading_with_content():
    text = "Nice to have: Docker, AWS"

    assert levels(text) == {"Docker": PREFERRED, "AWS": PREFERRED}
    assert extract_requirements(text, DEFAULT_CATALOG)[0].evidence == text


def test_colon_inside_sentence_is_not_a_heading():
    text = "Requirements\nProficiency in at least one of: Java, C++, or Python"

    assert levels(text) == {"Java": REQUIRED, "C++": REQUIRED, "Python": REQUIRED}


def test_sentence_cue_overrides_section():
    text = "Requirements\n- Python\n- Experience with AWS is a plus"

    assert levels(text) == {"Python": REQUIRED, "AWS": PREFERRED}


def test_required_cue_in_sentence_without_section():
    text = "Knowledge of SQL is required. Kubernetes experience is a bonus."

    assert levels(text) == {"SQL": REQUIRED, "Kubernetes": PREFERRED}


def test_word_requirements_inside_sentence_is_not_a_cue():
    assert levels("You will turn product requirements into React components.") == {
        "React": UNSPECIFIED
    }


def test_non_requirement_heading_resets_section():
    text = "Requirements:\n- Python\nBenefits\n- Free AWS training"

    assert levels(text) == {"Python": REQUIRED, "AWS": UNSPECIFIED}


def test_line_listing_skills_is_not_mistaken_for_heading():
    text = "Preferred qualifications\nGo, Rust"

    assert levels(text) == {"Go": PREFERRED, "Rust": PREFERRED}


def test_duplicate_mentions_produce_one_requirement():
    requirements = extract_requirements("Python. Python! More Python.", DEFAULT_CATALOG)

    assert len(requirements) == 1


def test_long_evidence_is_truncated():
    text = "We use Python " + "and many other things " * 30

    (requirement,) = extract_requirements(text, DEFAULT_CATALOG)

    assert len(requirement.evidence) <= 240
    assert requirement.evidence.endswith("…")


def test_text_without_known_skills_yields_nothing():
    assert extract_requirements("We value curiosity and teamwork.", DEFAULT_CATALOG) == []


def mentioned(text: str) -> list[tuple[str, str]]:
    _, mentions = extract(text, DEFAULT_CATALOG)
    return [(m.skill, text[m.start : m.end]) for m in mentions]


def test_mentions_point_at_the_original_text():
    text = "Requirements:\n- Python and Git\nNice to have: Postgres. Docker is a plus."

    assert mentioned(text) == [
        ("Python", "Python"),
        ("Git", "Git"),
        ("PostgreSQL", "Postgres"),
        ("Docker", "Docker"),
    ]


def test_mentions_include_repeats():
    assert mentioned("Python. More Python.") == [("Python", "Python"), ("Python", "Python")]


def test_mention_offsets_survive_windows_line_endings_and_emoji():
    text = "🚀 About us\r\n\r\n• Experience with React Native 🎉 and SQL\r\n"

    assert mentioned(text) == [("React Native", "React Native"), ("SQL", "SQL")]
