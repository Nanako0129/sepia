# Voice registry — the voice-fit line and opt-in triggers

Loaded on every fiction operation for the Opt-in section; the `Voice fit:` line is produced only on review and on refactor stage 1 (never on write or recreate). Not loaded on professional routes in this version (the professional-route suggestion is tracked in issue #227). This file is the single home of the voice-fit mechanism and of the per-profile data it reads, and it lists each profile's opt-in triggers. It contains no voice moves and no style rules; a profile body loads only when the user opts in.

## The rule

- **Inputs.** Only what the fiction review already records: the rubric report's observed signals, each named by its rubric row heading with quoted evidence, and its advisories. Nothing is re-read or re-judged for this line.
- **Threshold.** A profile is suggested when at least the stated number of its signature rows appear among the report's observed signals AND none of its anti-signal items is recorded. Each item is a yes/no inspection of the report, never of the text. The registry adds no numeric cutoff of its own: whether a numeric row is an observed signal is the rubric's qualitative comparison, made once in the review, and the count inherits that judgment.
- **Output.** One line, the last line of the report, after `Plan:` — the count is emitted only once the findings, the quoted evidence, and the fix plan are all committed, so a number written early cannot steer any of them toward the suggested profile. Suggesting: `Voice fit: <profile> (<matched>/<signature size> recorded findings) — opt in with "<phrase>"`. Not suggesting: `Voice fit: none (anti-signal: <item>)` when an anti-signal is recorded, otherwise `Voice fit: none (<matched>/<size>)`. When the voice is already declared (by phrase, by intent trigger, or through the `sepia-hemingway` entry): `Voice fit: <profile> — applied`; the voice's expected costs are then reported through the expectation table in `voice-skills.md`. The count is a count of recorded findings, not a score or a detection verdict.
- **Expected quiet.** Text already written in a profile's voice, reviewed without declaring it, usually records that profile's anti-signals (its known costs) and reads `none`; that is intended.
- **Invariants.** The line is a suggestion. It is not a defect and is excluded from refactor stage 2's fix list. It loads no profile body and changes no operation.

## Opt-in

A profile body loads when any of its triggers is met. Every trigger is an explicit request by the user. When a trigger other than the exact phrase fires, sepia says in one line which profile it is applying and that "no voice" runs plain sepia; nothing is applied silently.

## hemingway

- Body: `references/voices/hemingway.md`
- Opt-in phrase: `apply the Hemingway voice`
- Intent triggers (fiction route only): the user asks for strong, aggressive, or maximal de-AI on a story, or asks that it read as human as possible — for example "strong de-AI", "make this read as human as you can", 「去 AI 味要重」「盡量像人寫的」. On a professional route these requests do not load the profile; its professional section is available only by the exact phrase.
- Entry: `sepia-hemingway` (fiction write or refactor with the profile declared).

Fiction signature (5 rubric rows, verbatim headings; ≥3 recorded → suggest):

| # | Rubric row | Recorded as |
|---|---|---|
| 1 | Group A — Thematic explicitness | observed signal with quoted evidence |
| 2 | Group A — Narrator thematic commentary | observed signal with quoted evidence |
| 3 | Group B — Dominant emotion mode | embodied dominance flagged |
| 4 | Group B — Setting as psychological mirror | observed signal with quoted evidence |
| 5 | Group C — Resolution mode | internal acceptance flagged |

Fiction anti-signal (recorded → `Voice fit: none`):

| # | Recorded item |
|---|---|
| a | An over-correction advisory on "Depth of interior access" or "Thematic explicitness" (the two costs the profile documents) |

Dialogue share is not an anti-signal here; the profile's own dialogue row carries the calibration caution (a measured Gemini fingerprint) and applies it when the voice is used.
