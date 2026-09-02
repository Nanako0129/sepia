# Pass 3 — Surface style

Run last, after structure is fixed. Evidence: LAMP/CHI 2025 (L), Reinhart et al. PNAS 2025 (P), Russell et al. ACL 2025 (R), Shaib et al. slop taxonomy (S), fiction/RP community ban lists (F). Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local. Prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention. Editing operations should skew **replace 74% / delete 18% / insert 8%** (L) — when in doubt, cut. The one exception that may grow text: adding concrete specificity.

## 1 The seven artifacts (professional-editor taxonomy, L)

Ordered by how often professional writers actually fixed each, which is the priority order:

| # | Artifact | Fix |
|---|---|---|
| 1 | Awkward word choice (28%) | Replace misused or off-register words. "Seem to + verb" → the verb itself, unless uncertainty is real. Fix unclear pronouns and excess passives. |
| 2 | Poor sentence structure (20%) | Split run-ons into two sentences. One tangled thought = two plain ones. |
| 3 | Redundant exposition (18%) | Delete what the scene already implies. The pattern "[main clause], [trailing participial phrase restating it]" → delete after the comma ("cast long shadows over the desolate landscape" → "cast a long shadow"). |
| 4 | Cliché (17%) | Replace with fresh, scene-specific language — **never with a blander paraphrase** (that is the documented machine failure). If nothing fresh is available, delete the line. |
| 5 | Lack of specificity | The only additive fix: real names, objects, numbers, actions from lived detail. If you lack the material, ask the user — filling in more generic description makes it worse. |
| 6 | Purple prose | Simplify. Long abstract-noun sentences conveying one feeling → short concrete sentences ("She cried. She cried for unfairness. She cried without relief."). |
| 7 | Tense inconsistency | Pin the tense; hunt drift inside paragraphs. |

## 2 Syntax templates to hunt

These part-of-speech shapes are 2–5× overrepresented in LLM prose and heavily edited out by professionals (L, P):

| Template | Examples | Fix |
|---|---|---|
| a/the [abstract noun] of [noun] (and [noun]) | a mix of pride and fear · a sense of wonder · a pang of nostalgia · the weight of expectation | Name the concrete thing or cut the wrapper noun |
| the [adj] [noun] of [possessive] | the intricate tapestry of its · the unspoken plea in her | Rewrite from scratch |
| Trailing/leading participial clause | "…, evading Show's heavy blows" · "Stuffing his mouth, Joe ran" | Break into its own short sentence with a finite verb (LLM usage: up to 5× human) |
| Nominalization | realization, determination, transformation as sentence subjects | Turn back into verbs (2× human rate) |
| Paired abstractions "X and Y" | desperation and resolve · curiosity and caution | Keep one |
| not only X but also Y · it's not X, it's Y | — | Say the one thing you mean |
| Rule of three | three parallel adjectives/clauses/images, everywhere | Two or four; break the rhythm |

## 3 Vocabulary

Merged ban list (R Table 12 + P excess-vocab + L signature phrases + F fiction slop). A single hit is not a verdict — **slop is cumulative** (S): count hits, and rewrite when they cluster.

| Class | Words/phrases |
|---|---|
| Abstract-grandeur nouns | tapestry, testament, symphony, kaleidoscope, landscape, realm, journey, beacon, camaraderie, solace, resilience, nuance, myriad |
| Performance verbs | delve, underscore, foster, harness, navigate, resonate, elevate, embrace, transcend, unravel, ignite, grapple, weave/weaving |
| Inflation adjectives | intricate, vibrant, palpable, profound, pivotal, crucial, seamless, robust, transformative, multifaceted, fleeting, bustling |
| Fiction slop (F) | ozone, petrichor, shimmering, thrums, gossamer, "barely above a whisper", "eyes gleam/glint/alight", "despite herself", "breath catches", "heart skips", "shivers down the spine", "voice like [material]" |
| Signature phrases (L) | unspoken, the weight of, hung in the air, the air was thick, in the pit of her/my stomach, a constant reminder of |
| Formula phrases (R) | paving the way, it's important to note, in a world of/where, a testament to, cautionary tale, "amidst" |
| Filter words (F) | felt, seemed, realized, noticed, knew, watched as — delete the filter, render the thing directly |

## 4 What to add back — the underused human register

Instruct-tuned models systematically suppress these (P: usage 13–80% of human rate). Restore them *to the degree the genre and the author's voice allow* — sprinkled, not poured:

| Restore | Examples |
|---|---|
| Contractions | don't, it's, wouldn't |
| Discourse particles and fillers | well, anyway, just, really, actually |
| Plain causal connectives | because (GPT-4o uses it at 20% of human rate), so |
| Hedges and emphatics | almost, sort of, for sure, obviously |
| Negation | "no answer was good enough" — synthetic negation runs at half human rate |
| Pro-verb do | "and she did" |
| Plain speech tags | *says/said* on repeat is human; rotating *notes, observes, remarks, muses* is machine elegance |
| First/second person, direct questions | where POV permits |
| Coarse or blunt language | where the register genuinely calls for it |

## 5 Genre alignment

Reinhart et al. report that instruction-tuned models favor an informationally dense, noun-heavy style and struggle to match genre-aligned variation (P). Before editing, state the target register (literary / pulp / YA / essayistic) and edit toward *that* — a de-AI'd thriller and a de-AI'd literary story should not end up in the same voice. Sentence length variance, contraction rate, and vocabulary plainness are genre parameters, not universal constants.

## 6 The read-aloud test

Grammatically correct but unsayable is a distinct slop dimension (S: "the earthen area that formerly held the puddle was now dry"). Read dialogue and any sentence you rewrote aloud (mentally): if no native speaker would say it or write it in a letter, redo it in speech-shaped syntax.

## 7 False-positive whitelist

Do **not** flag or "fix" these — over-correction is its own fingerprint:

| Not evidence of AI | Why |
|---|---|
| Correct grammar and clean punctuation | Plenty of humans write cleanly; imperfection-injection is a detectable gimmick |
| A single em-dash, semicolon, or "delve" | One hit means nothing; only clusters count |
| Neutral or formal tone in a formal genre | Register match beats forced casualness |
| A banned word inside quoted dialogue or an in-world document | Quoted material keeps its texture |
| The author's own verified habits | If the user's samples use em-dashes or "moreover," those stay |
| Moderate ordinary sentences | Slack is human; do not polish every line to distinctiveness |

> Informality is not a disguise. In Russell et al.'s tested humanization conditions, expert readers still detected other machine-patterned cues; adding casual language alone did not remove them. The claim does not establish that every informal model output is detectable.
