# Chinese calibration for the style pass

Load this file at the style-pass step whenever the target text is Chinese, in any variant, on any route. It changes nothing else about the route. The English ban lists in `style-pass.md` §3 do not transfer word for word; what transfers is the *shape* of the checks — the syntax templates of §2, the restore list of §4, the rhythm check of §5, the whitelist of §7 — and this file says what each shape looks like in Chinese.

Evidence: one measured corpus, HC3-Chinese — 6,586 human and 6,586 ChatGPT answers to the same open-domain questions, GPT-3.5-era ChatGPT, Simplified Chinese, 2023 — analysed with 159 Chinese CTAP features by 朱君輝 et al., CCL 2023 (Z), with Guo et al. 2023 (H) supplying a second measure on the same corpus; a 2025 joke-generation study by 蔣彥廷 and 應以周, CCL 2025 (J), is used only where it contradicts Z. Everything else below is a Sepia inference or a marked editorial heuristic. Stable source identities are in the repository research ledger.

## 1 Measured (Z, per-answer means; H where named)

| Feature | Human | ChatGPT | Unit and note |
|---|---|---|---|
| Sentence-length SD | 9.248 | 6.729 | words (詞); in characters (字) 15.150 vs 12.842 — the gap holds in both units |
| Mean sentence length | 25.067 | 21.823 | words — humans *longer*; in characters 40.893 vs 42.396, the direction flips, so length itself is not a signal |
| Paragraphs per answer | 1.442 | 3.681 | ChatGPT wrote *more* paragraphs; mean paragraph length 123.907 vs 92.747 characters |
| Punctuation density | 0.135 | 0.136 | Z; the same corpus measured as punctuation share of tokens reads 16.0% vs 13.4% (H) — contradictory measures, not a signal |
| 語氣詞 density | 0.016 | 0.003 | five times higher in human answers |
| 連詞 density | 0.013 | 0.036 | 「和」 alone: 4.13 vs 11.76 per answer |
| Pronoun density | 0.052 | 0.069 | second person 0.010 vs 0.021 |
| Monosyllabic word share | 0.483 | 0.379 | disyllabic share 0.445 vs 0.532; disyllabic word count was selected as a key feature by both of Z's filters |
| Type-token ratio | 0.725 | 0.543 | content-word richness 0.822 vs 0.647 |
| Mean dependency distance | 3.900 | 3.659 | longest 29.452 vs 23.991 |

## 2 What to hunt (Sepia inferences from §1; shapes of `style-pass.md` §2)

| Shape | Chinese form | Fix |
|---|---|---|
| Connective stacking (連詞 density 0.036 vs 0.013) | 「和／以及／並且／同時／此外／因此／然而」 chained across clauses; 「和」 joining whole clauses rather than nouns | Delete the connective and let juxtaposition carry the link; Chinese parataxis is the human default |
| Second-person address outside dialogue or instructions | 「你會發現」「您可以」 in expository prose | Delete or recast as a statement |
| Disyllabic padding where a monosyllable is idiomatic | 「進行討論」「加以說明」「予以處理」「做出決定」 | 「討論」「說明」「處理」「決定」 — the verb alone |
| Flat sentence length (SD 6.729 vs 9.248 words) | Runs of adjacent sentences of about the same length | Apply the §5 check as written (runs of three or more adjacent near-equal sentences): split one long sentence, merge two short ones, delete a clause. §5 sets no length cutoff in any language; no Chinese short- or long-sentence share is measured, and none is invented here. Count in whichever unit you use consistently — the SD gap holds in both 詞 and 字 |

## 3 What to restore (Sepia inferences; shape of `style-pass.md` §4)

Sprinkled, never poured, and only where the register allows: sentence-final and mid-sentence 語氣詞 (啊、吧、呢、嘛、喔、啦、耶) — the largest measured gap in §1; monosyllabic verbs and adjectives; a spread of sentence lengths; subject ellipsis and colloquial contraction where a native writer would drop the subject, the Chinese counterpart of §4's contractions. Formal venues keep their register: a legal notice does not get 「嘛」.

## 4 Editorial heuristics — unmeasured, marked

Reported by Taiwan editors and readers in 2026 (自由時報 2026-07-12; 數位時代 2026-04-22; ledger "Consulted" table); none has a corpus number, and each is a Chinese form of a template already in `style-pass.md` §2:

| Reported tell | Maps to |
|---|---|
| 「不是…而是…」「這不是 X，而是 Y」 | §2 "it's not X, it's Y" |
| Nominalized subjects 「○○性／○○感／○○化」 (「自我的探索」 for 「找自己」) | §2 nominalization |
| Three parallel clauses or images, everywhere | §2 rule of three |
| Paragraph openers 「其實…」「事實上…」; abstractions in quotation marks (「趨勢」「關鍵」「必然」) | §3 formula phrases |

## 5 Not signals in Chinese

Punctuation density and comma or period counts (§1: contradictory measures); long sentences counted in words (humans are longer); paragraph count (ChatGPT split *more*, the reverse of the folk belief that AI writes one block); word-frequency level (Z finds humans using commoner words, J finds LLMs doing so — two corpora, two eras, no rule). Mainland Chinese lexicon in a Taiwan venue (視頻、軟件、質量 for 影片、軟體、品質) is a register mismatch under the venue-corpus guardrail in `SKILL.md`, not an AI tell: fix it only when the venue is Taiwanese and the author's own samples do not use it.

## 6 Evidence boundary

One corpus, one model era, Simplified Chinese question answering, default un-prompted ChatGPT of 2023. No study measures 2024–2026 models on Chinese narrative or expository prose; J covers single-sentence jokes from four 2025 models and reports lexical richness (human 0.547 vs 0.384–0.461) but no sentence or punctuation statistics. No Taiwan academic study compares human and machine Traditional Chinese; the Taiwan sources above are editorial. Treat every number here as a direction observed once, not a calibration constant.
