"""簡報的確定性檢查（Slides Graph 第 3 步）。

用法：$PY tools/check_slides.py [slides/index.html]

檢查項目
- S1 每張投影片（section.slide）都有 data-sources
- S2 data-sources 列出的檔案都存在
- S3 投影片文字沒有用到 glossary 的「不採用寫法」
       （例外：class="ja" 的日文原文、全形括號（…）裡的原文註記 —— 與 lint_wiki 的 E5 規則一致）
- S4 <img src> 指向的圖片都存在
- S5 嵌入的 YouTube 影片都有對應的來源頁（wiki/sources/）或列在 raw/backlog.md（無字幕、只作視覺示範）
報告寫到 checks/slides-check-<時間>.md；有 error 時回傳 1。
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_wiki import ROOT, CHECKS, glossary_variants  # noqa: E402

VOID = {"img", "br", "hr", "meta", "link", "input", "source", "wbr"}


class Slide:
    def __init__(self, idx: int, sources: str | None):
        self.idx = idx
        self.sources = sources
        self.text: list[str] = []      # 一般文字（要掃描不採用寫法）
        self.imgs: list[str] = []
        self.videos: list[str] = []
        self.title = ""


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides: list[Slide] = []
        self.cur: Slide | None = None
        self.depth = 0            # 在 slide 內的巢狀深度
        self.ja_depth = 0         # 在 class="ja" 元素內
        self.stack: list[tuple[str, bool]] = []
        self.in_h2 = False
        self.skip = 0             # script/style

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
            return
        cls = (a.get("class") or "").split()
        if tag == "section" and "slide" in cls:
            self.cur = Slide(len(self.slides) + 1, a.get("data-sources"))
            self.slides.append(self.cur)
            self.depth = 0
        if self.cur is None:
            return
        if tag == "img" and a.get("src"):
            self.cur.imgs.append(a["src"])
        if a.get("data-id") and "yt" in cls:
            self.cur.videos.append(a["data-id"])
        if tag in VOID:
            return
        is_ja = "ja" in cls or (a.get("lang") or "").startswith("ja")
        self.stack.append((tag, is_ja))
        self.ja_depth += is_ja
        self.depth += 1
        if tag == "h2":
            self.in_h2 = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
            return
        if self.cur is None or tag in VOID:
            return
        if self.stack:
            t, is_ja = self.stack.pop()
            self.ja_depth -= is_ja
        self.depth -= 1
        if tag == "h2":
            self.in_h2 = False
        if self.depth <= 0 and tag == "section":
            self.cur = None

    def handle_data(self, data):
        if self.cur is None or self.skip:
            return
        if self.in_h2 and not self.cur.title:
            self.cur.title = data.strip()
        if self.ja_depth == 0:
            self.cur.text.append(data)


def main() -> int:
    target = (Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "slides" / "index.html").resolve()
    html = target.read_text(encoding="utf-8")
    p = Parser()
    p.feed(html)
    variants = glossary_variants()
    backlog = (ROOT / "raw" / "backlog.md").read_text(encoding="utf-8")
    source_pages = "\n".join(f.read_text(encoding="utf-8") for f in (ROOT / "wiki" / "sources").glob("*.md"))

    errors, warns, rows = [], [], []
    for s in p.slides:
        label = f"#{s.idx}「{s.title or '（封面）'}」"
        srcs = [x.strip() for x in (s.sources or "").split(",") if x.strip()]
        if not srcs:
            errors.append(f"S1 {label} 沒有 data-sources")
        for x in srcs:
            if not (ROOT / x).is_file():
                errors.append(f"S2 {label} 出處不存在：`{x}`")
        text = "".join(s.text)
        text_wo_paren = re.sub(r"（[^（）]*）", "", text)
        for bad, std in variants.items():
            if bad in text_wo_paren:
                errors.append(f"S3 {label} 用了不採用寫法「{bad}」→ 應為「{std}」")
        for src in s.imgs:
            if src.startswith(("http:", "https:", "data:")):
                continue
            if not (target.parent / src).is_file():
                errors.append(f"S4 {label} 圖片不存在：`{src}`")
        for vid in s.videos:
            in_src = vid in source_pages
            in_backlog = vid in backlog
            if not (in_src or in_backlog):
                errors.append(f"S5 {label} 影片 {vid} 沒有來源頁，也不在 backlog")
            elif not in_src:
                warns.append(f"S5 {label} 影片 {vid} 只在 backlog（未 ingest）→ 只能當視覺示範，內容不可寫進投影片")
        rows.append(f"| {s.idx} | {s.title or '（封面）'} | {len(srcs)} | {', '.join(s.videos) or '—'} |")

    now = dt.datetime.now()
    ok = not errors
    report = [
        "---", f"title: 簡報檢查 {now:%Y-%m-%d %H:%M}", "type: check", "---", "",
        f"# 簡報檢查（tools/check_slides.py）", "",
        f"- 檔案：`{target.relative_to(ROOT).as_posix()}`",
        f"- 結果：**{'✅ PASS' if ok else '❌ FAIL'}**",
        f"- 投影片數：{len(p.slides)}",
        f"- Error：{len(errors)}　Warning：{len(warns)}",
        f"- 掃描的不採用寫法：{len(variants)} 個", "",
        "## Errors", "", *(f"- {e}" for e in errors or ["（無）"]), "",
        "## Warnings", "", *(f"- {w}" for w in warns or ["（無）"]), "",
        "## 每張投影片", "", "| # | 標題 | 出處數 | 影片 |", "|---|---|---|---|", *rows, "",
    ]
    CHECKS.mkdir(exist_ok=True)
    out = CHECKS / f"slides-check-{now:%Y%m%d-%H%M%S}.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report[6:12]))
    for e in errors:
        print("  ", e)
    for w in warns:
        print("  ", w)
    print(f"報告：{out.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
