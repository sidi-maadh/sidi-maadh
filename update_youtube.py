#!/usr/bin/env python3
"""
Génère assets/youtube_latest.svg avec la dernière vidéo de la chaîne ChingueTech.
Utilise le flux RSS public de YouTube (aucune clé API requise).
"""
import os
import re
import html
import urllib.request

HANDLE = "ChingueTech"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", errors="replace")


def resolve_channel_id():
    page = get(f"https://www.youtube.com/@{HANDLE}")
    m = re.search(r'"channelId":"(UC[\w-]+)"', page) or re.search(r'channel/(UC[\w-]+)', page)
    if not m:
        raise RuntimeError("Channel ID introuvable")
    return m.group(1)


def latest_video(channel_id):
    feed = get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    # Premier <entry> = dernière vidéo
    entry = feed.split("<entry>", 2)
    block = entry[1] if len(entry) > 1 else feed
    vid = re.search(r"<yt:videoId>([\w-]+)</yt:videoId>", block)
    title = re.search(r"<title>(.*?)</title>", block)
    return (
        vid.group(1) if vid else "",
        html.unescape(title.group(1)) if title else "Latest video",
    )


def wrap(text, max_chars=42):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
        if len(lines) == 2:
            break
    if cur and len(lines) < 2:
        lines.append(cur)
    if len(lines) == 2 and len(" ".join(words)) > len(" ".join(lines)):
        lines[1] = lines[1][:max_chars - 1] + "…"
    return lines


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(video_id, title):
    lines = wrap(title)
    line_svg = ""
    ty = 62 if len(lines) == 2 else 70
    for ln in lines:
        line_svg += f'<text x="120" y="{ty}" fill="#e6eaf2" font-size="15" font-weight="600">{esc(ln)}</text>'
        ty += 22
    return f'''<svg width="900" height="150" viewBox="0 0 900 150" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="ytbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="ytacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="150" rx="16" fill="url(#ytbg)"/>
  <rect x="0.5" y="0.5" width="899" height="149" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  <g transform="translate(40, 40)">
    <rect x="0" y="-14" width="4" height="20" rx="2" fill="url(#ytacc)"/>
    <text x="16" y="2" fill="#f0f3f9" font-size="16" font-weight="700">Latest on YouTube</text>
    <text x="196" y="2" fill="#4b5263" font-size="13">// @ChingueTech</text>
  </g>
  <!-- thumbnail placeholder w/ play -->
  <rect x="40" y="56" width="64" height="64" rx="12" fill="#13161c" stroke="#222831"/>
  <circle cx="72" cy="88" r="18" fill="#a78bfa" fill-opacity="0.15"/>
  <path d="M67 80 l12 8 l-12 8 z" fill="#a78bfa"/>
  {line_svg}
  <text x="120" y="{ty + 4}" fill="#6b7280" font-size="12">▶ Watch now on ChingueTech</text>
</svg>
'''


def main():
    cid = resolve_channel_id()
    vid, title = latest_video(cid)
    svg = build_svg(vid, title)
    os.makedirs("assets", exist_ok=True)
    with open("assets/youtube_latest.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    # Sauvegarde l'ID vidéo pour le lien dans le README (optionnel)
    with open("assets/youtube_latest_id.txt", "w") as f:
        f.write(vid)
    print(f"OK — dernière vidéo: {title} ({vid})")


if __name__ == "__main__":
    main()
