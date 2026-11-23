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
