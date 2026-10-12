# Product

<!-- impeccable:product-schema 1 -->

> Written without an interview: the owner asked to work uninterrupted. Facts come from README.md;
> lines marked *(inferred)* are assumptions to confirm.

## Platform

web

## Users

Students preparing for their first software engineering internship, often with limited professional experience. They hold a specific posting they are considering and want to know how their current skills line up with it and what to work on next. *(inferred)* Typically used on a laptop while browsing job boards or planning study time, one posting at a time.

## Product Purpose

Turn an internship description into a structured, evidence-based view of matched skills, potential gaps, and next steps, so students prepare strategically instead of interpreting long job descriptions on their own. Success: the student leaves knowing which requirements they meet, which they lack, which they simply haven't listed, and why each was flagged.

## Positioning

Transparent, explainable matching: every result points back to the sentence in the posting it came from and says in plain language why it was matched or flagged. It distinguishes a confirmed gap (the student said they lack the skill) from missing profile information (the skill isn't listed), and it never presents a match percentage as a probability of being hired.

## Operating Context

The student pastes the full posting text, builds a skill profile (name plus optional self-reported level, including "don't have it yet"), and runs an analysis. They iterate: add a skill they forgot, re-run, compare. Inputs are remembered in the browser between visits. No accounts, no saved history yet.

## Capabilities and Constraints

- Rule-based extraction from a fixed skill catalog (~60 skills with aliases); unknown terms are not recognized.
- Requirement levels: required, preferred, unspecified (posting doesn't say).
- Match statuses: matched, missing (confirmed gap), unlisted (not in profile).
- Backend: FastAPI (`POST /api/analyze`, `GET /api/skills`). Frontend: React + TypeScript + Vite, plain CSS.
- Not yet built: learning recommendations (Phase 6), resume parsing, saved analyses.

## Brand Commitments

Name: Internship Skill Gap Analyzer. Tagline from README: "Turn internship requirements into an actionable plan for becoming a stronger candidate." Voice is plain, honest, and encouraging without hype.

## Evidence on Hand

No real postings, users, testimonials, or metrics yet. The sample posting in the UI is synthetic and must stay labeled as an example. Do not invent outcomes, success rates, or employer names.

## Product Principles

1. Show the evidence: every claim traces to text in the posting.
2. Never score a person: no readiness percentages or hiring odds.
3. Missing information is not a missing skill; say which one it is.
4. The next step should be obvious from every result.

## Accessibility & Inclusion

*(inferred)* WCAG 2.1 AA: full keyboard use, visible focus, sufficient contrast in light and dark, status not conveyed by color alone.
