# sepia

[English](README.md) | **繁體中文**

> 從真正會讓 AI 洩底的層次下手。小說先修敘事架構，再碰字句；專業文件（發版說明、PR 回覆、事故檢討、工單、技術文章）則按 venue 各用一套規則。

這是一套可攜的 [Agent Skill](https://agentskills.io/specification)：任何支援這個標準的 agent 都能載入；[Skills CLI](https://skills.sh)（支援 77+ 家 agent）一行指令就能裝。Claude Code、Codex、Grok Build 與 Antigravity 另有原生 plugin 打包，四家都實機裝過。全平台共用唯一一份正典 `SKILL.md`，不另開平台分支。四種操作：**write**、**review**（只診斷）、**refactor**（最小修改）、**recreate**（整篇重寫）。

## 為什麼還需要另一個 humanizer

常見的 humanizer 都在改用詞與句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026：61,608 篇故事，涵蓋人類與 5 個頂尖 LLM）顯示，只靠**敘事結構特徵**的分類器就能以 93.2% macro-F1 偵測 AI 小說；把字句風格修掉，分類表現也只從 95.5% 降到 93.9%。留下的破綻都在架構層：敘事者直接講明主題、單線且因果收得過於工整的情節、情緒只靠身體感受呈現、沒有真實世界的參照、讀者缺席、時間全程線性，以及靠主角成長與接納收束的結局。

sepia 把這些實測差距，連同 [`research/`](research/) 裡整理過的十一篇相關研究，轉成小說寫作與修訂的三個 pass 流程：

| Pass | 層次 | 例子 |
|---|---|---|
| 1 | 敘事架構（小說） | 別再解釋主題、鬆開因果鏈、把揭露往後放、混用情緒呈現模式、稀疏的角色網絡、點名真實事物 |
| 2 | 篇章推進 | 拆掉段落—問題序列的模板、修掉故事中段的鬆垮、變換節奏與位置 |
| 3 | 字句風格 | 所有 humanizer 都在修的那層：陳腔濫調、句法模板、用詞、語域 |

另附 30 項特徵的診斷 rubric，以及各模型的指紋修正（Claude、GPT、Gemini、DeepSeek、Kimi）。

專業文字露餡的方式不同。研究指出，常見問題包括沒有資訊量的填充文字、該下判斷時還在閃躲、chatbot 殘留語氣、無視 venue 的語域，以及像同一個模子印出的排版。每種文件都共用一份檢查表，再各配一份精簡規則檔：

| 領域 | 要點 |
|---|---|
| 發版說明／公告 | 使用者影響擺前面、每項宣稱附佐證、不灌行銷詞 |
| PR／issue 回覆 | 先給答案、引用 `file:line`、不反射性稱讚、篇幅與事情的重要程度相稱 |
| 事故檢討 | 對人不究責，對機制追到底；附時間戳記、記錄走過的死路、每個行動項目都有負責人 |
| 工單 | 標題寫結果、驗收條件能測、能連結就別重複 |
| 技術文章 | 從問題切入、保留一條真實走過的死路、提出一個明確判斷、數字附上適用條件 |

貫穿全篇的原則：**以整個人類分布為校準目標，別把 AI 分布直接倒過來套**。人類的數值多落在中間。每條規則都用上的故事會形成另一種指紋；sepia 每篇只選 3–5 個手法，其餘留白。

## 操作入口

完整 plugin package 會在 Claude Code、Codex、Grok Build 與 Antigravity 提供一個通用 router，以及四個可直接呼叫的操作入口：

| 操作 | Claude Code | Codex | Grok Build | Antigravity | 用途 |
|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | 撰寫新內容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | 只診斷，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 依原始事實與意圖重新撰寫 |

通用 router 仍可透過 `/sepia`（Claude Code、Grok Build、Antigravity）或 `$sepia`（Codex）使用。操作 wrapper 依賴同一套 package 裡的正典 skill，不支援單獨安裝；請安裝完整 plugin package。這張表只記錄 package 語法；本次變更尚未實測安裝後的 UI 與 runtime 行為。

## 實驗性功能：疊加聲音 skill

v0.4.0 起，sepia 定義了跟聲音／風格類 skill（極簡主義方法、品牌語調、persona 指南）疊加使用的介面。採 opt-in：你明講聲音 skill 在場，sepia 才會在原路由之上載入 `references/voice-skills.md`；不講就不載入，sepia 也永遠不會自己注入美學。

條約摘要：sepia 的架構決策先行，聲音技法選擇性套用（每篇挑 3–5 招招牌技法，招牌結尾公式偶爾故意打破）。review 只回報聲音的已知代價、不代修，但均勻性 finding 不打折：聲音不能豁免節拍器。專業路由上 venue 仍定語域，直接衝突交回給你決定。這個介面的依據是一次極簡規格樣本的盲審實驗，屬單一案例，不是量測證據。

## 安裝

下列指令一律寫成 **user scope**：安裝一次，每個專案都能用。

### 任何 agent（Skills CLI，77+ 家）

```bash
npx skills add Nanako0129/sepia -g     # -g 才是 user scope；預設是 project
npx skills update sepia -g             # 更新
npx skills remove sepia -g             # 解除安裝
```

[Skills CLI](https://skills.sh) 支援的 agent 都能裝：Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等；安裝時會問你要裝到哪幾家。四大平台以外的執行行為我們沒有實測過；skill 本體是 Agent Skills 標準下的純 markdown，你的 agent 若吃不動歡迎開 issue。

下面四個平台另有原生 plugin installer，各自實機裝過。驗證範圍是裝得完、sepia 入口出現；runtime 行為如上所述未逐一實測。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

在 session 裡開啟 `/plugin install` 對話框時，系統會要求選 scope；請選 **User**。

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

Grok 也會自動找到既有的 Claude Code sepia 安裝；兩種方式都能用。

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### Project scope（替代方案）

某個 repo 要固定自己的版本時，把 `skills/sepia/` commit 到該 repo，放在 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 解除安裝

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

## 目錄結構

```text
sepia/
├── plugin.json              # Antigravity packaging
├── skills/
│   ├── sepia/                # 正典 skill（Agent Skills standard）
│   │   ├── SKILL.md          # routing、operations、calibration rules、guardrails
│   │   └── references/       # passes、rubric、fingerprints、domain rules、voice-skills（實驗性）
│   ├── sepia-write/SKILL.md  # 固定單一操作的薄 wrapper
│   ├── sepia-review/SKILL.md
│   ├── sepia-refactor/SKILL.md
│   └── sepia-recreate/SKILL.md
├── .claude-plugin/          # Claude Code packaging (plugin.json, marketplace.json)
├── .codex-plugin/           # Codex packaging
├── .agents/                 # Codex/Antigravity workspace-mode discovery + Antigravity workflow
└── research/                # digested evidence base with sources
```

## Star 趨勢

<a href="https://www.star-history.com/?repos=nanako0129%2Fsepia&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&theme=dark&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=nanako0129%2Fsepia&type=date&legend=top-left&sealed_token=tvzQmDPYfGPfGtBVAmiPEqqGYMMK8T1SUMAXlEaJL1B2Me9ZcXDPNjPj0qV3TVzyz-_uYj4Xh25L3X81y9pimzDevwlWTlJQKZr38HogEqXFAPRbtrv8NFnNCrguM2lvqNG5_DS_1W_8rttYAiJEOaGd1onyFf4NYmmQPGoHuwTyhiJDPdmiYOL3AOKK">
  </picture>
</a>

## 資料來源

完整摘要與連結見 [`research/`](research/)。主要來源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 授權

MIT
