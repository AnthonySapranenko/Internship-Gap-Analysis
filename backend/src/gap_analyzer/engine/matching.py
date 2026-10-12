"""Compare extracted requirements against a student profile."""

from gap_analyzer.engine.catalog import SkillCatalog
from gap_analyzer.models import (
    AnalysisResult,
    MatchStatus,
    Proficiency,
    ProfileSkill,
    Requirement,
    RequirementMatch,
    StudentProfile,
)


def _key(name: str, catalog: SkillCatalog) -> str:
    """The catalog name for known skills, so "JS" and "JavaScript" compare equal."""
    skill = catalog.lookup(name)
    return skill.name if skill else " ".join(name.split()).casefold()


def _index_profile(profile: StudentProfile, catalog: SkillCatalog) -> dict[str, ProfileSkill]:
    index: dict[str, ProfileSkill] = {}
    for profile_skill in profile.skills:
        # Two aliases of the same skill ("JS" and "JavaScript"): keep the first.
        index.setdefault(_key(profile_skill.name, catalog), profile_skill)
    return index


def _explain(requirement: Requirement, profile_skill: ProfileSkill | None) -> str:
    name = requirement.skill
    if profile_skill is None:
        return (
            f"{name} is not in your profile. "
            "Add it if you have experience with it; otherwise it is a potential gap."
        )

    listed_as = "" if profile_skill.name == name else f" (listed as {profile_skill.name!r})"
    if profile_skill.proficiency is Proficiency.NONE:
        return f"Your profile says you don't have experience with {name}{listed_as} yet."
    level = f" at {profile_skill.proficiency.value} level" if profile_skill.proficiency else ""
    return f"Your profile lists {name}{listed_as}{level}."


def match_requirements(
    requirements: list[Requirement], profile: StudentProfile, catalog: SkillCatalog
) -> AnalysisResult:
    index = _index_profile(profile, catalog)
    matches = []
    for requirement in requirements:
        profile_skill = index.get(_key(requirement.skill, catalog))
        if profile_skill is None:
            status = MatchStatus.UNLISTED
        elif profile_skill.proficiency is Proficiency.NONE:
            status = MatchStatus.MISSING
        else:
            status = MatchStatus.MATCHED
        matches.append(
            RequirementMatch(
                requirement=requirement,
                status=status,
                profile_skill=profile_skill,
                explanation=_explain(requirement, profile_skill),
            )
        )
    return AnalysisResult(matches=tuple(matches))
