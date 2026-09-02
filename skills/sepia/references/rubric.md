# Diagnosis rubric — the 30 core features

The 30 narrative features below come from StoryScope's released taxonomy and corpus summary (AI-core and human-core tables 14–15; all-30 means and gaps, Table 16). StoryScope's Core Only 30-feature XGBoost held-out classifier reached 84.8% macro-F1 (AUPRC .828); this manual rubric is heuristic triage, not that classifier or an authorship detector. See [StoryScope arXiv v6](https://arxiv.org/abs/2604.03136v6) for the pinned study.

Use the Human and AI columns as corpus calibration references, not targets for an individual story. Observed signals are not authorship probabilities. This rubric makes no validated aggregate-detector or revision-threshold claim; any future aggregate claim requires a separate, documented evaluation.

## Protocol

1. Read **one group at a time**, in five separate passes. Never assess the whole rubric in one read: models self-evaluating text collapse onto one or two salient dimensions and go blind to the rest (measured on the slop taxonomy — span precision 0.13–0.16 across tested prompting conditions).
2. For each observed signal, quote the short passage that justifies it. No quote, no signal.
3. Record numeric, ordinal, and categorical observations beside the corpus references; do not convert them into authorship probabilities or a combined score.
4. Mark a feature **n/a** when the text offers no occasion to assess it, and record over-correction separately.

## Reading rules

| Case | Rule |
|---|---|
| Numeric rows (scale/ordinal) | Record the story's observed score and compare it qualitatively with the Human and AI corpus references. Do not apply a numeric cutoff. |
| Percentage rows (categorical/binary) | Record whether the AI-column option appears and quote its context. The corpus percentages are calibration context, not per-story probabilities or ratio cutoffs; absence of a human-leaning option is not itself a finding. |
| Group D | Record each human-positive marker separately with its quoted evidence. Do not collapse the markers into a group score. |
| Not applicable | A feature with no occasion in the text (no jeopardy → pre-threat investment; no reveal → recontextualization) is **n/a** and does not force a judgment. Reference explicitness is n/a only when the story makes no allusive gesture at all — an unnamed borrowed quotation or a recognizable unattributed retelling *is* an occasion (record it as implicit). Short texts produce several n/a — that is expected, not a defect of the story. |
| Over-correction | A numeric score at the far extreme *away* from the AI direction (e.g. discontinuity 5/5, thematic explicitness 1/5) → flag as **over-correction advisory**. Report it separately as a humanizer-fingerprint failure mode; do not reinterpret it as an AI-leaning signal. |

## Group A — Thematic over-determination (AI drifts high)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Thematic explicitness | 1 = themes stay implicit; 5 = thesis-like statements tell the reader how to interpret events | ~3.3 | 3.9 |
| Moral/philosophical weighting | How far ethical debate and thematic exposition outweigh story pleasure; check narrator commentary and climactic speeches | ~3.3 | 3.7 |
| Thematic unity | 5 = every scene, subplot, image reinforces one thematic core | ~4.4 | 4.7 |
| Narrator thematic commentary | Does the narrating voice generalize about what events mean ("That is how people are")? | yes in ~52% | 77% |
| Dialogue as philosophical debate | Do key dialogues argue ideas rather than advance want/conflict? | dominant in ~34% | 59% |
| Reference explicitness | Vague unnamed allusion as the dominant intertext mode (the human-leaning state is a balanced mix of named + implicit, 37% vs 16%) | implicit-only ~50% | 72% |

## Group B — Sensory & embodied performativity (AI drifts high)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Dominant emotion mode | Classify strong-affect scenes: explicit label / embodied sensation / behavior / ambiguous; flag embodied dominance as an AI-leaning signal | embodied dominant in ~38% | 81% |
| Setting as psychological mirror | Do weather/landscape/architecture consistently externalize inner states? | ~3.6 | 4.1 |
| Environmental emphasis | Landscape and ecology beyond backdrop | ~2.8 | 3.2 |
| Olfactory imagery | Smell among regularly engaged senses — judge salience relative to length (one prominent instance counts in flash-length text; recurring use in longer work) | ~57% | 82% |
| Sensory density | Proportion of text doing multi-sense description; 5 = lush, pace-slowing | ~3.7 | 3.9 |
| Depth of interior access | 1 = external only; 5 = stream of consciousness | ~3.7 | 3.9 |

## Group C — Structural streamlining (AI drifts high/tidy)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Causal-chain continuity | 5 = every event tightly linked in one line from incitement to end | ~3.9 | 4.2 |
| Subplots *(advisory signal)* | Absence of any subplot; too common in human stories (57%) to interpret without context | no-subplot ~57% | 79% |
| Resolution agency | Turning point triggered by protagonist choice vs chance/others | choice ~46% | 69% |
| Resolution mode | External act / internal acceptance / partial / open / catastrophic; flag internal acceptance as an AI-leaning signal | internal ~27% | 47% |
| Protagonist introduction | Device at first substantial appearance — one of: external description / in-action / in-dialogue / inner thought / others' reports. Flag external description as an AI-leaning signal; the other four are not signals by themselves (in-dialogue is the strongest human marker) | description ~30% | 52% |
| Opening spatial grounding | How completely the first scene fixes local + global place (1–4) | ~2.1 | 2.3 |
| Spatial granularity | Density of place names, rooms, routes (1–4) | ~2.3 | 2.5 |
| Pre-threat investment | Interiority/backstory built before jeopardy | ~2.8 | 3.0 |

## Group D — Human-positive markers

| Marker | How to judge | Human | AI |
|---|---|---|---|
| Named intertextuality | Any real text/author/work explicitly named | present in ~47% | 24% |
| Fourth-wall gesture | Any wink, aside, or reader acknowledgement anywhere | present in ~67% | 39% |
| Direct reader address | Any "you"/"dear reader" moment | present in ~28% | 7% |

## Group E — Temporal complexity & diversity (AI drifts low/tidy)

| Feature | How to judge | Human reference | AI reference |
|---|---|---|---|
| Chronological discontinuity | Frequency/sharpness of time jumps | ~2.4 | 2.1 |
| Anachrony intensity | Scene-level flashbacks/flash-forwards as structure | ~2.6 | 2.3 |
| Nonlinear framing for disclosure | Time devices used to stage revelations | ~2.0 | 1.7 |
| Recontextualization after surprise | How much earlier text a reveal recolors | ~3.3 | 3.0 |
| Location variety *(Sepia heuristic advisory)* | Optional editorial check: flag a 3,000+ word story that never leaves one locale unless the premise demands confinement | measured ordinal mean 1.34 | 1.08 |
| Dialogue proportion | Fraction of text in quoted speech (1 = none, 3 = balanced, 5 = dominates) | ~3.0 | 2.7 |
| Moral polarity toward protagonist | Narrative's final stance; flag a clearly affirmative or clearly condemning stance as an AI-leaning signal | ambivalent ~59% | clear 62% |

## Report format

Cite by quoting a short phrase, not by paragraph number. Keep the report descriptive: it records candidate signals for editorial review, not authorship probabilities or an aggregate action score.

```text
SEPIA DIAGNOSIS — <title>
Scope: heuristic triage; corpus references only; no authorship probability or validated aggregate detector
Model: author=<value> executor=<value>   (value: unknown | <family> version=unknown | <family> <release>; a release is an exact tag like Fable 5.1 or GPT-5.6 — "GPT-5" alone is a family, write "GPT version=unknown")
Narrative layer: author=<prior | none> executor=<prior | none>
Prose layer: author=<operative | prior | none> executor=<operative | prior | none>   (operative = the release's own table is operative and the family's other tables are priors)
Group A: observed signals …; n/a … (narrator commentary — "It was then she learned…"; …)
Group B: observed signals … (…)
Group C: observed signals …; n/a … (…)
Group D: marker observations … (named intertextuality present — "…")
Group E: observed signals … (…)
Advisories: over-correction …; subplots …; single-location …
Quoted evidence: <short phrase for each reported signal>
Plan: <ordered fixes, deepest layer first, each tied to a quoted passage>
```
