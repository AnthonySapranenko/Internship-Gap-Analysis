import pytest
from pydantic import ValidationError

from gap_analyzer.models import (
    AnalysisResult,
    InternshipDescription,
    MatchStatus,
    Proficiency,
    ProfileSkill,
    Requirement,
    RequirementLevel,
    RequirementMatch,
    Skill,
    SkillCategory,
    StudentProfile,
)


def make_requirement(skill: str = "Python") -> Requirement:
    return Requirement(
        skill=skill,
        level=RequirementLevel.REQUIRED,
        evidence=f"Experience with {skill}",
    )


def test_skill_accepts_aliases():
    skill = Skill(name="JavaScript", category=SkillCategory.LANGUAGE, aliases=("JS",))

    assert skill.aliases == ("JS",)


def test_strings_are_stripped():
    skill = ProfileSkill(name="  Python  ")

    assert skill.name == "Python"


@pytest.mark.parametrize("name", ["", "   "])
def test_profile_skill_rejects_blank_name(name):
    with pytest.raises(ValidationError):
        ProfileSkill(name=name)


def test_profile_skill_proficiency_is_optional():
    assert ProfileSkill(name="Git").proficiency is None


def test_profile_parses_from_json_values():
    profile = StudentProfile.model_validate(
        {"skills": [{"name": "SQL", "proficiency": "beginner"}, {"name": "Docker"}]}
    )

    assert profile.skills[0].proficiency is Proficiency.BEGINNER
    assert profile.skills[1].proficiency is None


def test_profile_rejects_duplicate_skills_case_insensitively():
    with pytest.raises(ValidationError, match="duplicate skill"):
        StudentProfile(skills=(ProfileSkill(name="Python"), ProfileSkill(name="python")))


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        ProfileSkill.model_validate({"name": "Python", "years": 3})


def test_invalid_enum_value_is_rejected():
    with pytest.raises(ValidationError):
        ProfileSkill.model_validate({"name": "Python", "proficiency": "expert"})


def test_requirement_needs_evidence():
    with pytest.raises(ValidationError):
        Requirement(skill="SQL", level=RequirementLevel.PREFERRED, evidence="")


def test_internship_description_rejects_empty_text():
    with pytest.raises(ValidationError):
        InternshipDescription(text="   ")


def test_models_are_immutable():
    skill = ProfileSkill(name="Python")

    with pytest.raises(ValidationError):
        skill.name = "Java"


def test_analysis_result_filters_by_status():
    matched = RequirementMatch(
        requirement=make_requirement("Python"),
        status=MatchStatus.MATCHED,
        profile_skill=ProfileSkill(name="Python"),
        explanation="Python is listed in the profile.",
    )
    unlisted = RequirementMatch(
        requirement=make_requirement("SQL"),
        status=MatchStatus.UNLISTED,
        explanation="SQL is not mentioned in the profile.",
    )
    result = AnalysisResult(matches=(matched, unlisted))

    assert result.with_status(MatchStatus.UNLISTED) == (unlisted,)
    assert result.with_status(MatchStatus.MISSING) == ()


def test_analysis_result_round_trips_through_json():
    result = AnalysisResult(
        matches=(
            RequirementMatch(
                requirement=make_requirement(),
                status=MatchStatus.MISSING,
                profile_skill=ProfileSkill(name="Python", proficiency=Proficiency.NONE),
                explanation="The profile says Python is not a current skill.",
            ),
        )
    )

    assert AnalysisResult.model_validate_json(result.model_dump_json()) == result
