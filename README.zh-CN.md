# sepia

[English](README.md) | **简体中文**

> 从真正会让 AI 泄底的层次下手。小说先修叙事架构，再碰字句；专业文件（发版说明、PR 回复、事故检讨、工单、技术文章）则按 venue 各用一套规则。

这是一套可携的 [Agent Skill](https://agentskills.io/specification)：任何支援这个标准的 agent 都能载入；[Skills CLI](https://skills.sh)（支援 77+ 家 agent）一行指令就能装。Claude Code、Codex、Grok Build 与 Antigravity 另有原生 plugin 打包，四家都实机装过。全平台共用唯一一份正典 `SKILL.md`，不另开平台分支。四种操作：**write**、**review**（只诊断）、**refactor**（最小修改）、**recreate**（整篇重写）。

## 为什么还需要另一个 humanizer

常见的 humanizer 都在改用词与句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026：61,608 篇故事，涵盖人类与 5 个顶尖 LLM）显示，只靠**叙事结构特征**的分类器就能以 93.2% macro-F1 侦测 AI 小说；把字句风格修掉，分类表现也只从 95.5% 降到 93.9%。留下的破绽都在架构层：叙事者直接讲明主题、单线且因果收得过于工整的情节、情绪只靠身体感受呈现、没有真实世界的参照、读者缺席、时间全程线性，以及靠主角成长与接纳收束的结局。

sepia 把这些实测差距，连同 [`research/`](research/) 里整理过的十一篇相关研究，转成小说写作与修订的三个 pass 流程：

| Pass | 层次 | 例子 |
|---|---|---|
| 1 | 叙事架构（小说） | 别再解释主题、松开因果链、把揭露往后放、混用情绪呈现模式、稀疏的角色网络、点名真实事物 |
| 2 | 篇章推进 | 拆掉段落—问题序列的模板、修掉故事中段的松垮、变换节奏与位置 |
| 3 | 字句风格 | 所有 humanizer 都在修的那层：陈腔滥调、句法模板、用词、语域 |

另附 30 项特征的诊断 rubric，以及各模型的指纹修正（Claude、GPT、Gemini、DeepSeek、Kimi）。

专业文字露馅的方式不同。研究指出，常见问题包括没有资讯量的填充文字、该下判断时还在闪躲、chatbot 残留语气、无视 venue 的语域，以及像同一个模子印出的排版。每种文件都共用一份检查表，再各配一份精简规则档：

| 领域 | 要点 |
|---|---|
| 发版说明／公告 | 使用者影响摆前面、每项宣称附佐证、不灌行销词 |
| PR／issue 回复 | 先给答案、引用 `file:line`、不反射性称赞、篇幅与事情的重要程度相称 |
| 事故检讨 | 对人不究责，对机制追到底；附时间戳记、记录走过的死路、每个行动项目都有负责人 |
| 工单 | 标题写结果、验收条件能测、能连结就别重复 |
| 技术文章 | 从问题切入、保留一条真实走过的死路、提出一个明确判断、数字附上适用条件 |

贯穿全篇的原则：**以整个人类分布为校准目标，别把 AI 分布直接倒过来套**。人类的数值多落在中间。每条规则都用上的故事会形成另一种指纹；sepia 每篇只选 3–5 个手法，其余留白。

## 操作入口

完整 plugin package 会在 Claude Code、Codex、Grok Build 与 Antigravity 提供一个通用 router，以及四个可直接呼叫的操作入口：

| 操作 | Claude Code | Codex | Grok Build | Antigravity | 用途 |
|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | 撰写新内容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | 只诊断，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 依原始事实与意图重新撰写 |

通用 router 仍可透过 `/sepia`（Claude Code、Grok Build、Antigravity）或 `$sepia`（Codex）使用。操作 wrapper 依赖同一套 package 里的正典 skill，不支援单独安装；请安装完整 plugin package。这张表只记录 package 语法；本次变更尚未实测安装后的 UI 与 runtime 行为。

## 实验性功能：叠加声音 skill

v0.4.0 起，sepia 定义了跟声音／风格类 skill（极简主义方法、品牌语调、persona 指南）叠加使用的介面。采 opt-in：你明讲声音 skill 在场，sepia 才会在原路由之上载入 `references/voice-skills.md`；不讲就不载入，sepia 也永远不会自己注入美学。

条约摘要：sepia 的架构决策先行，声音技法选择性套用（每篇挑 3–5 招招牌技法，招牌结尾公式偶尔故意打破）。review 只回报声音的已知代价、不代修，但均匀性 finding 不打折：声音不能豁免节拍器。专业路由上 venue 仍定语域，直接冲突交回给你决定。这个介面的依据是一次极简规格样本的盲审实验，属单一案例，不是量测证据。

## 安装

下列指令一律写成 **user scope**：安装一次，每个专案都能用。

### 任何 agent（Skills CLI，77+ 家）

```bash
npx skills add Nanako0129/sepia -g     # -g 才是 user scope；预设是 project
npx skills update sepia -g             # 更新
npx skills remove sepia -g             # 解除安装
```

[Skills CLI](https://skills.sh) 支援的 agent 都能装：Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等；安装时会问你要装到哪几家。四大平台以外的执行行为我们没有实测过；skill 本体是 Agent Skills 标准下的纯 markdown，你的 agent 若吃不动欢迎开 issue。

下面四个平台另有原生 plugin installer，各自实机装过。验证范围是装得完、sepia 入口出现；runtime 行为如上所述未逐一实测。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

在 session 里开启 `/plugin install` 对话框时，系统会要求选 scope；请选 **User**。

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

Grok 也会自动找到既有的 Claude Code sepia 安装；两种方式都能用。

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### Project scope（替代方案）

某个 repo 要固定自己的版本时，把 `skills/sepia/` commit 到该 repo，放在 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 解除安装

各套工具都使用原生指令：

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
│   ├── sepia/                # 正典 skill（Agent Skills standard）
│   │   ├── SKILL.md          # routing、operations、calibration rules、guardrails
│   │   └── references/       # passes、rubric、fingerprints、domain rules、voice-skills（实验性）
│   ├── sepia-write/SKILL.md  # 固定单一操作的薄 wrapper
│   ├── sepia-review/SKILL.md
│   ├── sepia-refactor/SKILL.md
│   └── sepia-recreate/SKILL.md
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
└── research/                # digested evidence base with sources
```

## Star 趋势

<a href="https://www.star-history.com/?repos=Nanako0129%2Fsepia&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Nanako0129%2Fsepia&type=date&theme=dark&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
  </picture>
</a>

## 资料来源

完整摘要与连结见 [`research/`](research/)。主要来源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 授权

MIT
