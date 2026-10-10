# Internship Skill Gap Analyzer

**Turn internship requirements into an actionable plan for becoming a stronger candidate.**

The Internship Skill Gap Analyzer is a full-stack application designed to help students understand how their technical skills align with real software engineering internship requirements.

By analyzing internship descriptions against a student's existing skills, the application identifies potential skill gaps, explains which qualifications need attention, and generates a prioritized roadmap for improvement.

Rather than leaving students to interpret lengthy job descriptions on their own, the goal is to provide a structured, evidence-based approach to internship preparation.

> **Project status:** In development.

## Table of Contents

- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Core Features](#core-features)
- [Example Workflow](#example-workflow)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Development Roadmap](#development-roadmap)
- [Testing and Quality](#testing-and-quality)
- [Privacy and Responsible Use](#privacy-and-responsible-use)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Conventions](#development-conventions)
- [Future Improvements](#future-improvements)
- [Project Goals](#project-goals)
- [Vision](#vision)

## The Problem

Preparing for a first software engineering internship can be challenging, especially for students with limited professional experience.

- **Unclear expectations:** Internship listings often contain extensive lists of programming languages, frameworks, tools, and qualifications.
- **Difficulty identifying gaps:** Students may struggle to determine how their current skills compare with an employer's requirements.
- **Inefficient preparation:** Without clear priorities, students may spend time learning technologies that are less relevant to their target roles.
- **Disconnected learning:** Finding practical projects and learning activities that address specific skill gaps takes time.
- **Lack of direction:** Students need a structured way to turn internship requirements into achievable learning goals.

## The Solution

The Internship Skill Gap Analyzer transforms internship descriptions into personalized skill assessments and learning recommendations.

Users provide an internship description and a profile of their current skills. The application analyzes the relationship between the two and produces an organized breakdown of matched skills, potential gaps, and recommended next steps.

The objective is not to decide whether someone deserves an internship. It is to help users understand role expectations, identify opportunities for improvement, and prepare more strategically.

## Core Features

### 1. Internship Requirement Extraction

- Accept internship descriptions as text.
- Identify relevant technical skills, programming languages, frameworks, and developer tools.
- Organize extracted requirements into understandable categories.
- Distinguish required qualifications from preferred qualifications when the source makes that distinction clear.

### 2. Student Skill Profiles

- Allow users to specify their existing technical skills.
- Organize skills into categories such as programming, databases, web development, and developer tools.
- Support self-reported proficiency levels where appropriate.
- Provide a consistent format for comparing skills across different internship opportunities.

### 3. Skill Gap Analysis

- Compare extracted internship requirements against the student's profile.
- Identify matched skills, potential gaps, and skills requiring further development.
- Recognize relevant terminology and related skill names where supported.
- Explain why a requirement was matched or flagged.
- Distinguish missing profile information from confirmed lack of experience.

### 4. Personalized Learning Roadmap

- Prioritize gaps according to the internship's stated requirements.
- Suggest practical exercises and portfolio projects.
- Break improvement goals into manageable tasks.
- Connect learning recommendations to specific requirements rather than providing generic advice.

### 5. Results Dashboard

- Display skill matches and potential gaps in an organized interface.
- Summarize the most important areas for improvement.
- Present evidence from the internship description alongside analysis results.
- Provide a clear overview of recommended next steps.

### 6. Reliable Analysis

- Validate user input and handle malformed descriptions.
- Normalize common variations in skill terminology.
- Account for ambiguous requirements and uncertain matches.
- Test matching behavior against representative examples.
- Avoid presenting an arbitrary match percentage as a reliable probability of getting hired.

*Features will be marked as implemented as development progresses. The list above describes the intended functionality, not a claim that every feature is already available.*

## Example Workflow

Consider a student applying for a software engineering internship requiring Python, SQL, Git, REST APIs, and automated testing.

The student enters their current skills and submits the internship description.

The application could produce an analysis such as:

| Requirement | Example result |
|---|---|
| Python | Matched to the student's profile |
| Git | Matched to the student's profile |
| SQL | Potential skill gap |
| REST APIs | Potential skill gap |
| Automated testing | Potential skill gap |

Based on these results, the application might recommend:

1. Practice SQL queries and relational database concepts.
2. Build a small REST API using Python and FastAPI.
3. Write unit and integration tests for the API.
4. Document the project and publish the code in a personal GitHub repository.

This turns a job listing into a practical development plan.

*The example is illustrative and does not represent an actual analysis performed by the current application.*

## Technology Stack

The planned technology stack emphasizes widely used tools and practical software engineering principles.

| Technology | Purpose |
|---|---|
| Python | Core analysis logic and backend development |
| FastAPI | REST API and request validation |
| React | Frontend user interface |
| TypeScript | Frontend type safety and maintainability |
| PostgreSQL | Persistent storage if saved profiles and analysis history are implemented |
| Pytest | Unit and integration testing |
| Git and GitHub | Version control and source management |

Additional libraries may be introduced when they solve a specific problem, rather than adding dependencies without a clear purpose.

## Architecture

The application is designed with separate responsibilities for the frontend, backend, analysis engine, and optional persistent storage.

```text
┌──────────────────────────────────┐
│           Frontend               │
│       React + TypeScript         │
│                                  │
│  Inputs · Results · Dashboard    │
└────────────────┬─────────────────┘
                 │ HTTP / REST
                 ▼
┌──────────────────────────────────┐
│            FastAPI               │
│                                  │
│  API Endpoints · Validation      │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│         Analysis Engine          │
│                                  │
│  Requirement Extraction          │
│  Skill Normalization             │
│  Requirement Matching            │
│  Gap Identification              │
│  Recommendation Generation       │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│       Optional Persistence       │
│            PostgreSQL            │
└──────────────────────────────────┘
```

Separating the analysis engine from the API allows the matching logic to be tested independently and improved without tightly coupling it to the user interface.

## Development Roadmap

Development will proceed incrementally, prioritizing a reliable end-to-end workflow before advanced features.

- [x] **Phase 1 — Foundation:** Establish repository structure, development environment, documentation, and coding conventions.
- [ ] **Phase 2 — Data models:** Define internship requirements, normalized skills, and student skill profiles.
- [ ] **Phase 3 — Analysis engine:** Implement skill extraction, normalization, matching, and gap identification.
- [ ] **Phase 4 — Backend API:** Expose analysis functionality through validated FastAPI endpoints.
- [ ] **Phase 5 — Frontend:** Build the interface for entering internship descriptions and reviewing analysis results.
- [ ] **Phase 6 — Recommendations:** Generate prioritized learning tasks tied to identified gaps.
- [ ] **Phase 7 — Automated testing:** Cover matching rules, edge cases, malformed input, and API behavior.
- [ ] **Phase 8 — Evaluation:** Compare results against manually reviewed internship descriptions and document limitations.
- [ ] **Phase 9 — Deployment:** Deploy the application and publish usage instructions, screenshots, and a live demo.
- [ ] **Phase 10 — Expansion:** Consider saved analyses, resume comparison, external learning resources, and advanced language processing.

## Testing and Quality

Testing is a core part of the project, not an afterthought.

Planned quality checks include:

- Unit tests for skill normalization and matching logic.
- Tests for missing, ambiguous, and overlapping requirements.
- API tests for valid and invalid requests.
- Integration tests for critical application workflows.
- Evaluation against a manually labeled set of internship descriptions.
- Documentation of known limitations and incorrect matches discovered during testing.

Where possible, analysis quality will be measured using appropriate metrics such as precision and recall on manually labeled skill-extraction or matching examples.

The goal is to make the system's behavior understandable, repeatable, and measurable.

## Privacy and Responsible Use

The application is intended to support career preparation, not make employment decisions.

- Collect only information necessary for the implemented functionality.
- Protect uploaded resumes and personal data if file uploads are introduced.
- Keep API keys and other secrets out of source control.
- Avoid storing sensitive information without a clear need.
- Explain the basis of skill matches and recommendations.
- Treat self-reported skills as estimates rather than independently verified abilities.
- Make clear that missing keywords do not necessarily mean a student lacks a skill.
- Do not represent readiness scores as guarantees of interviews, offers, or employment.

## Getting Started

### Prerequisites

- Python 3.12 or newer
- Node.js 20 or newer, with npm
- Git
- PostgreSQL, only once database-backed features are added

### Installation

Clone the repository:

```bash
git clone https://github.com/AnthonySapranenko/Internship-Gap-Analysis.git
cd Internship-Gap-Analysis
```

Set up the backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -e ".[dev]"
cp .env.example .env            # optional; defaults work for local development
```

Set up the frontend:

```bash
cd frontend
npm install
```

### Running locally

Start the backend and frontend in two separate terminals.

```bash
# Terminal 1, from backend/ with the virtual environment active
uvicorn gap_analyzer.api.main:app --reload
```

```bash
# Terminal 2, from frontend/
npm run dev
```

Open http://localhost:5173. The page shows whether it can reach the backend. The frontend dev server forwards `/api` requests to the backend on port 8000. Interactive API docs are at http://localhost:8000/docs.

### Running checks

```bash
# backend/
pytest              # tests
ruff check .        # lint
ruff format .       # format

# frontend/
npm run lint
npm run build       # type-check and production build
```

The same checks run automatically on GitHub for every push and pull request (see `.github/workflows/ci.yml`).

## Project Structure

```text
backend/
  pyproject.toml            Dependencies and tool configuration
  .env.example              Example environment variables
  src/gap_analyzer/
    config.py               Settings loaded from environment variables
    api/                    FastAPI app and routes
    engine/                 Analysis engine, independent of the web layer
  tests/                    Pytest test suite
frontend/
  src/                      React + TypeScript application
  vite.config.ts            Dev server and API proxy configuration
.github/workflows/ci.yml    Automated lint, test and build checks
```

## Development Conventions

- **Branches and commits:** keep `main` working. Make small, focused commits with messages that say what changed and why.
- **Separation of concerns:** the analysis engine must not import FastAPI. The API layer validates input and calls the engine.
- **Python:** formatted and linted with Ruff, with type hints on public functions. Every engine change comes with tests.
- **TypeScript:** strict mode, linted with oxlint. Call the backend only through relative `/api` URLs.
- **Configuration:** settings come from environment variables prefixed with `GAP_`. Real `.env` files are never committed.
- **Formatting:** line endings and indentation are set by `.editorconfig` and `.gitattributes`.

## Future Improvements

Potential future enhancements include:

- Resume parsing and comparison against internship requirements.
- Analysis of multiple internship descriptions to identify recurring skills.
- Links to relevant courses, documentation, and tutorials.
- Saved profiles and progress tracking.
- Advanced natural language processing for related terminology and contextual matching.
- Carefully evaluated AI-assisted recommendations with clear explanations.
- Exportable skill-gap reports and learning plans.

These improvements will be considered after the core workflow is functional, tested, and useful.

## Project Goals

This project is intended to demonstrate practical software engineering skills through the development of a complete application.

Key learning and engineering objectives include:

- Designing RESTful APIs.
- Building modular backend services.
- Processing and normalizing semi-structured text.
- Implementing transparent matching algorithms.
- Designing and testing data models.
- Developing an interactive frontend.
- Writing automated unit and integration tests.
- Evaluating software behavior using measurable criteria.
- Applying secure development practices.
- Maintaining a codebase through version control and incremental development.

## Vision

The Internship Skill Gap Analyzer aims to make technical career preparation more structured, transparent, and actionable.

By connecting real internship requirements to concrete learning activities, the application helps students move beyond wondering whether they are qualified and start identifying what they can do to become stronger candidates.

**The goal is simple: turn internship requirements into a clear path for growth.**

---

*This is an independent educational software project. Its results are intended for career preparation and should not be interpreted as hiring decisions or guarantees of employment.*
