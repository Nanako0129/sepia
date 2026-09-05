# Pass 3 — Surface style

Run last, after structure is fixed. Evidence: LAMP/CHI 2025 (L), Reinhart et al. PNAS 2025 (P), Russell et al. ACL 2025 (R), Shaib et al. slop taxonomy (S), fiction/RP community ban lists (F), Desaire et al. 2023 (D), Gude et al. 2026 (G), Muñoz-Ortiz et al. 2024 (M), 朱君輝 et al. CCL 2023 on Chinese (Z), Freeburg 2026 (E). Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local. Prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention. Editing operations should skew **replace 74% / delete 18% / insert 8%** (L) — when in doubt, cut. Text may grow for one reason, concrete specificity; repair is not growth (§4, last paragraph).

## 1 The seven artifacts (professional-editor taxonomy, L)

Ordered by how often professional writers actually fixed each, which is the priority order:

| # | Artifact | Fix |
|---|---|---|
| 1 | Awkward word choice (28%) | Replace misused or off-register words. "Seem to + verb" → the verb itself, unless uncertainty is real. Fix unclear pronouns and excess passives. |
| 2 | Poor sentence structure (20%) | Split run-ons into two sentences. One tangled thought = two plain ones. |
| 3 | Redundant exposition (18%) | Delete what the scene already implies. The pattern "[main clause], [trailing participial phrase restating it]" → delete after the comma ("cast long shadows over the desolate landscape" → "cast a long shadow"). |
| 4 | Cliché (17%) | Replace with fresh, scene-specific language — **never with a blander paraphrase** (that is the documented machine failure). If nothing fresh is available, delete the line. |
| 5 | Lack of specificity | The additive fix (§4, last paragraph): real names, objects, numbers, actions from lived detail. If you lack the material, ask the user — filling in more generic description makes it worse. |
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

**Restoring is not padding.** Machine editing of human prose leaves a trace of its own, and it is not the words it changes: relative to their human sources, machine-edited texts show a sharp fall in lexical density (share of content words; d = −3.10) with entropy down and lexical diversity barely up — the reverse of the generation footprint, which raises both (Shan et al. 2026, ledger `SHAN-EDIT-2026`; measured on English, extended to other languages as a Sepia inference). Read plainly: an editor's fingerprint is the filler it pours in around the content. So on refactor, before finishing, run two tests. The **deletion test** on every word or phrase you added: strike it; if the sentence still parses and still says the same thing, it was filler — delete it. The **reversion test** on every replacement: put back what it replaced; if the old wording was sound and said the same in fewer words, keep the old. Repair fails both tests and stays: the article and preposition a broken sentence needs, the subject a split run-on needs, the verb that replaces a nominalization, the reordering that makes an ungrammatical sentence grammatical; repair is not growth. The items in the table above are restored on purpose and would fail neither test's spirit, so they are allowed on one condition: the same edit must have removed filler somewhere in the passage, and the passage must not end longer than it began. Generation and editing leave different traces and are checked differently: §2–3 and §5 hunt the generation trace; this paragraph guards the editing trace.

## 5 Genre alignment and sentence rhythm

Reinhart et al. report that instruction-tuned models favor an informationally dense, noun-heavy style and struggle to match genre-aligned variation (P). Before editing, state the target register (literary / pulp / YA / essayistic) and edit toward *that* — a de-AI'd thriller and a de-AI'd literary story should not end up in the same voice. Sentence length variance, contraction rate, and vocabulary plainness are genre parameters, not universal constants.

**What is measured about sentence length.** The *spread* of sentence lengths inside a text is smaller in LLM output than in human writing in each of the four studies that measured it, across two model generations and two languages: within-paragraph standard deviation and the length difference between consecutive sentences both run higher in human paragraphs (D, values not printed); sentences of 1–15 tokens make up 32–33% of human news sentences against 1–4% for 2025 instruction-tuned models (G); sentences of 41 tokens or more are 12.0% of human sentences against 5.5% for a 2023 base model (M); Chinese answers show a per-answer sentence-length SD of 9.248 vs 6.729 words (Z). Three further English studies find the same direction only *between* texts (the spread of per-essay means), which is consistent but is not evidence for a within-text check and is not counted here. The *mean* is not a signal: against 2023 base models human sentences were about 10–20% longer, while 2025 aligned models write sentences 15–30% longer than humans (G, the paper's own wording), and on one Chinese corpus the direction flips with the unit of count (Z). No English study prints a within-text SD for humans versus LLMs, and the Chinese figure above comes from one corpus and one 2023 model, so no numeric threshold exists to quote, and none is set here.

**Check (Sepia inference).** Look for runs of adjacent sentences of about the same length — three or more in a row; "three" and "about the same" are reading conventions, not measured limits. This is the within-text form of D's consecutive-sentence-difference feature, and it works in any language and any unit of count as long as the unit is used consistently. Such a run is a *candidate* signal that counts only alongside other hits (slop is cumulative, §3). Do not score a passage by counting sentences under or over a length cutoff: the tail rates above are corpus-level and genre-specific, measured in tokens on news leads (G, M) and in words on science paragraphs (D), so a paragraph with no very short or very long sentence is ordinary human prose, and no per-passage cutoff can be derived from them. The check needs running prose of at least paragraph length, which is the unit D measured: a one-line reply, a bullet list, a table, or a commit-style release note has no rhythm to measure, and the scan reports `none`. For Chinese, `languages/zh.md` gives the same check with the Chinese numbers.

**Fix.** Break the run by moving words, never by adding them (the 74/18/8 rule above): split one long sentence, merge two short ones, or delete a clause. Which way to break it comes from the text — a run of long sentences wants one short one, a run of short ones wants one long one. Do not shorten everything: a passage of uniformly short sentences is the same defect seen from the other side, and it reads as pastiche. One measured prior may inform the direction: when the model that produced the text under check — the author on review and on refactor's diagnostic stage, the executor on write — is one of the four 2025 aligned releases G measured (Qwen 2.5, LLaMA 3.3, Mistral v0.3, GPT-4o, on news leads), the short sentences are the ones that went missing; for every other family, including Claude and Gemini, no sentence-length study exists, and a current executor reviewing human or older-model text does not import the prior either.

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
| Punctuation density, or a comma/period count | Measured directions contradict: on one Chinese Q&A corpus, punctuation density reads 0.135 human vs 0.136 ChatGPT (Z) while the punctuation share of tokens reads 16.0% vs 13.4% (Guo et al. 2023, same corpus); in English news the human share is 11.88% against 10.77–12.14% for four base models, one of them above human (M). No per-type human-vs-LLM count (comma, period, semicolon) exists for English or Chinese. The English pipeline that Pangram described in its 2025 workshop paper (a 12B-parameter classifier) lower-cased and unidecode-normalized input before scoring, which collapses typographic variants toward ASCII (an em dash arrives as two hyphens, curly quotes as straight ones) rather than erasing them; its 2026 architecture is different and its preprocessing undescribed. That weakens glyph choice as something such a detector reads without ruling it out; the whitelist rests on the contradictory measurements above, not on this |
| Em dash frequency as a model-agnostic tell | Measured per 1,000 words across 2025–26 releases: 10.62 (GPT-4.1), 9.09 (Claude Opus 4.6), 1.43 (GPT-5.4), 0.00 (Llama 3.x), against a human mean of 3.23 from eight essays (E). It is a release property, so the cluster rule above and the release-scoped prose layer in `model-fingerprints.md` apply — never a blanket rule |
| Paragraph count or average paragraph length | Directions contradict across corpora: LLM paragraphs longer in how-to text (82.01 vs 68.83 words), shorter in generated papers (39.82 vs 51.12), and more numerous in Chinese answers (3.681 vs 1.442). Only uniformity of paragraph length *within* the text is a signal (`discourse-pass.md` §3) |

> Informality is not a disguise. In Russell et al.'s tested humanization conditions, expert readers still detected other machine-patterned cues; adding casual language alone did not remove them. The claim does not establish that every informal model output is detectable.
