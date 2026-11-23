# 御宅藝 LLM Wiki — Schema

本檔是這個 LLM Wiki 的「schema」：告訴 LLM（Claude Code）wiki 怎麼組織、頁面怎麼寫、
新增資料／查詢／健檢時要走哪些流程。設計依據 Karpathy 的 *LLM Wiki* pattern
（raw sources → wiki → schema 三層）。

- **主題**：御宅藝（ヲタ芸 / Wotagei）及其周邊文化 —— 地下偶像、地下藝、地上藝（表演藝）、
  MIX／CALL、螢光棒、技、流行曲結構與打法、厄介爭議。
- **語言**：一律以**繁體中文（台灣用語）**撰寫。日文原文、羅馬拼音只出現在 `glossary.md`、
  頁面 frontmatter 的 `aliases`，以及首次提到某詞時的括號註記，例如「家虎（イエッタイガー）」。
- **最終產出**：「御宅藝文化講座」120 分鐘社課的教學 HTML 簡報（`slides/`），內容必須可以追溯回 wiki。

---

## 1. 三層架構與目錄

```
raw/                 第一層：原始資料（不可修改，immutable）
  web/               網頁來源（S##-slug.md）
  youtube/           影片來源（S##-<videoId>.md 是公開的後設資料；.private.md 是逐字稿全文）
  inbox/             使用者手動丟進來、還沒處理的檔案
  discussion/        ingest 討論時使用者的補充與修正（原文照錄，只追加不修改）→ 對應來源 S00
  backlog.md         候選來源（還沒 ingest，或被剔除的，附原因）
wiki/                第二層：LLM 撰寫、維護的知識庫（LLM 全權負責）
  index.md           內容目錄：每頁一行（連結＋一句摘要），依分類排列
  log.md             依時間累加的操作紀錄（ingest / query / lint）
  overview.md        御宅藝總覽（新手入口頁）
  glossary.md        用語對照表 —— 全專案「標準寫法」的唯一依據
  sources/           每份來源的摘要頁（S##-slug.md）
  concepts/          概念：御宅藝、地下偶像、地下藝、地上藝、MIX、CALL、厄介…
  techniques/        技：各個打藝的動作
  gear/              道具：螢光棒（ケミカルライト、ペンライト…）
  music/             流行曲結構（前奏、Aメロ、Bメロ、サビ…）× 各段落的打法
  history/           年表、演變
  culture/           現場禮儀、爭議、各地的發展（台灣、日本）
  outputs/           query 的產出（簡報大綱、比較表、查核報告），寫回 wiki 累積
tools/               確定性工具腳本（Python，用 CLAUDE conda 環境執行）
checks/              每次檢查的報告（lint、slides check），是「檢查紀錄」的證據
slides/              教學 HTML 簡報
docs/                workflow.md（loop / graph 設計）、reflection.md（反思）
Assets/              簡報用的圖片素材
```

Python 一律用：`C:/Users/Hibiki/anaconda3/envs/CLAUDE/python.exe`（下文簡寫為 `$PY`）。

### 版權規則（repo 是公開的）
- 維基百科（CC BY-SA 4.0）：全文可以 commit，frontmatter 要註明授權與網址。
- 其他網站、YouTube 逐字稿：全文存成 `*.private.md`（已被 `.gitignore` 排除，只留在本機）；
  repo 中只 commit 後設資料檔（網址、標題、作者、日期），以及 ingest 時摘錄的**短引文**。

---

## 2. 頁面格式

### 檔名
- 路徑用英文或羅馬拼音的 kebab-case（例如 `techniques/romance.md`、`concepts/underground-idol.md`），
  方便 GitHub、Windows 與 URL 處理；中文標題寫在 frontmatter 的 `title`。
- 來源編號 `S01`、`S02`… 依 ingest 順序遞增，一旦給定就不再變動。
- **`S00` 是「使用者討論紀錄」**：使用者在討論時提供的圈內實務知識（沒有書面來源）。
  原文照錄在 `raw/discussion/discussion-notes.md`，wiki 引用時標 `[S00]`。
  S00 的說法與書面來源衝突時，**兩邊都保留**，用「⚠️ 說法分歧」並列，不擅自刪除。

### Frontmatter（每個 wiki 頁面都必須有，`index.md`、`log.md` 除外）
```yaml
---
title: 家虎
type: concept        # concept | technique | gear | music | history | culture | source | overview | glossary | output
aliases: [イエッタイガー, Yetta Tiger, 耶太嘎]
sources: [S04, S06]  # 這頁的內容依據哪些來源
updated: 2026-11-23
---
```

### 內文規則
1. **每個事實性陳述都要標出處**，格式是行內連結到來源摘要頁：`……（[S01](../sources/S01-ja-wiki-wotagei.md)）`。
   沒有出處的推論要明確寫「（整理者推論）」。
2. **頁面之間用相對路徑的標準 Markdown 連結**（不用 `[[wikilink]]`，因為 GitHub 不會渲染）。
3. **來源之間說法矛盾時，不要擅自選一個**：用 `> ⚠️ 說法分歧：` 區塊並列兩邊的說法和出處。
4. 用語一律採用 `glossary.md` 的「標準寫法」，不使用「不採用寫法」欄裡的寫法。
   例外：全形括號（…）裡的原文註記、`>` 引文區塊，不在此限。
5. 每頁開頭先用 1～2 句話白話說明「這是什麼」（給新手看），再展開細節。
6. 結尾放「相關頁面」清單（至少 1 個連結），避免孤兒頁。

### 來源摘要頁（`wiki/sources/S##-*.md`）
```markdown
---
title: S01 日文維基百科「ヲタ芸」
type: source
source_id: S01
source_kind: web | youtube
url: https://...
raw: ../../raw/web/S01-ja-wiki-wotagei.md
author: …          # 頻道或作者
published: …       # 已知的話填
fetched: 2026-11-23
reliability: 高 | 中 | 低   # 加上一句理由
sources: [S01]
updated: 2026-11-23
---
## 一句話摘要
## 重點（經使用者確認）
## 這份來源特別適合用來說明
## 可信度與限制
## 影響的 wiki 頁面
```

### glossary.md 表格欄位
`| 標準寫法 | 日文 | 羅馬拼音／英文 | 不採用寫法 | 說明 | 出處 |`
—— 「不採用寫法」欄以 `、` 分隔，`tools/lint_wiki.py` 會掃描 wiki 是否誤用這些寫法。

---

## 3. 工作流程（Operations）

### 3.1 Ingest（新增資料）—— 一次一份來源，每份都要停下來跟使用者討論
使用者說 `ingest <網址或檔案>` 時：

1. **判斷類型、抓取**（存進 raw/，之後不再修改）
   - 一般網頁／維基百科：`$PY tools/fetch_web.py <url> --id S##`
     - 維基百科會自動改用 MediaWiki API 取得乾淨的純文字（zh 一律用 `zh-tw` 字形轉換）。
     - 遇到需要 JS 或擋爬蟲的網站 → 改用 chrome-devtools MCP 打開頁面後擷取正文。
   - YouTube 影片：`$PY tools/fetch_youtube.py <url> --id S##`
     - 優先順序：作者上傳的字幕 > 自動字幕。**完全沒有字幕的影片先剔除**，
       記到 `raw/backlog.md` 並告知使用者（目前約定不做語音辨識）。
     - **規劃來源時**就對每一支候選影片跑一次 `--list`／字幕檢查，不要等到抓取時才發現（S06a 的教訓）。
   - YouTube 播放清單：`$PY tools/fetch_youtube.py <playlist-url> --list`，
     列出每支影片的字幕狀態，讓使用者挑選；同一主題的影片可以綁成一個來源編號（S##a、S##b…）。
   - 本機檔案：使用者放進 `raw/inbox/`，搬到 `raw/web/` 或 `raw/youtube/` 並補上 frontmatter。
2. **讀完整份來源**，逐字稿要特別注意自動字幕把圈內用語聽錯的情況（對照 glossary 修正，
   修正只寫在 wiki，raw 保持原樣）。
3. **🧑 停下來跟使用者討論**（「先討論、後生成」—— 這一步不可省略）：
   - 用條列呈現：一句話摘要、5～10 個重點、會新增或修改的 wiki 頁面清單、
     新出現的用語、與既有 wiki 矛盾的地方、可信度評估。
   - 等使用者確認或修正後，才進行下一步。
   - 使用者的修正或補充 → 原文追加到 `raw/discussion/discussion-notes.md`（標明是哪一次 ingest），並以 S00 引用。
   - **（檢查前移，見 docs/reflection.md）**「新出現的用語」要逐一對照 glossary 的「不採用寫法」欄，
     當場決定標準寫法；使用者的修正如果**推翻**了既有說法，要列出「會被推翻的舊說法」。
4. **寫入 wiki**：來源摘要頁 → 更新或新增主題頁 → 更新 `glossary.md` → 更新 `overview.md`（如果需要）。
   - 有被推翻的舊說法時，用 `grep` 找出全 wiki 所有出現的地方（**一定包含 overview.md**）一起改，
     並把 grep 的關鍵字與修改的頁面記到 log。
5. **✅ 檢查**：`$PY tools/lint_wiki.py`（報告會寫進 `checks/`）。有 error 就修正後重跑，直到通過為止。
6. **記帳**：更新 `index.md`，在 `log.md` 追加一筆紀錄，
   然後 `git commit -m "ingest: S## <標題>"`。

### 3.2 Query（查詢／產出）
1. 先讀 `wiki/index.md` 找出相關頁面，再進入那些頁面；**只根據 wiki 回答**，並附上 wiki 頁面連結。
2. wiki 資料不足時要明講「wiki 缺資料」，並建議要補哪份來源，不可以用模型自己的知識硬補。
3. 有價值的產出（大綱、比較表、分析）存到 `wiki/outputs/`，並更新 index 和 log。

### 3.3 Lint（健檢）
- 自動部分：`$PY tools/lint_wiki.py` —— 斷鏈、缺 frontmatter、缺出處、孤兒頁、
  沒列進 index 的頁面、誤用「不採用寫法」。
- LLM 部分（每 3～4 次 ingest，或做簡報前跑一次）：跨來源的矛盾、已經過時的說法、
  被提到卻沒有自己頁面的重要概念、資料缺口（要補什麼來源）。結果寫到 `checks/lint-llm-<日期>.md`。

### 3.4 簡報產出（Slides Graph）
1. 讀 `index.md` → 產出教學大綱，存到 `wiki/outputs/slides-outline.md` → **🧑 使用者審核大綱**。
2. 逐段撰寫投影片：每張投影片都要用 `data-sources="wiki/…md, …"` 標出依據的 wiki 頁。
3. **✅** `$PY tools/check_slides.py`：每張投影片都有出處、出處檔案存在、沒有用到不採用寫法。
4. **✅** LLM 事實查核：逐張比對投影片陳述與 wiki 頁 → 報告存到 `checks/`。
   - wiki 寫錯 → 修 wiki；wiki 缺資料 → 回到 Ingest 補來源；投影片寫錯 → 重寫該張。
5. **✅** 渲染檢查：用 chrome-devtools 打開，逐頁截圖，檢查文字溢出、圖片、影片能否嵌入播放。
6. commit → push → 打開 GitHub Pages 的線上網址確認。

---

## 4. log.md 格式
每筆以固定前綴開頭，方便用 `grep "^## \[" wiki/log.md` 解析：
```
## [2026-11-23 21:30] ingest | S01 日文維基百科「ヲタ芸」
- 新增：…；更新：…
- 討論修正：使用者指出…
- lint：通過（第 2 次；第 1 次的問題：…）
```
類型：`ingest` | `query` | `lint` | `slides` | `fix` | `schema`（修改本檔時要記一筆） | `docs`（docs/、README、入口頁）。
時間一律先執行 `date '+%Y-%m-%d %H:%M'` 取得，不可估計。

---

## 5. Git 與發布
- repo 根目錄就是本資料夾（`Project/`），遠端是 GitHub `wotagei-llm-wiki`，用 GitHub Pages 發布。
- 每一個操作單位 commit 一次。commit message 前綴：`ingest:`、`lint:`、`slides:`、`fix:`、`schema:`、`tools:`、`docs:`。
- 不要 commit `*.private.md`。
