# PF3 baseline arm

## PF3-F-WRITE

At 5:10 each morning, Inez, the ferry mechanic, recorded the engine tick from the deck. On a rainy Tuesday, Bo held the phone while she opened the hatch.

“Is the ferry sick?” he asked.

“Only when we rush it,” Inez said.

The recording caught three knocks beneath the engine’s ticking. Before Inez could look, the horn called them back to shore. Bo pocketed the phone, still recording. As they crossed the wet deck, he heard Inez ask the unseen deckhand why he had moved the wrench.

## PF3-F-REVIEW

- Character and stakes: Marla’s action is clear, but “found the lost wallet” supplies no obstacle or personal stake.
- Connection: “The rain stopped” is a setting change without a connection to the wallet or Marla’s choice.
- Characterization: Marla returns the wallet, but the story gives no specific detail about her decision or Mr. Chen’s response beyond thanks.
- Ending and theme: “honesty always brings happiness” and “everyone who chooses kindness will be rewarded” state universal morals rather than developing them through the scene. “feeling proud” repeats that conclusion.

## PF3-F-REFACTOR

Leah watched the narrow road, her blue eyes fixed as her long brown hair whipped across her face, while the rescue truck slid toward the ditch. She knew she had to be brave. Leah took a deep breath, grabbed the rope, and pulled the driver to safety. Only then did she feel relieved.

## PF3-F-RECREATE

The old song played in the café while rain silvered the street. Nina watched the drops and remembered a summer she could not name: a suitcase by an open door, a train already waiting. When the singer finished, Nina folded the receipt, wrote an address on its back, and left it beside her cup. She walked into the night toward the station.

## PF3-P-WRITE

User impact: In `v2.4.0`, replace the CLI option `--cache-dir` with `--state-dir`.

PR #17 reports a benchmark of 1.8s before and 0.9s after, measured over 100 runs. No other release changes are supplied.

## PF3-P-REVIEW

- Template residue: stock opening (“Thanks for the great question!”), generic reassurance (“I hope this helps”), vague closing (“Let me know if you need anything else”), and the sign-off “Best regards, The Team.”
- Missing specificity: no file, line, behavior, or test name; no explanation of what “looks good overall” refers to; no concrete tests, acceptance condition, owner, or follow-up scope.

## PF3-P-REFACTOR

Timeline: At 14:00, the deploy failed and the team rolled it back. Recovery timestamp and duration: TODO.

Response: We fixed the problem, and the service recovered. Root cause and mechanism: TODO. Commands used: TODO. Impact metrics: TODO.

Follow-up: We will improve monitoring. Owner and due date: TODO. Everyone worked hard during the response.

## PF3-P-RECREATE

Caching can avoid repeating expensive work when the same data is requested again, but it adds freshness and eviction decisions.

Illustrative example: for a profile request, check `profile:user-42` first. On a hit, return the cached profile; on a miss, read the database, store the result with a bounded TTL, and return it. Invalidate or refresh that key when the profile changes, and define what happens if the cache is unavailable. The useful design is the one whose reuse, freshness, and failure behavior fit the data.
