from fastapi.testclient import TestClient

from gap_analyzer.api.main import app

client = TestClient(app)

POSTING = """\
Requirements:
- Python and Git
Nice to have: Docker
"""


def analyze(body: dict):
    return client.post("/api/analyze", json=body)


def test_analyze_returns_matches_with_status_and_evidence():
    response = analyze(
        {
            "internship": {"title": "SWE Intern", "text": POSTING},
            "profile": {
                "skills": [
                    {"name": "python", "proficiency": "intermediate"},
                    {"name": "Git", "proficiency": "none"},
                ]
            },
        }
    )

    assert response.status_code == 200
    matches = response.json()["matches"]
    summary = [(m["requirement"]["skill"], m["requirement"]["level"], m["status"]) for m in matches]
    assert summary == [
        ("Python", "required", "matched"),
        ("Git", "required", "missing"),
        ("Docker", "preferred", "unlisted"),
    ]
    assert matches[0]["requirement"]["evidence"] == "Python and Git"
    assert matches[0]["explanation"]


def test_analyze_with_empty_profile_marks_everything_unlisted():
    response = analyze({"internship": {"text": POSTING}, "profile": {}})

    assert response.status_code == 200
    assert {m["status"] for m in response.json()["matches"]} == {"unlisted"}


def test_analyze_posting_without_known_skills_returns_no_matches():
    response = analyze({"internship": {"text": "We value teamwork."}, "profile": {}})

    assert response.status_code == 200
    assert response.json() == {"matches": []}


def test_analyze_rejects_empty_description():
    response = analyze({"internship": {"text": "   "}, "profile": {}})

    assert response.status_code == 422


def test_analyze_rejects_oversized_description():
    response = analyze({"internship": {"text": "x" * 50_001}, "profile": {}})

    assert response.status_code == 422


def test_analyze_rejects_duplicate_profile_skills():
    response = analyze(
        {
            "internship": {"text": POSTING},
            "profile": {"skills": [{"name": "Python"}, {"name": "python"}]},
        }
    )

    assert response.status_code == 422
    assert "duplicate skill" in response.text


def test_analyze_rejects_invalid_proficiency():
    response = analyze(
        {
            "internship": {"text": POSTING},
            "profile": {"skills": [{"name": "Python", "proficiency": "expert"}]},
        }
    )

    assert response.status_code == 422


def test_analyze_rejects_missing_and_unknown_fields():
    assert analyze({"profile": {}}).status_code == 422
    assert analyze({"internship": {"text": POSTING}, "profile": {}, "x": 1}).status_code == 422


def test_list_skills_includes_categories_and_aliases():
    response = client.get("/api/skills")

    assert response.status_code == 200
    skills = {s["name"]: s for s in response.json()}
    assert skills["JavaScript"]["category"] == "language"
    assert "JS" in skills["JavaScript"]["aliases"]
