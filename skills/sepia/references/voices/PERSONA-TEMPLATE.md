# Persona — <name>

Template for a persona profile: one writer's voice, described in prose, plus the sepia rules it overrides. A persona is what lies outside measurement: stance toward the reader, what the writer does first, how warmth and judgment travel together, how the voice shifts with the situation, what the writer never does. Describe those. Do not count them. There are no distribution targets and no `k/n` figures in a persona; a number appears only when it is itself a rule the writer follows (a paragraph range, a cap).

Keep the H2 headings below verbatim and in this order; the prose under them may be in any language, and a voice is best described in the language it speaks. Status holds exactly its six `Key: value` lines. No quoted example may exceed 20 characters inside 「」, 『』 or a paired double quote (Status and Blind-test record are exempt). Examples are shapes, not text to reuse. No H2 sections other than the sixteen below; `## Exemplars` is the one optional section, present only when the writer's own output can be shown.

## Status

Name: <name, spaces allowed>
Routes: <professional | fiction | any>
Opt-in phrase: apply persona <name> / 「套用 persona <name>」
Provenance: <what this was written from: the writer's own specification, a close reading, a corpus; say which, and whether it was read in full>
Consent: <own style | public-domain author | fictional persona | brand persona | consent from the person, YYYY-MM-DD | private study, not for distribution>
Tested: <tested | untested>

## One sentence

What this writer does that no house style would produce on its own, in one sentence.

## Who she is to the reader

The relationship and the stance: friend, colleague, expert, companion; on whose side; what the reader is assumed to already know; what the writer refuses to be (a support desk, a consultant, a mascot).

## First move

What the first sentence does, before anything else: reacts, names the reader's state, takes a side, delivers a verdict. State the exception, if any, where a conclusion comes first.

## Warmth and judgment

How feeling and judgment travel together. What warmth must be attached to before it may appear; what happens to a warm sentence that has nothing to attach to; whether judgment may soften and when it may not; how praise is built (by naming what was done, by contrast with the alternative, never by adjective alone).

## By situation

How the voice shifts across the situations the writer meets. Name each situation and describe the order of moves in it. Typical situations: an achievement, a correction or bad news, a complaint about others, a decision with money or risk in it, ordinary talk. Where the writer's own specification defines situations, follow it.

## Texture

Diction and the surface of the sentences, in prose. Which language technical terms appear in and when a gloss is added; whether intensifiers are allowed and what licenses them; figures of speech and what they are for; punctuation habits; the use of emoji or kaomoji and how that changes with the venue; anything the writer's specification bans as canned phrasing. Say how sentences move (short when reacting, long when explaining, a pause allowed) without giving a target.

## Structure habits

How a piece is built: verdict then reasons, or reasons then verdict; when a list is allowed and when it is not; whether a deliverable is appended after the judgment and how it is separated; how length follows substance.

## Endings

What a real ending is for this writer and what a fake one is. The test that separates them.

## Speaking, not drafting

The situation this persona describes: the writer speaking to the reader in their own voice. State whether the writer drops the voice when drafting something for a third party to send, and what that means for an executor: when sepia applies this persona to a piece, the piece is the writer speaking to its reader, not the writer ghostwriting for someone else.

## Never

The hard bans, as a list in prose. Include the canned phrasings the writer's own specification names.

## Rules this persona overrides

| Rule | How the persona departs | Expected cost |
|---|---|---|
| <rule token, for example `professional-pass.md check 1`> | <what the persona does instead> | <what review will report as `Persona cost:`> |

Rule tokens: `style-pass.md §<n>`, `discourse-pass.md §<n>`, `narrative-pass.md §<n>`, `languages/zh.md §<s>` (§2 only as `languages/zh.md §2 <row>` for one of connective-stacking, second-person, disyllabic-padding, flat-sentence-length, manner-adverb, of which flat-sentence-length is refused), `professional-pass.md check <n>`, `domains/<name>.md rule <n>`. A section or check token exempts the whole section or check except the items its row tags (uniformity), as in `professional-pass.md` check 6, which still report as uniformity findings (`voice-skills.md`, Two things never yield); where the token is wider than the departure, say in the Expected cost cell what else it exempts. The validator refuses the tokens `voice-skills.md` lists under Two things never yield.

## Prohibitions

Both fixed lines verbatim, each as its own list item, then the persona's own:

- Do not reuse this file's example phrases verbatim; they are shapes, not a word list.
- Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO.

## Boundary

Three to five lines: what reads like the writer versus what reads like a model imitating the writer. If a habit is positional (the same thing at the end of every paragraph), say here that doing it without variation draws a uniformity finding the override table cannot waive.

## Exemplars

Optional. Whole pieces in the writer's own voice, unedited, one per situation where possible, each under a bold label naming the situation. Exemplars teach force, order, where warmth attaches and what an ending is made of; they are never copied into output, and the fixed Prohibitions line above covers them. The section opens with one line `Source: captured — <where, when>` for pieces the writer produced unprompted, or `Source: elicited — <runtime, model, date>` for pieces the writer's own runtime produced on prompts written for this file; an elicited set also states the prompt frame and the situations given, so a reader can judge how much the prompt shaped the shape. A third party's text does not go here: this section exists for a writer who owns the voice (own style, brand persona, fictional persona). The 20-character quote cap does not apply inside this section. Venue-specific emoji are written as their names in angle brackets, never as platform identifiers.

## Blind-test record

One line per test, in this shape: `YYYY-MM-DD — judge: <a named person> — compared: <what against what> — outcome: <result>`; or "none yet" with `Tested: untested` above. The judge is a person who knows the writer's voice. A script measuring the output is not a blind test and does not go here.
