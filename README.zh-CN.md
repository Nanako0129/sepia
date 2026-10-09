# sepia

[English](README.md) | [繁體中文](README.zh-TW.md) | **简体中文**

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 从真正让 AI 露馅的那一层下手去 AI 味。小说在调整措辞之前先修复叙事架构；专业文档（发布说明、PR 回复、复盘报告、工单、技术文章）各自匹配符合场景的规则。

这是一套 [Agent Skill](https://agentskills.io/specification)。只要支持该标准的 agent 均可直接加载，支持 77+ 款 agent 的 [Skills CLI](https://skills.sh) 仅需单条命令即可完成安装。Claude Code、Codex、Grok Build、Antigravity 和 QwenPaw 额外提供了原生插件包。全平台共用一份标准 `SKILL.md`，不对各个平台建立独立分支。提供四种操作：**write**、**review**（仅诊断）、**refactor**（最小改动）与 **recreate**（整篇重写）。

## 目录

- [为什么还需要另一个 humanizer](#为什么还需要另一个-humanizer)
- [操作入口](#操作入口)
- [实验性功能：叠加语气／风格 skill](#实验性功能叠加语气风格-skill)
- [句长节奏与中文校准](#句长节奏与中文校准)
- [安装](#安装)
- [卸载](#卸载)
- [目录结构](#目录结构)
- [Star 趋势](#star-趋势)
- [参考资料](#参考资料)
- [赞助](#赞助)
- [许可证](#许可证)

---

## 为什么还需要另一个 humanizer

常规去 AI 工具大多只在字词和句法上打转。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026: 61,608 篇故事，包含人类创作与 5 款前沿 LLM）表明，分类器**仅凭叙事结构特征**检测 AI 小说的 macro-F1 就达到 93.2%。同一项研究的 LAMP 编辑条件下（人类编辑改写了表层风格），检测率也只从 95.5% 降到 93.9%。留存的特征都位于架构层：叙述者直接阐释主题、因果关系过于工整的单线情节、情绪只靠身体感受呈现、没有现实世界的参照、读者缺席、时间全程线性，以及靠主角成长与接纳收束的结局。

sepia 将这些实测差距，连同 [`research/`](research/) 里梳理的相关研究，转化为针对小说写作与修订的三 pass 流程：

| Pass | 层次 | 例子 |
|---|---|---|
| 1 | 叙事架构（小说） | 避免直接解释主题、松开因果链、把揭露往后放、混用情绪呈现模式、稀疏的角色网络、点名真实事物 |
| 2 | 篇章推进 | 去除段落—问题序列模板、改善故事中段节奏松散的问题、变换节奏与位置 |
| 3 | 措辞风格 | 多数 humanizer 处理的层面：陈词滥调、句法模板、用词、语域 |

另附一套 30 项特征的诊断标准；当已知起草或执行模型时，会在两个层次套用各模型专属的指纹：

| 模型家族 | 叙事层（StoryScope） | 句子级散文层（厂商提示词指南） |
|---|---|---|
| Claude | 实测 | Claude Fable 5.1 与 Mythos 5.1、Fable 5 与 Mythos 5、Opus 5、Opus 4.8 |
| GPT | 实测 | GPT-5.6、GPT-6 Astra |
| Gemini | 实测 | Gemini 3 与 3.1 |
| DeepSeek | 实测 | 已查阅（未公开发布指南） |
| Kimi | 实测 | 已查阅（未公开发布指南） |

> **注意：** 未公开提示词指南的厂商记录为已查阅，不予猜测。

专业文档暴露破绽的方式不同，而结构层的结论在这里同样成立：2026 年的一项研究把 StoryScope 复制到商业博客文章上，2,250 篇真人文对上 11,250 篇 AI 镜像，仅用结构特征就以 98.0 macro-F1 区分两者，AI 那一侧被描述为「整齐、自我预告」（ledger 代号 `SLOPSHAPE-2026`，arXiv:2609.15369；预印本，特征由 LLM 评分；测的是对原文与模型自我改写稿的检测，没有测过人工编辑）。[`research/`](research/) 里梳理的研究指出的问题是：没有信息量的填充文字、需要判断时闪烁其词、聊天机器人的残留语气、无视具体场合的语域、像一个模子印出来的排版。每类文档都在一份共用检查清单之上，各配一份精简的规则文件：

| 领域 | 要点 |
|---|---|
| 发版说明／公告 | 用户影响放在前面、每项宣称附佐证、避免营销化表达 |
| PR／issue 回复 | 先给答案、引用 `file:line`、避免条件反射式称赞、篇幅与事情的重要程度相称 |
| 事故复盘 | 不追究个人责任，深入分析机制；附时间戳、记录经历过的无效路径、每个行动项都有负责人 |
| 工单 | 标题写结果、验收条件可测试、可通过链接引用，避免重复 |
| 技术文章 | 从问题切入、记录一条真实经历过的无效路径、提出一个明确判断、数字附上适用条件 |
| 长篇新闻（特稿、调查、数据报道） | 导语与正文采用两种语体、引语保留口语质感、每个数字都带比较基准、不写总结式结尾 |

> **核心原则：** 以人类分布为校准基准，不要直接反转 AI 分布。人类写作的各项指标大多落在中段区间，把每条规则都用上的故事反而会形成一套新的特征指纹。本 skill 针对每篇故事只挑选 3–5 种手法套用，给文本留出余地。

## 操作入口

完整的插件包为 Claude Code、Codex、Grok Build、Antigravity 和 QwenPaw 带来了一个通用路由以及五个直达入口。QwenPaw 的插件包不自行注册命令，由 QwenPaw 原生的 `/<skill 名称>` 分派调用已安装的 skill：

| 操作 | Claude Code | Codex | Grok Build | Antigravity | QwenPaw | 用途 |
|---|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | `/sepia-write` | 撰写新内容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | `/sepia-review` | 只诊断，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 根据原始事实与意图重新撰写 |
| hemingway | `/sepia-hemingway` | `$sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | 应用内置海明威语气写作或改写小说 |

通用的 `/sepia`（Claude Code、Grok Build、Antigravity 与 QwenPaw）或 `$sepia`（Codex）路由依旧可用。各平台具体验证了哪些内容，参见[安装](#安装)一节。

> **注意：** 各操作 wrapper 均依赖同级的规范 skill，不支持单独安装，请直接安装完整的插件包。

## 实验性功能：叠加语气／风格 skill

从 v0.4.0 开始，sepia 定义了一套接口，允许在上层叠加声音或风格类 skill（极简主义方法、品牌语调、persona 指南）。采用 opt-in 机制：明确告知 sepia 启用了声音 skill 后，它才会在常规路由之上加载 `references/voice-skills.md`；不说就不加载外部声音。

接口契约在各操作与路径间遵循固定的优先级规则：

| 规则维度 | 接口规范 |
|---|---|
| 架构 | sepia 的架构决策先行。 |
| 手法选择 | 声音手法的套用必须节制（每篇选取 3–5 种代表手法，叙事形态稀疏或事实不足时更少；偶尔有意打破公式化的收尾）。 |
| 诊断审查 | review 会报告该声音已知的代价，不代改。 |
| 均匀性检查 | 均匀性 finding 维持原样：有了声音也不能写成节拍器。 |
| 专业语域 | 在专业写作路径上，语域仍由发布场合决定。 |
| 冲突解决 | 一旦发生直接冲突，交由你定夺。 |

> **注意：** 这套声音 skill 接口源自针对一份极简主义样本的盲审实验，属单一案例，并非量测证据。

`references/voices/` 下内置了两套 profile，并附带一种拥有声明式覆盖权的 persona profile：

| Profile | 适用路径 | 来源与特征 | Opt-in 与调用方式 |
|---|---|---|---|
| 海明威（`references/voices/hemingway.md`） | 小说与专业散文 | 小说采用冰山式省略，专业文体遵循堪萨斯城星报规则；每项手法均标明出处 | 直达入口 `/sepia-hemingway`（或 `$sepia-hemingway`）。在小说路径上，要求强力去除故事里的 AI 味才算 opt-in（sepia 会说明正在套用哪个 profile 以及如何关闭）。未 opt-in 时，小说 review 发现文本符合该 profile 时仅做提示，不加载任何内容。 |
| 台湾深度报道（`references/voices/tw-journalism.md`） | 仅限专业路径 | 九种叙事形态各自的手法，来自私下测量的繁体中文新闻语料及其细读 | opt-in 短语：「套用台灣深度報導 voice」或 `"apply the Taiwan journalism voice"`。遵守与海明威相同的规则。 |
| Persona 模板（`references/voices/PERSONA-TEMPLATE.md`） | 作者自定义 | 单一写作者的风格，带声明式覆盖权；由 `scripts/check_persona.py` 校验 | 由作者创建 profile。模板位于 `references/voices/PERSONA-TEMPLATE.md`。 |
| Nyaneko（`references/voices/personas/nyaneko.md`） | 仅限专业路径 | 内置的伙伴声线，依维护者撰写的语音规格与示范句编写 | opt-in 短语：`"apply persona Nyaneko"` 或 `「套用 persona Nyaneko」`。 |

### 用 persona 写东西：一段简短教程

sepia 的规则负责去掉 AI 味。温度另有来源：写的人知道自己是谁在对谁说话。这个项目自己的一个案例，只是观察、没有测量：v0.12.0 的 Threads 帖子用同一个模型、同一份 release notes 写了两次。第一次的提示给了骨架（版本行、条列、修正、工程备注、更新方式），出来是照表填格。第二次的提示给的是身份，「我是这个项目的维护者，刚发了 v0.12.0，用我自己的口吻讲给关注者听，怎么组织由你决定」，加上 notes 当唯一事实来源和平台限制，出来的是维护者留下来用的那篇。之后用 sepia review 扫那篇，tell 集中在开头与收尾（历程铺陈、格言式结尾、几个绝对化的词），refactor 去掉它们，中间没动。

验证有效的顺序是：

1. 先给身份。
2. 事实另附，作为唯一来源。
3. 限制只写平台限制，结构留给模型。
4. 最后以 sepia 作为检查。

```text
不要使用工具，需要的东西都在下面。
我是〈谁〉，写给〈谁〉看，讲的是〈刚发生的什么事〉。用我自己的口吻；怎么组织由你决定。
平台限制：〈长度、标记、提及〉。
事实只能来自下面的 notes，数字与编号要对得上。
===== notes =====
〈来源文件〉
```

persona profile 就是把这个身份写下来一次，之后每篇都从它出发：他和读者是什么关系、第一句做什么、温度挂在什么事实上、绝不做什么，以及几篇他自己声音的范文。模板位于 `references/voices/PERSONA-TEMPLATE.md`，内置的 `references/voices/personas/nyaneko.md` 是一份完整示例，接口校验脚本负责检查 profile 结构：

```bash
python3 scripts/check_persona.py <file>
```

鼓励你写自己的一套；范文承载的内容比描述更多。

## 句长节奏与中文校准

style pass 重点检查句长的*变化幅度*。这是量测过它的研究里唯一方向一致的句法指标：无论英文还是中文，人类文本在同一段落内的方差均表现得更大。

| 句法指标 | 状态 | 实证依据 |
|---|---|---|
| 句长变化幅度 | 纳入检查的信号 | 无论是英文还是中文研究，人类文本在同一段落内的方差均表现得更高。具体证据与数据见 [`research/rhythm-syntax.md`](research/rhythm-syntax.md)。 |
| 平均句长 | 舍弃 | 各语料库的测量方向相互矛盾。 |
| 标点数量 | 舍弃 | 各语料库的测量方向相互矛盾。 |
| 段落长度 | 舍弃 | 各语料库的测量方向相互矛盾。 |

中文文本会加载 `references/languages/zh.md`，跨越四个不同的证据层次对 style pass 进行校准：

| 层次／来源 | 证据性质 | 语料与校准详情 |
|---|---|---|
| HC3（2023） | 实测语料库 | 人机对照中文语料库基准。 |
| 繁体中文新闻 | 人类侧实证测量 | 来自一家未具名台湾出版方的约两千篇文章，跨度约十年（语料未公开；摘要见 [`research/zh-news-corpus.md`](research/zh-news-corpus.md)）。 |
| 对照组 | 机器侧实证对照 | 涵盖三个模型的 119 篇合成文，采用同一份基础提示词（其中一个模型包含一行变体）。 |
| 台湾惯例 | 规范标准 | 取自公开规范与一级共识的简短台湾写作惯例规范章节。 |

> **注意：** 上述三种实证中文来源的局限性均已在 `references/languages/zh.md` 中说明。

## 安装

> **注意：** 下列所有命令均按 **user scope** 编写——一次安装，即可在所有项目中直接使用。

### 任何 agent（Skills CLI，支持 77+ 个 agent）

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update sepia -g             # update
npx skills remove sepia -g             # uninstall
```

只要是 [Skills CLI](https://skills.sh) 支持的 agent 均可安装（Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等）。安装过程中按提示选择你使用的 agent 即可。对于下方五款平台以外的运行时表现，我们尚未进行过实机测试；本 skill 基于 Agent Skills 标准编写，属于纯 Markdown 文件，如果你的 agent 运行遇到问题，欢迎提交 issue。

> **注意：** 所谓「验证」，是指安装流程能够顺利走完并出现 sepia 相关的入口。五款原生插件安装程序均进行过实机安装测试（QwenPaw 由贡献者完成）。安装后各入口的具体行为尚未逐个平台进行实测。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

> **提示：** 会话中的 `/plugin install` 弹窗会要求选择 scope——请在此处勾选 **User**。

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

如果你本地已经通过 Claude Code 安装过 sepia，Grok 也能自动检测到；两种安装途径均可正常使用。

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

> **注意：** 由贡献者在 QwenPaw 2.2.1 上实机验证（#250、#289，维护者未自行复现）：安装流程能顺利走完，插件包中打包的 `skills` 符号链接会被 `shutil.copytree` 展开为真实目录，`/sepia <文本>` 与 `/sepia-write <文本>` 都会通过 QwenPaw 的 skill 分派启动 agent。另外四个入口走同一分派，没有逐个实测。若插件包读不到 skill（zip 安装，或不支持符号链接的 checkout），会记录一条错误并且不注册任何内容，请改用 git clone 安装。

### Project scope（替代方案）

当某个仓库需要锁定独立副本时，可将 `skills/sepia/` 作为 `.agents/skills/sepia`（Codex + Antigravity）或 `.claude/skills/sepia`（Claude Code）提交至该仓库。

## 卸载

各个工具均使用各自的原生命令：

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
├── .qwenpaw-plugin/         # QwenPaw packaging (plugin.json, plugin.py, skills symlink)
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

Nanako0129/sepia 随时间变化的 Star 增长历史趋势。

## 参考资料

完整摘要与链接见 [`research/`](research/)。主要研究包括：

| 来源 | 发表场合／标识符 |
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

## 赞助

sepia 任何人都能免费使用，不需要注册账号。每条规则背后的研究全部公开。项目的实际开销只有维护者的时间与两种模型额度：委派研究 agent 阅读论文原文进行文献调查，以及在规则变更上线前使用真实模型跑 A/B 对照小说与跨平台的端到端审查。欢迎在 Patreon 上支持本项目。

[![Support sepia on Patreon](https://img.shields.io/badge/Support_on_Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/Nanako0129/membership)

## 许可证

MIT
