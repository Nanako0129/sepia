# Composing with voice skills (experimental)

Status: experimental and opt-in. Load this file only when the user says a voice or style skill is stacked with sepia — a minimalism method, a brand voice, a persona guide. Never assume one is in play, and never inject an aesthetic that sepia's own references don't prescribe: the voice is the user's choice, sepia's job is calibration around it. This opt-in scope covers the composition rules below and the built-in profile bodies under `voices/`; the report's `Voice fit:` line is a different thing — it comes from `voices/registry.md`, which SKILL.md loads by default on the fiction route on review and refactor stage 1, and that file holds its own rule and the opt-in triggers.

Precedence on professional routes: the venue corpus still sets the register (`professional-pass.md`), and the voice operates inside it. Where a declared voice and the venue's register directly conflict, surface the conflict and let the user pick — never silently override either. The same applies on every route when a voice move directly contradicts a `style-pass.md` §4 restore item (a voice that forbids negation against §4's "restore negation", for instance): name both rules in the report and leave the choice to the user.

Built-in profile bodies: `voices/hemingway.md` (opt-in phrase: "apply the Hemingway voice"). A built-in profile may also declare intent triggers in `voices/registry.md` — user requests that count as opting in; sepia announces the profile it is applying and how to decline, so nothing is ever applied silently.

## Why the two need an interface

sepia calibrates toward the human distribution and the venue. A voice skill aims at one specific aesthetic, and a strong aesthetic deliberately pushes some measured axes away from the human band. Stacked naively, the two fight: sepia's review flags the voice's signature restraint or ornament as drift, and the voice's uniform application manufactures exactly the fingerprints sepia hunts. The rules below are the interface.

## Composition order (write and recreate)

For **recreate**, the canonical preflight still comes before everything: extract and verify the source's facts, claims, and intent first — the steps below begin only after that preservation set exists.

1. sepia's architecture decisions first (fiction: the architecture sheet in `narrative-pass.md`; professional: the domain file).
2. The voice skill's moves next, applied selectively (see below).
3. sepia review last, with the adjusted expectations in the table.

For **review**, the canonical contract is unchanged: diagnose without editing. Under a declared voice the adjustment is interpretive only — score with the expectation table below.

For **refactor**, stage 1 is unchanged: the complete defect list first, scored with the expectation table, and the voice's expected costs are not listed as defects. In stage 2 the declared voice supplies the fix vocabulary: a voice move may be applied only as the fix for an item on the stage-1 list, chosen from the 3–5 selected for the piece, and a passage with no listed defect is not touched. The voice does not license edits the defect list did not call for; that is what keeps refactor minimal under a voice.

## Selection applies to voice moves too

A voice skill applied wholesale produces a house style, and a house style is a fingerprint. Extend sepia's selection rule to the voice: at most 3–5 of its signature moves per piece, varied across pieces. A signature ending formula ("return to the recurring object, shortest sentence last") fails the echo test once it appears every time — break it deliberately in some pieces. Leave slack: a human writing in a strict style still slips out of it somewhere; a piece where no paragraph is allowed to fail reads as a metronome.

## Reviewing voice-composed text

| Finding class | Handling under a declared voice |
|---|---|
| Over-correction advisories on axes the voice deliberately pushes (a minimalism method driving interior access, sensory density, or thematic explicitness to the low extreme) | Expected: report them as the voice's known cost, and do not prescribe fixes against the user's chosen aesthetic. Escalate only if the user hasn't been told the trade-off |
| Uniformity findings: the same sentence recipe in every paragraph, the key line always closing the paragraph, a complete setup-payoff ledger, a formula ending | Hard findings at full strength — a voice does not excuse a metronome |
| Style-pass vocabulary and syntax hits | Unchanged — style-pass's own clustering thresholds and whitelists stay in force; a declared voice neither excuses nor hardens them |
| Specificity and fact guardrails | Unchanged: never invent, voice or no voice |

## Worked example (single run, not measured evidence)

One blind sepia review was run on a specimen written strictly to a published minimalism method (new-concept-writing, MIT: numbers as emotional anchors, one recurring object, repetition with one break, zero exposition, image ending). The drift concentrated in structural tidiness (a full setup-payoff ledger; a protagonist-completed ritual ending that fails the echo test) and uniformity (every paragraph beat at the paragraph end, one recipe throughout), with four over-correction advisories where the method pushes axes to the far pole. Its emotion handling landed in the human band (behavior-led), against the naive assumption that "show don't tell" methods drift AI-ward. Treat this as one worked example on one specimen — a reason for the rules above, not a measurement.
