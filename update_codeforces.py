#!/usr/bin/env python3
"""
Génère assets/cp/codeforces.svg avec le vrai rating Codeforces (API publique).
"""
import os
import json
import urllib.request

HANDLE = "sidi_maadh"

# Codeforces rank -> couleur officielle
RANK_COLORS = {
    "newbie": "#808080",
    "pupil": "#008000",
    "specialist": "#03A89E",
    "expert": "#0000FF",
    "candidate master": "#AA00AA",
    "master": "#FF8C00",
    "international master": "#FF8C00",
    "grandmaster": "#FF0000",
    "international grandmaster": "#FF0000",
    "legendary grandmaster": "#FF0000",
}


def fetch():
    url = f"https://codeforces.com/api/user.info?handles={HANDLE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode())
    if data.get("status") != "OK":
        raise RuntimeError(data.get("comment", "API error"))
    u = data["result"][0]
    return {
        "rating": u.get("rating", 0),
        "maxRating": u.get("maxRating", 0),
        "rank": (u.get("rank") or "unrated").title(),
        "rankLower": (u.get("rank") or "unrated").lower(),
    }


def build_svg(info):
    color = "#1F8ACB"
    for key, c in RANK_COLORS.items():
        if key == info["rankLower"]:
            color = c
            break
    rank_label = info["rank"]
    # raccourcir si trop long
    display_rank = rank_label if len(rank_label) <= 12 else rank_label.split()[-1]
    return f'''<svg width="210" height="110" viewBox="0 0 210 110" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="208" height="108" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="208" height="4" rx="2" fill="{color}"/>
  <text x="20" y="34" fill="#8b93a7" font-size="12" font-weight="600" letter-spacing="0.5">Codeforces</text>
  <text x="20" y="66" fill="{color}" font-size="24" font-weight="700">{display_rank}</text>
  <text x="20" y="90" fill="#6b7280" font-size="13">Rating {info["rating"]} · max {info["maxRating"]}</text>
</svg>
'''


def main():
    info = fetch()
    svg = build_svg(info)
    os.makedirs("assets/cp", exist_ok=True)
    with open("assets/cp/codeforces.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — {info['rank']} (rating {info['rating']}, max {info['maxRating']}).")


if __name__ == "__main__":
    main()
