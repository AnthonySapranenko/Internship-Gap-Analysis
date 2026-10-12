"""Analysis engine: requirement extraction, skill normalization, matching, and gap identification.

Kept independent of FastAPI so it can be tested on its own.
"""

from gap_analyzer.engine.catalog import SkillCatalog
from gap_analyzer.engine.extraction import extract_requirements
from gap_analyzer.engine.matching import match_requirements
from gap_analyzer.models import AnalysisResult, StudentProfile

DEFAULT_CATALOG = SkillCatalog()


def analyze(
    description: str, profile: StudentProfile, catalog: SkillCatalog = DEFAULT_CATALOG
) -> AnalysisResult:
    """Extract the requirements from an internship description and match them to a profile."""
    requirements = extract_requirements(description, catalog)
    return match_requirements(requirements, profile, catalog)


__all__ = [
    "DEFAULT_CATALOG",
    "SkillCatalog",
    "analyze",
    "extract_requirements",
    "match_requirements",
]
