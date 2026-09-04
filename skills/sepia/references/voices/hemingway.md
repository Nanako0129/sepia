# Voice profile — Hemingway (built-in, experimental)

Status: a built-in voice profile for the experimental interface in `voice-skills.md`. It loads only when the user opts in ("apply the Hemingway voice"); a review may report a fit for it (the rule and its data live in `references/voices/registry.md`) but never applies it. Everything in `voice-skills.md` governs: sepia's architecture decisions first, 3–5 voice moves per piece, uniformity findings at full strength, venue precedence on professional routes, never invent.

Evidence tiers, kept apart (IDs in the research ledger): the author's own statements (`HEMINGWAY-*`, author testimony), the Kansas City Star style sheet (`KC-STAR-STYLE-1915`, style manual), criticism and corpus work (`LEVIN-1951`, `SMITH-1983`, `LAMB-2010`, `RICE-2017`, `IHRMARK-NILSSON-2021`, `LIAN-2025`). None of these is a measurement of AI text; the sepia-axis column below is a Sepia inference linking the move to StoryScope/LAMP findings that live in the passes. Digest: `research/hemingway.md`.

## The method in the author's words

- Omission: "If a writer of prose knows enough of what he is writing about he may omit things that he knows and the reader, if the writer is writing truly enough, will have a feeling of those things as strongly as though the writer had stated them." (*Death in the Afternoon*, 1932; 46 words)
- The iceberg: "The dignity of movement of an ice-berg is due to only one-eighth of it being above water." (same, 17 words) — "Anything you know you can eliminate and it only strengthens your iceberg. It is the part that doesn't show." (Paris Review, 1958; 20 words)
- The true sentence: "If I started to write elaborately, or like someone introducing or presenting something, I found that I could cut that scrollwork or ornament out and throw it away and start with the first true simple declarative sentence I had written." (*A Moveable Feast*, 1964; 43 words)
- Made, not described: "After you learn to write your whole object is to convey everything, every sensation, sight, feeling, place and emotion to the reader." / "It is made; not described." ("Monologue to the Maestro", *Esquire*, 1935)
- The newspaper rules he kept: "Use short sentences. Use short first paragraphs. Use vigorous English. Be positive, not negative." (`KC-STAR-STYLE-1915`)

**The precondition is knowledge.** Omission works because the writer knows what was left out. Under this voice the existing specificity rules stay at full strength — on the fiction route, SKILL.md's "Never invent specifics" guardrail and style-pass §1 row 5 (lack of specificity); on professional routes, professional-pass check 5. A fact the writer does not have is a gap to ask about, not something to omit around. Omission that hides ignorance produces vagueness, and vagueness is a tell.

## Fiction route — the iceberg

| Move | Source | Sepia axis it moves (inference) | Known cost |
|---|---|---|---|
| Leave the meaning out: no sentence that says what the story is about, no character realizing the theme, no narrator gloss on the ending | Omission (DIA 1932; Paris Review 1958); Smith 1983 shows the cut endings in manuscript | Rubric Group A: thematic explicitness, narratorial thematic commentary (narrative-pass §1) | Thematic explicitness drops toward the low pole; expect an over-correction advisory and report it as the voice's cost. Keep one thing the reader is allowed to understand |
| Emotion as action and speech: what she does, what is said, what is not answered | "It is made; not described." | Rubric Group B: emotion via embodied sensation → behavior-led (narrative-pass §5) | Depth of interior access drops toward the low pole; expect an over-correction advisory and report it as the voice's cost. Plain naming stays allowed in one or two places — the author did it ("he felt quite sure that he would never die", "Indian Camp", 1925, US public domain) |
| Weather is weather, objects are objects: setting does not mirror the inner state | Omission; Baker 1972 ("prune language and avoid waste motion") | Rubric Group B: setting mirrors inner state (narrative-pass §5) | None beyond the general slack rule |
| Open in the situation, not the establishing shot | "cut that scrollwork … like someone introducing or presenting something"; Lamb 2010 on openings | discourse-pass §4 machine opening | None |
| Let information move through talk, including what is not said | Lamb 2010 (dialogue's role); Rice 2017 (twice the average dialogue share) | Rubric Group C: protagonist introduced in-dialogue (human marker); Group E dialogue proportion | Dialogue share is a calibration parameter: "direct speech dominates" is a measured Gemini fingerprint. Do not push past the human band |
| Base rhythm of short declaratives, broken by an occasional paratactic run joined with "and" | *A Moveable Feast*; Levin 1951 (parataxis); Rice 2017 (short sentences define him less over his career) | style-pass §1 row 2 (sentence structure); voice-skills uniformity rule | The break is the point. Uniform short sentences are the metronome that `voice-skills.md` names as a hard finding |
| Keep the plain adverbs: then, now, never; drop the -ly manner adverbs | Rice 2017 (more adverbs than average, almost none in -ly) | style-pass §4 restore plain connectives and particles | None |

Select 3–5 of these per piece. The paratactic run is one move, used once or twice, not a texture.

## Professional routes — the Kansas City Star rules

| Rule (verbatim) | Sepia check it maps to | Note |
|---|---|---|
| "Use short sentences." | professional-pass check 10; style-pass §1 row 2 | Base rhythm, not a ceiling. Check 9 (sameness of rhythm) still applies |
| "Use short first paragraphs." | professional-pass check 3 (relevance); domains: answer first | Same as the domain files' lead rule |
| "Use vigorous English." | style-pass §1 row 1 (word choice); §3 performance verbs are the counterfeit of this | Vigorous means the concrete verb, not the inflated one |
| "Be positive, not negative." | **CONFLICT** with style-pass §4 (synthetic negation runs at half the human rate; restoring some is a human marker) | Handled by the precedence rule in `voice-skills.md`: a voice move that directly conflicts with a §4 restore item is surfaced with both rules named and left to the user |
| "Avoid the use of adjectives, especially such extravagant ones as splendid, gorgeous, grand, magnificent, etc." | style-pass §3 inflation adjectives; §1 row 6 purple prose | Same list, older source |
| "Eliminate every superfluous word." | professional-pass check 2 (density) | Density fails in both directions; a cut that drops a required caveat fails check 2 too |
| "This is common abuse of the conjunction." (a "but" that implies a contrast the facts do not carry) | discourse-pass §1 QUD check; professional-pass check 10 | A connective must carry a relation that is actually there |
| "He died of heart disease, not heart failure — everybody dies of heart failure." | professional-pass check 5 (specificity) | Precision is a fact question first: the number, the timestamp, the key |

## Voice fit

The rule and the signature/anti-signal data for this profile live in `references/voices/registry.md`, which sepia loads on review and refactor stage 1. This body loads only after the opt-in phrase `apply the Hemingway voice`; composition, precedence, and uniformity rules stay in `voice-skills.md`.

## Worked examples

Both Afters were produced as write/recreate from the Before **plus the source facts listed under it**. Those facts came from the specimen's author; they are not in the Before, and a refactor that has not been given them may not add them (SKILL.md "Never invent specifics"). The examples show the voice's moves, not permission to invent.

### A — fiction (specimen written for this profile; not Hemingway's text)

Before:

> The letter sat on the kitchen table like an accusation. Mara's chest tightened as she read it a second time, the words blurring as grief and betrayal warred inside her. Outside, the rain had begun again, as if the sky itself understood what she had lost. She realized then that trust, once broken, could never truly be mended, and that the mother she had known had been a stranger all along.

Source facts supplied by the author (not in the Before): the mother kept receipts on the kitchen table; the kitchen window over the sink was open; Mara made tea; Teo lives forty minutes away by highway.

After (moves used: leave the meaning out; emotion as action and speech; weather is weather; one paratactic run; plain "Then"):

> The letter was on the kitchen table where her mother kept the receipts. Mara read it standing up. Then she sat down and read it again.
>
> "You knew," she said.
>
> Nobody answered. It was raining and the window over the sink was open and the rain came in on the sill and she did not close it. She put the kettle on. When it boiled she made the tea and drank it and it was too hot and she drank it anyway.
>
> Teo's was forty minutes on the highway. She put the letter in her coat.

| Change | Move | Axis |
|---|---|---|
| "trust, once broken…" and "a stranger all along" deleted | Leave the meaning out | Group A thematic explicitness, narratorial commentary |
| "chest tightened", "grief and betrayal warred" → standing, sitting, the open window, the too-hot tea | Emotion as action | Group B embodied → behavior-led |
| Rain no longer "understood what she had lost" | Weather is weather | Group B setting mirror |
| "You knew," she said. Nobody answered. | Information through talk and its absence | Group C / E dialogue |
| "It was raining and the window … and the rain … and she did not close it" | The paratactic run, once | Sentence-length variance |
| "like an accusation", "as if the sky itself" deleted | KC Star adjectives; mannered prose | style-pass §1 cliché / purple prose |
| "Then" kept | Plain adverbs | style-pass §4 |

Known cost of this After: interior access sits near the low pole (advisory expected); a whole story in this register would trip the uniformity finding. The moves were selected for one scene, not a house style.

### B — professional (incident summary)

Before:

> During the course of the incident, which unfortunately began at approximately 14:02 UTC, our team was not able to immediately identify the root cause, but eventually the issue was traced back to a misconfiguration in the retry queue, which caused a significant and highly impactful cascade of failures across multiple downstream services that were not expecting such a magnificent volume of traffic.

Source facts supplied by the author from the incident record (not in the Before): 412 retries landed inside one 200 ms window; the cause was found at 14:41; `RETRY_JITTER=full` was set at 14:47.

After:

> At 14:02 UTC the retry queue began resending failed jobs without jitter. Downstream services received 412 retries inside one 200 ms window and rate-limited each other. We found the cause at 14:41 and set `RETRY_JITTER=full` at 14:47.

| Change | Rule | Check |
|---|---|---|
| One 71-word sentence → three | "Use short sentences." | check 10; style §1 row 2 |
| "unfortunately", "significant and highly impactful", "magnificent" deleted | "Avoid the use of adjectives…" | style §3 |
| "was not able to immediately identify" → the time the cause was found | "Be positive, not negative." | postmortems domain (timestamps, mechanism); the §4 negation conflict does not arise here because the positive form carries more information, not less — that is the test |
| "During the course of", "approximately", "eventually" deleted | "Eliminate every superfluous word." | check 2 |
| ", but eventually the issue was traced" | "common abuse of the conjunction" | QUD check |
| 412, 200 ms, 14:41, 14:47 added | Precision | check 5; taken from the source facts above, never invented — without them the After would stop at the cause and leave a TODO |

## Grounding

One worked example per route, written for this profile, not measured evidence. Blind review of the fiction After by a fresh-context reviewer with the voice declared (2026-09-04): one scene, 99 words. The uniformity row did not fire: paragraph lengths 3/1/4/2 sentences, one paratactic run against short declaratives, the single quoted line standing alone. Group B recorded emotion as behavior-led and setting mirror at 2/5. Two over-correction advisories, depth of interior access 1/5 and thematic explicitness 1/5, reported as the voice's cost. Style scan recorded no hits. The Voice fit line read none on anti-signal (a); that review predates the declared-voice form, under which the line reads `hemingway — applied`.
