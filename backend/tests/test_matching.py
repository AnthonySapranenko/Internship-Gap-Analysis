from gap_analyzer.engine import DEFAULT_CATALOG, analyze, match_requirements
from gap_analyzer.models import (
    MatchStatus,
    Proficiency,
    ProfileSkill,
    Requirement,
    RequirementLevel,
    StudentProfile,
)


def requirement(skill: str) -> Requirement:
    return Requirement(skill=skill, level=RequirementLevel.REQUIRED, evidence=skill)


def profile(*skills: ProfileSkill) -> StudentProfile:
    return StudentProfile(skills=skills)


def match_one(skill: str, student: StudentProfile):
    (match,) = match_requirements([requirement(skill)], student, DEFAULT_CATALOG).matches
    return match


def test_listed_skill_is_matched():
    match = match_one("Python", profile(ProfileSkill(name="Python")))

    assert match.status is MatchStatus.MATCHED
    assert match.explanation == "Your profile lists Python."


def test_proficiency_appears_in_explanation():
    match = match_one(
        "Python", profile(ProfileSkill(name="Python", proficiency=Proficiency.INTERMEDIATE))
    )

    assert match.explanation == "Your profile lists Python at intermediate level."


def test_profile_alias_matches_canonical_requirement():
    match = match_one("JavaScript", profile(ProfileSkill(name="js")))

    assert match.status is MatchStatus.MATCHED
    assert "listed as 'js'" in match.explanation


def test_proficiency_none_is_a_confirmed_gap():
    match = match_one("SQL", profile(ProfileSkill(name="SQL", proficiency=Proficiency.NONE)))

    assert match.status is MatchStatus.MISSING
    assert match.profile_skill.name == "SQL"


def test_skill_not_in_profile_is_unlisted():
    match = match_one("Docker", profile(ProfileSkill(name="Python")))

    assert match.status is MatchStatus.UNLISTED
    assert match.profile_skill is None
    assert "not in your profile" in match.explanation


def test_skill_outside_catalog_matches_by_name():
    match = match_one("Haskell", profile(ProfileSkill(name="haskell")))

    assert match.status is MatchStatus.MATCHED


def test_two_aliases_of_one_skill_in_profile_use_the_first():
    student = profile(
        ProfileSkill(name="JS", proficiency=Proficiency.ADVANCED),
        ProfileSkill(name="JavaScript", proficiency=Proficiency.NONE),
    )

    assert match_one("JavaScript", student).status is MatchStatus.MATCHED


def test_analyze_end_to_end():
    description = """\
Requirements:
- Python and Git
- Experience with SQL
Nice to have: REST APIs, unit testing
"""
    student = profile(
        ProfileSkill(name="python", proficiency=Proficiency.INTERMEDIATE),
        ProfileSkill(name="Git"),
        ProfileSkill(name="SQL", proficiency=Proficiency.NONE),
    )

    result = analyze(description, student)

    statuses = {m.requirement.skill: (m.requirement.level, m.status) for m in result.matches}
    assert statuses == {
        "Python": (RequirementLevel.REQUIRED, MatchStatus.MATCHED),
        "Git": (RequirementLevel.REQUIRED, MatchStatus.MATCHED),
        "SQL": (RequirementLevel.REQUIRED, MatchStatus.MISSING),
        "REST APIs": (RequirementLevel.PREFERRED, MatchStatus.UNLISTED),
        "Automated testing": (RequirementLevel.PREFERRED, MatchStatus.UNLISTED),
    }


def test_capitalization_difference_is_not_called_out():
    match = match_one("Python", profile(ProfileSkill(name="python")))

    assert match.explanation == "Your profile lists Python."
