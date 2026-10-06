# Voice profile — Taiwan long-form journalism (built-in, experimental, professional routes only)

Status: a built-in voice profile for the experimental interface in `voice-skills.md`. It loads only when the user opts in with the exact phrase `apply the Taiwan journalism voice` or 「套用台灣深度報導 voice」, optionally followed by a shape name from the tables below (for example 「，場景導入」, the exact token from the shape table). It never loads on the fiction route, declares no intent triggers, and produces no `Voice fit:` line (professional-route Voice fit is tracked in issue #227). Everything in `voice-skills.md` governs: sepia's architecture decisions first (here, `domains/journalism.md`), 3–5 voice moves per piece, uniformity findings at full strength, venue precedence, never invent. Shape selection happens in this order. First the route: when the request is on another professional route (a ticket, a PR reply, a release note), no shape is selected whatever the facts allow; sepia says so in one line, applies at most the cross-shape moves that fit that venue, and the closing line reads `Voice applied: tw-journalism/none — not a journalism route; cross-shape moves: <names or none>`. On the journalism route: when a shape is named and its precondition holds, moves come from that shape's table plus the cross-shape table; when a shape is named but its precondition fails, sepia does not use the named shape, says in one line which precondition failed, and then applies the same table-order rule as the unnamed case (the first row whose precondition holds is the spine; the line names it and the runner-up, or `runner-up: none` when only one precondition holds), or, when no other precondition holds, takes the no-shape path below; when none is named, sepia picks the shape from the decision table and says which; when no shape's precondition holds, the closing line reads `Voice applied: tw-journalism/none — no shape precondition met; cross-shape moves: <names or none>`. The venue's own domain file still governs the text; this profile never overrides it.

**Closing line (this body's own rule).** A write or recreate under this voice ends with one line, outside the prose: `Voice applied: tw-journalism/<shape> — moves: <3–5 move names>`, or, on either no-shape path defined above, the `tw-journalism/none` form with zero to five names. The 3–5 count binds when a selected shape's table plus the cross-shape table offer at least three moves whose facts exist; 時間軸 (two moves) and 懸念揭露 (one move) may declare fewer, and so may any shape whose precondition holds but whose facts support only one or two moves: the line then names the moves that have facts and adds `fewer: facts`. A move is never added to satisfy the count; the 3–5 range is a ceiling and a target, not a floor enforced by invention. Review and refactor stage 1 (the diagnosis) print their normal report, including the declared-voice section `voice-skills.md` specifies (voice and shape named, moves seen, costs reported rather than fixed), and omit only this closing line; refactor stage 2 (the edits) ends with the same line naming the shape and only the moves its edits actually applied: on refactor a move is applied only as the fix for a stage-1 defect (`voice-skills.md`), so the count there is bounded by the defects, may be one or two or zero, and the line then adds `fewer: defects`; nothing is edited to reach three; this line exists so a reader can check the selection rule without re-deriving it.

Evidence tiers, kept apart: (T) one private human-side measurement of Traditional Chinese long-form journalism, ledger `ZH-NEWS-CORPUS-2026`, whose numbers live in `languages/zh.md` §1b and, for contrast-only forms, the Human column of §1c; (C) a close reading of 169 articles from the same corpus, cited as counts of 169 or of a shape subgroup within those 169 (sample sizes, not corpus sizes; the subgroup counts come from the same private close-reading notes as the digest and are published here at the same granularity; a bare `C` or a qualitative C label such as `C: scene pieces` or `C: the norm` marks an observation from the same notes that was not counted, and carries inference weight); (I) Sepia inference. There is no author-testimony tier; a machine side (M) exists for this register (`languages/zh.md` §1c) but this profile cites only T and C, and makes no machine-side measurement or generalization: nothing here says what machines do as a class, only what this register does. The Grounding section records one executor's one-off review and write behaviour on one example as validation of this body, not as evidence about machines. The corpus is about two thousand articles from one unnamed Taiwanese publication, spanning about ten years, human text only, not distributed. No sentence of any article appears in this file; every example is synthetic.

## The precondition is reporting

Every shape below needs facts the writer actually has. A scene needs scene facts (who, where, what they were doing, when); a number needs its comparison basis; a two-sided layout needs two sides on the record; a timeline needs timestamps. Under this voice the specificity rules stay at full strength (SKILL.md "Never invent specifics"; `professional-pass.md` check 5): a missing fact is a TODO or a question to the user, never a sentence. A shape whose precondition is not met is not chosen.

## Choosing a shape

| What the reporting has | Shape | Precondition that must hold |
|---|---|---|
| A place someone can stand in, a person doing something there, and the time of day | 場景導入 (scene lead) | scene facts with a time of day |
| A result that happened today or this week relative to a publication date the facts supply | 倒金字塔 (inverted pyramid) | date, actor, outcome, count, publication date |
| One person whose time span carries the piece | 人物弧線 (person arc) | at least three dated episodes |
| A policy or number gap to take apart | 論證式 (argument) | two parties on the record |
| A dataset the reporter built or obtained | 數據驅動 (data-led) | source, method, a baseline |
| One speaker whose words are the content | 問答 (Q&A) | a transcript |
| Three or more standpoints or sites | 多線並置 (parallel threads) | comparable material per thread |
| A reconstructable sequence of moments | 時間軸 (timeline) | timestamps from documents |
| An image that can hold two paragraphs unnamed | 懸念揭露 (reveal) | rare (C: 1 of 169 pure); use once |

Mixed pieces (C: 98 of 169) pick one spine and borrow at most one move from a second shape: the second shape is the decision table's runner-up (its precondition must hold too), the borrowed move counts toward the 3–5 and is named on the closing line as `<shape>: <move>`. When the user names the spine, borrowing happens only if the request also names the second shape; otherwise the named shape's table plus the cross-shape table are the whole move set. When no shape is named and more than one precondition holds, the table's order is the priority: the first row whose precondition holds is the spine, and sepia's one line names it and the runner-up (`runner-up: none` when only one precondition holds) so the user can override by naming a shape.

## Shape tables

Columns: Move / Source / Sepia check it maps to (I unless marked) / Known cost.

### 場景導入 (scene lead)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| Open on one person doing one small thing in one place, with no explanation of why the piece exists | C: scene or person lead in the majority of 169 | `journalism.md` tells row 1 (announcing lead); `journalism.md` rule 1 | Answer-first domains (postmortems, release notes) win by venue precedence; this move is not used there |
| Hold the first number until the third paragraph or later; a date or time of day in the opening is a scene fact, not a number | C: scene pieces | `journalism.md` rule 1 | Data-led and inverted-pyramid material cannot use it; a count the reader needs at once is a fact before it is a move |
| Cut sections by situation (a room, a shift, a road), not by numbered problems | C: 7 of the 9 pure scene pieces | `professional-pass.md` check 3; `journalism.md` rule 2 | Argument-heavy material scatters when cut by situation; use only on the scene sections of a mixed piece |
| Each section enters through the scene and exits through the institution; the institutional sentences do not outnumber the scene sentences | C: scene pieces | `discourse-pass.md` §1 QUD | Density (check 2) will report scene detail; `journalism.md` rule 8 says which detail is information |
| End by returning to the opening person or object at a later moment; the last sentence does not comment | C: endings return to person 20 / suspended 19 of 169; summary 7 of 169 | `professional-pass.md` check 7 | When the reader needs the outcome, an open ending is a missing fact, not a style choice |

### 倒金字塔 (inverted pyramid)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| The first sentence holds who, when, what, how many; only then walk the clock | C: 6 pure, 22 as a component | `journalism.md` rule 1 (standfirst register); domains answer-first | A long lead creates no `style-pass.md` §5 finding by itself; the risk is a run of three or more near-equal sentences after it |
| Write each provision in full every time (date, amount, deadline); never "as above" | C: inverted-pyramid pieces | check 5 specificity | check 2 will count repeated full names; use in provision-dense sections only |
| Bridge from the main scene to the outside with a run of captions or times, then re-enter with a count and a clock time | C | check 3 | None beyond the general slack rule |
| Non-corrective follow-ups go in a dated block after the body; a correction revises the body with a dated note instead (`journalism.md` rule 6) | C; `journalism.md` rule 6 | check 7 | An update that restates the body is residue; only new facts go there |

### 人物弧線 (person arc)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| Build character from several concrete episodes; no character adjectives | C: 9 pure, 14 component | `professional-pass.md` check 5 specificity; `style-pass.md` §3 inflation adjectives (the §2–3 scan runs on every non-fiction route, SKILL.md) | None |
| After a quotation, one gesture or expression, not an emotion adverb | C: about half of the 169 articles; T: manner adverb near zero (zh.md §1b) | `journalism.md` tells row 5 (manner adverb on speech verbs); on Chinese targets also the zh.md §2 manner-adverb row | A gesture after every quotation is a metronome; three or four per piece |
| At the emotional peak let the quotation stand whole; do not cut it into fragments | C | SKILL.md quoted-material guardrail; `journalism.md` rule 3 | Long quotations raise the quotation share; keep the count low elsewhere. On write from a supplied transcript only: an existing quotation that is already split is never recombined on refactor or recreate (SKILL.md quoted-material guardrail) |
| End on the person's own words or an everyday action, without comment | C: endings quotation 47 / return to person 20 of 169 | check 7 | Same as the scene-lead ending cost |

### 論證式 (argument)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| End a paragraph on a question; the next paragraph answers it with a source's data or words, never the reporter's | C: paragraph-end questions are the norm | `discourse-pass.md` §1 QUD; `journalism.md` tells (self-answered question) | One question per section; more reads as rhetoric |
| Put two or more experts in one section and let one disagree on the record | C: 9 of 11 pure argument pieces | check 4 stance as `journalism.md` rule 7 reads it | Needs two parties on the record; otherwise not available |
| Every number carries a comparison or a conversion; no figure stands alone | C; `journalism.md` rule 4 | check 5; `journalism.md` rule 4 | None |
| One collecting sentence per section at most, and it names the disagreement rather than settling it | C | check 7 | Two per section is a template |

### 數據驅動 (data-led)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| After each absolute figure, a bracket or clause with the rate, the change, or the prior period | C: 17 of 20 pure data pieces | check 5; `journalism.md` rule 4 | Bracket density in non-data venues reads as over-annotation; one conversion per paragraph |
| Convert unfamiliar units into a referent the reader already knows | C | check 5 | The referent is itself a fact with a source |
| State the method in the body (source, definition, limits) in the first person plural or the outlet's third person | C: about half of data notes | check 5; `journalism.md` rule 4 | Reads as a paper outside data pieces; only when the reporter built the dataset |
| After each section's figures, one plain-language reading from someone on the ground, not a reporter verdict | C (the §1b quotation row is a length proxy and licenses no attribution rule, so it is not cited here) | check 7; check 4 stance as `journalism.md` rule 7 reads it | One reading per section or figure cluster; a quotation after every single figure is the metronome this profile forbids |
| Sections by indicator or region, same skeleton, different content; no connective between them | C: data notes | `journalism.md` rule 2 (no connective between sections); check 8 templatedness | Identical skeletons are a uniformity risk; the difference must be in content |

### 問答 (Q&A)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| The preamble carries all background; the exchange repeats none of it | C: 8 pure, 10 component | check 3 | None |
| Keep the speaker's repetition, hesitation, code-switching, self-answering | C: Q&A pieces; `journalism.md` rule 3 | `journalism.md` rule 3 (spoken texture kept); SKILL.md quoted-material guardrail | None beyond the quotation share; the texture is inside quotations and is not a style-scan finding |
| The reporter's checks or additions go in an editor's note outside the quotation (after it, or as a separate bracketed line); on write from a supplied transcript a bracketed gloss may sit inside the quotation as the transcript shows it, but on refactor or recreate no bracketed gloss is inserted into an existing quotation | C | SKILL.md quoted-material guardrail; `journalism.md` rule 3 | None |
| One question per turn; no bundled sub-questions | C | check 8 templatedness | None |

### 多線並置 (parallel threads)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| State the format once ("the following is in each person's own words"); no per-thread reporter lead-in | C: 6 pure, 11 component | check 8 | None |
| Equal room per thread; no thread pre-declared the main one | C | check 4 as `journalism.md` rule 7 reads it | Equal length is a uniformity risk; vary inner shape |
| Switch threads with a subhead, never with 「另一方面」 | C; `journalism.md` rule 2 | `journalism.md` rule 2 and tells row 9; on Chinese targets also the zh.md §2 connective row | None |

### 時間軸 (timeline)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| Quote the original notice or message and stamp its time; let the reader compute the gap | C: 22 as a component | check 5; SKILL.md quoted-material guardrail | On write from supplied source material, select the excerpt the reader needs before quoting it; on refactor or recreate an existing quoted notice is never shortened or reflowed (SKILL.md quoted-material guardrail) |
| Record throughout, judge only in the last section | C | check 4, check 7 | Rarely carries a whole piece (C: 1 pure) |

### 懸念揭露 (reveal)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| Describe the image without naming it for two paragraphs, then a question, then the reveal | C: 1 pure, 2 component | `journalism.md` rule 1 | A fiction device; once per piece at most, and only when the image is a reported fact |

### Cross-shape moves (usable with any spine)

| Move | Source | Sepia check | Known cost |
|---|---|---|---|
| Two registers: the standfirst gives the result, the first body paragraph places the reader | C (qualitative: the split recurs across the close-reading notes, not counted); `journalism.md` rule 1 | `journalism.md` rule 1; `discourse-pass.md` §1 QUD | None |
| Subheads switch; consecutive paragraphs do not open on connectives (one paragraph-initial 「此外」 or 「然而」 is register-normal) | C; T: 「此外」「然而」 single use is register-normal (zh.md §1b); chains are the zh.md §2 row | zh.md §2; `journalism.md` rule 2 | None |
| A paragraph-end question answered by the next speaker | C: the norm | QUD; `journalism.md` tells | One per section |
| The reporter's first person for method, steering a source, recording a silence, or, in a first-person account, narrating what the reporter went to see and observed | C: fixed uses | `journalism.md` rule 5 | A first person that delivers a verdict the reporting did not establish is stance without reporting |
| A dated block for a non-corrective follow-up received after a publication date the facts supply; without that date the fact stays in the body or becomes a TODO; a correction revises the body with a dated note | C; `journalism.md` rule 6 | check 7 | Only new facts; the publication date is never assumed |
| No summary ending: stop on the last fact, quotation, person, or open question | C: 7 of 169 summary endings; T: 「總而言之」 0 per 100k (zh.md §1b) | check 7 | When the venue needs the outcome, end on the outcome as a fact |

## Register defaults

Sentence length, punctuation, quotation marks and connective rates for this register are in `languages/zh.md` §1b and, for the contrast-only human forms, the Human column of §1c; the machine columns there are not voice data, and this body repeats only the two values in the next sentence. One direction is worth naming here because a write under this voice measured against it on 2026-09-16 and landed far outside on dispersion: this register's within-article sentence-length SD has a per-article median of 34 (§1b), and that one write came out flat (SD 10.7; one observation, not an executor-wide measurement). After a write or a recreate, run the `style-pass.md` §5 check (three or more adjacent near-equal sentences) before adding the closing line, and where it fires, merge two sentences or let a clause carry a subordinate fact (the §5 fix). No length target: mean length is not a signal (§1b, zh.md §5); dispersion is the trait. In English journalism none of this is measured; the moves still apply as inference, the numbers do not.

## Voice fit

None on professional routes. The registry entry in `references/voices/registry.md` documents the opt-in only.

## Worked example

Synthetic facts (approved 2026-09-16; nothing else may be used, and any fact missing from this list is a TODO): 2026-03-04, 14:02 to 14:47 (UTC+8); an unnamed regional hospital emergency department in northern Taiwan; the retry queue had no jitter, 412 resends landed inside one 200 ms window, downstream services rate-limited each other; the cause was found at 14:41 and `RETRY_JITTER=full` was set at 14:47; the triage nurse (role only) clipped three paper triage slips to the whiteboard at 14:05 and kept triaging on paper; one synthetic quotation from the nurse, written for this example: 「電腦轉圈，我就先用紙。」; baseline about 3 resends per minute in a normal hour; the on-call platform engineer (role only) said the queue's default had never been reviewed; the default was changed for all queues on 2026-03-06; publication date 2026-03-05, supplied as the exercise's publication-context input and listed here so that no shape assumes it (it is not a reported fact).

The three Afters below are **write** outputs from the approved fact list, not refactors or recreates of the Before; the tables under each After list the Before's departures and what the written After does instead, not edits applied to the Before. The example is framed as first published on 2026-03-05, the day after the incident, so the inverted pyramid's "this week" condition is met and the 2026-03-06 default change arrives after publication, which is what makes it an update block under `journalism.md` rule 6; the frame is the publication-context input listed with the facts, not a reported fact. The Before is shown only to name the register departures each After avoids; its quotation 「系統一直轉圈圈，我們完全沒辦法作業。」 is itself synthetic and is not a source's words. On a real refactor or recreate, an existing quotation is never replaced or reworded (SKILL.md quoted-material guardrail); the Afters replace it here only because they are written fresh from a fact list that contains a different approved quotation.

Before (synthetic, written to carry the register's departures):

> 本文將探討一起發生在北部某區域醫院急診的系統事故。2026年3月4日下午，該院的掛號與檢傷系統突然變得非常緩慢，值班護理師無奈地表示：“系統一直轉圈圈，我們完全沒辦法作業。”值得注意的是，事故的根本原因——重試佇列缺乏抖動機制——導致在極短時間內產生了大量重複請求，進而引發下游服務相互限流的連鎖反應。技術團隊隨後迅速地進行了排查，並在當天下午成功地修復了問題。總而言之，這起事故凸顯了系統韌性的重要性，也提醒我們在設計重試機制時必須更加謹慎。

After A — 場景導入 (moves: open on a person; hold the first number until the third paragraph; update block; no summary ending):

> 3 月 4 日下午 2 點 05 分，北部一間區域醫院的急診，值班護理師把紙本檢傷單夾到白板上，之後的分級改用手寫。「電腦轉圈，我就先用紙。」
>
> 電腦轉圈的原因：重試佇列沒有設 jitter，失敗的請求在同一個時間窗裡反覆重送，下游服務於是互相限流。
>
> 夾上白板的紙本檢傷單有三張；夾上去的時候，重送已經進行了三分鐘：200 毫秒內 412 次，而平時每分鐘大約只有 3 次。2 點 41 分找到原因；值班平台工程師說，這個佇列的預設值從來沒有人檢視過。2 點 47 分，`RETRY_JITTER=full` 設上。
>
> 更新（3 月 6 日）：所有佇列的預設值已改。
>
> Voice applied: tw-journalism/場景導入 — moves: open on a person, hold the first number, update block, no summary ending

| Departure in the Before | What the After (a write) does instead; move | Check |
|---|---|---|
| 「本文將探討…」 | A date, a place, a person and a recorded action open the piece; open on a person | `journalism.md` tells row 1 |
| Cause and consequence stated before any scene, with the date as the only concrete detail | The count of slips and every figure wait for paragraph three; the opening keeps only the date and time of day, which the move treats as scene facts; hold the first number | `journalism.md` rule 1 |
| 「無奈地表示：“…”」 | The recorded action, then the approved quotation in 「」, no attribution verb, no adverb (a write from the fact list; on refactor the Before's quotation would stay as written) | zh.md §2 manner adverb; `journalism.md` rule 3 (attribution by context or a post-posed 說) |
| 「——…——」 insertion with single-glyph dashes presenting the cause without a quantified baseline | One plain sentence carries 412, 200 ms and the 3-per-minute baseline, in paragraph three; the two-cell paired 「──…──」 would itself be register-normal (zh.md §1b), the single-glyph 「—」 is the glyph slip | check 5; zh.md §1b single-glyph 「—」 row |
| 「迅速地」「成功地」 | Absent (manner adverbs; register default) | zh.md §2 manner-adverb row |
| 「非常」 | Absent because no approved fact supports an intensifier, not because one 「非常」 departs from the register (§1b: stacking against 「很」 is the departure) | check 5 |
| 「總而言之…重要性…謹慎」 | The piece stops on the dated update; no summary ending. The update block is the cross-shape move and is counted, as in After B and After C; the frame that makes it post-publication is a stated assumption of the exercise | check 7 |

Known cost and what the blind review taught: the shape's "return to the opening person or object at a later moment" move is not used, because the approved fact list has no later whiteboard fact; an earlier draft returned to the same 2 點 05 分 moment and the declared-voice review correctly reported it as density, not as the move. Four drafts before that added a gesture, a closing count, a pronoun and an attribution of the discovery that were in no fact list, and reviews caught each under check 5; one more claimed "scene in, institution out" for a piece with no sections. The precondition section and the audited closing line exist for exactly these. 「三分鐘」 is arithmetic on two approved times (14:02, 14:05).

After B — 倒金字塔 (moves: the first sentence holds who, when, what, how many; updates in a dated block; no summary ending). "Write each provision in full" is not claimed: the facts hold incident measurements and a setting, not provisions. A data-led After was drafted first and withdrawn: the fact list has a baseline but no source or method for the count, the decision table says a shape whose precondition is not met is not chosen, and a worked example that chooses it anyway would teach the opposite. The facts do hold the inverted pyramid's precondition (date, actor, outcome, count), and the stated publication frame (2026-03-05) puts the events inside the shape's "this week" window and the 03-06 change after publication.

> 3 月 4 日下午 2 點 02 分起，重試佇列把失敗請求在 200 毫秒內重送了 412 次，下游服務對彼此限流；2 點 47 分設上 `RETRY_JITTER=full`。〔TODO：何時恢復、是否因此恢復，事實清單未給。〕
>
> 重試佇列沒有設 jitter。平時每分鐘大約 3 次重送；這 200 毫秒裡的量相當於平時兩個多小時的總和。2 點 41 分找到原因。
>
> 急診端，值班護理師 2 點 05 分起把三張紙本檢傷單夾上白板。「電腦轉圈，我就先用紙。」
>
> 值班平台工程師說，這個佇列的預設值從來沒有人檢視過。
>
> 更新（3 月 6 日）：所有佇列的預設值已改。
>
> Voice applied: tw-journalism/倒金字塔 — moves: first sentence holds who when what how many, update block, no summary ending

| Departure in the Before | What the After (a write) does instead; move | Check |
|---|---|---|
| 「本文將探討…」 → one sentence with date, actor, count and the setting time; recovery is a TODO because the facts stop at the setting | First sentence holds who, when, what, how many | `journalism.md` rule 1 (standfirst register); check 5 |
| 412, 200 ms, the 3-per-minute baseline and the derived "two hours" (412 ÷ 3 ≈ 137 minutes) each written out | (register default under `journalism.md` rule 4; not the provisions move) | check 5 |
| The nurse's action and words, then the engineer's statement, each in its own paragraph without a verdict | (register default) | check 7 |
| 「總而言之…」 → a dated update line, and the piece stops there | Update block; no summary ending | check 7; `journalism.md` rule 6 |

Known cost of After B: the first sentence runs long with several commas, which is this shape's norm and will read as a rhythm candidate if the rest of the piece is uniform; here the following sentences are short. The derived figure is accepted under check 5 because both inputs are in the approved list.

After C — 論證式 spine (moves: question answered by the next speaker; update block; no summary ending). The clock times are used as facts, not as the 時間軸 shape: that shape's precondition is timestamps from documents, the fact list gives no document provenance, and a shape whose precondition is unmet is not chosen, so no timeline move is claimed. Two parties appear, but they do not disagree on the record, so the argument shape's "two experts, one disagreeing" move is not claimed.

> 3 月 4 日 14:02，重試佇列開始把失敗的請求重送。14:41 才找到原因。中間的 39 分鐘（14:02 到 14:41 的差），急診那邊怎麼過的？
>
> 值班護理師 14:05 就把三張紙本檢傷單夾上白板。「電腦轉圈，我就先用紙。」
>
> 系統這邊的狀況是：重試佇列沒有設 jitter，200 毫秒內重送 412 次，而平時每分鐘大約 3 次；下游服務對彼此限流。
>
> 值班平台工程師說，這個佇列的預設值從來沒有人檢視過。14:47，`RETRY_JITTER=full` 設上。
>
> 更新（3 月 6 日）：所有佇列的預設值已改。
>
> Voice applied: tw-journalism/論證式 — moves: question answered by the next speaker, update block, no summary ending

| Departure in the Before | What the After (a write) does instead; move | Check |
|---|---|---|
| 「本文將探討」 → two timestamps and a question that the nurse, not the reporter, answers in the next paragraph | Question answered by the next speaker | `discourse-pass.md` §1; `journalism.md` tells (self-answered question) |
| 412 in 200 ms set against the 3-per-minute baseline; 三張 and the clock times stand alone, so the "every number carries a comparison" move is not claimed | (register default; `journalism.md` rule 4 satisfied where a comparison exists) | check 5 |
| 「總而言之…」 → a dated update line | Update block (cross-shape) | check 7; `journalism.md` rule 6 |
| The piece stops on the update, no verdict | No summary ending (cross-shape) | check 7 |

Known cost of After C: the nurse and the engineer describe different sides of the same event and do not contradict each other, so the argument shape's central move (a disagreement on the record) is absent; with only these facts the piece is a clocked sequence wearing an argument's opening question. An earlier draft's closing line claimed that move and a "timestamps from the record" move that is in no table; both are gone.

## Grounding

Blind review of After A by a fresh executor (Claude Opus 5) on the professional route, 2026-09-16, once with the voice declared by the exact phrase and once without. The reviewed text is the After printed above except for one clause: the review read 「白板上那三張紙本檢傷單夾上去的時候」, the undeclared run reported 「那三張」 as a definite reference to a count never introduced (check 5), and the printed After now reads 「夾上白板的紙本檢傷單有三張；夾上去的時候」. Both runs loaded `domains/journalism.md`; only the declared run loaded `voice-skills.md` and this body. Neither run printed a `Voice fit:` line (professional route, #227).

- Declared: the report named the voice and shape, confirmed the precondition (scene facts with a time), and listed the three shape moves it saw performed (open on a person, first number held to paragraph three, no summary ending); it did not name the dated update block, the cross-shape move the closing line now counts, so on that head the audited line and the review differ by that one move; scene detail was listed as the voice's known cost, not a defect. `Passed: 1, 2, 3, 4, 6, 7, 8, 9, 10`. Failed: `discourse-pass.md` §1 (four first sentences form a clean outline; the implied questions run "what → why → how big and who fixed it → afterwards", a linear interview) and `#5 Specificity` in two parts: the opened scene is never closed (when the department went back to the system is neither a fact nor a TODO, which is where the unused "return to the person" move would sit), and the load-bearing figures carry no source or method, with the two rates in different units. Style scan: none; rhythm 50/11/66/50/33/19/18 characters, no run of three near-equal sentences. `Verdict: isolated hits → refactor`.
- Undeclared: `Passed: 1, 2, 3, 6, 7, 8, 9, 10`. Failed: `#5` three times (the 「那三張」 backreference, now fixed; the two rates in different units and 「大約 3 次」 unsourced; the system facts without provenance, the engineer attached to one sentence only) and `#4 Stance` twice (three agentless actions: found the cause, set the flag, changed the defaults; no comparison or verification paragraph, so the QUD holds only briefing → cause → consequence). It read the dated update block as rule-6-conformant. `Verdict: isolated hits → refactor`.

What the pair shows: with the voice declared, the review credits the shape's moves and stops treating scene detail as filler, then reports the shape's real weaknesses, a linear question order and an opened scene left open. Without it, the same text collects source and agency findings that are about missing facts. Both readings are correct for their frame; neither is passable on these facts alone, because the approved list closes no scene, sources no count, and names no agent for the fix, which is why the After carries TODO-shaped gaps rather than sentences. Six earlier drafts of After A were reviewed the same way; reviews caught a gesture, a closing count, a pronoun, an attribution of the discovery, a claimed move without sections, and a return to the same moment, none of them in the fact list, and each is recorded under the worked example. The write arm (`/sepia:sepia-write` on the approved fact list with the phrase) loaded this body, produced a four-paragraph piece with every fact traceable to the list, listed four TODOs for facts it did not have, and ended with `Voice applied: tw-journalism/場景導入 — moves: open on a person, sections cut by situation, scene in institution out, return to the object`. The last name on that line is a deviation the line makes visible, and the line as printed is not a conforming output: the move requires returning at a later moment, the fact list has no later whiteboard fact, and the piece returned to the 14:05 slips through a derived time gap. The conforming line for those facts names the first three moves only, and a review under this profile reports the fourth name as a move claimed without its fact (check 5). The same write measured mean sentence length 22.8 characters with within-article SD 10.7, against 59/34 for the register (zh.md §1b); the executor's default sentence shape is a dimension this profile did not yet push on, and the Register defaults line above now says to check it. One worked example and one write, not measured evidence.
