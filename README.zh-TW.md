# sepia

[English](README.md) | **繁體中文**

> 從真正會讓 AI 洩底的層次下手。小說先修敘事架構，再碰字句；專業文件（發版說明、PR 回覆、事故檢討、工單、技術文章）則按 venue 各用一套規則。

這是一套可攜的 [Agent Skill](https://agentskills.io/specification)，支援 Claude Code、Codex、Grok Build 與 Antigravity。全平台共用唯一一份正典 `SKILL.md`，不另開平台分支。四種操作：**write**、**review**（只診斷）、**refactor**（最小修改）、**recreate**（整篇重寫）。

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

## 安裝

每個平台都有原生安裝方式，也各自附上更新指令。全部預設採用 **user scope**：安裝一次，每個專案都能用。

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

Antigravity 沒有 marketplace。請使用下方經過驗證的安裝器；它會建立帶有 ownership 標記的 skill 副本與 `/sepia` workflow，之後更新時可先偵測本機修改，不會直接覆寫。

### 四個平台一次裝完（替代方案）

從 release notes 取得成對發布的 commit SHA 與 `install.sh` SHA-256，替換兩個 placeholder 後執行：

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

checksum 指令是執行前的信任邊界。Shell 已經開始執行後，安裝器無法回頭證明先前執行的 bytes；外部檢查通過後，安裝器還會要求下載內容、抓取的 commit、checkout `HEAD` 與 Git 追蹤的可執行 `install.sh` object 全都對應同一個完整 SHA。Branch 名稱與 tag 都不能作為機器契約。

這會把 repo clone 到 `~/.sepia`（可用絕對路徑的 `SEPIA_HOME` 覆寫），並以 user scope 安裝到四個平台。更新或 rollback 時，使用新版或前一版發布的 SHA/digest pair 重跑同一段。既有 checkout 的 origin 必須與指定的 `SEPIA_REPO` 完全一致，而且 worktree 必須乾淨；foreign origin、untracked file、本機修改或異常 installer type 都會中止。

所有目的地都會在任何目的地變更前完成檢查。既有路徑只有在確認是 Sepia symlink，或是未修改且帶 ownership 標記的 Antigravity 副本時才會接受。舊版無標記副本及其他碰撞一律中止，沒有 force 選項；檢查後先把衝突路徑移開，再重新執行。受管理的配置如下：

| 平台 | 位置 | 機制 |
|---|---|---|
| Claude Code | `~/.claude/skills/sepia` | symlink |
| Codex | `~/.agents/skills/sepia` | symlink |
| Grok Build | `~/.grok/skills/sepia` | symlink |
| Antigravity | `~/.gemini/config/skills/sepia` ＋ `/sepia` global workflow | copy |

安全解除安裝會保留 checkout，只移除目前未修改、且能明確認定由 Sepia 管理的項目。請使用已安裝 revision 對應的 published SHA/digest pair 重跑相同的下載與 checksum block，只把最後一行換成：

```bash
SEPIA_ACTION=uninstall SEPIA_REF="$SEPIA_REF" \
  SEPIA_HOME="${SEPIA_HOME:-$HOME/.sepia}" \
  SEPIA_REPO="${SEPIA_REPO:-https://github.com/Nanako0129/sepia.git}" \
  bash "$installer"
```

這一行必須留在 checksum 保護的 subshell 裡，讓通過驗證的 downloaded installer 先驗證 checkout，再執行其中的 installer。若安裝時有設定 `SEPIA_HOME` 或 `SEPIA_REPO`，解除安裝時也要傳入相同值。Uninstall 會先檢查全部項目，再移除其中任何一項；modified copy、unmanaged replacement、舊版無標記路徑或錯誤 symlink 都會讓操作中止，全部目的地與 symlink target 保持不變。

維護者以兩個步驟發布不可變的 installer 座標：先用 `git rev-parse '<tag>^{}'` 把 release tag 解析為完整 commit，再執行 `git show '<commit>:install.sh' | shasum -a 256`。請在 release notes 發布完全相同的 SHA/digest pair，並在後續 documentation commit 同步替換兩份 README 的 placeholder；tag 只供人閱讀，不是 installer input。

### Skills CLI（替代方案，77+ 個 agent）

```bash
npx skills add Nanako0129/sepia -g     # -g = user scope; the default is project
npx skills update -g                   # update
```

### Project scope（替代方案）

某個 repo 要固定自己的版本時，把 `skills/sepia/` commit 到該 repo，放在 `.agents/skills/sepia`（Codex＋Antigravity）或 `.claude/skills/sepia`（Claude Code）。

## 目錄結構

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

## 資料來源

完整摘要與連結見 [`research/`](research/)。主要來源：StoryScope ([arXiv:2604.03136](https://arxiv.org/abs/2604.03136)); LAMP ([CHI 2025](https://arxiv.org/abs/2409.14509)); Measuring AI Slop ([arXiv:2509.19163](https://arxiv.org/abs/2509.19163)); Reinhart et al. ([PNAS 2025](https://arxiv.org/abs/2410.16107)); Russell et al. ([ACL 2025](https://arxiv.org/abs/2501.15654)); NarraBench ([arXiv:2510.09869](https://arxiv.org/abs/2510.09869)); Echoes in AI ([PNAS 2025](https://arxiv.org/abs/2501.00273)); QUDsim ([COLM 2025](https://arxiv.org/abs/2504.09373)); Beguš ([2024](https://arxiv.org/abs/2310.12902)); Beyond Checkmate ([EMNLP 2025](https://arxiv.org/abs/2501.19301)); Nonaka & Perry ([2025](https://arxiv.org/abs/2510.18932)); Chakrabarty et al. ([2026](https://arxiv.org/abs/2510.13939)).

## 授權

MIT
