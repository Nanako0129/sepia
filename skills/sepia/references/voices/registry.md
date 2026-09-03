# Voice registry — the voice-fit line

Loaded on review and on refactor stage 1 (every route), never on write. This file is the single home of the voice-fit mechanism and of the per-profile data it reads. It contains no voice moves and no style rules; a profile body loads only when the user says its opt-in phrase.

## The rule

- **Inputs.** Only what the review already records: rubric observed signals with quoted evidence and advisories (fiction), `Failed:` check lines with their recorded direction tags and the `Style scan:` line (professional). Nothing is re-read or re-judged for this line.
- **Threshold.** A profile is suggested when at least the stated number of its signature items are recorded AND none of its anti-signal items is recorded. Each item is a yes/no inspection of the report, never of the text: a rubric row counts when the report lists it under that group's *observed signals* with quoted evidence (not under "no signal" or "n/a"); a categorical row counts when its flagged option is recorded; a check counts when it appears on a `Failed:` line. For numeric rows the registry adds no cutoff of its own — `rubric.md` forbids numeric cutoffs — so whether a moderate score is an observed signal is the rubric's qualitative comparison, made once in the review, and the count inherits that judgment rather than re-making it.
- **Output.** One line in the report, after `Prose layer:`. Suggesting: `Voice fit: <profile> (<matched>/<signature size> recorded findings) — opt in with "<phrase>"`. Not suggesting: `Voice fit: none (anti-signal: <item>)` when an anti-signal is recorded, otherwise `Voice fit: none (<matched>/<size>)`. When the user has already declared a voice, declaration controls and the line reads `Voice fit: <profile> — applied` whatever the counts say; the voice's expected costs are then reported through the expectation table in `voice-skills.md`, not through this line. The count is a count of recorded findings, not a score or a detection verdict.
- **Expected quiet.** Text already written in a profile's voice, reviewed without declaring it, usually records that profile's anti-signals (its known costs) and reads `none`; that is intended, the line exists for text that has not been given the voice yet.
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
| a | An over-correction advisory on "Depth of interior access" or "Thematic explicitness" (the two costs the profile documents) |
| b | Group E — "Dialogue proportion" observed at 4 or 5 on its 1–5 scale |

Professional signature (4 items; ≥3 recorded → suggest):

| # | Check or scan hit |
|---|---|
| 1 | professional-pass check 2 (density) failed with direction recorded as padding |
| 2 | professional-pass check 1 (chatbot residue) or check 7 (conclusion residue) failed |
| 3 | professional-pass check 10 (fluency) failed |
| 4 | any style-pass §3 hit recorded on the report's `Style scan:` line (whatever the scan recorded; the registry does not re-judge the text) |

Professional anti-signal (recorded → `Voice fit: none`):

| # | Recorded item |
|---|---|
| a | professional-pass check 9 (sameness of rhythm) failed with direction recorded as short (long or paragraph do not block) |
