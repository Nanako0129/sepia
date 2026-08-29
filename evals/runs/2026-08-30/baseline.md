# PF3 baseline arm

## PF3-F-WRITE

At 5:10 on a rainy Tuesday, Inez set her phone against the ferry’s rail and listened to the engine tick. She was the ferry mechanic; Bo, who was still a child, held the phone while she opened the hatch.

“Is the ferry sick?” Bo asked.

“Only when we rush it,” Inez said.

The recording caught three knocks from below, separate from the engine noise. Inez lifted her head. Before she could investigate, the horn called them back to shore. Bo pocketed the phone, still recording. As they crossed the deck, he heard Inez ask the unseen deckhand why he had moved the wrench.

## PF3-F-REVIEW

- The story has a clear action: Marla finds a wallet beside the bakery, returns it to Mr. Chen, receives his thanks, and walks home. The sequence is easy to follow, but the central action is summarized rather than developed.
- The sentence “Marla understood that honesty always brings happiness” states a general lesson instead of letting the wallet exchange carry the meaning. “Everyone who chooses kindness will be rewarded” widens that lesson beyond the supplied scene.
- “The rain stopped” and “She walked home feeling proud” provide a tidy close, but the ending resolves Marla’s feeling without adding a particular consequence or complication.
- The plain, compact voice is consistent. Dialogue and setting detail beyond the bakery are not applicable to the supplied story.

## PF3-F-REFACTOR

Defects:

- Appearance is stacked in “blue eyes” and “long brown hair,” while “heart pounded,” “stomach twisted,” and “cold sweat” stack familiar body-emotion cues.
- “She knew she had to be brave” and “courage means acting despite fear” explain the lesson instead of leaving it in the rescue.

Leah kept her blue eyes on the narrow road. Her long brown hair whipped across her face as the rescue truck slid toward the ditch. She was afraid, but took a deep breath, grabbed the rope, and pulled the driver to safety. When he was clear, she felt relieved.

## PF3-F-RECREATE

The old song played from the café’s radio, thin beneath the clink of cups. Nina looked out at the street. For a moment she remembered a summer she could not name: sun on a borrowed towel, the sharp smell of water, a door left open somewhere.

The singer finished. Nina left a coin beside her cup, smiled at the dark window, and walked into the night.

## PF3-P-WRITE

In `v2.4.0`, replace the CLI option `--cache-dir` with `--state-dir`.

PR #17 reports a benchmark of 1.8s before and 0.9s after over 100 runs.

## PF3-P-REVIEW

- “Thanks for the great question!” is generic thanks.
- “Your PR is a really thoughtful contribution” and “The implementation looks good overall” are broad praise without a specific implementation observation.
- “I hope this helps” and “Let me know if you need anything else” are generic offers of help.
- “Please consider adding tests” is vague: it names no behavior, scope, or acceptance condition.
- “Best regards, The Team” is a generic sign-off.
- The reply does not identify what the tests should cover or what concrete next step the recipient should take; no file or line details are supplied.

## PF3-P-REFACTOR

At 14:00, a deploy failed. The team rolled it back, and service recovered. The failure mechanism is TODO. Commands are TODO. Additional timestamps are TODO. Metrics are TODO.

Action: improve monitoring. Owner: TODO.

## PF3-P-RECREATE

A cache can avoid repeated work. On a cache read, use the stored result when one is available. On a miss, compute or fetch the result, return it, and store it for a later read.

Illustrative example: imagine an application that builds a user dashboard from the same inputs on each request. The first request is a miss, so the application builds the dashboard and stores the result. A later request reads that result instead of repeating the work. If the inputs change or the entry expires, the read is a miss and the dashboard is rebuilt.

Treat invalidation and stale data as part of the cache design. Measure the actual application before claiming a performance improvement; this example is illustrative and reports no benchmark.
