# sepia

**English** | [繁體中文](README.zh-TW.md)

> De-AI writing at the layer that actually gives AI away. Fiction gets its narrative architecture repaired before anyone touches word choice; professional documents (release notes, PR replies, postmortems, tickets, technical articles) each get rules matched to their venue.

A portable [Agent Skill](https://agentskills.io/specification) for Claude Code, Codex, Grok Build, and Antigravity. One canonical `SKILL.md`, no per-platform forks. Four operations: **write**, **review** (diagnose only), **refactor** (minimal edits), **recreate** (full rewrite).

## Why another humanizer

Every popular humanizer edits word choice and syntax. [StoryScope](https://arxiv.org/abs/2604.03136) (Russell et al., 2026: 61,608 stories, human + 5 frontier LLMs) showed that a classifier using **narrative-structure features alone** detects AI fiction at 93.2% macro-F1, and that editing the surface style away barely moves it (95.5% → 93.9%). The tells that survive are architectural: themes explained by the narrator, single-track causally-tidy plots, emotions rendered only as bodily sensation, no real-world references, no reader, linear time, endings resolved by protagonist growth and acceptance.

sepia turns those measured gaps, together with the eleven related studies digested in [`research/`](research/), into a three-pass writing and revision protocol for fiction:

| Pass | Layer | Examples |
|---|---|---|
| 1 | Narrative architecture (fiction) | stop explaining the theme, loosen the causal chain, back-load revelations, mix emotion modes, sparse character networks, name real things |
| 2 | Discourse flow | de-template the paragraph-question sequence, fix the mid-story sag, vary rhythm and positions |
| 3 | Surface style | the classic layer: clichés, syntax templates, vocabulary, register |

Plus a 30-feature diagnosis rubric and per-model fingerprint corrections (Claude, GPT, Gemini, DeepSeek, Kimi).

Professional prose fails differently. The studies point at filler that carries no information, hedging where a judgment was needed, chatbot leftovers, register that ignores the venue, and formatting that looks stamped out. Each document type gets a thin rule file on top of one shared checklist:

| Domain | The gist |
|---|---|
| Release notes / announcements | user impact first, artifacts per claim, no marketing inflation |
| PR / issue replies | answer first, cite `file:line`, no reflex praise, length ∝ stakes |
| Postmortems | blameless toward people, merciless toward mechanisms; timestamps, dead ends, owned action items |
| Tickets / work orders | title = outcome, testable acceptance criteria, link don't repeat |
| Technical articles | open at the problem, one real dead end, one committed opinion, numbers with conditions |

The governing principle throughout: **calibrate to the human distribution, don't invert the AI one.** Humans sit at moderate values; a story with every rule applied is a new fingerprint. The skill selects 3–5 moves per story and leaves slack.

## Install

Every platform has its own native install, each paired with its update commands. Default everywhere is **user scope** — install once, use it in every project.

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

Antigravity has no marketplace. Use the verified installer below; it creates an ownership-marked skill copy and `/sepia` workflow so later updates can detect local modifications instead of overwriting them.

### All four at once (alternative)

Get the published commit SHA and `install.sh` SHA-256 as a pair from the release notes, replace the two placeholders, then run:

```bash
(
  set -e
  SEPIA_REF='PASTE_PUBLISHED_40_HEX_COMMIT_SHA'
  SEPIA_INSTALL_SHA256='PASTE_PUBLISHED_INSTALL_SH_SHA256'
  installer="$(mktemp)"
  trap 'rm -f "$installer"' EXIT

  curl -fsSL "https://raw.githubusercontent.com/Nanako0129/sepia/$SEPIA_REF/install.sh" -o "$installer"
  if command -v shasum >/dev/null 2>&1; then
    printf '%s  %s\n' "$SEPIA_INSTALL_SHA256" "$installer" | shasum -a 256 -c -
  else
    printf '%s  %s\n' "$SEPIA_INSTALL_SHA256" "$installer" | sha256sum -c -
  fi
  SEPIA_REF="$SEPIA_REF" bash "$installer"
)
```

The checksum command is the pre-execution trust boundary. The installer cannot retroactively prove which bytes the shell already began executing; after that external check, it also requires the downloaded bytes, fetched commit, checkout `HEAD`, and tracked executable `install.sh` object to agree on the same full SHA. Branch names and tags are not accepted as the machine contract.

The command clones to `~/.sepia` (override with an absolute `SEPIA_HOME`) and installs at user scope for all four platforms. To update or roll back, rerun the block with the new or previous published SHA/digest pair. Existing checkouts must have exactly the selected `SEPIA_REPO` origin and be clean; the installer aborts on foreign origins, untracked files, modified files, or an unexpected installer type.

Every destination is checked before any destination changes. Existing paths are accepted only when positively identified as the Sepia symlink or an unmodified, ownership-marked Antigravity copy. Legacy copies and every other collision abort without a force option; move the path aside after reviewing it, then rerun. The managed layout is:

| Platform | Where | Mechanism |
|---|---|---|
| Claude Code | `~/.claude/skills/sepia` | symlink |
| Codex | `~/.agents/skills/sepia` | symlink |
| Grok Build | `~/.grok/skills/sepia` | symlink |
| Antigravity | `~/.gemini/config/skills/sepia` + `/sepia` global workflow | copy |

Safe uninstall keeps the checkout and removes only currently unmodified, positively identified managed artifacts. Rerun the same download-and-checksum block with the installed revision's published SHA/digest pair, replacing only its final line with:

```bash
SEPIA_ACTION=uninstall SEPIA_REF="$SEPIA_REF" \
  SEPIA_HOME="${SEPIA_HOME:-$HOME/.sepia}" \
  SEPIA_REPO="${SEPIA_REPO:-https://github.com/Nanako0129/sepia.git}" \
  bash "$installer"
```

Keep that line inside the checksum-guarded subshell so the verified downloaded installer validates the checkout before executing its installer. If the install used `SEPIA_HOME` or `SEPIA_REPO`, pass the same values to uninstall. Uninstall preflights every artifact before removing any of them; a modified copy, unmanaged replacement, legacy unmarked path, or wrong symlink aborts and leaves all destinations and symlink targets unchanged.

Maintainers publish immutable installer coordinates in two steps: resolve the release tag to its full commit with `git rev-parse '<tag>^{}'`, then compute `git show '<commit>:install.sh' | shasum -a 256`. Publish that exact SHA/digest pair in the release notes and replace the placeholders in both READMEs in a follow-up documentation commit; the tag remains a human alias, not installer input.

### Skills CLI (alternative, 77+ agents)

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update -g                   # update
```

### Project scope (alternative)

When one repo should pin its own copy, commit `skills/sepia/` into that repo as `.agents/skills/sepia` (Codex + Antigravity) or `.claude/skills/sepia` (Claude Code).

## Layout

```text
sepia/
├── skills/sepia/            # canonical skill (Agent Skills standard)
│   ├── SKILL.md             # routing, operations, calibration rules, guardrails
│   └── references/
│       ├── narrative-pass.md      # fiction pass 1: architecture (the differentiator)
│       ├── discourse-pass.md      # pass 2: paragraph-level flow
│       ├── style-pass.md          # pass 3: surface style
│       ├── rubric.md              # fiction 30-feature diagnosis
│       ├── model-fingerprints.md  # per-model corrections
│       ├── professional-pass.md   # shared non-fiction layer (slop checklist, venue matching)
│       └── domains/               # release-notes, dev-replies, postmortems, tickets, tech-articles
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
├── install.sh
└── research/                # digested evidence base with sources
```

## Sources

Full digests with links in [`research/`](research/). Primary: StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## License

MIT
