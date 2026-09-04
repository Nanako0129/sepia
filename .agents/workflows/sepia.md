# /sepia — de-AI writing

Apply the sepia skill to the current writing task.

1. Locate the skill's `SKILL.md`: first try `.agents/skills/sepia/SKILL.md` in this workspace; if absent, `~/.gemini/config/skills/sepia/SKILL.md`.
2. Read it and follow it exactly: route the text by type (fiction / release notes / PR-issue replies / postmortems / tickets / tech articles / other prose), pick the operation the user asked for (write, review, refactor, recreate), and load only the reference files that `SKILL.md`'s Routing section names for that text — the table row plus the conditional loads stated under it (model fingerprints, the Chinese calibration, the voice registry).
3. If the user passed text or a file path as the argument, treat it as the target; otherwise ask what to process and which operation they want.
