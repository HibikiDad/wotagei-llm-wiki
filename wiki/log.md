# 操作紀錄（log）

> 依時間累加，只新增不修改。前綴格式：`## [YYYY-MM-DD HH:MM] 類型 | 標題`，類型為 ingest / query / lint / slides / fix / schema。
> 快速查看最近 5 筆：`grep "^## \[" wiki/log.md | tail -5`

## [2026-11-23 16:00] schema | 建立專案骨架與 CLAUDE.md
- 建立三層架構（raw / wiki / schema）、工具腳本 fetch_web.py、fetch_youtube.py、lint_wiki.py。
- 約定：沒有字幕的 YouTube 影片先剔除，記到 raw/backlog.md。

