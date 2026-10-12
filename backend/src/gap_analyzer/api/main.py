from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from gap_analyzer import __version__
from gap_analyzer.config import settings
from gap_analyzer.engine import DEFAULT_CATALOG, analyze
from gap_analyzer.models import AnalysisResult, InternshipDescription, Skill, StudentProfile

app = FastAPI(title="Internship Skill Gap Analyzer", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    internship: InternshipDescription
    profile: StudentProfile


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/api/skills")
def list_skills() -> list[Skill]:
    """Every skill the analyzer recognizes, e.g. for suggestions when building a profile."""
    return list(DEFAULT_CATALOG.skills.values())


@app.post("/api/analyze")
def analyze_internship(request: AnalyzeRequest) -> AnalysisResult:
    """Extract the internship's skill requirements and compare them with the profile."""
    return analyze(request.internship.text, request.profile)
