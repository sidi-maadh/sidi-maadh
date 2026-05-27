#!/usr/bin/env python3
"""
Génère assets/youtube_latest.svg : carte large 900px avec les 3 dernières
vidéos de la chaîne (miniature + titre + date + bouton play).
Source : flux RSS YouTube (public, pas de clé API). Robuste : génère toujours un SVG.
"""
import os
import re
import html
import urllib.request
import base64
from datetime import datetime

HANDLE = "SidiMaadh"
FALLBACK_CHANNEL_ID = ""  # format UCxxxx si la résolution auto échoue


def get(url, timeout=25, binary=False):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode("utf-8", errors="replace")


def resolve_channel_id():
    if FALLBACK_CHANNEL_ID:
        return FALLBACK_CHANNEL_ID
    for url in (f"https://www.youtube.com/@{HANDLE}",
                f"https://www.youtube.com/c/{HANDLE}",
                f"https://www.youtube.com/{HANDLE}"):
        try:
            page = get(url)
            m = re.search(r'"channelId":"(UC[\w-]{22})"', page) or \
                re.search(r'channel/(UC[\w-]{22})', page)
            if m:
                return m.group(1)
        except Exception:
            continue
    return ""


def fetch_videos(channel_id, n=3):
    rss = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    xml = get(rss)
    videos = []
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    for e in entries[:n]:
        vid_m = re.search(r"<yt:videoId>([\w-]+)</yt:videoId>", e)
        title_m = re.search(r"<title>(.*?)</title>", e, re.DOTALL)
        date_m = re.search(r"<published>(.*?)</published>", e)
        if not vid_m:
            continue
        vid = vid_m.group(1)
        title = html.unescape(title_m.group(1).strip()) if title_m else "Untitled"
        date = ""
        if date_m:
            try:
                dt = datetime.fromisoformat(date_m.group(1).replace("Z", "+00:00"))
                date = dt.strftime("%b %d, %Y")
            except Exception:
                date = ""
        videos.append({"title": title, "vid": vid, "date": date})
    return videos


def thumb_data_uri(vid):
    for quality in ("mqdefault", "hqdefault", "default"):
        try:
            data = get(f"https://i.ytimg.com/vi/{vid}/{quality}.jpg", binary=True)
            if data and len(data) > 1000:
                b64 = base64.b64encode(data).decode()
                return f"data:image/jpeg;base64,{b64}"
        except Exception:
            continue
    return ""


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def truncate(s, n):
    return s if len(s) <= n else s[:n - 1] + "…"


def video_block(v, x):
    W = 270
    thumb = v.get("thumb", "")
    full = v["title"]
    line1, line2 = full, ""
    if len(full) > 30:
        words = full.split()
        l1 = ""
        for w in words:
            if len(l1) + len(w) + 1 <= 30:
                l1 = (l1 + " " + w).strip()
            else:
                break
        line1 = l1
        line2 = truncate(full[len(l1):].strip(), 30)
    line1, line2 = esc(line1), esc(line2)
    date = esc(v.get("date", ""))

    if thumb:
        img = (f'<image x="{x}" y="20" width="{W}" height="152" '
               f'preserveAspectRatio="xMidYMid slice" href="{thumb}"/>')
    else:
        img = f'<rect x="{x}" y="20" width="{W}" height="152" rx="10" fill="#1c2128"/>'

    href = f"https://www.youtube.com/watch?v={v['vid']}" if v['vid'] else f"https://www.youtube.com/@{HANDLE}"
    cx = x + W // 2
    return f'''
  <a href="{href}">
  <clipPath id="clip{x}"><rect x="{x}" y="20" width="{W}" height="152" rx="10"/></clipPath>
  <g clip-path="url(#clip{x})">{img}<rect x="{x}" y="20" width="{W}" height="152" fill="#000" fill-opacity="0.12"/></g>
  <circle cx="{cx}" cy="96" r="22" fill="#000000" fill-opacity="0.55"/>
  <path d="M{cx - 7} 86 l14 10 l-14 10 z" fill="#ffffff"/>
  <text x="{x}" y="196" fill="#e6eaf2" font-size="13" font-weight="600">{line1}</text>
  <text x="{x}" y="214" fill="#e6eaf2" font-size="13" font-weight="600">{line2}</text>
  <text x="{x}" y="234" fill="#6b7280" font-size="11">{date}</text>
  </a>'''


def build_svg(videos):
    blocks = ""
    positions = [40, 320, 600]
    for i, v in enumerate(videos[:3]):
        blocks += video_block(v, positions[i])
    return f'''<svg width="900" height="260" viewBox="0 0 900 260" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="ytbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
  </defs>
  <rect width="900" height="260" rx="16" fill="url(#ytbg)"/>
  <rect x="0.5" y="0.5" width="899" height="259" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
{blocks}
</svg>
'''


def placeholder():
    vids = [{"title": "Visit my YouTube channel", "vid": "", "date": "@" + HANDLE, "thumb": ""} for _ in range(3)]
    return build_svg(vids)


def main():
    os.makedirs("assets", exist_ok=True)
    try:
        cid = resolve_channel_id()
        if not cid:
            raise RuntimeError("channel id introuvable")
        videos = fetch_videos(cid, 3)
        if not videos:
            raise RuntimeError("aucune vidéo")
        for v in videos:
            v["thumb"] = thumb_data_uri(v["vid"])
        svg = build_svg(videos)
        print(f"OK — {len(videos)} vidéos YouTube récupérées")
    except Exception as e:
        print(f"Avertissement YouTube: {e} — carte par défaut.")
        svg = placeholder()
    with open("assets/youtube_latest.svg", "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
