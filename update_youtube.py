#!/usr/bin/env python3
"""
Génère 3 cartes vidéo individuelles dans assets/youtube/ (v1.svg, v2.svg, v3.svg),
chacune = 1 vidéo (miniature + bouton play + titre + date), cliquable.
Source : flux RSS YouTube (public, pas de clé API). Robuste : génère toujours les 3 SVG.
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


def build_card(v):
    """Une carte vidéo individuelle = 1 fichier SVG (288x230)."""
    W, IMG_H = 288, 162
    thumb = v.get("thumb", "")
    full = v["title"]
    line1, line2 = full, ""
    if len(full) > 32:
        words = full.split()
        l1 = ""
        for w in words:
            if len(l1) + len(w) + 1 <= 32:
                l1 = (l1 + " " + w).strip()
            else:
                break
        line1 = l1
        line2 = truncate(full[len(l1):].strip(), 32)
    line1, line2 = esc(line1), esc(line2)
    date = esc(v.get("date", ""))
    href = f"https://www.youtube.com/watch?v={v['vid']}" if v['vid'] else f"https://www.youtube.com/@{HANDLE}"
    cx, cy = W // 2, 16 + IMG_H // 2

    if thumb:
        img = (f'<image x="10" y="16" width="{W-20}" height="{IMG_H}" '
               f'preserveAspectRatio="xMidYMid slice" href="{thumb}"/>')
    else:
        img = f'<rect x="10" y="16" width="{W-20}" height="{IMG_H}" rx="10" fill="#1c2128"/>'

    return f'''<svg width="{W}" height="230" viewBox="0 0 {W} 230" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="{W-2}" height="228" rx="14" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="{W-2}" height="4" rx="2" fill="#ff0000"/>
  <a href="{href}">
    <clipPath id="c"><rect x="10" y="16" width="{W-20}" height="{IMG_H}" rx="10"/></clipPath>
    <g clip-path="url(#c)">{img}<rect x="10" y="16" width="{W-20}" height="{IMG_H}" fill="#000" fill-opacity="0.12"/></g>
    <circle cx="{cx}" cy="{cy}" r="24" fill="#ff0000" fill-opacity="0.9"/>
    <path d="M{cx-8} {cy-11} l16 11 l-16 11 z" fill="#ffffff"/>
    <text x="18" y="200" fill="#e6eaf2" font-size="13" font-weight="600">{line1}</text>
    <text x="18" y="218" fill="#e6eaf2" font-size="13" font-weight="600">{line2}</text>
  </a>
</svg>
'''


def placeholder_card(i):
    return build_card({"title": "Coming soon — new video", "vid": "", "date": "@" + HANDLE, "thumb": ""})


def main():
    os.makedirs("assets/youtube", exist_ok=True)
    videos = []
    try:
        cid = resolve_channel_id()
        if cid:
            videos = fetch_videos(cid, 3)
            for v in videos:
                v["thumb"] = thumb_data_uri(v["vid"])
    except Exception as e:
        print(f"Avertissement YouTube: {e}")

    # Toujours générer 3 cartes (vidéos réelles + placeholders si manquantes)
    for i in range(3):
        if i < len(videos):
            svg = build_card(videos[i])
        else:
            svg = placeholder_card(i)
        with open(f"assets/youtube/v{i+1}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"OK — 3 cartes vidéo générées ({len(videos)} réelles)")


if __name__ == "__main__":
    main()
