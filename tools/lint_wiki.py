"""Wiki 健檢（確定性的檢查）。報告寫到 checks/lint-<時間>.md；有 error 時 exit code 為 1。

檢查項目：
  E1 缺 frontmatter 或必要欄位（title / type / sources / updated）
  E2 斷鏈（相對路徑的 Markdown 連結指向不存在的檔案）
  E3 缺出處（內文沒有任何連結指向 sources/S##；output 類型的頁面可以改為連結到其他 wiki 頁）
  E4 沒有列在 index.md
  E5 使用了 glossary「不採用寫法」（引文區塊 >、行內程式碼、全形括號（…）內的原文註記不檢查）
  E6 frontmatter 的 sources 寫了不存在的來源編號
  W1 孤兒頁（除了 index.md 之外，沒有任何頁面連到它）
  W2 沒有「相關頁面」段落
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
CHECKS = ROOT / "checks"
SPECIAL = {"index.md", "log.md"}
REQUIRED = ["title", "type", "sources", "updated"]
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def parse_fm(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def body_of(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            return text[end + 4:]
    return text


def glossary_variants() -> dict[str, str]:
    """回傳 {不採用寫法: 標準寫法}。"""
    g = WIKI / "glossary.md"
    if not g.exists():
        return {}
    header, out = None, {}
    for line in g.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            header = None if not line.strip() else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "標準寫法" in cells and "不採用寫法" in cells:
            header = {name: i for i, name in enumerate(cells)}
            continue
        if not header or set("".join(cells)) <= set("-: "):
            continue
        std = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cells[header["標準寫法"]]).strip("* ")
        bad = cells[header["不採用寫法"]] if header["不採用寫法"] < len(cells) else ""
        for v in re.split(r"[、,，/]", bad):
            v = v.strip()
            if v and v not in ("—", "-", "（無）", "無"):
                out[v] = std
    return out


def main() -> int:
    pages = sorted(p for p in WIKI.rglob("*.md"))
    rel = {p: p.relative_to(WIKI).as_posix() for p in pages}
    texts = {p: p.read_text(encoding="utf-8") for p in pages}
    source_ids = set()
    for p in pages:
        m = re.match(r"(S\d+[a-z]?)-", p.name)
        if p.parent.name == "sources" and m:
            source_ids.add(m.group(1))

    errors: list[str] = []
    warns: list[str] = []
    inbound: dict[Path, set[Path]] = defaultdict(set)
    variants = glossary_variants()

    for p in pages:
        name = rel[p]
        text = texts[p]
        body = body_of(text)
        # 連結
        for _, target in LINK_RE.findall(body):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            tpath = (p.parent / target.split("#")[0]).resolve()
            if not tpath.exists():
                errors.append(f"E2 斷鏈：`{name}` → `{target}`")
            elif tpath.suffix == ".md" and WIKI in tpath.parents and tpath != p.resolve():
                inbound[tpath].add(p)
        if p.name in SPECIAL:
            continue
        fm = parse_fm(text)
        if fm is None:
            errors.append(f"E1 缺 frontmatter：`{name}`")
            fm = {}
        else:
            for k in REQUIRED:
                if not fm.get(k):
                    errors.append(f"E1 frontmatter 缺 `{k}`：`{name}`")
            for sid in re.findall(r"S\d+[a-z]?", fm.get("sources", "")):
                if sid not in source_ids:
                    errors.append(f"E6 frontmatter 引用不存在的來源 {sid}：`{name}`")
        cites_source = re.search(r"\]\([^)]*sources/S\d+[a-z]?-[^)]*\)", body) or (
            p.parent.name == "sources")
        cites_wiki = fm.get("type") == "output" and LINK_RE.search(body)
        if not (cites_source or cites_wiki):
            errors.append(f"E3 缺出處（沒有連到任何 sources/S## 頁）：`{name}`")
        if "相關頁面" not in body and p.name != "glossary.md":
            warns.append(f"W2 沒有「相關頁面」段落：`{name}`")
        # 用語
        if p.name != "glossary.md":
            for ln, line in enumerate(body.splitlines(), 1):
                if line.lstrip().startswith(">"):
                    continue
                clean = re.sub(r"`[^`]*`", "", line)
                clean = re.sub(r"\]\([^)]*\)", "]", clean)  # 不檢查連結網址
                clean = re.sub(r"（[^）]*）", "", clean)  # 不檢查括號內的原文註記
                for bad, std in variants.items():
                    if bad in clean:
                        errors.append(f"E5 用語：`{name}` 第 {ln} 行用了「{bad}」→ 應為「{std}」")

    index_text = texts.get(WIKI / "index.md", "")
    index_links = {(WIKI / t.split("#")[0]).resolve() for _, t in LINK_RE.findall(index_text)}
    for p in pages:
        if p.name in SPECIAL:
            continue
        if p.resolve() not in index_links:
            errors.append(f"E4 未列入 index.md：`{rel[p]}`")
        others = {q for q in inbound.get(p.resolve(), set()) if q.name not in SPECIAL}
        if not others and p.name not in ("overview.md", "glossary.md"):
            warns.append(f"W1 孤兒頁（只有 index 連到它）：`{rel[p]}`")

    now = dt.datetime.now()
    CHECKS.mkdir(exist_ok=True)
    report = CHECKS / f"lint-{now:%Y%m%d-%H%M%S}.md"
    status = "❌ FAIL" if errors else "✅ PASS"
    lines = [f"# Lint 報告 {now:%Y-%m-%d %H:%M:%S}", "",
             f"- 結果：**{status}**", f"- 頁面數：{len(pages)}（來源 {len(source_ids)} 份）",
             f"- Error：{len(errors)}　Warning：{len(warns)}", f"- glossary 不採用寫法：{len(variants)} 個", ""]
    lines += ["## Errors", ""] + ([f"- {e}" for e in errors] or ["（無）"]) + [""]
    lines += ["## Warnings", ""] + ([f"- {w}" for w in warns] or ["（無）"]) + [""]
    report.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"報告：{report.relative_to(ROOT).as_posix()}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
