# sepia

[English](README.md) | [繁體中文](README.zh-TW.md) | **简体中文**

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 从真正让 AI 露馅的那一层下手去 AI 味。小说在调整措辞之前先修复叙事架构。专业文档（发布说明、PR 回复、复盘报告、工单、技术文章）各自匹配符合场景的规则。

这是一套 [Agent Skill](https://agentskills.io/specification)。只要支持这个标准的 agent 都能直接加载，[Skills CLI](https://skills.sh) 支持 77+ 款 agent 且单条命令即可安装。Claude Code、Codex、Grok Build 和 Antigravity 额外提供了原生插件包。全平台共用一份标准 `SKILL.md`，不对各个平台建立独立分支。四种操作分别为 **write**、**review**（仅诊断）、**refactor**（最小改动）与 **recreate**（整篇重写）。

## 为什么还需要另一个 humanizer

常规去 AI 工具大多只在字词和句法上打转。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026: 61,608 篇故事，包含人类创作与 5 款前沿 LLM）表明，分类器**仅凭叙事结构特征**检测 AI 小说的 macro-F1 就达到 93.2%。同一项研究的 LAMP 编辑条件下（人类编辑改写了表层风格），检测率也只从 95.5% 降到 93.9%。留存的特征都位于架构层：叙述者直接阐释主题、因果关系过于工整的单线情节、情绪只靠身体感受呈现、没有现实世界的参照、读者缺席、时间全程线性，以及靠主角成长与接纳收束的结局。

sepia 将这些实测差距，连同 [`research/`](research/) 里梳理的相关研究，转化为针对小说写作与修订的三 pass 流程。

| Pass | 层次 | 例子 |
|---|---|---|
| 1 | 叙事架构（小说） | 避免直接解释主题、松开因果链、把揭露往后放、混用情绪呈现模式、稀疏的角色网络、点名真实事物 |
| 2 | 篇章推进 | 去除段落—问题序列模板、改善故事中段节奏松散的问题、变换节奏与位置 |
| 3 | 措辞风格 | 多数 humanizer 处理的层面：陈词滥调、句法模板、用词、语域 |

另附一套 30 项特征的诊断标准，以及分成两层的各模型指纹：叙事层特征由 StoryScope 测得（Claude、GPT、Gemini、DeepSeek、Kimi），句子层特征提取自厂商自家的 prompting 指南（Claude Fable 5.1 与 Mythos 5.1、Fable 5 与 Mythos 5、Opus 5、Opus 4.8；GPT-5.6；Gemini 3 系列），在已知起草或执行模型时套用。未公开此类指南的厂商记录为已查阅，不猜测。

专业文档暴露破绽的方式不同。[`research/`](research/) 里梳理的研究指出的问题是：没有信息量的填充文字、需要判断时闪烁其词、聊天机器人的残留语气、无视具体场合的语域、像一个模子印出来的排版。每类文档都在一份共用检查清单之上，各配一份精简的规则文件。

| 领域 | 要点 |
|---|---|
| 发版说明／公告 | 用户影响放在前面、每项宣称附佐证、避免营销化表达 |
| PR／issue 回复 | 先给答案、引用 `file:line`、避免条件反射式称赞、篇幅与事情的重要程度相称 |
| 事故复盘 | 不追究个人责任，深入分析机制；附时间戳、记录经历过的无效路径、每个行动项都有负责人 |
| 工单 | 标题写结果、验收条件可测试、可通过链接引用，避免重复 |
| 技术文章 | 从问题切入、记录一条真实经历过的无效路径、提出一个明确判断、数字附上适用条件 |

核心原则是**以人类分布为校准基准，不要直接反转 AI 分布。**人类写作的各项指标大多落在中段区间，把每条规则都用上的故事反而会形成一套新的特征指纹。这个 skill 针对每篇故事只挑选 3–5 种手法套用，给文本留出余地。

## 操作入口

完整的插件包为 Claude Code、Codex、Grok Build 和 Antigravity 带来了一个通用路由以及五个直达入口。

| 操作 | Claude Code | Codex | Grok Build | Antigravity | 用途 |
|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | 撰写新内容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | 只诊断，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 根据原始事实与意图重新撰写 |
| hemingway | `/sepia-hemingway` | `$sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | 应用内置海明威语气写作或改写小说 |

通用的 `/sepia`（Claude Code、Grok Build 与 Antigravity）或 `$sepia`（Codex）路由依旧可用。各操作 wrapper 都依赖同级的规范 skill，不支持单独安装，请直接安装完整的插件包。各平台验证了什么，写在「安装」一节。

## 实验性功能：叠加语气／风格 skill

从 v0.4.0 开始，sepia 定义了一套接口，允许在上层叠加声音或风格类 skill（极简主义方法、品牌语调、persona 指南）。采用 opt-in 机制：明确告知 sepia 启用了声音 skill 后，它才会在常规路由之上加载 `references/voice-skills.md`；不说就不加载外部声音。

简单说，sepia 的架构决策先行，声音手法的套用必须节制（每篇选取 3–5 种代表手法，偶尔有意打破公式化的收尾）。review 会报告这个声音已知的代价，不代改，但均匀性 finding 不打折：有了声音也不能写成节拍器。在专业写作路径上，语域仍由发布场合决定，一旦发生直接冲突就交由你定夺。这套接口源自针对一份极简主义样本的盲审实验，属单一案例，并非量测证据。`references/voices/` 内置了一套 profile（海明威：小说用冰山式省略，专业文体遵循堪萨斯城星报规则，每项手法都标明出处）。内置 profile 是「不说就不加载」的唯一例外：小说路线上，review 发现你的文本记录到的 findings 符合海明威 profile 时会提示，要求强力去除故事里的 AI 味也算 opt-in。sepia 会说明正在套用哪个 profile、怎么关闭。`/sepia-hemingway` 为直达入口。

## 句长节奏与中文校准

style pass 重点检查句长的*变化幅度*。这是量测过它的研究里唯一方向一致的句法指标（人类文本在同一段内变化更大，英文与中文皆然）；平均句长、标点数量、段落长度不当信号，因为各项量测的方向相互矛盾。中文文本会加载 `references/languages/zh.md`，这份校准基于目前唯一经过测量的中文语料库（HC3, 2023），相应局限已在文件内说明。具体证据与数据见 `research/rhythm-syntax.md`。

## 安装

下列命令都按 **user scope** 编写（一次安装，每个项目都能直接使用）。

### 任何 agent（Skills CLI，支持 77+ 个 agent）

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update sepia -g             # update
npx skills remove sepia -g             # uninstall
```

只要是 [Skills CLI](https://skills.sh) 支持的 agent 都可以安装（Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等）。安装过程中按提示选择你使用的 agent 即可。对于下方四款平台以外的运行时表现，我们尚未做过实机测试。本 skill 基于 Agent Skills 标准，属于纯 markdown 文件，如果你的 agent 跑起来遇到问题，欢迎提交 issue。

下方四款平台都提供原生插件安装方式，每款都跑过实机安装。所谓验证，指安装流程能够顺利走完并出现 sepia 相关的入口命令。装好之后入口的行为没有逐平台实测。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

在会话中唤出 `/plugin install` 弹窗时，系统会要求选择 scope，此时勾选 **User**。

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

如果你本地已经通过 Claude Code 安装过 sepia，Grok 也能自动检测到。两种安装途径都可以正常使用。

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### Project scope（替代方案）

如果某个仓库需要锁定自己的独立副本，可将 `skills/sepia/` 提交到该仓库，路径设为 `.agents/skills/sepia`（Codex + Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 卸载

各个工具都使用各自的原生命令。

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

## 目录结构

```text
sepia/
├── plugin.json              # Antigravity packaging
├── skills/
│   ├── sepia/                # 标准 skill（Agent Skills standard）
│   │   ├── SKILL.md          # routing、operations、calibration rules、guardrails
│   │   └── references/       # passes、rubric、fingerprints、domain rules、languages/zh.md、voice-skills（实验性）
│   ├── sepia-write/SKILL.md  # 固定单一操作的薄 wrapper
│   ├── sepia-review/SKILL.md
│   ├── sepia-refactor/SKILL.md
│   ├── sepia-recreate/SKILL.md
│   └── sepia-hemingway/SKILL.md  # fiction write/refactor with the built-in voice
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
└── research/                # digested evidence base with sources
```

## Star 趋势

<a href="https://www.star-history.com/?repos=nanako0129%2Fsepia&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&theme=dark&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
  </picture>
</a>

## 参考资料

完整摘要与链接见 [`research/`](research/)。主要来源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 赞助

sepia 任何人都能免费用，也不需要注册账号。每条规则背后的研究全部公开。项目的实际开销只有维护时间和模型额度。额度花在两处：委派研究 agent 读论文原文做文献调查；规则改动上线前用真实模型跑 A/B 对照小说，也跑跨平台的端到端审查。欢迎在 Patreon 上支持这个项目。

[![Support sepia on Patreon](https://img.shields.io/badge/Support_on_Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/Nanako0129/membership)

## 许可证

MIT
