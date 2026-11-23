"""抓取網頁來源並存成 raw Markdown。

用法：
    python tools/fetch_web.py <url> --id S01 [--slug ja-wiki-wotagei]

- 維基百科：走 MediaWiki API（prop=extracts, explaintext），中文版強制 zh-tw 字形轉換。
  授權 CC BY-SA 4.0，全文存成 raw/web/S##-slug.md（可 commit）。
- 其他網站：用 trafilatura 擷取正文，全文存成 raw/web/S##-slug.private.md（不 commit），
  另外產生一個只有後設資料的 raw/web/S##-slug.md。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_WEB = ROOT / "raw" / "web"
UA = "wotagei-llm-wiki/0.1 (course project; python urllib)"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def wiki_fetch(url: str) -> dict:
    p = urllib.parse.urlparse(url)
    lang = p.netloc.split(".")[0]
    path = urllib.parse.unquote(p.path)
    m = re.match(r"^/(wiki|zh-tw|zh-hant|zh-cn|zh-hk|zh-hans)/(.+)$", path)
    if not m:
        raise SystemExit(f"無法解析維基百科網址：{url}")
    title = m.group(2)
    params = {
        "action": "query", "format": "json", "formatversion": "2",
        "prop": "extracts|info|revisions", "explaintext": "1",
        "exsectionformat": "wiki", "inprop": "url", "rvprop": "ids|timestamp",
        "redirects": "1", "titles": title,
    }
    if lang == "zh":
        params["variant"] = "zh-tw"
    api = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    data = json.loads(http_get(api))
    page = data["query"]["pages"][0]
    if page.get("missing"):
        raise SystemExit(f"維基百科找不到條目：{title}")
    rev = (page.get("revisions") or [{}])[0]
    text = page["extract"]
    # MediaWiki 的 == 標題 == 轉成 Markdown 標題
    def h(mm: re.Match) -> str:
        level = len(mm.group(1))
        return "#" * level + " " + mm.group(2).strip()
    text = re.sub(r"^(={2,6})\s*(.+?)\s*\1\s*$", h, text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return {
        "title": page["title"],
        "text": text,
        "lang": lang,
        "license": "CC BY-SA 4.0（Wikipedia）",
        "revision": f"{rev.get('revid')} @ {rev.get('timestamp')}",
        "canonical": page.get("fullurl", url),
        "private": False,
    }


def generic_fetch(url: str) -> dict:
    import trafilatura

    html = trafilatura.fetch_url(url)
    if not html:
        raise SystemExit("抓取失敗（可能需要 JS 或被擋）→ 請改用 chrome-devtools 擷取")
    text = trafilatura.extract(html, output_format="markdown", include_links=True,
                               include_tables=True, favor_recall=True)
    meta = trafilatura.extract_metadata(html)
    if not text or len(text) < 200:
        raise SystemExit("擷取到的正文太短 → 請改用 chrome-devtools 擷取")
    return {
        "title": (meta.title if meta and meta.title else url),
        "text": text,
        "lang": "",
        "license": "版權屬原作者（只留在本機，不 commit）",
        "revision": (meta.date if meta and meta.date else ""),
        "canonical": url,
        "private": True,
        "author": (meta.author if meta and meta.author else ""),
        "sitename": (meta.sitename if meta and meta.sitename else ""),
    }


def frontmatter(d: dict) -> str:
    lines = ["---"]
    for k, v in d.items():
        v = "" if v is None else str(v).replace("\n", " ")
        lines.append(f'{k}: "{v}"' if any(c in v for c in ":#[]{}") else f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--id", required=True, help="來源編號，例如 S01")
    ap.add_argument("--slug", help="檔名 slug，預設由網址推導")
    a = ap.parse_args()

    is_wiki = "wikipedia.org" in urllib.parse.urlparse(a.url).netloc
    info = wiki_fetch(a.url) if is_wiki else generic_fetch(a.url)
    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", urllib.parse.urlparse(a.url).netloc.lower()).strip("-")
    RAW_WEB.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    meta = {
        "source_id": a.id, "kind": "web", "title": info["title"], "url": a.url,
        "canonical_url": info["canonical"], "lang": info["lang"], "license": info["license"],
        "revision": info["revision"], "fetched": today, "fetched_by": "tools/fetch_web.py",
    }
    base = RAW_WEB / f"{a.id}-{slug}"
    if info["private"]:
        meta.update({"author": info.get("author", ""), "site": info.get("sitename", "")})
        full = Path(str(base) + ".private.md")
        full.write_text(frontmatter(meta) + f"\n\n# {info['title']}\n\n" + info["text"] + "\n", encoding="utf-8")
        stub = Path(str(base) + ".md")
        stub.write_text(frontmatter(meta) + "\n\n全文只保存在本機（" + full.name +
                        "），版權屬原作者。\n\n## 摘錄\n\n（ingest 時補上短引文）\n", encoding="utf-8")
        print(f"[private] {full.relative_to(ROOT)}\n[stub]    {stub.relative_to(ROOT)}")
    else:
        out = Path(str(base) + ".md")
        out.write_text(frontmatter(meta) + f"\n\n# {info['title']}\n\n" + info["text"] + "\n", encoding="utf-8")
        print(f"[saved] {out.relative_to(ROOT)}")
    print(f"字數：{len(info['text'])}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
