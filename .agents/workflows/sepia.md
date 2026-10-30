# /sepia — de-AI writing

Apply the sepia skill to the current writing task.

1. Locate the skill's `SKILL.md`: first try `.agents/skills/sepia/SKILL.md` in this workspace; if absent, `~/.gemini/config/skills/sepia/SKILL.md`.
2. Read it and follow it exactly: route the text and pick the operation the user asked for as its Routing and Operations sections say, and load the reference files `SKILL.md` directs you to for that text, starting from Routing — not the whole references directory.
3. If the user passed text or a file path as the argument, treat it as the target; a missing target is handled as `SKILL.md` *Call-time scope and unattended mode* says.
