# Pass 1 — Narrative architecture

Seven decision groups. Each lists the measured human-vs-AI gap, what to do when **generating**, and what to check when **revising**. Numbers are from StoryScope (S), Beguš 2024 (B), Xu et al. PNAS 2025 (X), Nonaka & Perry 2025 (N), QUDsim (Q), and, for the one row that names it, Rohrbacher et al. 2026 (ledger `ROHRBACHER-2026`, cited by ID); percentages and frequencies read *human vs AI*. Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local. Generate/Revise prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention.

Work through all seven groups when filling the architecture sheet, but **enact only 3–5 human-leaning moves per story** (see SKILL.md Calibration). The groups marked ⚑ were absent from the tools sampled in the repository's 2026-08-27 ecosystem snapshot; treat that as a bounded product observation, not proof of universal zero coverage.

## Architecture sheet template

Fill this before drafting (Workflow A) or as the diagnosis summary (Workflow B):

| Decision | Choice for this story | Target band |
|---|---|---|
| Theme handling | stated / implied / withheld | implied by default |
| Subplot | none / parallel / contrasting / independent | one subplot, ~40% of stories |
| Resolution driver | protagonist choice / mixed / external | mixed or external ~50% |
| Ending mode | external act / internal acceptance / partial / open / catastrophic | avoid internal-acceptance default |
| Time structure | linear / moderate anachrony / braided | moderate (2–3 on a 1–5 scale) |
| Revelation pacing | front-loaded / even / back-loaded | back-loaded |
| Emotion strategy | mix of: explicit labels / behavior / embodied / ambiguous | behavior-led mix; embodied only at peaks |
| Protagonist introduction | description / in-action / in-dialogue / thought / others' reports | in-dialogue or in-action |
| Moral stance on protagonist | affirmative / tragic-flaw / ambivalent / antiheroic | ambivalent ~60% |
| Real-world anchors | list actual works, places, brands to name | ≥1 explicit named reference |
| Network shape | who never meets whom; who dislikes whom | sparse, net-neutral affect |
| Rarity move | the one structural choice atypical for this premise | exactly one |

## 1 ⚑ Theme: stop explaining it

| Feature | Human | AI |
|---|---|---|
| Narrator explicitly states the theme (S) | 52% | 77% |
| Thematic explicitness, 1–5 (S) | 3.28 | 3.94 |
| Dialogue used for philosophical debate (S) | 34% | 59% |
| Moral/philosophical weighting, 1–5 (S) | 3.26 | 3.68 |
| Thematic unity, 1–5 (S) | 4.41 | 4.74 |

**Generate:** Decide the theme, then trust the events to carry it. The narrator never summarizes the lesson; the grieving character's arc does **not** end with what she learned. Dialogue does plot and relationship work — characters argue about the rent, not about the nature of grief. Let one scene or image exist for texture alone, serving no theme (humans score 4.4/5 on unity, not 5/5 — near-total unity is the tell, total unity is worse).

**Revise:** Search the last three paragraphs and any narrator generalization ("That is how people are", "It was then she learned…", "In the end, what mattered was…") — cut or convert to a concrete action or image. Where dialogue debates ideas, rewrite so the disagreement is about something specific the characters want. If a symbol is explained in-text, delete the explanation and keep the symbol.

> Beguš reports recurring moralizing final lines such as "love knows no boundaries" in the tested model stories. Treat that pattern as a candidate signal, not evidence that a conclusive ending is necessarily machine-written.

## 2 ⚑ Plot: loosen the single track

| Feature | Human | AI |
|---|---|---|
| No subplots at all (S) | 57% | 79% |
| Subplot thematically parallel to main plot (S) | 42% | 21% |
| Causal-chain continuity, 1–5 (S) | 3.92 | 4.20 |
| Plot elements that reappear on regeneration — "drop ratio" (X) | 3.7% | 9–11% |

**Generate:** Give roughly two in five stories a subplot; when present, let it echo the main theme obliquely rather than restate it. Allow the causal chain to break once: an episode that isn't caused by the inciting incident, a consequence that arrives from offstage. Plant one detail that never fires — humans leave loose ends; the fully-paid-off setup inventory is machine bookkeeping.

**Revise:** Outline the draft as a beat list. If every beat is caused by the previous beat in one unbroken line to the climax, sever one link: move a cause offstage, or insert an event with its own origin. If the story has no second thread and its length can carry one, braid one in.

**Echo test (X):** for each turning point ask — *if this premise were regenerated twenty times, would this same turn appear again?* The helpful stranger, the problem that solves cleanly, the reconciliation on schedule: these reappear. Replace inevitable turns with one that requires this story's particulars. Kafka's traffic cop says "Give it up!" and walks away; twenty regenerations produce twenty cops giving directions.

## 3 Endings and resolution

| Feature | Human | AI |
|---|---|---|
| Resolution driven by protagonist's own choice (S) | 46% | 69% |
| Resolution via internal understanding/acceptance (S) | 27% | 47% |
| Morally ambivalent protagonist (S) | 59% | 38% |

**Generate:** Do not default to the arc where the protagonist, having grown, chooses the resolution and makes peace with it — that compound default (agency + acceptance + growth) is the strongest ending fingerprint in the data. Half the time, let chance, other people, or institutions decide the outcome. Endings may be partial, open, or catastrophic. The protagonist's final moral position can stay mixed: vindicated in the event, wrong in the act.

**Revise:** If the draft ends with the protagonist deciding + accepting + understanding, change at least one leg of the tripod. Cut denouement paragraphs that settle every account; ending one beat *earlier* than feels complete is usually the fix.

## 4 ⚑ Time: linearity is a choice, not a default

| Feature | Human | AI |
|---|---|---|
| Chronological discontinuity, 1–5 (S) | 2.40 | 2.12 |
| Anachrony (flashback/flash-forward) intensity, 1–5 (S) | 2.58 | 2.31 |
| Nonlinear framing used to delay disclosure, 1–5 (S) | 1.96 | 1.68 |
| Recontextualization depth after a reveal, 1–5 (S) | 3.28 | 2.95 |
| Revelation pacing (human fingerprint, S) | back-loaded | even/front-loaded |

**Generate:** The human band is *moderate* nonlinearity — a story that opens at the funeral and spirals back through decades, not a shuffled puzzle-box. Use time jumps to **stage information**: hold back the cause, open with the effect. Aim reveals so they force rereading — the best twist recolors earlier scenes (target 3/5, not a twist that changes nothing and not a total inversion). Keep the biggest disclosure late (back-loaded pacing is a measured human fingerprint).

**Revise:** If the draft narrates first-cause-to-final-effect in order, find the scene whose impact grows when withheld and move it. Check that DeepSeek-style front-loading (all context delivered before the story starts moving) isn't present: cut the briefing, let context leak out mid-motion.

## 5 ⚑ Emotion and senses: break the show-don't-tell dogma

| Feature | Human | AI |
|---|---|---|
| Emotion conveyed mainly via embodied sensation/metaphor (S) | 38% | 81% |
| Emotion conveyed mainly via explicit labels (S) | 29% | 8% |
| Olfactory imagery among dominant senses (S) | 57% | 82% |
| Setting mirrors characters' inner states, 1–5 (S) | 3.58 | 4.07 |
| Opening sentences classified as perceived space, setting sensed for mood and atmosphere (`ROHRBACHER-2026`; English, normalized frequency, GPT 4.1; the other three tested models also above human) | ~0.19 | ~0.47 |
| Sensory density, 1–5 (S) | 3.66 | 3.93 |
| Depth of interior access, 1–5 (S) | 3.67 | 3.93 |

**Generate:** AI executes "show don't tell" as dogma: fear is always a tightening chest, cold sweat, dimming lamplight. Humans mix four modes and lean on the plainest two — behavior first, plain naming second ("She was afraid" is a human sentence; models almost never write it). Reserve embodied rendering for one or two peaks per story. Let weather be weather: not every storm carries the marriage. Ration smell — it has become the connoisseur sense of machine prose. Ground the setting in action space, the space a character moves through and uses, rather than in perceived space, the space sensed for mood and atmosphere. In the human baseline action space is the most frequent spatial mode; in the four models tested (GPT 4.1, LlaMA 3.3, Mistral 3.2, Gemma 3) the English openings ran perceived space above the human level in all four, about twice it for GPT 4.1 (`ROHRBACHER-2026`).

**Revise:** Inventory every emotion beat and classify its mode. If embodied dominates, convert most to behavior (what she does) or plain statement (what she feels, named), keeping the strongest one or two embodied. Strip pathetic fallacy where the environment shadows mood scene after scene. Thin sensory description toward moderate density — cut the third sense in three-sense sentences. Sort setting sentences by what they do: sensed for mood and atmosphere (perceived space), used by a character who moves through it or handles something in it (action space), or neither (space viewed from a still position, or plain description); the study classifies all five of its categories, and only these two are compared here because the gap it reports is between them. If sensed dominates used, convert most of the sensed sentences to used and leave the neither sentences alone; the one or two embodied peaks kept above may stay sensed.

## 6 ⚑ Characters and the social network

| Feature | Human | AI |
|---|---|---|
| Protagonist introduced via external description (S) | 30% | 52% |
| Human fingerprint: introduced in-dialogue (S) | strongest human marker | rare |
| Network density — share of character pairs that interact (N) | 0.18 | 0.34–0.47 |
| Mean relationship affect (N) | −0.06 (net neutral) | +0.24 to +0.66 (all positive) |
| Clustering among antagonistic ties (N) | 0.395 | 0.07–0.21 |
| Investment built before putting a character in danger, 1–5 (S) | 2.76 | 2.99 |

**Generate:** Bring the protagonist on stage talking or doing, not described ("The dog arrived on a Tuesday" beats a paragraph of appearance-and-backstory). Keep the cast graph sparse: some characters never meet; some know each other only through a third. Sum of relationship affect should sit near neutral — real casts contain dislike that has nothing to do with the plot. Give antagonism *structure*: the antagonist has allies, internal rifts, their own network — not a lone hostile node pointed at the hero. It's fine to endanger a character the reader barely knows.

**Revise:** Draw the cast graph with signed edges. If everyone connects to everyone, delete edges. If every edge is warm, cool several. If the villain is isolated, give them one relationship that doesn't involve the protagonist.

## 7 ⚑ The outside world and the reader

| Feature | Human | AI |
|---|---|---|
| Explicit named references to real texts/authors (S) | 47% | 24% |
| Balanced mix of explicit + implicit reference (S) | 37% | 16% |
| Any fourth-wall permeability (S) | 67% | 39% |
| Direct reader address (S) | 28% | 7% |
| Distinct meaningful locations (S, ordinal) | 1.34 | 1.08 |
| Dialogue-to-narration proportion, 1–5 (S) | 2.95 | 2.70 |

**Generate:** Name real things — an actual novel on the shelf, a real band, the specific highway (accuracy rule in SKILL.md applies: only real, correct references; ask the user for material if needed). Mix named references with unnamed echoes. An occasional aside that admits a reader exists ("you know the kind of house") is a human move — *occasional*: an aside or two, not a metafictional frame. Let scenes happen in one or two more places than the premise strictly needs. Give dialogue slightly more floor than exposition.

**Revise:** If the draft gestures at "a famous poet" or "an old song," make one of them specific and real. If the story visits a single room for 5,000 words and the premise doesn't demand confinement, move one scene. Vague allusion everywhere = machine caution.

## The rarity move

Human stories are structurally *rarer* than AI stories (rarity percentile 0.71 vs 0.49; the five models cluster in one region of narrative space and humans scatter). Beyond the band-calibrated rules above, make **exactly one** structural choice that is genuinely atypical for the premise — an unexpected narrator distance, a resolution mode the genre rarely uses, a frame that recasts the genre (crossover literary ambition is a measured human fingerprint). One. More than one reads as performance.
