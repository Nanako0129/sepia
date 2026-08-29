# PF3 Sepia arm

## PF3-F-WRITE

At 5:10 on a rainy Tuesday morning, Bo held the phone while Inez, the ferry mechanic, opened the hatch. Water tapped on the deck. Inez knelt beside the engine and listened.

“Is the ferry sick?” Bo asked.

“Only when we rush it,” Inez said.

She started the recording and leaned into the hatch. The engine ticked. Under it came three knocks, close together. Inez lifted her head. They were not engine noise.

The horn called them back to shore before she could investigate. Inez shut the hatch and looked toward the empty end of the deck. Bo pocketed the phone, still recording.

As they walked, Inez stopped. “Why did you move the wrench?” she asked the unseen deckhand.

Bo kept walking. In his pocket, the phone kept listening.

## PF3-F-REVIEW

SEPIA DIAGNOSIS — Marla and the Wallet

Scope: heuristic narrative diagnosis.

Group A: Thematic explicitness and moral/philosophical weighting are high: “honesty always brings happiness” and “everyone who chooses kindness will be rewarded” state the lesson and make a universal claim beyond the scene. Narrator thematic commentary is present. Dialogue as philosophical debate is n/a. Reference explicitness is n/a; there is no allusive gesture.

Group B: The dominant emotion mode is an explicit label in “feeling proud.” Embodied emotion is n/a. Setting as a psychological mirror is n/a; “The rain stopped” is a weather change, not a sustained inner-state mirror. Environmental emphasis and sensory density are low. Interior access is shallow, limited to “feeling proud.”

Group C: The plot is linear and tightly closed: Marla “found the lost wallet,” “returned it,” Mr. Chen “thanked her,” and she “walked home feeling proud.” Resolution agency is present in Marla’s choice to return it; the resolution then closes on pride. Subplots, revelation pacing, temporal framing, and pre-threat investment are n/a. The protagonist is introduced in action: “Marla found.”

Group D: Named intertextuality, a fourth-wall gesture, and direct reader address are n/a.

Group E: Chronological discontinuity, anachrony, nonlinear disclosure, and recontextualization are n/a. Dialogue proportion is none in the supplied scene. Location variety is n/a at this length. Moral polarity is clearly affirmative: kindness is said to be rewarded, and Marla feels proud.

Advisories: The short piece offers limited occasions for several dimensions. The explicit moral and tidy emotional closure are the main structural signals.

Plan: If revising, first replace the stated lesson with a concrete consequence or image; then leave the ending less fully explained. Keep the wallet, bakery, thanks, rain, and walk-home beats.

## PF3-F-REFACTOR

Defects:

- The opening stacks two appearance details: “blue eyes” and “long brown hair.”
- “Her heart pounded, her stomach twisted, and cold sweat gathered” crowds the fear beat with three body cues.
- “She knew she had to be brave” and “courage means acting despite fear” explain the lesson instead of letting the action carry it.

Revised story:

Leah watched the narrow road as the rescue truck slid toward the ditch. Her blue eyes stayed on it while her long brown hair whipped across her face. Leah was afraid. She took a deep breath, grabbed the rope, and pulled the driver to safety. She was relieved.

## PF3-F-RECREATE

The old song played in the café while Nina looked out at the street. A delivery bike clicked past the window, and a woman held a newspaper over her hair. The song pulled Nina toward a summer she could not name: a cracked step, a bicycle against a fence, somebody calling from a yard. She had carried those pieces for years without the name.

The singer finished. Nina left a coin under her cup, pushed open the café door, and smiled at the dark street. Then she walked into the night.

## PF3-P-WRITE

### v2.4.0

Use `--state-dir` in place of `--cache-dir`.

PR #17 reports a benchmark of 1.8s before and 0.9s after over 100 runs.

## PF3-P-REVIEW

- “Thanks for the great question!” is a stock praise opener and delays the review point.
- “Your PR is a really thoughtful contribution” is broad praise without code-specific evidence.
- “I hope this helps” and “Let me know if you need anything else” are generic help-offer residue.
- “Please consider adding tests” names no behavior, case, or acceptance criterion, so the next step is vague.
- “Best regards, The Team” is a generic sign-off for a short PR reply.

## PF3-P-REFACTOR

**Incident**

At 14:00, a deploy failed. The team rolled it back. The problem was fixed, and service recovered.

**Unknowns**

- Date, timezone, and recovery time: `TODO`
- Deploy command: `TODO`; rollback command: `TODO`
- Failure mechanism and root cause: `TODO`
- Impact metrics: `TODO`

**Action**

- Improve monitoring. Owner: `TODO`

## PF3-P-RECREATE

Caching avoids repeating work when the same result can be reused. Read the cache before doing the original work; on a miss, do that work, store the result, and return it.

Illustrative example (pseudocode, not a measured benchmark or production result): suppose an endpoint repeatedly needs profile `user:42`. It checks the cache for that key first. A hit returns the stored profile. A miss loads the profile from its source, stores the result, and returns it; a later request can read the cached value instead of repeating the load.

Treat misses as a normal path, and define expiry or invalidation for data that changes. Add caching when repeated work and acceptable staleness justify the extra state; otherwise, leave the direct lookup alone.
