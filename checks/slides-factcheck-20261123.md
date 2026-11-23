---
title: 簡報事實查核 2026-11-23
type: check
---

# 簡報事實查核（Slides Graph 第 4 步，LLM）

- 對象：`slides/index.html`（33 張）
- 方法：逐張列出投影片上的具體陳述（年份、數字、時間碼、技的動作與拍數、分類、名稱），
  用 `grep` 回到該張 `data-sources` 列出的 wiki 頁找對應句子，再看那句的行內出處。
  對不上的分成三類處理（依 CLAUDE.md §3.4）：
  **投影片寫錯 → 重寫該張；wiki 寫錯／漏寫 → 修 wiki；wiki 缺資料 → 回 Ingest 或標成資料缺口**。
- 結果：**查核約 120 條陳述，找到 5 個問題，全部已處理**；修正後 `check_slides.py` 與 `lint_wiki.py` 都 PASS。

## 發現的問題與處理

| # | 張 | 問題 | 類型 | 處理 |
|---|---|---|---|---|
| 1 | 3 | 「御宅藝不一定要拿螢光棒、不限於肢體動作」只寫在來源頁 `sources/S10b`，主題頁 `concepts/wotagei.md` 雖然 frontmatter 列了 S10b，內文卻沒有這句；投影片另外加了「口號、應援都算在內」，S10b 原文沒有這樣說 | wiki 漏寫＋投影片過度延伸 | wotagei.md 補上 S10b 的 FAQ 說明；投影片刪掉「口號、應援都算在內」 |
| 2 | 20 | 「在台灣，喊家虎會被當成厄介」來自 S07 討論；之後 S10 討論補充「地下藝在 DJ 場、地下偶像場是同樂」，但 `concepts/yetta-tiger.md` 沒有跟著更新，和第 30 張（場合表）互相矛盾 | wiki 過時 | yetta-tiger.md 加上 ⚠️ 資料缺口（家虎是否依場合而定未確認，整理者推論很可能一樣）；投影片同步改寫 |
| 3 | 28 | 把ロマンス列為「副歌技舉例」，但 `techniques/sabi-waza.md` 與 `romance.md` 都把它歸為**定番**動作；「應援、表演兩邊都有人打」在 wiki 是整理者推論，投影片沒標 | 投影片寫錯 | 改成「另一個定番動作ロマンス」，並標「（整理者推論）」 |
| 4 | 29 | 爭議年表順序錯：2017-08 排在 2015 前面 | 投影片寫錯 | 調整為 2008 → 2015 → 2017-08 → 2020-02-02 |
| 5 | 29 | 「2015 AKB48 禁止帶入化學螢光棒」出自 `gear/glowstick.md`，但該張 `data-sources` 只列 `culture/controversies.md` | 出處不完整 | data-sources 補上 `wiki/gear/glowstick.md` |

> 第 5 項是 `check_slides.py` 抓不到的：它只檢查列出的檔案存不存在，不知道陳述實際來自哪一頁。

## 逐單元查核結果（摘要）

| 單元 | 張 | 對照的 wiki 頁 | 結果 |
|---|---|---|---|
| 0 開場 | 1–2 | overview、slides-outline | ✅（時間配置與大綱一致：合計 120 分） |
| 1 御宅藝是什麼 | 3–6 | wotagei、general-support、chika-gei、performance-gei、call、mix、S05 | 3 張 ⚠️→已修（#1）；S05 時間碼 00:33／01:06／01:38 ✅；三分法 vs 二分法分歧 ✅ |
| 2 從哪裡來 | 7–8 | timeline、romance、competitions、taiwan | ✅ 1989／2002／2006／2009／2014／2017／2018／2004／2011（400 萬）／2019～2020 都對得上 |
| 3 地下偶像與台灣圈 | 9–12 | underground-idol、local-idol、taiwan、competitions、taiwan-original-waza | ✅ 45～50 組、近 200 人、約 1,000 場；團體地圖；風城界隈 2018-08 → 2020-01；評分比例 30/30/20/10/10、40/40/10/10；初心幻刃本家 |
| 4 螢光棒 | 13–15 | glowstick、controversies、yakkai | ✅ 6～8 小時、酸化液＋蛍光液、15 分鐘以內、三種握法、經銷商備註；S04a vs 廠商分歧 ✅ |
| 5 曲子結構 | 16–17 | song-structure、mix、yetta-tiger | ✅ 段落定義、各段落喊／打什麼 |
| 6 打call | 18–21 | mix、yetta-tiger、S06c | 20 張 ⚠️→已修（#2）；woo hey 約四次／20 次、まだいかない、三連MIX 21 個詞、2020-02-02 ✅；S06c 時間碼 00:30／01:01／02:27／03:49 ✅ |
| 7 技：實作 | 23–28 | oad、nihai-ohai、soya、yddjj、rosario、los-angeles、sabi-waza、thunder-snake、romance | 28 張 ⚠️→已修（#3）；站姿分歧、OAD 第 1 拍開始第 2 拍擊掌、ロザリオ 4 拍×2、ロサンゼルス 8 拍、S08a 12:00 ✅ |
| 8 禮儀與厄介 | 29–31 | controversies、yakkai、chika-gei、glowstick | 29 張 ⚠️→已修（#4、#5）；S09 行為清單、場合表、指人／指行為分歧 ✅ |
| 9 總結 | 32–33 | overview、index | ✅ 資料缺口清單與 wiki 的 ⚠️ 資料缺口一致 |

## 刻意保留、不算錯誤的地方

- 第 19 張三連MIX 的羅馬音是整理者依日文轉寫，投影片上已註明。
- 第 28 張的副歌篇影片（7pO0AbJWxlE）沒有字幕、沒有 ingest，只當視覺示範；投影片沒有引用它的任何內容（`check_slides.py` S5 warning）。
- 第 31 張檢查表是依 wiki 事實整理的清單，已標「整理者整理」。

## 修正後的檢查

- `tools/lint_wiki.py`：PASS（W1：outputs/slides-outline.md 孤兒頁，可接受）
- `tools/check_slides.py`：PASS（S5 warning 1 個，如上）
