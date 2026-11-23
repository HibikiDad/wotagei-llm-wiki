# 操作紀錄（log）

> 依時間累加，只新增不修改。前綴格式：`## [YYYY-MM-DD HH:MM] 類型 | 標題`，類型為 ingest / query / lint / slides / fix / schema。
> 快速查看最近 5 筆：`grep "^## \[" wiki/log.md | tail -5`

## [2026-11-23 16:00] schema | 建立專案骨架與 CLAUDE.md
- 建立三層架構（raw / wiki / schema）、工具腳本 fetch_web.py、fetch_youtube.py、lint_wiki.py。
- 約定：沒有字幕的 YouTube 影片先剔除，記到 raw/backlog.md。

## [2026-11-23 16:10] schema | 新增 S00 討論紀錄來源、lint 排除括號註記
- CLAUDE.md：新增 raw/discussion/ 與 S00「使用者討論紀錄」；與書面來源衝突時兩邊並列。
- lint_wiki.py：E5 不檢查全形括號（…）內的原文註記。
- 起因：S01 討論時使用者提出與書面來源不同的三分類，需要可追溯的方式記錄圈內實務知識。

## [2026-11-23 16:10] ingest | S01 日文維基百科「オタ芸」
- 新增來源頁：S00、S01。
- 新增概念：御宅藝、一般應援、地下藝、表演藝、家虎。
- 新增技：地蔵、マワリ、ロマンス、PPPH、ケチャ、サンダースネイク、メリーゴーランド。
- 新增：年表、爭議與禁止、用語表、總覽。
- 討論修正：使用者指出「應援型 ≠ 地下藝」，改為三分法（一般應援／地下藝／表演藝），S01 的二分法以「⚠️ 說法分歧」並列；技名標準寫法用日文原名＋中文意譯。
- lint：通過（第 2 次）。第 1 次 3 個 E5：引述 S01 時直接寫日文「地下芸」而非「地下藝（地下芸）」。

## [2026-11-23 16:15] ingest | S02 中文維基百科「臺灣地下偶像文化」
- 新增：S02 來源頁、地下偶像、台灣的地下偶像與御宅藝圈。
- 更新：年表（加入 5 個台灣時間點）、地下藝（出現場合）、用語表（地下偶像、拼盤、ACG）、總覽、index。
- 討論修正：使用者補充「台灣地下藝大多出現在地下偶像應援場合」「地下藝的『地下』大概率與地下偶像有關（待證實）」→ 以 S00 引用。
- lint：一次通過。自我檢查：用語表「拼盤＝対バン」不在 S02 內，改標「整理者推論」。


## [2026-11-23 16:20] ingest | S03 中文維基百科「在地偶像」
- 新增：sources/S03-zh-wiki-local-idol.md、concepts/local-idol.md
- 更新：concepts/underground-idol.md（台灣定義、⚠️ 說法分歧：S03 視為同義 vs. 本 wiki 分兩頁）、concepts/chika-gei.md（整理者推論：為什麼要吸引表演者注意）、culture/taiwan.md、history/timeline.md（1993／1995／1996）、glossary.md（在地偶像、秋葉系）、sources/S00-discussion-notes.md（補 S02、S03 討論）、index.md
- 討論修正：使用者決定在地偶像與地下偶像分兩頁；同意寫入推論
- lint：通過（第 2 次；第 1 次 E5 ×3：glossary 把「秋葉原系」列為不採用，但改寫時照抄原文 → 改為「秋葉系（秋葉原系）」）

## [2026-11-23 16:23] ingest | S04a 日文維基百科「ケミカルライト」＋ S04b「ペンライト」
- 新增：sources/S04a-ja-wiki-chemical-light.md、sources/S04b-ja-wiki-penlight.md、gear/glowstick.md
- 更新：history/timeline.md（1974／1986／1996／2002／2010／2015）、concepts/performance-gei.md（サイリウムダンス名稱）、culture/controversies.md（化學螢光棒安全）、glossary.md（新增「道具」表）、overview.md、sources/S00-discussion-notes.md、index.md
- 討論修正：使用者補充台灣也叫 LED 螢光棒「手燈」、台灣以 LED 為主；決定合併成一頁
- lint：通過（第 1 次）

## [2026-11-23 16:31] ingest | S05 YouTube【EvolutioN】御宅藝文化詳細介紹
- 新增：sources/S05-K97ZqVhf-mA.md、techniques/sabi-waza.md；raw/youtube/S05-K97ZqVhf-mA.md 補上短引文與時間碼
- 更新：culture/taiwan.md（台灣御宅藝圈：團體地圖、風城界隈校園傳承、入坑理由 → 填掉資料缺口）、concepts/wotagei.md／general-support.md（打call）／chika-gei.md（通常不拿螢光棒、刷認知佐證推論）／performance-gei.md（光棒藝、基扭特戰隊 2009）／yetta-tiger.md、techniques/romance.md／thunder-snake.md（台灣中文叫法確認、⚠️ 分歧）、history/timeline.md、glossary.md、overview.md、index.md、S00
- 討論修正：地下藝通常不拿螢光棒；打call＝一般應援；十字架＝ロザリオ；基扭特戰隊為台灣通稱；小祈＝S07 的祈哥；S05 可信度高；S04 可信度回改為中
- lint：通過（第 1 次）

## [2026-11-23 16:45] ingest | S06b、S06c YouTube 無用男Rain MIX／家虎講座

- 來源：S06b yzX_SkMQAfw（2018 流行 MIX 大集合，英文字幕）、S06c dLfZSCgwyMY（發動 MIX＋家虎講座，繁中字幕）。S06a IgyO088HTH8 ingest 時才發現沒有字幕 → 剔除，記錄在 raw/backlog.md。
- 討論（S00）：使用者**修正 S05 討論時的結論**——打call 是總稱，一般應援與地下藝都包含在內；MIX 不是地下藝專有；地下藝的 call 是約定俗成、讓聲音大到被偶像注意的念法；「虎火三連」最常用，並提供 kknews 文章。
- 新增：concepts/call.md、concepts/mix.md、music/song-structure.md、sources/S06b、sources/S06c。
- 更新：general-support（移除「打call」別名）、wotagei、overview、glossary（打call／一般應援列修正；新增 MIX 相關用語與曲子段落表）、yetta-tiger（喊的時機）、chika-gei、index、S00。
- 重新編號：kknews 插入為 S07 → 祈哥改為 S08a-b、厄介改為 S09（各頁的「待 S0x」一併更新）。
- 檢查：第一次 lint E5 ×2（S06c 來源頁直接寫了不採用的「耶太嘎」「愛孥語」→ 改為放進（）原文註記），重跑通過。

## [2026-11-23 17:00] ingest | S07 kknews〈日式應援中mix，家虎，火虎，厄介都是什麼意思？〉

- 來源：使用者在 S06 討論時提供；trafilatura 直接抓取成功（全文 .private.md）。
- 新增：sources/S07、concepts/yakkai.md（厄介）。
- 更新：mix（三連MIX 喊詞表、8 拍、警報、虎火發動）、yetta-tiger（名稱由來、ファイボー ワイパー）、controversies（厄介段落，取代資料缺口）、chika-gei、overview、glossary（虎火發動、woo hey、Urya-Hi、厄介、阿伊努語列為不採用）、index、S00、S06c（喊詞疑點已解）。
- 討論修正：「虎火三連」＝一般三連MIX，與 S07 的「虎火發動」不同（整理者原本以為可能相同）；喊聲以羅馬音為標準；台灣喊家虎、打地下藝會被當成厄介；可信度由提議的低～中改為**高**。

- lint：第 1 次即通過。

## [2026-11-23 17:20] ingest | S08a、S08b YouTube 祈哥 Hong〈新手村入門〉主歌篇、導歌篇

- 來源：zGVnPOHCoRA（主歌，13:20）、HIsBsrt1bBw（導歌，8:26），皆為作者上傳繁中字幕。
- 新增：sources/S08a、S08b；techniques/oad、nihai-ohai、soya、yddjj、rosario、los-angeles（一技一頁）。
- 更新：music/song-structure（主歌／導歌打法表，移除資料缺口）、gear/glowstick（王劍／電棒／大閃光、折法、拿法 → 補上 S04 起的缺口）、performance-gei、sabi-waza、overview、glossary（技表、道具表）、index、S00；jizo 等 5 頁的「待 S08」改為「S08 沒有教到」。
- 討論修正：使用者把「演唱會用 LED、表演藝用化學棒」的推論修正為「通常」，並補上例外（地下偶像場常見化學棒、表演藝因成本改用電棒）與圈內叫法王劍／電棒；技名標準為日文原名（羅馬拼音），OAD 照寫。

- lint：第 1 次即通過。

## [2026-11-23 17:30] lint | LLM Lint Pass（簡報前）

- 報告：checks/lint-llm-20261123.md。
- 修正：glowstick（「台灣現場以 LED 為主」過度概括 → 限定演唱會；化學棒與地下藝不拿棒的關係加註）、general-support（過時的缺口說明、王劍）、timeline（補 2017-10、2018-12、2020-01）、5 個技頁的語句。
- 缺口：厄介日文定義（S09）、副歌技例子、NIHAIOHAI／SOYA／YDDJJ 日文原名等 → 簡報中標示。

## [2026-11-23 17:40] slides | 簡報大綱（Slides Graph 第 1 步）
- 新增：outputs/slides-outline.md（10 單元、33 張、120 分鐘；每張列出依據的 wiki 頁）
- 資料缺口在投影片中標示：厄介日文定義（S09）、副歌技例子、NIHAIOHAI／SOYA／YDDJJ 日文原名
- 狀態：等待使用者審核大綱

## [2026-11-23 18:10] ingest | S10a～S10d EvolutioN 官網（首頁、常見問題、比賽頁、台灣原創技）
- 抓取：使用者提供首頁，正文很短；Claude 列出子頁面，挑出 faq、competition、twotageiskill_cultureshock 一起 ingest（S09 預留給厄介，故用 S10）
- 新增：sources/S10a～S10d、techniques/taiwan-original-waza.md、culture/competitions.md
- 更新：wotagei（藝師、不等於螢光棒舞蹈）、chika-gei（同樂 vs 吸引注意 ⚠️ 分歧）、yakkai（台灣依場合分兩列）、performance-gei（技／技連／本家、拍光軌、比賽）、oad（站姿 ⚠️ 分歧）、rosario（4 拍×2＝八拍）、glowstick（品牌、15 分鐘、握法）、taiwan、timeline（2011 戰鬥哥改為確定年份、2017～2025 比賽與原創技）、song-structure、glossary（藝師、光棒藝、比賽、技、技連、本家、副手、台灣原創技）
- 討論修正：使用者補充ロザリオ是兩個 4 拍動作＝一個八拍；地下藝在 DJ 場、地下偶像場是同樂，在正經演唱會才會被當成厄介；藝師＝打師
- 順手修正：glowstick 頁殘留的錯誤引用「{Bb}」→ S08b；taiwan 頁「台灣現場以 LED 為主」→ 限定為演唱會（LLM lint 時漏改的同一句）
- lint：通過（第 1 次）

## [2026-11-23 18:20] ingest | S11a～S11c LUMICA 官網（商品一覧、化学発光体について、沿革）
- 抓取：使用者提供商品頁，正文很短；Claude 挑出 about_cl（化學發光原理、安全）與 history（沿革）一起 ingest；technology 頁與 about_cl 重複，未抓
- 新增：sources/S11a～S11c
- 更新：glowstick（化學棒原理「冷光」、保存、外漏處理、安全 ⚠️ 分歧、サイリューム銷售權、年表 1982／1993／2012／2018）、timeline（1982、2019 MAF展）、competitions（MAF展獲獎、LUMICA 贊助關係）、glossary（大閃光、冷光）、S00、index
- 討論修正：使用者確認台灣圈「大閃光」通常指化學棒；安全說法 S04a 與廠商並列；MAF展性質不明 → 照原文記錄
- lint：通過（第 1 次）

## [2026-11-23 18:25] slides | 簡報大綱依 S10、S11 修訂
- 更新：outputs/slides-outline.md（第 3、8、9、12、13、15、23、27、30、31、33 張；加入比賽與台灣原創技、化學棒原理與外漏處理、站姿與安全的 ⚠️ 分歧、地下藝看場合）
- 狀態：等待使用者審核大綱

## [2026-11-23 18:40] ingest | S09 萌娘百科「厄介」
- 抓取：正文很短；「典型例子」一節只抓到網站導覽框，不採用
- 新增：sources/S09
- 更新：yakkai（定義改為「行為」、⚠️ 指人／指行為分歧、非地下偶像系演唱會一列、厄介行為清單；移除「待補 S09」缺口，改為「仍缺日文來源」）、controversies、yetta-tiger、glowstick（丟棒子是厄介）、glossary、S00、index、backlog
- 討論修正：使用者表示厄介偏向指行為；S09 的行為清單台灣圈都認同；可信度低～中
- lint：通過（第 1 次）

## [2026-11-23 18:45] slides | 簡報大綱審核通過
- 更新：outputs/slides-outline.md —— 年表 10→6 分（3→2 張）、台灣圈 10→14 分（3→4 張，新增「台灣主要團體」）、第 28 張嵌入副歌篇影片、第 30～31 張依 S09 改寫
- 狀態：使用者審核通過 → 進入 Slides Graph 第 2 步（撰寫投影片）
