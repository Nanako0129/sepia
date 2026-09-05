# sepia

[English](README.md) | **繁體中文** | [简体中文](README.zh-CN.md)

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 從結構層次去除文字的 AI 痕跡。小說在動到任何字詞選擇之前，先修復敘事架構；專業文件（發佈說明、PR 回覆、事後檢討、工單、技術文章）則各自搭配符合其發表場合的規則。

這是一套 [Agent Skill](https://agentskills.io/specification)。只要遵循這項標準的 agent 都能載入，且 [Skills CLI](https://skills.sh) 支援 77+ 款 agent，一行指令就能裝好。Claude Code、Codex、Grok Build 與 Antigravity 額外提供原生外掛打包，四者都通過安裝驗證。專案維持單一正典 `SKILL.md`，不針對個別平台開 fork 分支。四種操作分別為 **write**、**review**（僅診斷）、**refactor**（最少修改）與 **recreate**（整篇重寫）。

## 為什麼還需要另一個 humanizer

一般的 humanizer 多半只修飾字詞選擇與句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026: 61,608 篇故事，包含人類與 5 款尖端 LLM）指出，光靠**敘事結構特徵**的分類器就能以 93.2% 的 macro-F1 抓出 AI 小說，把表面風格修飾掉也幾乎動搖不了結果（95.5% → 93.9%）。沒被抹掉的破綻本質上都是架構問題。這些特徵包括敘事者自己跳出來解釋主題、因果收得過於工整的單線情節、情緒全寫成生理反應、完全沒有現實世界的參照、缺少讀者意識、線性的時間軸，以及靠主角心理成長與接納來收束的結局。

sepia 把這些量測出來的落差，連同在 [`research/`](research/) 裡梳理的十一篇相關研究，轉化為一套針對小說的三道 pass 寫作與修訂流程。

| Pass | 層次 | 例子 |
|---|---|---|
| 1 | 敘事架構（小說） | 別再解釋主題、鬆開因果鏈、把揭露往後放、混用情緒呈現模式、稀疏的角色網絡、點名真實事物 |
| 2 | 篇章推進 | 拆掉段落—問題序列的模板、修掉故事中段的鬆垮、變換節奏與位置 |
| 3 | 字句風格 | 所有 humanizer 都在修的那層：陳腔濫調、句法模板、用詞、語域 |

此外還有一套涵蓋兩個層次、共 30 項特徵的診斷標準與各模型指紋。敘事層面的破綻透過 StoryScope 量測（Claude、GPT、Gemini、DeepSeek、Kimi），句子層級的特徵則整理自各廠商自家的 prompt 指南（Claude Fable 5.1、Fable 5、Opus 5、Opus 4.8；GPT-5.6；Gemini 3 系列），在已知執筆或執行的模型時套用。至於未發佈這類指引的廠商，一律記錄為已查閱，絕不妄加揣測。

專業文字露餡的方式則不同。各項研究直指那些缺乏資訊量的填充廢話、該下判斷時卻閃爍其詞的保留說法、殘留的 chatbot 語氣、忽視場合的語域，以及看起來千篇一律的刻板排版。每種文件類型都會在一份共用的檢查清單之上，各自搭配一份精簡的規則檔案。

| 領域 | 要點 |
|---|---|
| 發版說明／公告 | 使用者影響擺前面、每項宣稱附佐證、不灌行銷詞 |
| PR／issue 回覆 | 先給答案、引用 `file:line`、不反射性稱讚、篇幅與事情的重要程度相稱 |
| 事故檢討 | 對人不究責，對機制追到底；附時間戳記、記錄走過的死路、每個行動項目都有負責人 |
| 工單 | 標題寫結果、驗收條件能測、能連結就別重複 |
| 技術文章 | 從問題切入、保留一條真實走過的死路、提出一個明確判斷、數字附上適用條件 |

最核心的原則是：**向人類常態分佈對齊，切忌直接反轉 AI 的分佈**。人類的特徵值多半落在中間區間；每條規則都照單全收的故事，只會產生另一種新的指紋。這套 skill 在每篇故事中只會挑選 3–5 個手法，適度留白。

## 操作入口

完整的外掛套件為 Claude Code、Codex、Grok Build 與 Antigravity 提供了一個通用 router 以及五個直接入口。

| 操作 | Claude Code | Codex | Grok Build | Antigravity | 用途 |
|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | 撰寫新內容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | 只診斷，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 依原始事實與意圖重新撰寫 |
| hemingway | `/sepia-hemingway` | `$sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | 套用內建海明威聲音寫或改小說 |

通用的 `/sepia`（Claude Code、Grok Build 與 Antigravity）或 `$sepia`（Codex）router 依然可用。各操作的 wrapper 仰賴同套件內的正典 skill，因此不支援單獨安裝 wrapper，請安裝完整的外掛套件。這張表格僅記錄套件語法，安裝後的 UI 與 runtime 行為並未包含在此次變更的測試範圍中。

## 實驗性功能：疊加聲音 skill

從 v0.4.0 開始，sepia 定義了一套介面，用來疊加特定的聲音或風格 skill（例如極簡主義寫作法、品牌語調或角色設定指南）。這項功能採取主動啟用（opt-in）。只要向 sepia 表明聲音 skill 正在使用中，它就會在一般流程上載入 `references/voice-skills.md`。除非你明確指定，否則它什麼都不會載入，更絕不會擅自注入任何特定美學。

簡單來說，sepia 的架構決策永遠在先，風格手法則採選擇性套用（每篇文章選用 3–5 個招牌手法，偶爾故意打破公式化結尾）。Review 會指出該風格已知的負面代價而不會擅自修掉，對均勻度的診斷結果也維持完整強度；擁有風格不能當作文字像節拍器般死板的藉口。在專業文字的流程中，場合依然決定語域高低，一旦出現直接衝突會交還給你定奪。這套介面源自一次針對嚴格極簡主義樣本的盲審實驗（這是一組範例示範，並非量測證據）。`references/voices/` 底下內建了一份 profile（海明威風格，小說部分涵蓋冰山省略法，專業文字採用堪薩斯市星報守則，每個手法都清楚標記出處）。在小說處理上，review 若比對出文字記錄符合該特徵便會提出回報，直接要求對故事強力去 AI 也算作同意啟用；sepia 會明示正在套用該 profile 並說明停用方式。`/sepia-hemingway` 則是直接入口。

## 句長節奏與中文校準

風格 pass 會檢查句子長度的 *spread*（離散分佈）。在所有測量過句法的研究裡，這是唯一結論完全一致的指標（無論英文或中文，人類文字在同一個段落內的句長變化幅度都更大）。平均句長、標點符號數量與段落長度則列為非訊號，因為各項測量的走向彼此矛盾。中文文字會載入 `references/languages/zh.md`，這份校準資料建立在唯一一份經過測量的中文語料庫（HC3, 2023）上，其限制已於檔案內敘明。相關證據與數據都記錄在 `research/rhythm-syntax.md`。

## 安裝

下列指令均以 **user scope** 撰寫（安裝一次，即可在每個專案中使用）。

### 任何 agent（Skills CLI，77+ 家）

```bash
npx skills add Nanako0129/sepia -g     # -g 才是 user scope；預設是 project
npx skills update sepia -g             # 更新
npx skills remove sepia -g             # 解除安裝
```

凡是 [Skills CLI](https://skills.sh) 支援的 agent 都能安裝（包含 Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等）。出現提示時直接勾選你的 agent 即可。下列四個平台以外的 runtime 行為我們尚未實際測試過；這套 skill 是 Agent Skills 標準下的純 markdown 檔案，要是你的 agent 讀取卡住，歡迎開 issue 回報。

下方四個平台具備原生外掛安裝程式，各自都經過實際安裝測試。所謂驗證是指安裝順利完成且 sepia 入口正常出現，runtime 行為則如前文所述。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

在 session 裡的 `/plugin install` 對話視窗會要求你挑選 scope，請在該處選擇 **User**。

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

如果你原本就有在 Claude Code 安裝過 sepia，Grok 也會自動偵測到該安裝，兩種路徑都行得通。

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### Project scope（替代方案）

當 repo 需要鎖定自己的版本時，將 `skills/sepia/` commit 到該 repo 內，存放為 `.agents/skills/sepia`（Codex + Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 解除安裝

各工具均使用自家的原生指令。

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
│   │   └── references/       # passes、rubric、fingerprints、domain rules、languages/zh.md、voice-skills（實驗性）
│   ├── sepia-write/SKILL.md  # 固定單一操作的薄 wrapper
│   ├── sepia-review/SKILL.md
│   ├── sepia-refactor/SKILL.md
│   ├── sepia-recreate/SKILL.md
│   └── sepia-hemingway/SKILL.md  # fiction write/refactor with the built-in voice
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

## 贊助

sepia 免費，不需要帳號。每條規則背後的研究也都是公開的。專案的實際開銷只有維護時間與兩種模型額度：委派研究 agent 讀論文原文做文獻調查，以及規則改動發布前用真實模型實測 A/B 對照小說與跨平台端到端審查。歡迎前往 Patreon 贊助支持。

[![Support sepia on Patreon](https://img.shields.io/badge/Support_on_Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/Nanako0129/membership)

## 授權

MIT
