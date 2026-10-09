# sepia

[English](README.md) | **繁體中文** | [简体中文](README.zh-CN.md)

[![behavioral eval](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/behavioral-eval.yml) [![version consistency](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml/badge.svg)](https://github.com/Nanako0129/sepia/actions/workflows/version-consistency.yml) [![release](https://img.shields.io/github/v/release/Nanako0129/sepia)](https://github.com/Nanako0129/sepia/releases/latest) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 從真正會讓 AI 洩底的層次下手。小說先修敘事架構，再碰字句；專業文件（發版說明、PR 回覆、事故檢討、工單、技術文章）按 venue 各配規則。

這是一套可攜式 [Agent Skill](https://agentskills.io/specification)：任何支援該標準的 agent 都能載入；[Skills CLI](https://skills.sh)（支援 77+ 家 agent）一行指令即可安裝。Claude Code、Codex、Grok Build、Antigravity 與 QwenPaw 另有原生 plugin 打包。全平台共用唯一正典 `SKILL.md`，不另開平台分支。提供四種操作：**write**、**review**（只診斷）、**refactor**（最小修改）、**recreate**（整篇重寫）。

## 目錄

- [為什麼還需要另一個 humanizer](#為什麼還需要另一個-humanizer)
- [操作入口](#操作入口)
- [實驗性功能：疊加聲音 skill](#實驗性功能疊加聲音-skill)
- [句長節奏與中文校準](#句長節奏與中文校準)
- [安裝](#安裝)
- [解除安裝](#解除安裝)
- [目錄結構](#目錄結構)
- [Star 趨勢](#star-趨勢)
- [資料來源](#資料來源)
- [贊助](#贊助)
- [授權](#授權)

---

## 為什麼還需要另一個 humanizer

常見的 humanizer 都在改用詞與句法。[StoryScope](https://arxiv.org/abs/2604.03136)（Russell et al., 2026：61,608 篇故事，涵蓋人類與 5 個頂尖 LLM）顯示，只靠 **敘事結構特徵** 的分類器就能以 93.2% macro-F1 偵測 AI 小說。同一份研究的 LAMP 編輯條件下（人類編輯改寫了字句風格），偵測率也只從 95.5% 降到 93.9%。留下的破綻都在架構層：敘事者講明主題、單線且因果收得過於工整的情節、情緒只靠身體感受呈現、沒有真實世界的參照、讀者缺席、時間全程線性，以及靠主角成長與接納收束的結局。

sepia 把這些實測差距，連同 [`research/`](research/) 裡整理過的相關研究，轉成小說寫作與修訂的三個 pass 流程：

| Pass | 層次 | 例子 |
|---|---|---|
| 1 | 敘事架構（小說） | 別再解釋主題、鬆開因果鏈、把揭露往後放、混用情緒呈現模式、稀疏的角色網絡、點名真實事物 |
| 2 | 篇章推進 | 拆掉段落—問題序列的模板、修掉故事中段的鬆垮、變換節奏與位置 |
| 3 | 字句風格 | 所有 humanizer 都在修的那層：陳腔濫調、句法模板、用詞、語域 |

另附 30 項特徵的診斷 rubric，以及分成兩層的各模型指紋，在已知寫作或執行的模型時套用：

| 模型家族 | 敘事層（StoryScope） | 字句層（廠商 prompting 指南） |
|---|---|---|
| Claude | 已量測 | Claude Fable 5.1 與 Mythos 5.1、Fable 5 與 Mythos 5、Opus 5、Opus 4.8 |
| GPT | 已量測 | GPT-5.6、GPT-6 Astra |
| Gemini | 已量測 | Gemini 3 與 3.1 |
| DeepSeek | 已量測 | 已查閱（未發布指南） |
| Kimi | 已量測 | 已查閱（未發布指南） |

> **注意：** 沒有發布 prompting 指南的廠商只記錄為「已查閱」，不作臆測。

專業文字露餡的方式不同，而結構層的結論在這裡同樣成立：2026 年一份研究把 StoryScope 複製到商業部落格文上，2,250 篇真人文對上 11,250 篇 AI 鏡像，只用結構特徵就以 98.0 macro-F1 分開兩者，AI 那一側被描述為「整齊、自我預告」（ledger 代號 `SLOPSHAPE-2026`，arXiv:2609.15369；preprint，特徵由 LLM 評分；量的是對原文與模型自我改寫稿的偵測，沒有測過人工編輯）。[`research/`](research/) 裡整理的研究指出的問題是：沒有資訊量的填充文字、該下判斷時還在閃躲、chatbot 殘留語氣、無視 venue 的語域、像同一個模子印出的排版。每種文件類型均在共用檢查表之上，各配一份精簡規則檔：

| 領域 | 要點 |
|---|---|
| 發版說明／公告 | 使用者影響擺前面、每項宣稱附佐證、不灌行銷詞 |
| PR／issue 回覆 | 先給答案、引用 `file:line`、不反射性稱讚、篇幅與事情的重要程度相稱 |
| 事故檢討 | 對人不究責，對機制追到底；附時間戳記、記錄走過的死路、每個行動項目都有負責人 |
| 工單 | 標題寫結果、驗收條件能測、能連結就別重複 |
| 技術文章 | 從問題切入、保留一條真實走過的死路、提出一個明確判斷、數字附上適用條件 |
| 長篇新聞（特寫、調查、數據報導） | 導言與正文兩種語域、引語保留口語質地、每個數字都有對照、不用總結收尾 |

> **核心原則：** 以整個人類分布為校準目標，別把 AI 分布倒過來套。人類的數值多落在中間。每條規則都用上的故事會形成另一種指紋；sepia 每篇只選 3–5 個手法，其餘留白。

## 操作入口

完整 plugin package 會在 Claude Code、Codex、Grok Build、Antigravity 與 QwenPaw 提供通用 router 與五個直接入口。QwenPaw 的 package 不自己註冊指令，由 QwenPaw 原生的 `/<skill-name>` 分派呼叫已安裝的 skill：

| 操作 | Claude Code | Codex | Grok Build | Antigravity | QwenPaw | 用途 |
|---|---|---|---|---|---|---|
| write | `/sepia-write` | `$sepia-write` | `/sepia-write` | `/sepia-write` | `/sepia-write` | 撰寫新內容 |
| review | `/sepia-review` | `$sepia-review` | `/sepia-review` | `/sepia-review` | `/sepia-review` | 只診斷，不修改 |
| refactor | `/sepia-refactor` | `$sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | `/sepia-refactor` | 在原文上做最小修改 |
| recreate | `/sepia-recreate` | `$sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | `/sepia-recreate` | 依原始事實與意圖重新撰寫 |
| hemingway | `/sepia-hemingway` | `$sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | `/sepia-hemingway` | 套用內建海明威聲音寫或改小說 |

通用 router 仍可透過 `/sepia`（Claude Code、Grok Build、Antigravity、QwenPaw）或 `$sepia`（Codex）使用。各平台驗證了什麼，寫在 [安裝](#安裝) 一節。

> **注意：** 不支援單獨安裝操作 wrapper。操作 wrapper 依賴同 package 裡的正典 skill；請安裝完整 plugin package。

## 實驗性功能：疊加聲音 skill

v0.4.0 起，sepia 定義了跟聲音／風格類 skill（極簡主義方法、品牌語調、persona 指南）疊加使用的介面。採 opt-in：你明講聲音 skill 在場，sepia 才會在原路由之上載入 `references/voice-skills.md`；不講就不載入外部聲音。

介面約定在各操作與路由間遵循固定的優先規則：

| 規則維度 | 約定規格 |
|---|---|
| 架構決策 | sepia 的架構決策先行。 |
| 技法選擇 | 聲音技法選擇性套用（每篇挑 3–5 招招牌技法，敘事型稀疏或事實不夠時更少；招牌結尾公式偶爾故意打破）。 |
| 審查診斷 | review 只回報聲音的已知代價，不代為修改。 |
| 均勻性要求 | 均勻性 finding 不打折：聲音不能豁免節拍器。 |
| 專業語域 | 專業路由上 venue 仍定語域。 |
| 衝突解決 | 直接衝突交回給你決定。 |

> **注意：** 聲音 skill 介面依據極簡規格樣本的盲審實驗，屬單一案例，非量測證據。

`references/voices/` 內建兩個 profile，另附一種帶宣告式覆蓋權的 persona profile 類型：

| Profile | 目標路線 | 來源與特點 | Opt-in 與調用 |
|---|---|---|---|
| 海明威（`references/voices/hemingway.md`） | 小說與專業文體 | 小說用冰山省略、專業文體用堪薩斯市星報規則，每招都標出處 | 直接入口 `/sepia-hemingway`（或 `$sepia-hemingway`）。小說路線上，要求「強力去 AI 味」即算 opt-in（sepia 會說明正在套用哪個 profile 以及如何取消）。沒有 opt-in 時，小說 review 僅在文本符合該 profile 時提出提示，不載入任何內容。 |
| 台灣深度報導（`references/voices/tw-journalism.md`） | 僅限專業路線 | 九種敘事型各自的手法，來自私下量測的繁中新聞語料與細讀 | Opt-in 片語：「套用台灣深度報導 voice」（或 `"apply the Taiwan journalism voice"`）。遵循與海明威 profile 相同的規則。 |
| Persona 模板（`references/voices/PERSONA-TEMPLATE.md`） | 作者自訂 | 單一寫作者的風格，帶宣告式覆蓋權；由 `scripts/check_persona.py` 檢查 | 作者自行建立的 profile，模板位於 `references/voices/PERSONA-TEMPLATE.md`。 |
| Nyaneko（`references/voices/personas/nyaneko.md`） | 僅限專業路線 | 專案內建的夥伴聲線，依維護者寫的語音規格撰寫並附她本人的示範句 | Opt-in 片語：「套用 persona Nyaneko」或 `apply persona Nyaneko`。 |

### 用 persona 寫東西：一段簡短教學

sepia 的規則負責拿掉 AI 味。溫度另有來源：寫的人知道自己是誰在對誰說話。這個專案自己的一個案例，只是觀察、沒有量測：v0.12.0 的 Threads 貼文用同一個模型、同一份 release notes 寫了兩次。第一次的提示給了骨架（版本行、條列、修正、工程備註、更新方式），出來是照表填格。第二次的提示給的是身分，「我是這個專案的維護者，剛發了 v0.12.0，用我自己的口吻講給追蹤者聽，怎麼組織由你決定」，加上 notes 當唯一事實來源和平台限制，出來的是維護者留下來用的那篇。之後用 sepia review 掃那篇，tell 集中在開頭與收尾（歷程鋪陳、格言式結尾、幾個絕對化的詞），refactor 拿掉它們，中間沒動。

有效的順序是：

1. 先給身分。
2. 事實另附，作為唯一來源。
3. 限制只寫平台限制，結構留給模型。
4. 最後用 sepia 當檢查。

```text
不要使用工具，需要的東西都在下面。
我是〈誰〉，寫給〈誰〉看，講的是〈剛發生的什麼事〉。用我自己的口吻；怎麼組織由你決定。
平台限制：〈長度、標記、提及〉。
事實只能來自下面的 notes，數字與編號要對得上。
===== notes =====
〈來源文件〉
```

persona profile 就是把這個身分寫下來一次，之後每篇都從它出發：他跟讀者是什麼關係、第一句做什麼、溫度掛在什麼事實上、絕不做什麼，以及幾篇他自己聲音的範文。模板在 `references/voices/PERSONA-TEMPLATE.md`，內建的 `references/voices/personas/nyaneko.md` 是一份完整範例，介面驗證腳本可檢查 profile 結構：

```bash
python3 scripts/check_persona.py <file>
```

鼓勵你寫自己的一套；範文承載的東西比描述多。

## 句長節奏與中文校準

style pass 會檢查句長的變化幅度，這是有量到它的研究裡唯一方向一致的句法量測：人類文本在同一段內變化較大，英文與中文皆然。

| 句法量測 | 狀態 | 實證依據 |
|---|---|---|
| 句長變化幅度 | 檢查訊號 | 英文與中文研究均顯示，人類文本在同一段內的變異數一致較高。證據與數字見 [`research/rhythm-syntax.md`](research/rhythm-syntax.md)。 |
| 句長平均值 | 排除不計 | 各語料庫量測方向互相矛盾。 |
| 標點計數 | 排除不計 | 各語料庫量測方向互相矛盾。 |
| 段落長度 | 排除不計 | 各語料庫量測方向互相矛盾。 |

中文文本會載入 `references/languages/zh.md`，跨四個不同證據層次校準 style pass：

| 層次／來源 | 證據性質 | 語料庫與校準細節 |
|---|---|---|
| HC3（2023） | 實測語料庫 | 人機對照中文語料庫基準。 |
| 繁中新聞量測 | 人類側實證量測 | 來自一家未具名台灣出版方，約兩千篇，橫跨約十年（語料未散布；摘要見 [`research/zh-news-corpus.md`](research/zh-news-corpus.md)）。 |
| 機器側對照組 | 機器側實證對照 | 三個模型共 119 篇合成文，使用同一份基礎提示，其中一個模型多一行變體。 |
| 台灣寫作慣例 | 規範標準 | 取自公開規範與一級共識的台灣寫作慣例簡短章節。 |

> **注意：** 三個中文實證來源的限制均寫在 `references/languages/zh.md` 檔案中。

## 安裝

> **注意：** 下列指令一律寫成 **user scope**：安裝一次，每個專案都能用。

### 任何 agent（Skills CLI，77+ 家）

```bash
npx skills add Nanako0129/sepia -g     # -g 才是 user scope；預設是 project
npx skills update sepia -g             # 更新
npx skills remove sepia -g             # 解除安裝
```

[Skills CLI](https://skills.sh) 支援的 agent 都能裝：Cursor、Cline、Windsurf、Copilot、OpenCode、goose 等；安裝時會提示選擇要裝到哪幾家 agent。五大平台以外的執行階段行為我們沒有實測過；skill 本體是 Agent Skills 標準下的純 Markdown，若你的 agent 無法正常讀取歡迎提出 issue。

> **注意：** 所謂「已驗證」是指安裝能完成且 sepia 入口有出現。五個原生 plugin 安裝管道均經過實機安裝驗證（QwenPaw 由貢獻者驗證）。安裝後各入口的行為是否與文件所述完全一致，並未逐一跨平台實測。

### Claude Code

```bash
# install
claude plugin marketplace add Nanako0129/sepia
claude plugin install sepia@sepia --scope user

# update
claude plugin marketplace update sepia
claude plugin update sepia
```

> **提示：** 在 session 內使用 `/plugin install` 對話框時會要求選擇 scope，請在此處選擇 **User**。

### Codex

```bash
# install
codex plugin marketplace add Nanako0129/sepia
codex plugin add sepia@sepia

# update — 更新 marketplace 快照後重新新增，以取得新版本
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

Grok 也會自動偵測既有的 Claude Code sepia 安裝；兩種方式都能使用。

### Antigravity

```bash
# install directly from GitHub
agy plugin install https://github.com/Nanako0129/sepia
```

### QwenPaw

```bash
# install：qwenpaw 只吃本機目錄（或 zip URL），先 clone；
# package 裡的 skills 符號連結在 clone 內就能解析
git clone https://github.com/Nanako0129/sepia
qwenpaw plugin install ./sepia/.qwenpaw-plugin

# uninstall
qwenpaw plugin uninstall sepia
```

> **注意：** 由貢獻者在 QwenPaw 2.2.1 上實機驗證（#250、#289，維護者未自行重跑）：安裝能完成，package 裡的 `skills` 符號連結會被 `shutil.copytree` 展開成實體目錄，`/sepia <text>` 與 `/sepia-write <text>` 都會透過 QwenPaw 的 skill 分派啟動 agent。另外四個入口走同一個分派，沒有逐一實測。若 package 讀不到 skill（zip 安裝，或不支援符號連結的 checkout），會記一條錯誤且不註冊任何東西，請改用 git clone 安裝。

### Project scope（替代方案）

當特定 repo 需要固定自己的版本時，將 `skills/sepia/` commit 至該 repo 內，路徑設為 `.agents/skills/sepia`（Codex 與 Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 解除安裝

各工具均使用其原生指令：

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
├── .qwenpaw-plugin/         # QwenPaw packaging (plugin.json, plugin.py, skills symlink)
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

Nanako0129/sepia 隨時間推移的 GitHub Star 成長趨勢。

## 資料來源

完整摘要與連結見 [`research/`](research/)。主要研究包含：

| 資料來源 | 發布場合／識別碼 |
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

## 贊助

sepia 免費，不需要帳號。每條規則背後的研究也都是公開的。專案的實際開銷只有維護時間和模型額度。額度花在兩處：委派研究 agent 讀論文原文做文獻調查；規則改動發布前用真實模型跑 A/B 對照小說，也跑跨平台的端到端審查。歡迎前往 Patreon 贊助。

[![Support sepia on Patreon](https://img.shields.io/badge/Support_on_Patreon-FF424D?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/cw/Nanako0129/membership)

## 授權

MIT
