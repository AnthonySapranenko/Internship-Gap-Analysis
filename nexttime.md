# Next time

Handoff notes for the next working session. Last updated 2026-10-12.

## Where things stand

Phases 1–5 are done and pushed. This session finished part of the Phase 5 design wrap-up.

### Done this session

- **Design checker warnings silenced, narrowly.** The `border-accent-on-rounded` rule is turned off only for
  `frontend/src/index.css` and the three layout sketches in `.impeccable/mocks/decision/`. Both exceptions,
  with their reasons, are in `.impeccable/config.json`. The red top rule on the posting sheet, skill chips and
  result cards is the index-card header line, and their top corners are square, so the clash the rule
  describes never shows on the page.
- **Surface brief corrected.** `.impeccable/surfaces/frontend-src-app-tsx.md` now records the Marked-up
  posting layout you picked, instead of the original two-column layout.
- **Final design review ran.** Verdict: **fix**, with 8 items. The plugin's own reviewer agent isn't loaded in
  these sessions, so a fresh general-purpose agent ran it, following the reviewer's instructions.
- **Fixes applied (you chose the two bugs plus the layout polish):**
  - Phones: the marked-up posting shows in full, with no inner scroll hiding the Preferred highlights.
  - An "Example posting" label shows while the sample posting is loaded and unedited (PRODUCT.md requires this).
  - The posting's first line shows as a heading on the sheet (`splitTitle` in `marks.ts`, with tests).
  - Skill names on result cards are bigger (1.25rem).
  - The results summary reads "Matched: 2 of 4 required, 0 of 3 preferred, 1 of 3 mentioned" and fits on one
    line on desktop.
  - The ruled lines inside an opened card line up with its text, and the "I have this" button sits between them.
  - The ignore rule's reason was reworded to name all three elements it covers.
- Frontend checks pass: type check, 9 tests, lint. The screenshots in `.impeccable/review/` were retaken after
  the fixes.

## Next steps

1. **Send the fixes back to the reviewer for a verdict.** It scores each of its 8 items as resolved, partial
   or unresolved, using the new screenshots in `.impeccable/review/`. It hasn't run yet: the session stopped
   right after the recapture. Expect items 3 (typeface) and 5 (posting title) to come back as below.
2. **Write DESIGN.md.** Run the plugin's documenter step after the verdict. It records the finished design
   (colours, highlight and underline styles, card rules) in `DESIGN.md` plus `.impeccable/design.json`. Don't
   record the system font as a design rule; the reviewer flagged it.
3. **Decide on the typeface (skipped this session).** The reviewer wants a self-hosted, handwritten-style font
   for headings and skill names, with a plain font for body text. You haven't decided yet.
4. **Known leftovers the reviewer may flag again:**
   - The posting title only becomes a heading when its first line has no highlighted skill and is 100
     characters or fewer.
   - On desktop the posting sheet ends with about six empty ruled lines.
   - Opened cards end with a 10px strip below the last line.
5. **Skim PRODUCT.md.** Lines marked *(inferred)* were filled in from the README and need confirming.
6. **Phase 6.** Start once the design wrap-up is closed.

## How to recapture screenshots

Start the backend (`backend/.venv/Scripts/uvicorn gap_analyzer.api.main:app --port 8000`) and the frontend
(`npm run dev` in `frontend/`). A previous session left a Puppeteer script that captures `empty`, `desktop`,
`mobile` and `desktop-dark` into a folder you name. It lives in that session's temp scratchpad, so it may be
gone. If so, rewrite it: load the example posting with skills Python (intermediate), Git, React (beginner)
and SQL (don't have it yet), then select a mark.
