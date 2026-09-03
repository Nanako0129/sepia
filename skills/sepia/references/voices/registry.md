# Voice registry — the voice-fit line

Loaded on review and on refactor stage 1 (every route), never on write. This file is the single home of the voice-fit mechanism and of the per-profile data it reads. It contains no voice moves and no style rules; a profile body loads only when the user says its opt-in phrase.

## The rule

- **Inputs.** Only what the review already records: rubric observed signals with quoted evidence and advisories (fiction), `Failed:` check lines and the `Style scan:` line (professional). Nothing is re-read or re-judged for this line.
- **Threshold.** A profile is suggested when at least the stated number of its signature items are recorded AND none of its anti-signal items is recorded. Each item is a yes/no inspection of a named rubric row, advisory, or check.
- **Output.** One line in the report, after `Prose layer:`. Suggesting: `Voice fit: <profile> (<matched>/<signature size> recorded findings) — opt in with "<phrase>"`. Not suggesting: `Voice fit: none (anti-signal: <item>)` or `Voice fit: none (<matched>/<size>)`. When the user has already declared that voice: `Voice fit: <profile> — applied`. The count is a count of recorded findings, not a score or a detection verdict.
- **Expected quiet.** Text already written in a profile's voice usually records that profile's anti-signals (its known costs) and reads `none`; that is intended, the line exists for text that has not been given the voice yet.
- **Invariants.** The line is a suggestion. It is not a defect and is excluded from refactor stage 2's fix list. It loads no profile body and changes no operation. Only the user's opt-in phrase loads a profile, through `voice-skills.md`.

## hemingway

- Body: `references/voices/hemingway.md` (opt-in only)
- Opt-in phrase: `apply the Hemingway voice`

Fiction signature (5 rubric rows, verbatim headings; ≥3 recorded → suggest):

| # | Rubric row | Recorded as |
|---|---|---|
| 1 | Group A — Thematic explicitness | observed signal with quoted evidence |
| 2 | Group A — Narrator thematic commentary | observed signal with quoted evidence |
| 3 | Group B — Dominant emotion mode | embodied dominance flagged |
| 4 | Group B — Setting as psychological mirror | observed signal with quoted evidence |
| 5 | Group C — Resolution mode | internal acceptance flagged |

Fiction anti-signals (any 1 recorded → `Voice fit: none`):

| # | Recorded item |
|---|---|
| a | An over-correction advisory on "Depth of interior access", "Sensory density", or "Thematic explicitness" |
| b | Group E — "Dialogue proportion" observed at 4 or 5 on its 1–5 scale |

Professional signature (4 items; ≥3 recorded → suggest):

| # | Check or scan hit |
|---|---|
| 1 | professional-pass check 2 (density) failed |
| 2 | professional-pass check 1 (chatbot residue) or check 7 (conclusion residue) failed |
| 3 | professional-pass check 10 (fluency) failed |
| 4 | a style-pass §3 inflation-adjective hit recorded on the report's `Style scan:` line (that row names a class by example; an extravagant adjective of the same kind, such as "magnificent", is a hit) |

Professional anti-signal (recorded → `Voice fit: none`):

| # | Recorded item |
|---|---|
| a | professional-pass check 9 (sameness of rhythm) failed |
