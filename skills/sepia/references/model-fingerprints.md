# Per-model fingerprints

Two layers, two kinds of evidence, kept in separate tables:

- **Narrative layer (measured).** Each frontier model diverges from the *other AIs* on its own signature features (StoryScope §5, Table 17; 6-way attribution 68.4% macro-F1 from narrative features alone). See [StoryScope arXiv v6](https://arxiv.org/abs/2604.03136v6) for the pinned study. Measured on specific versions (Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2, Kimi K2.5, 2026). Fiction only.
- **Prose layer (vendor guidance, unmeasured).** What a model's own vendor says its current release does at the sentence level, taken from the vendor's prompting documentation. Tagged with the exact release the page names. Loaded on every route at the style-pass step only — never before the narrative and discourse passes — and written by the vendors for user-facing expository output: on the fiction route it applies to the non-narrative text an operation produces (the report, a summary for the user), and reaches narration only where a table's own scope note says so; otherwise `narrative-pass.md` §5 and the narrative layer govern narration.

Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local: S = StoryScope, V = vendor guidance. Corrections are Sepia inferences unless a source explicitly tested the intervention.

**Which rows apply is decided by the model-identity rule in `SKILL.md` (Routing), not here.** In short: each role (author, executor) is resolved on its own; a role's family selects its narrative layer as priors when that role's model produced or is producing the story, and its prose layer on every route — a table is *operative* only when the release matches its tag, a *prior* otherwise, so a role with a matching table has that one operative and the family's other tables as priors. Nothing in this file infers a model from the prose — attribution by reading is not the classifier that produced the 68.4%.

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

Scope note: this block is the one instruction in this section that does reach narration on the fiction route, and only subordinate to `narrative-pass.md` §5 — §5's emotion-mode band and its one-or-two-embodied-peaks rule decide where metaphor stays, and the block applies to narration outside those peaks. It is not a metaphor ban, and no figure from §5 is a metaphor budget.

### Prose layer (V; Claude Fable 5 and Claude Mythos 5, `ANTHROPIC-FABLE-5-PROMPTING`)

| Vendor-stated default | Handling |
|---|---|
| Un-steered, elaborates past the task: "surveying options it won't pursue, explaining root causes at length, producing heavily-structured PR descriptions, or writing comments that narrate what the next line does" | The brevity instruction below, operative or prior per the model-identity rule in `SKILL.md`: operative for a role whose release is Claude Fable 5 or Claude Mythos 5, a prior for any other Claude release. As the author's layer: hunt option surveys, root-cause essays, and structure that outweighs the content (professional-pass checks 2, 3, 6). As the executor's layer: apply the instruction to the non-narrative text you write, per the route scope in this file's header |
| In long agentic sessions, "dense arrow-chain shorthand, deep implementation detail, references to thinking the user never saw, or overly technical phrasing" | Hunt arrow chains, hyphen-stacked compounds, and labels the reader never saw defined; expand them into sentences (style-pass §6 read-aloud test) |

The vendor's brevity instruction, verbatim (compared against the source page 2026-09-03, matched):

```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

### Prose layer (V; Claude Opus 5, `ANTHROPIC-OPUS-5-PROMPTING`)

| Vendor-stated default | Handling |
|---|---|
| "Default user-facing responses run longer than prior Opus models'"; effort changes thinking volume, not visible length | Run density (professional-pass check 2) at the role's operative or prior strength. The conciseness instruction below, operative or prior per the model-identity rule in `SKILL.md`: operative for a role whose release is Claude Opus 5, a prior for any other Claude release; as the executor's layer, apply it to the non-narrative text you write, per the route scope in this file's header |
| Written files "are often longer than on prior models": filler sections, redundant summaries, boilerplate | Hunt the fractal-summary shape and sections that exist for completeness (professional-pass checks 6, 7). Vendor instruction: "Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate." |
| "Narrates readily during agentic work": announces what it is about to do; narrates corrections to earlier statements more than prior models | In produced text, cut announcements of intent and corrections that change nothing for the reader |

The vendor's conciseness instruction, verbatim (compared against the source page 2026-09-03, matched):

```text
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

### Prose layer (V; Claude Opus 4.8, `ANTHROPIC-OPUS-4-8-PROMPTING`)

| Vendor-stated default | Handling |
|---|---|
| "A direct, opinionated style with minimal validation-forward phrasing and sparing emoji use" | Absence of validation openers and emoji is this release's default, not evidence of a human. Stance (check 4) is usually present; look instead at density and specificity |
| Response length "calibrated to how complex it judges the task to be" | Length varies with the task by default; uniform length across tasks would be the tell, not variation |

Consulted with no prose-layer statement (2026-09-03): the Claude Sonnet 5 page says only that "prose style on long-form writing may shift"; Claude Opus 4.7, Opus 4.6, and Sonnet 4.6 have no model-specific prompting page. Those releases have no operative row; per the rule in `SKILL.md`, the Claude prose tables above apply to them as priors.

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
| More concise by default than GPT-5.5; brevity instructions can make answers too brief | Density fails in both directions. In non-narrative text, a short answer that dropped a required caveat or the next action is a defect (professional-pass check 2) |
| The vendor's recommended trims name the expected residue: introductions, repetition, generic reassurance, optional background, generic praise, sign-offs | Already hunted by professional-pass checks 1, 2, and 7; run them on non-narrative text at the role's operative or prior strength |
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

### Prose layer (V; Gemini 3 series, `GOOGLE-GEMINI-3-DEV-GUIDE`)

The vendor scopes its statements to the series (Gemini 3 Flash through Gemini 3.8 Flash), so any Gemini 3.x release matches this table.

| Vendor-stated default | Handling |
|---|---|
| "By default, Gemini 3 is less verbose and prefers providing direct, efficient answers"; a conversational or "chatty" persona appears only when explicitly prompted | Terse and unadorned is this series' default, so brevity is not evidence of a human here. In non-narrative text, check density in the other direction (professional-pass check 2): required caveats and next steps dropped for efficiency |

## DeepSeek

### Narrative layer (S; DeepSeek V3.2) — the front-loader

| Default | Correction |
|---|---|
| Crucial context delivered before the story moves | Withhold; leak backstory mid-motion (see narrative pass §4) |
| Visible, present narrator | Recede; let scenes run unhosted |
| Emotions via behavioral cues almost exclusively | Blend in plain naming and occasional interiority |
| Backstory evenly interleaved, metronomically | Cluster it irregularly |
| Embedded storytelling scenes (tales within the tale) | Use at most one, if any |

Prose layer: none. Consulted 2026-09-03 with no statement about the model's own writing: the DeepSeek API documentation (no prompting guide at all) and the DeepSeek-V3.2 model card (sampling parameters only).

## Kimi

### Narrative layer (S; Kimi K2.5) — the generic center

Fewest fingerprints (3) — it sits at the centroid of AI narrative space, which *is* its tell: no distinctive choices at all. Corrections: it opens in medias res with in-action introductions by reflex (vary the entry), and never labels traits explicitly (allowed to). Mostly, apply the shared passes at full strength and make the rarity move count.

Prose layer: none. Consulted 2026-09-03 with no statement about the model's own writing: the Kimi platform's "Best Practices for Prompts" (generic prompt-engineering advice, no version named) and the Kimi-K2.5 model card (its default system prompt was removed in the 2026-01-29 changelog).

## Human fingerprints — the positive targets

The features on which human authors diverge from every model, usable as direct recipes:

| Human marker | Recipe |
|---|---|
| Protagonist introduced in-dialogue (uniqueness 21.4 — the strongest single marker in the study) | First appearance: the character speaking, unannotated |
| Single focal perspective held | Depth over head-hopping |
| Narrator never addresses, then occasionally does | No system to the asides |
| Back-loaded revelation pacing | The biggest thing lands late |
| Crossover-genre literary ambition | Let the genre piece want to be something else too |
