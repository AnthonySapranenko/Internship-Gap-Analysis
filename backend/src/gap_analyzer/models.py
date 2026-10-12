"""Core data models shared by the analysis engine and the API.

The models only describe data and validate its shape. Extraction, normalization, and
matching logic live in `gap_analyzer.engine`.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _Model(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)


# --- Skills -----------------------------------------------------------------------------


class SkillCategory(StrEnum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    TOOL = "tool"
    CLOUD = "cloud"
    PRACTICE = "practice"  # e.g. automated testing, REST API design, agile
    OTHER = "other"


class Skill(_Model):
    """A normalized skill, e.g. name="JavaScript" with aliases ["JS", "ECMAScript"]."""

    name: str = Field(min_length=1)
    category: SkillCategory
    aliases: tuple[str, ...] = ()


# --- Internship requirements -------------------------------------------------------------


class RequirementLevel(StrEnum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    # The posting does not say whether the skill is required or preferred.
    UNSPECIFIED = "unspecified"


class Requirement(_Model):
    """A skill an internship asks for, with the posting text it was extracted from."""

    skill: str = Field(min_length=1, description="Normalized skill name")
    level: RequirementLevel
    evidence: str = Field(min_length=1, description="Excerpt from the internship description")


class InternshipDescription(_Model):
    # Not stripped: mention offsets in the analysis index into the text exactly as sent.
    model_config = ConfigDict(str_strip_whitespace=False)

    title: str | None = None
    text: str = Field(min_length=1, max_length=50_000)

    @field_validator("text")
    @classmethod
    def _not_blank(cls, text: str) -> str:
        if not text.strip():
            raise ValueError("the description is empty")
        return text


class Mention(_Model):
    """Where a skill appears in the description: text[start:end] (code point offsets)."""

    skill: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)


# --- Student profile ----------------------------------------------------------------------


class Proficiency(StrEnum):
    # The student says they do not have this skill. Lets the analysis tell a confirmed gap
    # apart from a skill that simply is not mentioned in the profile.
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProfileSkill(_Model):
    name: str = Field(min_length=1, max_length=100)
    # Self-reported and optional; None means "has the skill, level not given".
    proficiency: Proficiency | None = None


class StudentProfile(_Model):
    skills: tuple[ProfileSkill, ...] = Field(default=(), max_length=200)

    @field_validator("skills")
    @classmethod
    def _no_duplicate_skills(cls, skills: tuple[ProfileSkill, ...]) -> tuple[ProfileSkill, ...]:
        seen: set[str] = set()
        for skill in skills:
            key = skill.name.casefold()
            if key in seen:
                raise ValueError(f"duplicate skill in profile: {skill.name!r}")
            seen.add(key)
        return skills


# --- Analysis results ---------------------------------------------------------------------


class MatchStatus(StrEnum):
    MATCHED = "matched"  # in the profile with a proficiency other than NONE
    MISSING = "missing"  # in the profile with proficiency NONE: a confirmed gap
    UNLISTED = "unlisted"  # not in the profile: a potential gap, or the profile is incomplete


class RequirementMatch(_Model):
    requirement: Requirement
    status: MatchStatus
    profile_skill: ProfileSkill | None = Field(
        default=None, description="The profile entry this requirement was compared with, if any"
    )
    explanation: str = Field(min_length=1)


class AnalysisResult(_Model):
    matches: tuple[RequirementMatch, ...] = ()
    mentions: tuple[Mention, ...] = ()

    def with_status(self, status: MatchStatus) -> tuple[RequirementMatch, ...]:
        return tuple(match for match in self.matches if match.status == status)
