# sepia

[English](README.md) | [繁體中文](README.zh-TW.md) | **简体中文**

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 从真正会暴露 AI 痕迹的层面入手。小说先修叙事架构，再处理措辞；专业文档（发版说明、PR 回复、事故复盘、工单、技术文章）则按 venue 各用一套规则。

这是一套可移植的 [Agent Skill](https://agentskills.io/specification)：任何支持这个标准的 agent 都能加载；[Skills CLI](https://skills.sh)（支持 77+ 个 agent）一条命令即可安装。Claude Code、Codex、Grok Build 与 Antigravity 另有原生 plugin 打包，四个平台均已完成安装验证。全平台共用唯一一份标准 `SKILL.md`，不为不同平台维护独立分支。四种操作：**write**、**review**（只诊断）、**refactor**（最小修改）、**recreate**（整篇重写）。

## 为什么还需要另一个 humanizer

常见的 humanizer 都在改用词与句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026：61,608 篇故事，涵盖人类与 5 个顶尖 LLM）显示，只靠**叙事结构特征**的分类器就能以 93.2% macro-F1 检测 AI 小说；把表层风格改掉，分类表现也只从 95.5% 降到 93.9%。剩余特征都位于架构层：叙事者直接讲明主题、单线且因果收得过于工整的情节、情绪只靠身体感受呈现、没有真实世界的参照、读者缺席、时间全程线性，以及靠主角成长与接纳收束的结局。

sepia 把这些研究测得的差距，连同 [`research/`](research/) 里整理过的十一篇相关研究，转化为小说写作与修订的三阶段流程：

| Pass | 层次 | 例子 |
|---|---|---|
| 1 | 叙事架构（小说） | 避免直接解释主题、松开因果链、把揭露往后放、混用情绪呈现模式、稀疏的角色网络、点名真实事物 |
| 2 | 篇章推进 | 去除段落—问题序列模板、改善故事中段节奏松散的问题、变换节奏与位置 |
| 3 | 措辞风格 | 多数 humanizer 处理的层面：陈词滥调、句法模板、用词、语域 |

另附 30 项特征的诊断 rubric，以及分成两层的各模型指纹：StoryScope 测得的叙事层特征（Claude、GPT、Gemini、DeepSeek、Kimi），加上取自各厂商官方 prompting 指南的措辞层特征（Claude Fable 5.1、Fable 5、Opus 5、Opus 4.8；GPT-5.6；Gemini 3 系列），在已知是哪个模型在写或在执行时应用。没有发布这类指南的厂商只记录「已查阅」，不猜测。

专业文档暴露 AI 痕迹的方式不同。研究指出，常见问题包括没有信息量的填充文字、需要作出判断时仍然回避、chatbot 残留语气、无视 venue 的语域，以及排版高度同质化。每种文档都共用一份检查表，再各配一份精简规则文件：

| 领域 | 要点 |
|---|---|
| 发版说明／公告 | 用户影响放在前面、每项宣称附佐证、避免营销化表达 |
| PR／issue 回复 | 先给答案、引用 `file:line`、避免条件反射式称赞、篇幅与事情的重要程度相称 |
| 事故复盘 | 不追究个人责任，深入分析机制；附时间戳、记录经历过的无效路径、每个行动项都有负责人 |
| 工单 | 标题写结果、验收条件可测试、可通过链接引用，避免重复 |
| 技术文章 | 从问题切入、记录一条真实经历过的无效路径、提出一个明确判断、数字附上适用条件 |

贯穿全篇的原则：**以整个人类分布为校准目标，不要简单反向应用 AI 分布**。人类的数值多落在中间。应用全部规则的故事会形成另一种指纹；sepia 每篇只选择 3–5 种手法，其余留白。

## 操作入口

完整 plugin package 会在 Claude Code、Codex、Grok Build 与 Antigravity 提供一个通用 router，以及四个可直接调用的操作入口：

| 操作 | Claude Code | Codex | Grok Build | Antigravity | 用途 |
|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | 撰写新内容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | 只诊断，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 根据原始事实与意图重新撰写 |

通用 router 仍可通过 `/sepia`（Claude Code、Grok Build、Antigravity）或 `$sepia`（Codex）使用。操作 wrapper 依赖同一套 package 里的标准 skill，不支持单独安装；请安装完整 plugin package。这张表仅记录 package 的调用语法；本次变更尚未实际测试安装后的 UI 与 runtime 行为。

## 实验性功能：叠加语气／风格 skill

v0.4.0 起，sepia 定义了与语气／风格类 skill（极简主义方法、品牌语调、persona 指南）叠加使用的接口。采用 opt-in：你明确说明已启用语气／风格 skill，sepia 才会在原路由之上加载 `references/voice-skills.md`；未明确说明则不加载，sepia 也永远不会自己注入美学。

接口约定摘要：sepia 的架构决策先行，语气技法选择性应用（每篇选择 3–5 种代表性技法，代表性结尾公式偶尔故意打破）。review 只报告语气／风格的已知代价、不直接修改，但一致性问题不因此减弱：语气风格不能免除节奏检查。在专业文档路由中，venue 仍决定语域，发生直接冲突时交由你决定。这个接口的依据是一次极简主义样本的盲审实验，属单一案例，不是量化证据。`references/voices/` 下附带一个内置 profile（海明威：小说用冰山式省略、专业文体用堪萨斯城星报规则，每一招都标注出处）；review 会在你的文本记录到的 findings 符合某个 profile 时给出提示，但在你明确说要应用之前不会加载任何内容。

## 安装

下列命令均采用 **user scope**：安装一次，每个项目都能用。

### 任何 agent（Skills CLI，支持 77+ 个 agent）

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update sepia -g             # update
npx skills remove sepia -g             # uninstall
```

[Skills CLI](https://skills.sh) 支持的 agent 均可安装：Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等；安装时会询问你要安装到哪些 agent。四大平台以外的执行行为我们尚未实际测试；skill 本身是 Agent Skills 标准下的纯 markdown，如果你的 agent 无法正常使用，欢迎提交 issue。

下面四个平台还提供原生插件安装方式，均已完成实际安装验证。验证范围包括成功安装并出现 sepia 入口；如上所述，尚未逐项测试运行时行为。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

在 session 里开启 `/plugin install` 对话框时，系统会要求选择 scope；请选 **User**。

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

Grok 也会自动找到现有的 Claude Code sepia 安装；两种方式均可使用。

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### Project scope（替代方案）

如果某个 repo 需要固定版本，可将 `skills/sepia/` 提交到该 repo，并置于 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 卸载

各工具都使用原生命令：

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

<a href="https://www.star-history.com/?repos=nanako0129%2Fsepia&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&theme=dark&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
  </picture>
</a>

## 参考资料

完整摘要与链接见 [`research/`](research/)。主要来源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 许可证

MIT
