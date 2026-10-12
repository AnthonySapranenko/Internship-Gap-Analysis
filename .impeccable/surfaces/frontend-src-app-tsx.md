---
version: 1
slug: "frontend-src-app-tsx"
primary_target: "frontend/src/App.tsx"
related_targets: ["frontend/src/Results.tsx","frontend/src/SkillsEditor.tsx","frontend/src/index.css"]
---

# Analyzer workspace (frontend/src/App.tsx)

Scope: the single-page analyzer: paste a posting, build a skill profile, read results. Mode: Operate.
Audience/job: a CS student checking one internship posting against their skills; iterates by adding forgotten skills and re-running.
Constraints: no scores or hiring odds; evidence quote on every result; missing vs unlisted always distinguished; status never by colour alone.
Run notes: owner asked for no questions, so the direction was taken unattended (assigned roll, no decision page). Code-led (operate).

## Direction contract

THESIS: The study index card. Each requirement is a ruled card you could pin above a desk; refuses the grey dashboard with a score ring and stat tiles.
OWN-WORLD: White card stock with a red header rule and pale blue ruled lines; status is the card stock (green matched, pink missing, canary unlisted) plus a printed status word; card-box divider tabs head each group; blue-black ballpoint ink text on a cool desk-blue ground under a filing-box blue header band. Level marker by fill: solid square required, outline preferred, dotted mentioned.
STORY: The student sees which requirements they meet, which they confirmed missing, which they never listed, and the posting sentence behind each, then adds a forgotten skill in one click.
FIRST VIEWPORT: Blue header band with product name and one-line purpose. Left column (5/11): posting sheet (ruled textarea) with example link, skill rows, primary Analyze button at the column foot. Right column (6/11): one-line level summary, then divider-tabbed stacks of cards: Gaps to work on, Not in your profile, Matched.
FORM: Index-card study system, candidate 3 of 7 in my ordered list; seed 364da7a6. Signature move: "I have this" re-files the card into Matched with a one-time stock-colour change. Raises: from labanotation, level encoded by fill shape not colour; from ticket wallet, state is a printed word on the card; from centre-rail setting, every rule a crisp 1px hairline; from datamatics, tabular numerals on every count.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
