---
version: 1
slug: "frontend-src-app-tsx"
primary_target: "frontend/src/App.tsx"
related_targets: ["frontend/src/PostingSheet.tsx","frontend/src/SkillsBar.tsx","frontend/src/Results.tsx","frontend/src/index.css"]
---

# Analyzer workspace (frontend/src/App.tsx)

Scope: the single-page analyzer: paste a posting, build a skill profile, read results. Mode: Operate.
Audience/job: a CS student checking one internship posting against their skills; iterates by adding forgotten skills and re-running.
Constraints: no scores or hiring odds; evidence quote on every result; missing vs unlisted always distinguished; status never by colour alone.
Run notes: the world (index-card study system) was taken unattended from an assigned roll. The layout was then put to the owner on a decision page (.impeccable/mocks/decision/: Profile rail, Marked-up posting, Three steps); the owner picked Marked-up posting (marked.html), which is the critique reference, not an approved comp. Code-led (operate).

## Direction contract

THESIS: The study index card. Each requirement is a ruled card you could pin above a desk; refuses the grey dashboard with a score ring and stat tiles.
OWN-WORLD: White card stock with a red header rule and pale blue ruled lines; status is the card stock (green matched, pink missing, canary unlisted) plus a printed status word; card-box divider tabs head each group; blue-black ballpoint ink text on a cool desk-blue ground under a filing-box blue header band. Level marker by fill: solid square required, outline preferred, dotted mentioned.
STORY: The student sees the posting itself marked up like a printout gone over with highlighters: every skill it mentions is marked where it appears, in its status colour and underline, and the card beside it says what was matched, confirmed missing, or never listed, quoting that sentence; a forgotten skill is added in one click.
FIRST VIEWPORT (owner's pick: Marked-up posting): Blue header band with product name and one-line purpose. Skills as a chip bar under the header with the primary Analyze button at its right end. Left (wide): the posting on a ruled sheet under a red header rule, every skill mention highlighted by status (green matched, pink missing, canary not listed; underline style differs per status). Right: one-line level summary and legend, then divider-tabbed stacks of cards: Gaps to work on, Not in your profile, Matched; selecting a mark opens its card with the posting quote and explanation. Phones: single column, skills, then posting, then results.
FORM: Index-card study system, candidate 3 of 7 in my ordered list; seed 364da7a6. Signature move: "I have this" re-files the card into Matched with a one-time stock-colour change. Raises: from labanotation, level encoded by fill shape not colour; from ticket wallet, state is a printed word on the card; from centre-rail setting, every rule a crisp 1px hairline; from datamatics, tabular numerals on every count.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
