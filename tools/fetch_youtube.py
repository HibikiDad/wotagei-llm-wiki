"""抓取 YouTube 影片字幕，存成 raw Markdown。

用法：
    python tools/fetch_youtube.py <video-url> --id S05        # 單支影片
    python tools/fetch_youtube.py <playlist-url> --list       # 列出清單中每支影片的字幕狀態

字幕優先順序：作者上傳（zh-TW > zh-Hant > zh > ja > en > 其他）> 自動字幕（原語言 -orig > zh-TW > zh > ja）。
完全沒有字幕 → 以 exit code 2 結束（依 CLAUDE.md 約定：剔除並記到 raw/backlog.md）。

輸出：
    raw/youtube/S##-<videoId>.private.md   逐字稿全文（不 commit）
    raw/youtube/S##-<videoId>.md           後設資料＋影片說明＋章節（commit）
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_YT = ROOT / "raw" / "youtube"
YTDLP = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node", "--no-warnings"]

MANUAL_PREF = ["zh-TW", "zh-Hant", "zh", "zh-HK", "zh-Hans", "zh-CN", "ja", "en"]
AUTO_PREF = ["zh-TW", "zh-Hant", "zh", "ja", "en"]


def run(args: list[str]) -> str:
    r = subprocess.run(YTDLP + args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[-800:])
    return r.stdout


def info_of(url: str) -> dict:
    return json.loads(run(["-J", "--skip-download", url]))


def pick_track(info: dict) -> tuple[str, str] | None:
    """回傳 (kind, lang)；kind = manual | auto。"""
    subs = {k: v for k, v in (info.get("subtitles") or {}).items() if k != "live_chat"}
    for lang in MANUAL_PREF:
        if lang in subs:
            return "manual", lang
    if subs:
        return "manual", next(iter(subs))
    auto = info.get("automatic_captions") or {}
    orig = [k for k in auto if k.endswith("-orig")]
    if orig:
        return "auto", orig[0]
    for lang in AUTO_PREF:
        if lang in auto:
            return "auto", lang
    return None


def ts(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 3600:d}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if sec >= 3600 else f"{sec // 60:02d}:{sec % 60:02d}"


def parse_vtt(text: str, para_seconds: int = 30) -> str:
    """把 VTT 轉成每段約 30 秒、附時間碼的純文字；去掉自動字幕的滾動重複行。"""
    cue_re = re.compile(r"(\d+):(\d{2}):(\d{2})\.(\d{3})\s+-->")
    paras: list[tuple[float, list[str]]] = []
    last_line = ""
    start = None
    for block in re.split(r"\n\s*\n", text.replace("\r", "")):
        lines = block.strip().split("\n")
        idx = next((i for i, l in enumerate(lines) if cue_re.search(l)), None)
        if idx is None:
            continue
        m = cue_re.search(lines[idx])
        t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        for raw in lines[idx + 1:]:
            line = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
            if not line or line == last_line:
                continue
            last_line = line
            if start is None or t - start >= para_seconds:
                start = t
                paras.append((t, []))
            paras[-1][1].append(line)
    return "\n\n".join(f"[{ts(t)}] " + " ".join(ls) for t, ls in paras)


def fm(d: dict) -> str:
    out = ["---"]
    for k, v in d.items():
        v = "" if v is None else str(v).replace("\n", " ")
        out.append(f'{k}: "{v}"' if any(c in v for c in ":#[]{}\"") and not v.startswith('"') else f"{k}: {v}")
    out.append("---")
    return "\n".join(out)


def fetch_one(url: str, sid: str) -> int:
    info = info_of(url)
    vid = info["id"]
    track = pick_track(info)
    if not track:
        print(f"[no-subs] {vid} {info.get('title')} —— 沒有任何字幕，依約定剔除。")
        return 2
    kind, lang = track
    with tempfile.TemporaryDirectory() as td:
        flag = "--write-subs" if kind == "manual" else "--write-auto-subs"
        run(["--skip-download", flag, "--sub-langs", lang, "--sub-format", "vtt",
             "-o", str(Path(td) / "%(id)s.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"])
        vtts = list(Path(td).glob("*.vtt"))
        if not vtts:
            print(f"[error] 字幕下載失敗：{vid} {kind}:{lang}")
            return 1
        transcript = parse_vtt(vtts[0].read_text(encoding="utf-8"))

    up = info.get("upload_date") or ""
    meta = {
        "source_id": sid, "kind": "youtube", "title": info.get("title"),
        "url": f"https://www.youtube.com/watch?v={vid}", "video_id": vid,
        "channel": info.get("channel") or info.get("uploader"),
        "published": f"{up[:4]}-{up[4:6]}-{up[6:]}" if len(up) == 8 else up,
        "duration": info.get("duration_string"), "subtitle": f"{kind}:{lang}",
        "license": "版權屬原作者（逐字稿全文只留在本機）",
        "fetched": dt.date.today().isoformat(), "fetched_by": "tools/fetch_youtube.py",
    }
    RAW_YT.mkdir(parents=True, exist_ok=True)
    base = RAW_YT / f"{sid}-{vid}"
    priv = Path(str(base) + ".private.md")
    priv.write_text(fm(meta) + f"\n\n# {info.get('title')}\n\n> 字幕來源：{kind}:{lang}"
                    "（自動字幕可能把圈內用語聽錯，引用前請對照 wiki/glossary.md）\n\n"
                    + transcript + "\n", encoding="utf-8")
    chapters = info.get("chapters") or []
    chap_md = "\n".join(f"- [{ts(c['start_time'])}] {c['title']}" for c in chapters) or "（無）"
    desc = (info.get("description") or "").strip() or "（無）"
    pub = Path(str(base) + ".md")
    pub.write_text(fm(meta) + f"\n\n# {info.get('title')}\n\n逐字稿全文只保存在本機（`{priv.name}`），版權屬原作者。\n\n"
                   f"## 影片說明\n\n{desc}\n\n## 章節\n\n{chap_md}\n\n## 摘錄\n\n（ingest 時補上短引文與時間碼）\n",
                   encoding="utf-8")
    print(f"[ok] {vid} {kind}:{lang} 段落數={transcript.count(chr(10)*2)+1} 字數={len(transcript)}")
    print(f"     {priv.relative_to(ROOT)}\n     {pub.relative_to(ROOT)}")
    return 0


def list_playlist(url: str) -> None:
    out = run(["--flat-playlist", "--print", "%(id)s\t%(title)s", url])
    for line in out.strip().splitlines():
        vid, title = line.split("\t", 1)
        try:
            t = pick_track(info_of(f"https://www.youtube.com/watch?v={vid}"))
            status = f"{t[0]}:{t[1]}" if t else "無字幕（剔除）"
        except RuntimeError as e:
            status = "無法存取：" + str(e).splitlines()[-1][:60]
        print(f"{vid}\t{status}\t{title}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--id", help="來源編號，例如 S05 或 S06a")
    ap.add_argument("--list", action="store_true", help="播放清單模式：只列出字幕狀態")
    a = ap.parse_args()
    if a.list:
        list_playlist(a.url)
        return 0
    if not a.id:
        ap.error("單支影片需要 --id")
    return fetch_one(a.url, a.id)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
