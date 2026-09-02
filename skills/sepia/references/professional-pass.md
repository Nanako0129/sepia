# Professional pass — shared layer for non-fiction

Applies to every non-fiction domain (release notes, PR/issue replies, postmortems, tickets, technical articles, and anything else that isn't narrative). Evidence: the slop taxonomy (Shaib et al., S), expert AI-detector studies (Russell et al., R), genre-alignment findings (Reinhart et al., P), and the Wikipedia/humanizer corpus of documented tells (W). Stable source identities live in the repository research ledger; single-letter aliases in this file are file-local. Prescriptions are Sepia design inferences unless a cited source explicitly tested the intervention.

> In professional genres the goal is not "fool a detector" — it is that the text carries information, has a stance, and sounds like it came from the person whose name is on it. Conventional structure is *fine* here; slop is the filler inside the structure.

## Read the venue first

Before writing or editing, sample 2–3 recent human-written artifacts from the same venue — the repo's past release notes, the maintainer's recent replies, the team's last postmortem — and match their register, length norms, and formatting habits. Reinhart et al. report that instruction-tuned models favor an informationally dense, noun-heavy style and struggle to match genre-aligned variation (P). The venue corpus, not this skill, defines the target voice. When no corpus exists, the domain file's baseline applies.

## The checklist

Run these one at a time (a combined pass goes blind — measured on this very taxonomy). Slop is **cumulative**: one hit means nothing; clusters mean rewrite.

| # | Check | What to hunt |
|---|---|---|
| 1 | Chatbot residue | "Great question", "Thanks for raising this!", "I hope this helps", "Certainly!", "You're absolutely right", offers of further help, apology openers, "Let's dive in". Delete — a colleague doesn't talk like a support desk. |
| 2 | Density | Could this say the same at half the length? Generic statements true in any context ("in today's fast-paced world", "it's important to note") carry zero information — cut. Length must be proportional to stakes, in both directions: a trimmed answer that lost a required caveat or the next step fails too. |
| 3 | Relevance | Does every paragraph serve *the reader's task* — the thing they came to find out? Background the reader already has, restated questions, and scope tours are filler. |
| 4 | Stance | Where a judgment is required, commit to one. Absent subjectivity is a measured slop dimension (S): a review without a verdict, a comparison without a recommendation, a postmortem without an admitted mistake. Hedge once per genuinely fragile claim, not per sentence. |
| 5 | Specificity | Versions, numbers, file:line, commands, error text verbatim, names — present and **real**. Never pad with invented specifics; a wrong fact stated confidently is itself a top-tier tell (R). Missing info → ask or leave an explicit TODO. |
| 6 | Formatting tells | Bold-mini-heading bullet lists where prose would do; emoji as decoration; Title Case headings; every section the same length; lists of exactly three, everywhere; a heading restated by its first sentence; fractal summaries (announce → say → recap at every level) (W). The absence of these is not evidence of a human: which formatting a model over- or under-uses changes with its release (see the prose layers in `model-fingerprints.md`). |
| 7 | Conclusion residue | "In conclusion/summary" sections, restating what was said, generic future outlook ("we will continue to improve…"). End when the content ends. |
| 8 | Templatedness | The same sentence frame recycled ("X, a Y at Z, said that…" three times); every item phrased identically. Vary or tabulate. |
| 9 | Sameness of rhythm | Uniform paragraph and sentence lengths throughout. Human professional prose is uneven — depth where it matters, one-liners where it doesn't. |
| 10 | Fluency | Grammatically correct but unsayable ("the earthen area that formerly held the puddle"). Read it aloud; if no one would say or write it in an email, redo it in speech-shaped syntax. |

Then finish with the vocabulary/syntax scan in `style-pass.md` §2–3 (the ban tables apply to professional prose too; the fiction-slop table does not).

## Domain weighting

Which checks dominate depends on document shape (measured: S):

| Document shape | Weight first |
|---|---|
| Article-like (postmortem, tech article, announcement) | Relevance, density, stance/tone, coherence |
| Short answers (PR/issue replies, review comments, tickets) | Factuality, specificity, templatedness — density and tone matter less at short length |

Weighting sets the order and depth of attention, not an exemption: a short reply drowning in filler still fails density.

For long-form (articles, postmortems), also run the outline test and QUD check in `discourse-pass.md` §1–3: extract first sentences per paragraph; a clean-summary outline and a briefing→justification→consequences→reflection question-sequence are both machine shapes.

## Report format (review operation)

```text
SEPIA REVIEW — <document type, venue>
Loaded: <files used>
Model: author=<value> executor=<value>   (value: unknown | <family> version=unknown | <family> <release>; a release is an exact tag like Fable 5.1 or GPT-5.6 — "GPT-5" alone is a family, write "GPT version=unknown")
Prose layer: author=<operative | prior | none> executor=<operative | prior | none>   (operative = the release's own table is operative and the family's other tables are priors)
Venue corpus: <artifacts sampled, or "none — using domain baseline">
Failed: <#n check-name — quoted evidence>   (one line per failed check)
Passed: <check numbers only>
Verdict: <clean / isolated hits / cluster> → <ship / refactor / recreate>
```

## Whitelist — conventional ≠ slop

| Do not flag | Why |
|---|---|
| Changelog categories, issue/PR templates, RFC sections, runbook formats | Formulaic containers by convention; the community expects them |
| Formal register in a formal venue | Register match beats forced casualness |
| Bullets for genuinely enumerable items | Tables and lists are correct for enumerable facts |
| Terse, unadorned replies | Brevity is the human default in dev venues, not a tell |
| The author's own verified habits | Edit toward their voice, not a generic "human" |
