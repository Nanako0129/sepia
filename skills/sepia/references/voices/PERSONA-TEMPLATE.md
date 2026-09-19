# Persona — <name>

Template for a persona profile: one writer's style as prescriptive moves plus the sepia rules it overrides. The contract is in `voice-skills.md` (persona section); `scripts/check_persona.py` checks a body against this template. Keep the H2 headings below verbatim and in this order; the prose under them may be in any language. Status holds exactly its six `Key: value` lines and nothing else. No quoted example may exceed 20 characters inside 「」, 『』 or a paired double quote (Status and Blind-test record are exempt: their quotes are metadata); single quotes and apostrophes are not counted. No H2 sections other than the fourteen below. Examples are shapes, not text to reuse.

## Status

Name: <name, spaces allowed>
Routes: <professional | fiction | any>
Opt-in phrase: apply persona <name, spaces allowed> / 「套用 persona <name, spaces allowed>」
Provenance: <what was read: how many pieces, which years or kinds, full readings or not>
Consent: <own style | public-domain author | fictional persona | brand persona | consent from the person, YYYY-MM-DD | private study, not for distribution>
Tested: <tested | untested>

## One sentence

What this writer does that no house style would produce on its own, in one sentence.

## Beat and themes

Subjects, venues and recurring concerns; whether the concerns enter the narration directly or only through sources.

## Metric fingerprint

Measured deviations from a stated baseline (sentence length distribution, punctuation, attribution habits), or "none measured" with the close-reading difference stated instead. Numbers name their unit.

## Moves by frequency

Descriptive: what the writer does, grouped by opening, paragraph and beat, sentence shape, quotation and attribution, diction and figures, narrator, structure and subheads, ending. Each move carries a count such as `k/n pieces`.

## Negatives

What this writer does not do.

## Meaning for sepia

Which of the moves above a current sepia rule would remove, and what a model imitating the writer gets wrong.

## Every piece

Prescriptive, 3–8 numbered moves. Each has move text and ends with `(overrides: <rule token>)`, naming a token from the table below, or `(overrides: none)`; the validator checks the count, the text, the suffix and the table membership.

## Only with facts

Moves that appear only when the material supplies the fact they need; a missing fact is a TODO, never a sentence.

## Sentence shape

Targets for the narration as a distribution (a mean and a spread, a share of long and short sentences), never a fixed length; both ends of the distribution must appear. Write what was measured, not what would be nice: nothing in the report enforces this section, and after a write or a recreate the executor compares the piece against it by hand (`voice-skills.md`, persona section).

## Rules this persona overrides

| Rule | How the persona departs | Expected cost |
|---|---|---|
| <rule token, for example `style-pass.md §3`> | <what the persona does instead> | <what review will report as `Persona cost:`> |

Rule tokens: `style-pass.md §<n>`, `discourse-pass.md §<n>`, `narrative-pass.md §<n>`, `languages/zh.md §<s>` (§2 only as `languages/zh.md §2 <row>` for one of connective-stacking, second-person, disyllabic-padding, manner-adverb; the whole section cannot be named). A section token exempts the whole section, so where that is wider than the signature, say in the Expected cost cell what else it exempts, `professional-pass.md check <n>`, `domains/<name>.md rule <n>`. The validator refuses `style-pass.md §5`, `professional-pass.md check 9`, `languages/zh.md §2 flat-sentence-length`, `discourse-pass.md §3` (uniformity) and `professional-pass.md check 5`, `domains/journalism.md rule 1`, `domains/tech-articles.md rule 1`, `domains/postmortems.md rule 2` (never invent) and `domains/journalism.md rule 3` (quoted material). Fenced code blocks do not count as structure.

## Prohibitions

Both fixed lines verbatim, each as its own list item (a paragraph does not count), then the persona's own:

- Do not reuse this file's example phrases verbatim; they are shapes, not a word list.
- Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO.

## Boundary

Three to five lines: what reads like the writer versus what reads like a model imitating the writer. If a signature is a rhythm, say here that it draws a uniformity finding on every piece, because the override table cannot waive that one.

## Blind-test record

One line per test, in this shape: `YYYY-MM-DD — judge: <who> — compared: <what against what> — outcome: <result>`; or "none yet" with `Tested: untested` above. A placeholder such as TODO does not count as a record.
