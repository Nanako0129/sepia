# 新聞寫作教科書與風格指南：可轉成規則的部分（digest）

> 目的：把新聞寫作與敘事性非虛構的教科書、通訊社與公共媒體手冊、台灣官方語文規範，整理成「哪一條主張、誰說的、什麼等級」，給 `references/languages/zh.md`（標點與數字的規範側）與 `references/domains/journalism.md`（venue 規則的出處）對照用。這份不是量測，是規範；量測在 `zh-news-corpus.md`。
>
> 來源與方法：2026-09-17 以 Grok 4.6 headless 做一次網頁調查（提示在快取，不進 repo），要求每條主張附出處與等級、找不到就寫「未查到」；調查列出 19 個來源、106 處「未查到」。本文只收其中兩類：(1) 我逐頁核對過原文的（標 **核對**）；(2) 調查有給頁碼、URL 或 ISBN 且多份一級來源同向的（標 **調查**）。調查給不出原文頁碼的主張不收；唯一例外是 §三 的環境資訊中心列，只留作數字門檻的對照，不當來源使用。調查所報的 URL 與 ISBN 列在文末〈附：調查所報出處〉，除標 **核對** 者（§一 兩份台灣規範、Reuters 的引語一條）外未逐一核對。等級：**一級**＝教科書、官方或準官方手冊、政府語文規範；**二級**＝教學網站、講義、書評、轉述。

## 一、台灣官方規範（核對，一級）

### 教育部《重訂標點符號手冊》修訂版（`MOE-PUNCT-2008`）

| 符號 | 位置 | 說明（手冊原文或近原文） |
|---|---|---|
| 引號「」『』 | 前後符號各占一個字 | 「用於標示說話、引語、特別指稱或強調的詞語」；「引號分單引號及雙引號，通常先用單引號，如果有需要，單引號內再用雙引號」；「一般引文的句尾符號標在引號之內」；「引文用作全句結構中的一部分，其下引號之前，通常不加標點符號」 |
| 破折號 ── | 占行中二格 | 「用於語意的轉變、聲音的延續，或在行文中為補充說明某詞語之處，而此說明後文氣需要停頓」 |
| 刪節號 …… | 占行中二格（六點） | 「用於節略原文、語句未完、意思未盡，或表示語句斷斷續續等」 |
| 夾注號 | 甲式（　）各占一字；乙式──　──各占二格 | 「用於行文中需要注釋或補充說明」 |
| 問號 ？ | 占一個字 | 「一、用於疑問句之後。二、用於歷史人物生死或事件始末之時間不詳。」（頁面沒有間接問句的規定） |
| 書名號 乙式《》〈〉 | 前後各占一格 | 「《 》多用於書名，〈 〉多用於篇名」；「用於書名、篇名、歌曲名、影劇名、文件名、字畫名等」；附注「書刊的題簽、文章的標題、報刊雜誌的刊頭或宣傳海報等，不必用書名號」 |
| 間隔號 ． | 占一個字，居正中 | 用於書名與篇章卷名之間、套書與單本之間、「原住民命名習慣之間隔」、「翻譯外國人的名字與姓氏之間」；附注：國字整數與小數分界處也可用 |

對 sepia：台灣新聞的第一層引號是「」，“ ” 是西文或大陸習慣；破折號的手冊形式是兩格的「──」，單格「—」不是手冊形式（`zh.md` §1b 把它當字形選擇、至多是語域不符，不當錯誤）；刪節號是六點。這三條是 `zh.md` §1b 標點列的規範側；量測側（人類 61% 文章用單「──」、「……」2%、成對插入語 15%）與規範方向一致。手冊不規範數字寫法與化名標示。

### 行政院《公文書橫式書寫數字使用原則》（`EY-NUMERALS-2004`，院臺秘字第 0930089122 號函）

- 具一般數字意義（代碼、身分證統一編號、編號、發文字號、日期、時間、序數、電話、門牌）、統計意義（計量單位、統計數據），或以阿拉伯數字較清楚者，用阿拉伯數字。
- 描述性用語、專有名詞（地名、書名、人名、頭銜）、慣用語，或以中文數字較妥者，用中文數字。

對 sepia：這是公文原則，不是報社法；台灣新聞實務在它之上疊了各社的百分比與紀年規則。量測到的人類新聞以阿拉伯數字為主（每千 token 18.7 對中文數字 5.1），三個對照模型把數字全寫成中文（§1c）；這是總量分布，量測未標註每個數字的語意類別，所以既不能說人類側與原則「一致」、也不能說中文數字「多為慣用語」、更不能說機器側違反原則。原則本身仍是規範側的規則，sepia 只把它當 ledger `EY-NUMERALS-2004` 的規範文件引用，不從量測推出違規。「三讀」「九二一」「三代」這類慣用語仍應是漢字；`zh.md` 沒有也不會寫成「一律阿拉伯數字」。

## 二、英文教科書與手冊（調查，一級為主）

| 來源 | 引語 | 歸因動詞 | 句子 | 收尾 | 反問 | 第一人稱 |
|---|---|---|---|---|---|---|
| AP Stylebook（quotations in the news 條） | 幾乎不可改；文法小錯不改；口誤極少才用刪節號 | 用 said；避免 claimed、admitted 等帶評價的動詞 | — | — | — | — |
| Reuters（Journalistic Standards 頁，**核對**；其餘欄位出自調查所述的 Handbook of Journalism，未核對） | 引語「神聖」（頁面原句 Quotes are sacrosanct，核對）；只能刪冗詞不改意思；窘迫口語改用轉述（調查） | said 精神（調查） | 句子宜短但要變化，避免機關槍節奏（調查） | — | — | 意見不進新聞（調查） |
| BBC News Style Guide | 選最好的幾句直接引，其餘轉述；不把文法錯誤端上螢幕 | admit 要小心，寧用 said；廣播體歸因放在斷言之前 | 早期版：短句短詞、S-V-O | — | 現行 A–Z 未查到禁令 | 消息不以 The BBC 自賣開頭 |
| The Economist Style Guide | 少用直接引語，能改寫得更短就改寫 | — | 能刪就刪；one idea per sentence（轉述） | 不要清喉嚨、不先鋪場景 | rhetorical questions rarely（轉述） | — |
| Roy Peter Clark, *Writing Tools* | 對話與引語分開看 | — | 不要怕長句；最有力的思想用最短句；複雜處反而要短 | — | — | — |
| William Zinsser, *On Writing Well* | 用他自己的話，比你寫得好 | — | 剝到最乾淨，不是每句都要短；journalese 是壞習慣 | — | — | 非虛構盡量用 I，但報紙消息不用 |
| Jack Hart, *Storycraft*／*Wordcraft* | — | — | — | 敘事的結尾是高潮後的 denouement，不是可刪段 | — | 敘事距離可調 |
| Carole Rich, *Writing and Reporting News*（第 8 版） | — | — | — | kicker 要收束但不重複已說的話；quote kicker 最常見；WSJ 用 circle kicker | — | — |
| Melvin Mencher, *News Reporting and Writing*（第 11–12 版；Poynter 轉載語錄） | Get a good quote up high | Don't fear using the word "said" | Write tightly | 倒金字塔的結尾最不重要 | — | 記者不把個人偏見放進報導（轉述） |
| Missouri Group, *News Reporting and Writing*（第 13 版） | 目錄有 Using Quotes Effectively | 未查到 | 未查到 | 未查到 | 未查到 | 未查到 |

## 三、華文教材與媒體規範（調查）

| 來源 | 等級 | 可用主張 |
|---|---|---|
| 聯合報《新聞寫作通則》（經行政院《文書處理手冊》附錄轉載，2000 年代） | 一級（舊） | 導言 ≤ 60 字；每段 ≤ 150 字；主動優於被動；少評價形容詞；職稱全銜在姓名前，其後可「某院長」；舊規以漢字寫年份與百分比（今日多數新聞網站已改阿拉伯數字與 %） |
| 彭家發《新聞寫作》等三書 | 一級（書目核到，主張未核對） | 調查稱為華爾街日報公式在台灣中文教學的來源，但缺頁碼引句；依本檔納入規則不當一級主張使用 |
| 中國大陸《新聞寫作教程》類（劉明華等） | 一級（地區不同） | 導語本身就是 nut，不另叫 nut graf；消息結尾可有可無；含政治導向，台灣不適用 |
| 環境資訊中心編輯原則 | 二級（單一媒體） | 一至十用國字、二位數以上用阿拉伯數字、五位數以上用萬億；一律西元年 |
| 教育部、聯合報通則、中央社公開頁 | — | 「化名」的標點公式**均未查到**一級條文，是倫理慣例不是 stylebook |
| 中央社、公視、自由時報用字手冊；端傳媒、明報風格指南；王洪鈞、鍾蔚文、林照真的寫作細則 | — | **查無一級文本**，不假裝有規則 |

## 四、指南之間的分歧（不寫成單一規則）

1. **引語可不可以清理**：AP、Reuters 幾乎照錄；BBC 多一層「保護說話者免於出糗」；經濟學人把改寫當預設；Zinsser 用原話。sepia 的立場已在 SKILL.md（真實引語是 load-bearing，refactor 不動，只能依使用者提供的逐字稿校正），與通訊社一側。
2. **歸因位置**：美國報紙「先話後人」（Smith said），BBC 廣播「先人後話」。中文新聞量測到的是：含任何「」的句子 61% 無歸因動詞，但那個計數含術語與反諷引號，不能推論說話引語的歸因（`zh.md` §1b 的讀法）；「說」多放在引語之後是 169 篇細讀的觀察，不是量測。
3. **第一人稱**：Reuters、聯合報通則不准或高度限制；Zinsser、Hart、《Telling True Stories》在敘事非虛構鼓勵。`journalism.md` rule 5 走中間：方法、拉回、記錄沉默、第一人稱紀實的觀察。
4. **句長**：「一段一句」是美國報紙入門訓練（LibreTexts 等講義），不是 Clark、Zinsser 或敘事非虛構的規則；Reuters 要短但要變化；Clark 不怕長句。台灣人類新聞量到的是長句多子句（句均 59 字、每句 4.5 個子句），三個對照模型都短五分之一到四成（`zh.md` §1c）。任何「短句＝人味」的規則在這個語域都站不住。
5. **數字 1–10**：AP、BBC 1–9 用文字；經濟學人 1–10；環境資訊中心一至十；行政院公文以「意義」分工而不以大小分工。
6. **nut graf**：Rich、Hart、Nieman 多數課要有；Nieman 2019 專輯承認極強敘事可以沒有；經濟學人不清喉嚨。
7. **結尾**：倒金字塔傳統結尾最不重要、可刪；敘事非虛構結尾是結構的一部分。台灣人類長篇新聞量到總結式收尾 7／169，是敘事那一側的做法（引語、資訊、回到人物、懸置），不是「可刪」那一側。
8. **反問句**：英美入門課視 question lead 為高風險；經濟學人 rarely；教育部手冊「間接問句不用問號」是間接限制。台灣人類長篇新聞量到 72% 文章有段末問句（`zh.md` §1c 人類欄，只計「段落以問句結尾」）；「下一段由受訪者接答」是 169 篇細讀的觀察，量測沒有記錄下一段是誰。兩者不衝突：教科書反對的是拿反問代替查證，細讀看到的是換段裝置。
9. **華爾街日報公式**：Rich 當公式教（彭家發的部分只核到書目，主張未核對）；WSJ 自己的主筆說沒有死板公式，只有抓住讀者、早點說清楚、用細節證明。
10. **職稱與姓名的順序**：聯合報通則要求首次全銜在姓名前；英美手冊只規範英文的 title before name；沒有第二份中文一級來源。台灣各社樣本兩種順序都有，不寫成單一規則，`zh.md` §0 只在 venue 樣本先職稱後姓名時才修。

## 五、最小公約數（多份一級來源同向、無強一級反對）

1. 硬消息先寫最重要的事；軟開頭要早點讓讀者知道這篇在做什麼。
2. 直接引語留給「這個人非這樣說不可」的句子，其餘轉述；直接引語幾乎照錄，窘迫的破句轉述不嘲弄。
3. 歸因動詞預設 said／說；claimed、admitted、指出、強調都帶評價。
4. 硬消息裡記者的「我」與評價形容詞預設不出現；敘事非虛構另論，且要標明距離與方法。
5. 能主動就不要被動；不堆形容詞；行話換日常詞。
6. 台灣標點：「」『』先單後雙；「──」與「……」各占兩格；外文與生卒年用（　）；書名《》篇名〈〉。
7. 台灣數字：統計、日期、度量用阿拉伯數字；成語、慣用語、專名用漢字；百分比與紀年依各社，同一篇不混用。
8. （撤回，2026-09-17）職稱先於姓名只有一份一級舊來源（§三 聯合報通則），沒有第二份一級來源同向，不構成公約數；移到 §四 10，`zh.md` §0 改為依 venue 樣本決定。
9. 消息不用反問代替事實；倒金字塔的結尾可刪，敘事的結尾是結構的一部分。
10. 結構為材料服務，不把材料塞進公式。

## 六、對 sepia 的意義（推論）

- `zh.md` §1b 的標點列與 §1c 的數字列現在有規範側可引：量測說「人類這樣做」，手冊說「應該這樣做」，兩者同向時才寫進 read-as。
- 第 4 點「短句不是人味」與第 7 點「總結式收尾在敘事側是結構的一部分」是教科書與量測互相支持的兩處，也是目前執行模型最常寫反的兩處。
- 第 3 點「歸因動詞預設說」：語料裡「表示／指出／強調」十年間上升是站方漂移，教科書其實反對；sepia 不把漂移當人味 restore。
- 不收進規則的：引語清理（分歧）、第一人稱（分歧，venue 決定）、數字 1–10 的門檻（三套不同）。

## 附：調查所報出處（Grok 4.6 調查 2026-09-17 回報；除標 **核對** 者外未逐一核對，僅供讀者追查）

| 來源 | 調查所報 URL／ISBN |
|---|---|
| AP Stylebook | https://www.apstylebook.com/ |
| Reuters Handbook of Journalism | 調查未給 URL。2026-09-17 以 curl 核對：handbook.reuters.com 轉址到 https://reutersagency.com/about/standards-values/ （Reuters Journalistic Standards），頁面含「Quotes are sacrosanct」；本檔引自 Reuters 的其餘主張（said、句長、意見）不在該頁，維持調查等級 |
| BBC News Style Guide | https://www.bbc.com/newsstyleguide/ ；A–Z https://www.bbc.com/newsstyleguide/all/ ；numbers https://www.bbc.com/newsstyleguide/numbers/ ；早期 PDF https://www.peteburns.com/downloads/BBC%20news%20styleguide.pdf |
| The Economist Style Guide | 存檔 PDF https://web.archive.org/web/20160914130123if_/http://www.frzee.com/Education/The%20Economist%20Style%20Guide.pdf |
| Roy Peter Clark, *Writing Tools* | ISBN 978-0-316-02840-0（十週年版）；Poynter 早期 30 tools http://www.poynter.org/uncategorized/716/thirty-tools-for-writers/ |
| William Zinsser, *On Writing Well* | ISBN 978-0-06-089154-1（30 週年版） |
| Jack Hart, *Storycraft* | ISBN 978-0-226-73692-1（2e）；https://press.uchicago.edu/ucp/books/book/chicago/S/bo71028154.html ；Nieman 訪談 https://niemanstoryboard.org/2011/10/20/jack-hart-storycraft-narrative-nonfiction-interview/ |
| *Telling True Stories*（Nieman） | ISBN 978-0-452-28755-6；https://niemanstoryboard.org/about/telling-true-stories/ |
| Carole Rich, *Writing and Reporting News*（第 8 版） | ISBN 978-1-305-07733-1；https://www.cengageasia.com/TitleDetails/isbn/9781305077331 |
| Melvin Mencher, *News Reporting and Writing*（第 12 版） | ISBN 978-0-07-351199-3 |
| Missouri Group, *News Reporting and Writing*（第 13 版） | ISBN 978-1-319-20816-5；https://www.macmillanlearning.com/college/us/product/News-Reporting-and-Writing/p/1319208169 |
| 美國國務院 IIP《Telling the Story》中譯 | https://usinfo.org/zhtw/PUBS/Handbook_Journalism/telling.htm |
| 聯合報《新聞寫作通則》（行政院《文書處理手冊》附錄） | https://www.dgpa.gov.tw/uploads/public/Data/8111417263071.pdf（約 p. 96–108） |
| 彭家發《進階新聞寫作》 | ISBN 978-957-11-5106-9；https://www.wunan.com.tw/bookdetail?NO=9109 |
| 牛隆光《新聞採訪與寫作》 | 博客來 0010471383 |
| 莊克仁《圖解新聞學》（2024 第 2 版） | ISBN 978-626-343-319-9 |
| 劉明華等《新聞寫作教程》 | ISBN 978-7-300-03981-7 |
| 中央社投稿流程 | https://www.cna.com.tw/postwrite/process |
| 公視 PeoPo 使用規範 | https://www.peopo.org/events/about/P2-2.htm |
| 環境資訊中心編輯原則 | 調查未給 URL；本檔只在 §三 與 §四 5 引它做數字門檻的對照，不進 §五 公約數，維持未核對 |
| 教育部《重訂標點符號手冊》、行政院數字原則 | 見 `sources.md`（已核對） |

