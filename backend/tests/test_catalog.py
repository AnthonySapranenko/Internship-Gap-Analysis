import pytest

from gap_analyzer.engine import DEFAULT_CATALOG, SkillCatalog
from gap_analyzer.models import Skill, SkillCategory


def names_in(text: str) -> list[str]:
    return [skill.name for _, skill in DEFAULT_CATALOG.find_in_text(text)]


@pytest.mark.parametrize(
    ("alias", "expected"),
    [
        ("JS", "JavaScript"),
        ("  postgres ", "PostgreSQL"),
        ("golang", "Go"),
        ("RESTful  APIs", "REST APIs"),
        ("k8s", "Kubernetes"),
    ],
)
def test_lookup_resolves_aliases(alias, expected):
    assert DEFAULT_CATALOG.lookup(alias).name == expected


def test_lookup_unknown_skill_returns_none():
    assert DEFAULT_CATALOG.lookup("Underwater basket weaving") is None


def test_finds_skills_in_reading_order():
    assert names_in("Experience with SQL, Python and Git.") == ["SQL", "Python", "Git"]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("C++ and C# experience", ["C++", "C#"]),
        ("Familiar with C/C++", ["C", "C++"]),
        ("ASP.NET or .NET Core", [".NET", ".NET"]),
        ("Node.js backend", ["Node.js"]),
        ("React.js and Vue.js", ["React", "Vue"]),
    ],
)
def test_handles_names_with_punctuation(text, expected):
    assert names_in(text) == expected


def test_longest_overlapping_mention_wins():
    assert names_in("Build apps with React Native") == ["React Native"]


@pytest.mark.parametrize(
    "text",
    [
        "Java experience",  # not JavaScript
        "We use PostgreSQL",  # not SQL
        "Scripts in TypeScript",  # not TS on its own, and not "Scripts"
    ],
)
def test_does_not_match_inside_other_words(text):
    assert len(names_in(text)) == 1


@pytest.mark.parametrize(
    "text",
    [
        "ready to go",
        "the gitignore file",
        "Go big or go home!",
        "Grade C or higher in CS101",
        "We are Series C funded",
    ],
)
def test_ignores_common_words(text):
    assert names_in(text) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Our Go microservices talk to Redis", ["Go", "Redis"]),
        ("Proficient in C or Python", ["C", "Python"]),
    ],
)
def test_ambiguous_names_count_next_to_other_skills(text, expected):
    assert names_in(text) == expected


def test_matches_multi_word_aliases_across_extra_spaces():
    assert names_in("Strong unit   testing habits") == ["Automated testing"]


def test_rejects_duplicate_skill_names():
    skill = Skill(name="Python", category=SkillCategory.LANGUAGE)

    with pytest.raises(ValueError, match="duplicate skill"):
        SkillCatalog([skill, skill])


def test_rejects_alias_shared_by_two_skills():
    with pytest.raises(ValueError, match="more than one skill"):
        SkillCatalog(
            [
                Skill(name="Java", category=SkillCategory.LANGUAGE, aliases=("J",)),
                Skill(name="Julia", category=SkillCategory.LANGUAGE, aliases=("j",)),
            ]
        )
