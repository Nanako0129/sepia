# Pass 2 — Discourse flow

The layer between plot and sentences: how paragraphs advance, where the energy sags, and where things sit on the page. Evidence: QUDsim/COLM 2025 (Q), Tripto et al. EMNLP 2025 (T), Russell et al. ACL 2025 (R), Beguš 2024 (B), asavvin's outline test (A). Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local. Prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention.

## 1 The QUD check — what question does each paragraph answer?

Every paragraph implicitly answers a question. In QUDsim's tested samples, two models given the same premise independently reused the sequence *scene briefing → justifying the deception → social consequences → the weight of responsibility* (Q). Surface rewording does not change that question sequence; changing it requires reordering or replacing the underlying moves.

**Check:** List one implicit question per paragraph/scene of the outline or draft. Flags:

| Flag | Symptom |
|---|---|
| Linear interview | Each question follows administratively from the last (what happened → why → what resulted → what it means) |
| The reflection tail | Final paragraphs answer "what does this mean / how does she feel about it now" — the machine's closing move |
| Missing move types | No paragraph *compares* (two times, two characters, two versions of an event), none *verifies* (doubts or contradicts an earlier paragraph's account), none *digresses* (memory or association that earns its place later) |

**Fix:** Reorder so at least one question arrives before its setup. Replace one consequence-paragraph with a comparison or a contradiction — LLMs use consequence/procedure moves ~19% of the time and comparison/verification moves ~0.2–0.3% (Q); a single "but that isn't how her sister remembers it" paragraph does more de-AI work than a page of rewording.

**Outline test (A):** extract the first sentence of every paragraph and read them as a list. If they form a clean summary of the piece, the structure is machine-shaped — a human outline has gaps, jumps, and sentences that make no sense out of context.

## 2 The middle is the choke point

Detectors and human judges find AI text most identifiable in the **body**, least in openings and endings — models imitate the formulaic bookends well and expose themselves in the long middle (T). LLM stories also show a measured mid-story collapse into predictable filler, rushing pace and leaving suspense unexplored (X, cited in narrative pass). Though this section speaks in fiction terms, the choke-point evidence was measured on news, essays, and email as well — for non-fiction, read "scene" as section and "event" as claim or finding.

**Fix, aimed at the middle third:**

- Put at least one event there that the opening does not predict.
- Vary texture between adjacent scenes: a dense scene then a fast one, a dialogue-heavy stretch then summary narration. Human writing shows high cross-paragraph variance ("burstiness"); models hold one register for the whole text (T).
- Let one thread slow down instead of resolving on schedule — the machine failure mode is acceleration past the interesting part.

## 3 Structural positions on the page

Position patterns survive paraphrase better than word choice does — after full paraphrasing, position tells became *more* visible to expert detectors, not less (R).

| Position tell | Machine habit | Human habit |
|---|---|---|
| Paragraph lengths | Uniform | Ragged — including a one-sentence paragraph |
| Quoted speech / key lines | Always closing a paragraph | Anywhere, including mid-paragraph |
| Lists of qualities, reasons, images | Exactly three items | Two, four, one — three sometimes |
| Scene transitions | Same connective formula each time | Varied: hard cut, time skip, dialogue pickup |
| Emphasis | Evenly distributed | Clustered where it matters, absent elsewhere |

The paragraph-length row means uniformity *within the text*. Paragraph length and paragraph count on their own are not signals: measured directions contradict across corpora (LLM paragraphs longer in how-to text, shorter in generated papers, more numerous in Chinese answers) and follow prompt limits and venue conventions; see the syntax section of the repository research ledger.

## 4 Openings

The machine opening: establish time + place + weather, introduce the character with description, then start the story (B: "Once upon a time"-style detachment; R: the "On a drab November morning" scene-setting lead; S: AI over-grounds the opening spatially, 2.33 vs 2.12).

**Fix:** open inside the situation — mid-conflict, mid-conversation, mid-error ("Sam didn't know she wasn't human"). Ground space with one working detail, not an establishing shot. Delay the character's appearance-and-backstory paragraph indefinitely; most stories never need it.

## 5 Names

The tested model outputs converged on recurring names such as Elara, Ava, and Amelia; Emily or Sarah appeared in 63–70% of the AI articles, and formal titles were overrepresented (B, R).

**Fix:** name characters from the story's specific world (ethnicity, region, generation, class), let surnames and nicknames do social work, drop titles except where the fiction needs them, and let different characters call the same person different things.
