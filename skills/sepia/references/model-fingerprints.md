# Per-model fingerprints

Two layers, two kinds of evidence, kept in separate tables:

- **Narrative layer (measured).** Each frontier model diverges from the *other AIs* on its own signature features (StoryScope §5, Table 17; 6-way attribution 68.4% macro-F1 from narrative features alone). See [StoryScope arXiv v6](https://arxiv.org/abs/2604.03136v6) for the pinned study. Measured on specific versions (Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2, Kimi K2.5, 2026). Fiction only.
- **Prose layer (vendor guidance, unmeasured).** What a model's own vendor says its current release does at the sentence level, taken from the vendor's prompting documentation. Tagged with the exact release the page names. Applies to professional prose and to fiction narration alike, at the style-pass step only — never before the narrative and discourse passes.

Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local: S = StoryScope, V = vendor guidance. Corrections are Sepia inferences unless a source explicitly tested the intervention.

**Which rows apply is decided by the model-identity rule in `SKILL.md` (Routing), not here.** In short: each role (author, executor) is resolved on its own; a role's family selects its narrative layer as priors when that role's model produced or is producing the story, and its prose layer on every route — *operative* only when the release matches the table's tag, a *prior* otherwise. Nothing in this file infers a model from the prose — attribution by reading is not the classifier that produced the 68.4%.

## Claude

### Narrative layer (S; Sonnet 4.6) — the most identifiable AI, 26 fingerprint features

| Default | Correction |
|---|---|
| Flattest event escalation of any source; uniform narrative voice throughout | Build real escalation: let stakes and intensity *jump*, unevenly. Allow the voice to strain, speed up, or coarsen at pressure points |
| Reverent/continuist toward literary tradition (62% of stories vs 39–56%) | Permit one convention to be broken or mocked rather than honored |
| Favors epilogues and flash-forward endings; quiet endings over "avalanche" endings | Ban the epilogue by default; end in motion. An avalanche ending is allowed |
| Avoids dream sequences entirely | A dream is available if the story wants one (do not force it — absence is only a tell in aggregate) |
| Setting mood drifts to uncanny/haunted | Vary the atmospheric register |

### Prose layer (V; Claude Fable 5.1 and Claude Mythos 5.1, `ANTHROPIC-FABLE-5-1-PROMPTING`)

| Vendor-stated default | Handling |
|---|---|
| Mannered prose: metaphor and flourish where a literal phrase exists | The block below, operative or prior per the model-identity rule in `SKILL.md`: operative for a role whose release is Claude Fable 5.1 or Claude Mythos 5.1 (the page names both), a prior for any other or unknown Claude release. As the author's layer: hunt metaphor standing in for an available literal phrase in the given text. As the executor's layer: apply the block to what you write |
| Denser than Fable 5: longer sentences, fewer paragraph breaks | Split run-ons (style-pass §1, row 2); break paragraphs where the topic turns |
| Less bold, fewer headers and lists than earlier Claude | Sparse formatting is not evidence of a human author. Do not add anti-formatting rules to compensate |

The vendor's own instruction, verbatim (compared against the source page 2026-09-02, matched):

```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

Scope: this block governs expository and professional prose. On the fiction route it is subordinate to `narrative-pass.md` §5 — §5's emotion-mode band and its one-or-two-embodied-peaks rule decide where metaphor stays, and the block applies only to narration outside those peaks. It is not a metaphor ban, and no figure from §5 is a metaphor budget.

## GPT

### Narrative layer (S; GPT-5.4) — the gossip and the long lens

| Default | Correction |
|---|---|
| Gossip/rumor as plot mechanism (64% vs 44–55%) | Let information move by observation, documents, or accident — not through the town talking |
| Distant retrospective narrator ("years later, she would…") | Narrate closer to the event; drop the decades-later frame |
| Subverts reader expectations more than any other AI (41%) | Do not add another twist; earn the one you have |
| Reconciliations left partial/ambiguous, habitually | Resolve one relationship fully — in either direction |
| Ensemble-heavy social webs (human-level density but formulaic) | Prune the ensemble to the characters the story uses |

### Prose layer (V; GPT-5.6, `OPENAI-GPT-5-6-PROMPTING`)

| Vendor-stated default | Handling |
|---|---|
| More concise by default than GPT-5.5; brevity instructions can make answers too brief | Density fails in both directions. A short answer that dropped a required caveat or the next action is a defect (professional-pass check 2) |
| The vendor's recommended trims name the expected residue: introductions, repetition, generic reassurance, optional background, generic praise, sign-offs | Already hunted by professional-pass checks 1, 2, and 7; treat those checks as high-prior when GPT wrote the text |
| Editing tasks drift: the vendor's preservation snippet warns against "adding new claims, sections, or a more promotional tone" | Vendor-implied, not stated as a defect. Enforce the register-drift clause of the `SKILL.md` guardrail "Deletion beats addition" |

## Gemini

### Narrative layer (S; Gemini 3 Flash) — the tidy pessimist

| Default | Correction |
|---|---|
| Tidiest endings + extended denouements | Cut the last scene; leave accounts unsettled |
| Bleak/oppressive settings in 88% of stories | Vary — let some settings be neutral or warm even when events are not |
| Frequent flashbacks as a reflex; over-indexes on dream sequences | Keep anachrony purposeful (staging disclosure), not decorative |
| Protagonist's social circle always expands | Allow shrinking or static trajectories |
| Direct speech dominates exchanges | Mix in indirect and summarized speech |

Prose layer: no vendor guidance ingested yet.

## DeepSeek

### Narrative layer (S; DeepSeek V3.2) — the front-loader

| Default | Correction |
|---|---|
| Crucial context delivered before the story moves | Withhold; leak backstory mid-motion (see narrative pass §4) |
| Visible, present narrator | Recede; let scenes run unhosted |
| Emotions via behavioral cues almost exclusively | Blend in plain naming and occasional interiority |
| Backstory evenly interleaved, metronomically | Cluster it irregularly |
| Embedded storytelling scenes (tales within the tale) | Use at most one, if any |

Prose layer: no vendor guidance ingested yet.

## Kimi

### Narrative layer (S; Kimi K2.5) — the generic center

Fewest fingerprints (3) — it sits at the centroid of AI narrative space, which *is* its tell: no distinctive choices at all. Corrections: it opens in medias res with in-action introductions by reflex (vary the entry), and never labels traits explicitly (allowed to). Mostly, apply the shared passes at full strength and make the rarity move count.

Prose layer: no vendor guidance ingested yet.

## Human fingerprints — the positive targets

The features on which human authors diverge from every model, usable as direct recipes:

| Human marker | Recipe |
|---|---|
| Protagonist introduced in-dialogue (uniqueness 21.4 — the strongest single marker in the study) | First appearance: the character speaking, unannotated |
| Single focal perspective held | Depth over head-hopping |
| Narrator never addresses, then occasionally does | No system to the asides |
| Back-loaded revelation pacing | The biggest thing lands late |
| Crossover-genre literary ambition | Let the genre piece want to be something else too |
