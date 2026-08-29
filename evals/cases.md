# PF3-EVAL-V1 cases

All inputs below were authored for this pack. They are short, original
prompts, not excerpts from published works; the old-song case contains no copyrighted passages or lyrics. Each arm must preserve the protected
facts and follow the exact operation request. Human-only questions are
recorded for a later editor and must remain `NOT_RUN` in `grades.md`.

## Cases

### PF3-F-WRITE

| Field | Content |
|---|---|
| Route | Fiction; `write` |
| Original input | At 5:10 each morning, Inez, the ferry mechanic, records the engine tick from the deck. One rainy Tuesday, a child named Bo holds the phone while Inez opens the hatch. Bo asks whether the ferry is sick. Inez says, “Only when we rush it.” The recording catches three knocks that are not engine noise. Before she can investigate, the horn calls them back to shore. Bo pockets the phone, still recording, and hears Inez ask the unseen deckhand why he moved the wrench. |
| Exact request | Write a short literary scene from this premise. Keep the maritime setting plain and uneasy, let the child remain a child, and do not explain the meaning of the knocks. |
| Protected facts / voice | Inez is the ferry mechanic; Bo is a child holding a phone; the time is 5:10 on a rainy Tuesday; there are three non-engine knocks, a horn call to shore, and a moved wrench. The voice is concrete, quiet, and unresolved. |
| Human-only questions | Would an editor hear a child’s question as child-sized rather than adult explanation? Does the quiet maritime unease feel earned? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a newly written fiction scene, not a review, plan, or explanation. |
| I2 | The route and operation remain fiction `write`; the scene begins from the recording premise. |
| I3 | The output preserves the named people, ferry mechanic role, child-held phone, rainy Tuesday, and 5:10 detail. |
| I4 | The three knocks, horn return, and moved wrench remain present without a resolved or moralizing explanation. |

### PF3-F-REVIEW

| Field | Content |
|---|---|
| Route | Fiction; `review` |
| Original input | Marla found the lost wallet beside the bakery. She returned it to Mr. Chen, and he thanked her. The rain stopped. Marla understood that honesty always brings happiness, and everyone who chooses kindness will be rewarded. She walked home feeling proud. |
| Exact request | Review this original story using the narrative rubric. Diagnose only, quote short evidence, and do not edit or rewrite the story. |
| Protected facts / voice | Marla finds and returns a wallet beside a bakery; Mr. Chen thanks her; rain stops; the narrator states a lesson about honesty and kindness; Marla walks home proud. Keep the plain, compact voice when quoting. |
| Human-only questions | Would an editor agree that the stated lesson outweighs the scene? Is the diagnosis useful to the person who wrote this small story? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a diagnosis-only fiction review and contains no replacement story. |
| I2 | The route and operation remain fiction `review`, with rubric-style observations rather than a rewrite. |
| I3 | The review quotes or accurately identifies the wallet, bakery, thanks, and walk-home facts without inventing context. |
| I4 | The review identifies the explicit moral generalization and tidy resolution with short evidence, while marking unsupported dimensions as not applicable when needed. |

### PF3-F-REFACTOR

| Field | Content |
|---|---|
| Route | Fiction; `refactor` |
| Original input | Leah’s blue eyes watched the narrow road while her long brown hair whipped around her face. Her heart pounded, her stomach twisted, and cold sweat gathered as the rescue truck slid toward the ditch. She knew she had to be brave. Leah took a deep breath, grabbed the rope, and pulled the driver to safety. She felt relieved and understood that courage means acting despite fear. |
| Exact request | Refactor this story minimally. Preserve its structure, facts, and voice while reducing stacked appearance and body-emotion cues and the explanatory moral ending. Add no events or characters. |
| Protected facts / voice | Leah, her blue eyes and long brown hair, the narrow road, the rescue truck and ditch, the rope, the driver’s rescue, fear, and relief. Preserve the linear order and minimal in-place revision. |
| Human-only questions | Does the edit still sound like the original narrator? Would an editor consider the reduction restrained rather than a new story? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a minimal fiction `refactor`, not a fresh story, diagnosis, or explanation. |
| I2 | Leah, the narrow road, rescue truck, ditch, rope, driver, and rescue outcome remain in linear order. |
| I3 | The appearance and embodied-emotion cluster is reduced or varied without deleting the scene’s fear and relief. |
| I4 | The output adds no event or character and removes or concretizes the explanatory “courage” lesson. |

### PF3-F-RECREATE

| Field | Content |
|---|---|
| Route | Fiction; `recreate` |
| Original input | The old song played in the café. Nina looked out at the street and remembered a summer she could not name. The singer finished, and Nina knew that every ending is a new beginning. She smiled and walked into the night. |
| Exact request | Recreate this as a fresh short story. Keep the premise anchors, replace generic explanation with concrete choices, and do not quote lyrics or invent a recognizable song passage. |
| Protected facts / voice | An unspecified old song plays in a café; Nina looks at the street, remembers an unnamed summer, hears the singer finish, smiles, and walks into the night. The rewrite is fresh, concrete, and contains no lyrics. |
| Human-only questions | Does the added specificity feel earned rather than decorative? Would an editor accept the ending without the original aphorism? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a full fiction `recreate`, not a review, patch list, or sentence-by-sentence edit. |
| I2 | The café, old song, Nina, street, unnamed summer, singer’s finish, smile, and walk into night remain recognizable. |
| I3 | The output contains no quoted lyrics or invented passage attributed to an existing song. |
| I4 | The generic “every ending” explanation is replaced by concrete story material without claiming facts absent from the input. |

### PF3-P-WRITE

| Field | Content |
|---|---|
| Route | Professional prose; release notes; `write` |
| Original input | Version `v2.4.0` changes the CLI option `--cache-dir` to `--state-dir`. PR #17 reports a benchmark of 1.8s before and 0.9s after over 100 runs. No other release changes are supplied. |
| Exact request | Write concise release notes for maintainers. Put user impact first, preserve the exact facts and benchmark conditions, and invent no additional changes or claims. |
| Protected facts / voice | Exact version `v2.4.0`; exact flag mapping; PR #17; 1.8s to 0.9s over 100 runs; release-note register; no other supplied changes. |
| Human-only questions | Would a maintainer find the flag migration and impact clear? Is the benchmark caveat proportionate to the evidence? |

| Invariant | Observable check |
|---|---|
| I1 | The output is release notes for `v2.4.0`, not an article, review, or implementation plan. |
| I2 | The CLI mapping is exactly `--cache-dir` to `--state-dir`, and PR #17 is retained. |
| I3 | The benchmark is exactly 1.8s to 0.9s over 100 runs, with no changed unit or invented test conditions. |
| I4 | No unsupplied feature, compatibility promise, or broad performance claim is added. |

### PF3-P-REVIEW

| Field | Content |
|---|---|
| Route | Professional prose; PR reply; `review` |
| Original input | “Thanks for the great question! Your PR is a really thoughtful contribution. I hope this helps. The implementation looks good overall, but please consider adding tests. Let me know if you need anything else. Best regards, The Team.” |
| Exact request | Review this PR reply only. List concrete template residue and missing specificity; do not rewrite it, invent file or line references, or add praise. |
| Protected facts / voice | Review-only operation; the reply contains generic thanks, broad praise, an offer of help, a vague test request, and a team sign-off. Keep findings short and evidence-based. |
| Human-only questions | Would the recipient know exactly what to do next? Does the tone fit a maintainer’s actual PR venue? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a diagnosis-only PR-reply review and does not rewrite the reply. |
| I2 | The route remains professional `review`, with findings tied to the supplied wording. |
| I3 | The review identifies at least one concrete template phrase and the vague test request without fabricating repository details. |
| I4 | The review preserves the short venue context and does not add unsupported praise, file paths, or line numbers. |

### PF3-P-REFACTOR

| Field | Content |
|---|---|
| Route | Professional prose; postmortem; `refactor` |
| Original input | At 14:00 the deploy failed and the team rolled it back. We fixed the problem and service recovered. We will improve monitoring. Everyone worked hard. |
| Exact request | Refactor this into a concise, blameless postmortem while preserving every known fact. Mark missing timestamps, commands, mechanism, metrics, and owners as `TODO`; do not invent a root cause. |
| Protected facts / voice | At 14:00 a deploy failed; the team rolled back; service recovered; monitoring improvement is intended; no cause, command, metric, or owner is supplied. Use a blameless, mechanism-focused postmortem voice and explicit `TODO`s. |
| Human-only questions | Would an incident reviewer see the missing mechanism represented honestly? Is the action item specific without pretending an owner is known? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a minimal postmortem `refactor`, not a newly invented incident report. |
| I2 | The 14:00 failed deploy, rollback, recovery, and monitoring action remain present. |
| I3 | Missing mechanism, commands, metrics, timestamps, and owners are marked `TODO` or explicitly unavailable; none are invented. |
| I4 | The prose is blameless and removes unsupported generic praise without assigning fault or adding an unprovided root cause. |

### PF3-P-RECREATE

| Field | Content |
|---|---|
| Route | Professional prose; technical article; `recreate` |
| Original input | Caching makes applications faster. First, add a cache. Next, read from it. Finally, remember to handle misses. Good caching improves performance and user experience. |
| Exact request | Recreate this as a concise technical article for engineers using one concrete but clearly illustrative example. Keep the advice accurate, label the example as illustrative, and imply no measured performance. |
| Protected facts / voice | The article concerns repeated work, cache reads, cache misses, and careful performance language. No backend, benchmark, or production result is supplied. The rewrite is concise and technically grounded. |
| Human-only questions | Would an engineer find the example actionable? Does the article take a clear enough position without overstating its evidence? |

| Invariant | Observable check |
|---|---|
| I1 | The output is a complete technical-article `recreate`, not a review, outline, or patch list. |
| I2 | The article retains cache reads, misses, and the reason caching can avoid repeated work. |
| I3 | Its one concrete example is explicitly illustrative and introduces no measured benchmark or production result. |
| I4 | The article uses accurate technical advice without claiming facts about an unspecified backend or application. |
