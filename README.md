# sepia

**English** | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> De-AI writing at the layer that actually gives AI away. Fiction gets its narrative architecture repaired before anyone touches word choice; professional documents (release notes, PR replies, postmortems, tickets, technical articles) each get rules matched to their venue.

A portable [Agent Skill](https://agentskills.io/specification): any agent that speaks the standard can load it, and the [Skills CLI](https://skills.sh), which supports 77+ agents, installs it with one command. Claude Code, Codex, Grok Build, and Antigravity additionally get native plugin packaging. One canonical `SKILL.md`, no per-platform forks. Four operations: **write**, **review** (diagnose only), **refactor** (minimal edits), **recreate** (full rewrite).

## Why another humanizer

Every popular humanizer edits word choice and syntax. [StoryScope](https://arxiv.org/abs/2604.03136) (Russell et al., 2026: 61,608 stories, human + 5 frontier LLMs) showed that a classifier using **narrative-structure features alone** detects AI fiction at 93.2% macro-F1. In the same study's LAMP-edited condition, where human editors had rewritten the surface style, detection dropped only from 95.5% to 93.9%. The tells that survive are architectural: themes explained by the narrator, single-track causally-tidy plots, emotions rendered only as bodily sensation, no real-world references, no reader, linear time, endings resolved by protagonist growth and acceptance.

sepia turns those measured gaps, together with the related studies digested in [`research/`](research/), into a three-pass writing and revision protocol for fiction:

| Pass | Layer | Examples |
|---|---|---|
| 1 | Narrative architecture (fiction) | stop explaining the theme, loosen the causal chain, back-load revelations, mix emotion modes, sparse character networks, name real things |
| 2 | Discourse flow | de-template the paragraph-question sequence, fix the mid-story sag, vary rhythm and positions |
| 3 | Surface style | the classic layer: clichés, syntax templates, vocabulary, register |

Plus a 30-feature diagnosis rubric and per-model fingerprints in two layers: narrative tells measured by StoryScope (Claude, GPT, Gemini, DeepSeek, Kimi) and sentence-level tells taken from the vendors' own prompting guides (Claude Fable 5.1 and Mythos 5.1, Fable 5 and Mythos 5, Opus 5, Opus 4.8; GPT-5.6; Gemini 3 series), applied when the writing or executing model is known. Vendors that publish no such guidance are recorded as consulted, not guessed.

Professional prose fails differently. The studies digested in [`research/`](research/) point at filler that carries no information, hedging where a judgment was needed, chatbot leftovers, register that ignores the venue, and formatting that looks stamped out. Each document type gets a thin rule file on top of one shared checklist:

| Domain | The gist |
|---|---|
| Release notes / announcements | user impact first, artifacts per claim, no marketing inflation |
| PR / issue replies | answer first, cite `file:line`, no reflex praise, length ∝ stakes |
| Postmortems | blameless toward people, merciless toward mechanisms; timestamps, dead ends, owned action items |
| Tickets / work orders | title = outcome, testable acceptance criteria, link don't repeat |
| Technical articles | open at the problem, one real dead end, one committed opinion, numbers with conditions |

The governing principle throughout: **calibrate to the human distribution, don't invert the AI one.** Humans sit at moderate values; a story with every rule applied is a new fingerprint. The skill selects 3–5 moves per story and leaves slack.

## Operation entries

The complete plugin package gives Claude Code, Codex, Grok Build, and Antigravity a general router plus five direct entries:

| Operation | Claude Code | Codex | Grok Build | Antigravity | Meaning |
|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | Create new prose |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | Diagnose without editing |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | Make minimal in-place edits |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | Rewrite from the source facts and intent |
| hemingway | `/sepia-hemingway` | `$sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | Write or refactor fiction with the built-in Hemingway voice applied |

The general `/sepia` (Claude Code, Grok Build, and Antigravity) or `$sepia` (Codex) router remains available. The operation wrappers depend on their sibling canonical skill, so standalone wrapper installation is unsupported; install the complete plugin package. What was verified on each platform is stated under Install.

## Experimental: composing with voice skills

Since v0.4.0, sepia defines an interface for stacking a voice or style skill on top of it — a minimalism method, a brand voice, a persona guide. It is opt-in: tell sepia the voice skill is in play, and it loads `references/voice-skills.md` over the normal route. No external voice is loaded unless you say so.

The contract in short: sepia's architecture decisions come first. The voice's moves are applied selectively (3–5 signature moves per piece, formula endings deliberately broken sometimes). Review reports the voice's known costs instead of fixing them away, while uniformity findings keep full strength: a voice does not excuse a metronome. On professional routes the venue still sets the register. Direct conflicts come back to you. The interface is grounded in one blind review experiment on a strict-minimalism specimen — a worked example, not measured evidence. One built-in profile ships under `references/voices/` (Hemingway: iceberg omission for fiction, the Kansas City Star rules for professional prose, each move traced to its source). The built-in profile is the one exception to "only when you say so": on fiction, a review reports when your text's recorded findings fit the Hemingway profile, and asking for strong de-AI on a story counts as opting in. sepia then says which profile it is applying and how to decline. `/sepia-hemingway` is the direct entry.

## Sentence rhythm and Chinese calibration

The style pass checks the *spread* of sentence lengths, the one syntactic measure on which every study that measured it agrees (human text varies more within a passage, in English and in Chinese); mean sentence length, punctuation counts, and paragraph length are not treated as signals because the measured directions contradict each other. Chinese text loads `references/languages/zh.md`, a calibration built on the one measured Chinese corpus (HC3, 2023) with its limits stated in the file; evidence and numbers are in `research/rhythm-syntax.md`.

## Install

Every command below is written for **user scope** — install once, use it in every project.

### Any agent (Skills CLI, 77+ agents)

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update sepia -g             # update
npx skills remove sepia -g             # uninstall
```

Installs on every agent the [Skills CLI](https://skills.sh) supports — Cursor, Cline, Windsurf, Copilot, OpenCode, goose, and more. Pick your agents when prompted. Runtime behavior outside the four platforms below has not been exercised by us; the skill is plain markdown under the Agent Skills standard, so file an issue if your agent trips on it.

The four platforms below have native plugin installers, each exercised with a live install. Verified means the install completes and the sepia entries appear. Whether the entries then behave as documented has not been checked platform by platform.

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

The in-session `/plugin install` dialog asks you to pick a scope — choose **User** there.

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

## Sources

Full digests with links in [`research/`](research/). Primary: StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## Support

You can use sepia for free without an account. The research behind every rule is open. Ongoing costs are just maintainer time and two kinds of model quota: delegating literature surveys to research agents that read primary papers, and running live models to test rule changes on A/B stories and cross-platform end-to-end reviews before shipping. You can support the project on Patreon.

[![Support sepia on Patreon](https://img.shields.io/badge/Support_on_Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/Nanako0129/membership)

## License

MIT
