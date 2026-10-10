from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gap_analyzer import __version__
from gap_analyzer.config import settings

app = FastAPI(title="Internship Skill Gap Analyzer", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
