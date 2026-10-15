# sepia

**English** | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> De-AI writing at the layer that actually gives AI away. Fiction gets its narrative architecture repaired before anyone touches word choice; professional documents (release notes, PR replies, postmortems, tickets, technical articles) each get rules matched to their venue.

A portable [Agent Skill](https://agentskills.io/specification): any agent that speaks the standard can load it, and the [Skills CLI](https://skills.sh), which supports 77+ agents, installs it with one command. Claude Code, Codex, Grok Build, Antigravity, and QwenPaw additionally get native plugin packaging. One canonical `SKILL.md`, no per-platform forks. Four operations: **write**, **review** (diagnose only), **refactor** (minimal edits), **recreate** (full rewrite).

## Table of Contents

- [Why another humanizer](#why-another-humanizer)
- [Operation entries](#operation-entries)
- [Experimental: composing with voice skills](#experimental-composing-with-voice-skills)
- [Sentence rhythm and Chinese calibration](#sentence-rhythm-and-chinese-calibration)
- [Install](#install)
- [Uninstall](#uninstall)
- [Layout](#layout)
- [Star History](#star-history)
- [Sources](#sources)
- [Support](#support)
- [License](#license)

---

## Why another humanizer

Every popular humanizer edits word choice and syntax. [StoryScope](https://arxiv.org/abs/2604.03136) (Russell et al., 2026: 61,608 stories, human + 5 frontier LLMs) showed that a classifier using **narrative-structure features alone** detects AI fiction at 93.2% macro-F1. In the same study's LAMP-edited condition, where human editors had rewritten the surface style, detection dropped only from 95.5% to 93.9%. The tells that survive are architectural: themes explained by the narrator, single-track causally-tidy plots, emotions rendered only as bodily sensation, no real-world references, no reader, linear time, endings resolved by protagonist growth and acceptance.

sepia turns those measured gaps, together with the related studies digested in [`research/`](research/), into a three-pass writing and revision protocol for fiction:

| Pass | Layer | Examples |
|---|---|---|
| 1 | Narrative architecture (fiction) | stop explaining the theme, loosen the causal chain, back-load revelations, mix emotion modes, sparse character networks, name real things |
| 2 | Discourse flow | de-template the paragraph-question sequence, fix the mid-story sag, vary rhythm and positions |
| 3 | Surface style | the classic layer: clichés, syntax templates, vocabulary, register |

A 30-feature diagnosis rubric and per-model fingerprints across two layers apply when the writing or executing model is known:

| Model family | Narrative layer (StoryScope) | Sentence-level prose layer (Vendor prompting guides) |
|---|---|---|
| Claude | Measured | Claude Fable 5.1 and Mythos 5.1, Fable 5 and Mythos 5, Opus 5, Opus 4.8 |
| GPT | Measured | GPT-5.6, GPT-6 Astra |
| Gemini | Measured | Gemini 3 and 3.1 |
| DeepSeek | Measured | Consulted (no guidance published) |
| Kimi | Measured | Consulted (no guidance published) |

> **Notice:** Vendors that publish no prompt guidance are recorded as consulted, not guessed.

Professional prose fails differently, and the structure-level finding holds there too: a 2026 replication of StoryScope on 2,250 company blog posts against 11,250 AI mirrors separated them at 98.0 macro-F1 from structural features alone, with the AI shape described as tidy and self-announcing (`SLOPSHAPE-2026` in the ledger, arXiv:2609.15369; a preprint whose features are LLM-scored; it tested detection of original and model-self-reworded posts, never human editing). The studies digested in [`research/`](research/) point at filler that carries no information, hedging where a judgment was needed, chatbot leftovers, register that ignores the venue, and formatting that looks stamped out. Each document type gets a thin rule file on top of one shared checklist:

| Domain | The gist |
|---|---|
| Release notes / announcements | user impact first, artifacts per claim, no marketing inflation |
| PR / issue replies | answer first, cite `file:line`, no reflex praise, length ∝ stakes |
| Postmortems | blameless toward people, merciless toward mechanisms; timestamps, dead ends, owned action items |
| Tickets / work orders | title = outcome, testable acceptance criteria, link don't repeat |
| Technical articles | open at the problem, one real dead end, one committed opinion, numbers with conditions |
| Narrative non-fiction (popular science, columns told as a story) | nothing invented, missing specifics become TODOs; the story's architecture is checked with the fiction rubric, read as a heuristic |
| Long-form journalism (features, investigations, data stories) | lead and body in two registers, quotations keep their spoken texture, every number carries a comparison, no summary ending |

> **Governing principle:** Calibrate to the human distribution, don't invert the AI one. Humans sit at moderate values; a story with every rule applied is a new fingerprint. The skill selects 3–5 moves per story and leaves slack.

## Operation entries

The complete plugin package gives Claude Code, Codex, Grok Build, Antigravity, and QwenPaw a general router plus five direct entries. On QwenPaw the package registers no commands of its own; the host's `/<skill-name>` dispatch serves each installed skill:

| Operation | Claude Code | Codex | Grok Build | Antigravity | QwenPaw | Meaning |
|---|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | `/sepia-write` | Create new prose |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | `/sepia-review` | Diagnose without editing |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | Make minimal in-place edits |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | Rewrite from the source facts and intent |
| hemingway | `/sepia-hemingway` | `$sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | Write or refactor fiction with the built-in Hemingway voice applied |

The general `/sepia` (Claude Code, Grok Build, Antigravity, and QwenPaw) or `$sepia` (Codex) router remains available. What was verified on each platform is stated under [Install](#install).

> **Notice:** Standalone wrapper installation is unsupported. The operation wrappers depend on their sibling canonical skill; install the complete plugin package.

## Experimental: composing with voice skills

Since v0.4.0, sepia defines an interface for stacking a voice or style skill on top of it — a minimalism method, a brand voice, a persona guide. It is opt-in: tell sepia the voice skill is in play, and it loads `references/voice-skills.md` over the normal route. No external voice is loaded unless you say so.

The interface contract operates under fixed precedence rules across operations and routes:

| Rule dimension | Contract specification |
|---|---|
| Architecture | sepia's architecture decisions come first. |
| Move selection | Voice moves are applied selectively (3–5 signature moves per piece, fewer when a sparse shape or the facts offer fewer; formula endings deliberately broken sometimes). |
| Review diagnostics | Review reports the voice's known costs instead of fixing them away. |
| Uniformity enforcement | Uniformity findings keep full strength: a voice does not excuse a metronome. |
| Professional register | On professional routes, the venue still sets the register. |
| Conflict resolution | Direct conflicts come back to you. |

> **Notice:** The voice-skills interface is grounded in one blind review experiment on a strict-minimalism specimen — a worked example, not measured evidence.

Two built-in profiles ship under `references/voices/`, alongside a persona profile kind with declared override rights:

| Profile | Target routes | Source & characteristics | Opt-in & invocation |
|---|---|---|---|
| Hemingway (`references/voices/hemingway.md`) | Fiction and professional prose | Iceberg omission for fiction, the Kansas City Star rules for professional prose; each move traced to its source | Direct entry `/sepia-hemingway` (or `$sepia-hemingway`). On fiction, asking for strong de-AI on a story counts as opting in (sepia announces the profile and how to decline). Without an opt-in, a fiction review only reports when the text fits the profile and loads nothing. |
| Taiwan long-form journalism (`references/voices/tw-journalism.md`) | Professional routes only | Nine narrative shapes with their moves, drawn from private human-side journalism measurement and its close reading | Opt-in phrase: `"apply the Taiwan journalism voice"`. Follows the same rules as Hemingway. |
| Persona template (`references/voices/PERSONA-TEMPLATE.md`) | Author-defined | One writer's style with declared override rights; checked by `scripts/check_persona.py` | Author-created profile. Template at `references/voices/PERSONA-TEMPLATE.md`. |
| Nyaneko (`references/voices/personas/nyaneko.md`) | Professional routes only | Built-in companion voice written from the maintainer's voice specification with her own exemplars | Opt-in phrase: `"apply persona Nyaneko"` or `「套用 persona Nyaneko」`. |

### Writing with a persona: a short how-to

sepia's rules remove tells. Warmth has another source: the writer knowing who is speaking, and to whom. One case from this project's own release, with nothing measured: the v0.12.0 Threads post was drafted twice by the same model from the same release notes. The first prompt handed it a skeleton (version line, bullets, fixes, engineering note, update line) and got a form filled in. The second prompt handed it an identity, "I maintain this project and just shipped v0.12.0; talk to my followers in my own voice; how you organise it is yours", plus the notes as the only fact source and the platform's limits, and got the post the maintainer kept. A sepia review of that post then found its tells clustered at the opening and the close (an opening about how the change came to be, a maxim ending, a few absolutes), and a refactor took them out without touching the middle.

The order that worked:

1. Identity first.
2. Facts separately, as the only source.
3. Constraints stated as platform limits, with the structure left to the model.
4. sepia as the check.

```text
Do not use tools; everything you need is below.
I am <who>, writing for <whom>, about <what just happened>. Use my own voice; how to organise it is yours.
Platform limits: <length, markup, mentions>.
Facts come only from the notes below; numbers and identifiers must match them.
===== notes =====
<the source document>
```

A persona profile is that identity written down once so every piece starts from it: what they are to the reader, what their first sentence does, how warmth attaches to a fact, what they never do, and pieces in their own voice as exemplars. The template is `references/voices/PERSONA-TEMPLATE.md`, the built-in `references/voices/personas/nyaneko.md` is a worked example, and the interface validator checks the profile structure:

```bash
python3 scripts/check_persona.py <file>
```

Write your own; the exemplars carry more than the description does.

## Sentence rhythm and Chinese calibration

The style pass checks the *spread* of sentence lengths, the one syntactic measure on which every study that measured it agrees: human text varies more within a passage, in English and in Chinese.

| Syntactic measure | Status | Empirical basis |
|---|---|---|
| Sentence length spread | Checked signal | Within-passage variance is consistently higher in human text across English and Chinese studies. Evidence and numbers are in [`research/rhythm-syntax.md`](research/rhythm-syntax.md). |
| Mean sentence length | Discarded | Measured directions contradict each other across corpora. |
| Punctuation counts | Discarded | Measured directions contradict each other across corpora. |
| Paragraph length | Discarded | Measured directions contradict each other across corpora. |

Chinese text loads `references/languages/zh.md`, calibrating the style pass across four distinct evidence layers:

| Layer / Source | Nature of evidence | Corpus & calibration details |
|---|---|---|
| HC3 (2023) | Measured corpus | Human-vs-machine Chinese corpus baseline. |
| Traditional Chinese journalism | Human-side empirical measurement | About two thousand articles from one unnamed Taiwanese publication spanning about ten years (corpus not distributed; digest in [`research/zh-news-corpus.md`](research/zh-news-corpus.md)). |
| Contrast group | Machine-side empirical contrast | 119 synthetic pieces across three models using one shared base prompt with a one-line variant for one model. |
| Taiwan conventions | Normative standard | Short normative section of Taiwan writing conventions drawn from public standards and first-tier consensus. |

> **Notice:** The limits of all three empirical Chinese sources are stated in `references/languages/zh.md`.

## Install

> **Notice:** Every command below is written for **user scope** — install once, use it in every project.

### Any agent (Skills CLI, 77+ agents)

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update sepia -g             # update
npx skills remove sepia -g             # uninstall
```

Installs on every agent the [Skills CLI](https://skills.sh) supports — Cursor, Cline, Windsurf, Copilot, OpenCode, goose, and more. Pick your agents when prompted. Runtime behavior outside the five platforms below has not been exercised by us; the skill is plain markdown under the Agent Skills standard, so file an issue if your agent trips on it.

> **Notice:** "Verified" means the install completes and the sepia entries appear. The five native plugin installers were each exercised with a live install (QwenPaw's by its contributor). Whether the entries then behave as documented has not been checked platform by platform.

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

> **Tip:** The in-session `/plugin install` dialog asks you to pick a scope — choose **User** there.

### Codex

```bash
# install
codex plugin marketplace add Nanako0129/sepia
codex plugin add sepia@sepia

# update — refresh the marketplace snapshot, then re-add to pick up the new version
codex plugin marketplace upgrade sepia
codex plugin add sepia@sepia
```

### Grok Build

```bash
# install
grok plugin install Nanako0129/sepia --trust

# update
grok plugin update
```

Grok also auto-discovers a Claude Code install of sepia if you have one; either route works.

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### QwenPaw

```bash
# install: qwenpaw takes a local directory (or a zip URL), so clone first;
# the package's skills symlink resolves inside the clone
git clone https://github.com/Nanako0129/sepia
qwenpaw plugin install ./sepia/.qwenpaw-plugin

# uninstall
qwenpaw plugin uninstall sepia
```

> **Notice:** Contributor-verified on QwenPaw 2.2.1 (#250, #289; not reproduced by the maintainer): the install completes, the packaged `skills` symlink is followed into a real tree by `shutil.copytree`, and `/sepia <text>` and `/sepia-write <text>` each start an agent turn through the host's skill dispatch. The other four entries use the same dispatch and were not run one by one. If the package cannot read its skills (a zip install, or a checkout without symlink support), it logs one error and registers nothing; install from a git clone instead.

### Project scope (alternative)

When one repo should pin its own copy, commit `skills/sepia/` into that repo as `.agents/skills/sepia` (Codex + Antigravity) or `.claude/skills/sepia` (Claude Code).

## Uninstall

Each tool uses its native command:

```bash
# Claude Code
claude plugin uninstall sepia@sepia --scope user

# Codex
codex plugin remove sepia@sepia

# Grok Build
grok plugin uninstall sepia

# Antigravity
agy plugin uninstall sepia

# QwenPaw
qwenpaw plugin uninstall sepia
```

## Layout

```text
sepia/
├── plugin.json              # Antigravity packaging
├── skills/
│   ├── sepia/                # canonical skill (Agent Skills standard)
│   │   ├── SKILL.md          # routing, operations, calibration rules, guardrails
│   │   └── references/       # passes, rubric, fingerprints, domain rules, languages/zh.md, voice-skills (experimental)
│   ├── sepia-write/SKILL.md  # thin fixed-operation wrappers
│   ├── sepia-review/SKILL.md
│   ├── sepia-refactor/SKILL.md
│   ├── sepia-recreate/SKILL.md
│   └── sepia-hemingway/SKILL.md  # fiction write/refactor with the built-in voice
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .qwenpaw-plugin/         # QwenPaw packaging (plugin.json, plugin.py, skills symlink)
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
└── research/                # digested evidence base with sources
```

## Star History

<a href="https://www.star-history.com/?repos=nanako0129%2Fsepia&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&theme=dark&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
  </picture>
</a>

Star history growth over time for Nanako0129/sepia.

## Sources

Full digests with links are in [`research/`](research/). Primary studies include:

| Source | Venue / Identifier |
|---|---|
| StoryScope | [arXiv:2604.03136](https://arxiv.org/abs/2604.03136) |
| LAMP | [CHI 2025](https://arxiv.org/abs/2409.14509) |
| Measuring AI Slop | [arXiv:2509.19163](https://arxiv.org/abs/2509.19163) |
| Reinhart et al. | [PNAS 2025](https://arxiv.org/abs/2410.16107) |
| Russell et al. | [ACL 2025](https://arxiv.org/abs/2501.15654) |
| NarraBench | [arXiv:2510.09869](https://arxiv.org/abs/2510.09869) |
| Echoes in AI | [PNAS 2025](https://arxiv.org/abs/2501.00273) |
| QUDsim | [COLM 2025](https://arxiv.org/abs/2504.09373) |
| Beguš | [2024](https://arxiv.org/abs/2310.12902) |
| Beyond Checkmate | [EMNLP 2025](https://arxiv.org/abs/2501.19301) |
| Nonaka & Perry | [2025](https://arxiv.org/abs/2510.18932) |
| Chakrabarty et al. | [2026](https://arxiv.org/abs/2510.13939) |
| Shan, Lee & Hao | [2026](https://arxiv.org/abs/2608.27855) |
| Rohrbacher et al. | [2026](https://arxiv.org/abs/2609.02482) |
| Sourati et al. | [2026](https://arxiv.org/abs/2502.11266) |

## Support

You can use sepia for free without an account. The research behind every rule is open. Ongoing costs are just maintainer time and two kinds of model quota: delegating literature surveys to research agents that read primary papers, and running live models to test rule changes on A/B stories and cross-platform end-to-end reviews before shipping. You can support the project on Patreon.

[![Support sepia on Patreon](https://img.shields.io/badge/Support_on_Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/Nanako0129/membership)

## License

MIT
