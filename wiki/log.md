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
