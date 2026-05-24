#!/usr/bin/env python3
"""
Génère assets/cp/codeforces.svg avec les vraies stats Codeforces (API publique).
Si l'utilisateur a un rating -> affiche le rang. Sinon -> affiche les problèmes résolus.
"""
import os
import json
import urllib.request

HANDLE = "sidi_maadh"

RANK_COLORS = {
    "newbie": "#808080", "pupil": "#008000", "specialist": "#03A89E",
    "expert": "#0000FF", "candidate master": "#AA00AA", "master": "#FF8C00",
    "international master": "#FF8C00", "grandmaster": "#FF0000",
    "international grandmaster": "#FF0000", "legendary grandmaster": "#FF0000",
}


def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())


def fetch_info():
    data = api(f"https://codeforces.com/api/user.info?handles={HANDLE}")
    if data.get("status") != "OK":
        raise RuntimeError("user.info error")
    u = data["result"][0]
    return {
        "rating": u.get("rating", 0),
        "maxRating": u.get("maxRating", 0),
        "rank": (u.get("rank") or "").lower(),
    }


def fetch_solved():
    """Compte les problèmes uniques résolus (soumissions OK)."""
    data = api(f"https://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=10000")
    if data.get("status") != "OK":
        return 0
    solved = set()
    for sub in data["result"]:
        if sub.get("verdict") == "OK":
            p = sub.get("problem", {})
            key = f"{p.get('contestId')}-{p.get('index')}"
            solved.add(key)
    return len(solved)


def build_svg(mode, big, sub, color):
    return f'''<svg width="210" height="110" viewBox="0 0 210 110" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="208" height="108" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="208" height="4" rx="2" fill="{color}"/>
  <text x="20" y="34" fill="#8b93a7" font-size="12" font-weight="600" letter-spacing="0.5">Codeforces</text>
  <text x="20" y="66" fill="{color}" font-size="26" font-weight="700">{big}</text>
  <text x="20" y="90" fill="#6b7280" font-size="13">{sub}</text>
</svg>
'''


def main():
    color = "#1F8ACB"
    big, sub = "—", ""
    try:
        info = fetch_info()
        if info["rating"] and info["rank"]:
            # A un rating -> afficher le rang
            color = RANK_COLORS.get(info["rank"], "#1F8ACB")
            label = info["rank"].title()
            big = label if len(label) <= 12 else label.split()[-1]
            sub = f'Rating {info["rating"]} · max {info["maxRating"]}'
        else:
            # Unrated -> afficher les problèmes résolus
            solved = fetch_solved()
            big = f"{solved}+" if solved else "Active"
            sub = "Problems solved"
    except Exception as e:
        print(f"Avertissement Codeforces: {e}")
        big, sub = "Active", "Problems solved"

    svg = build_svg("", big, sub, color)
    os.makedirs("assets/cp", exist_ok=True)
    with open("assets/cp/codeforces.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — Codeforces: {big} ({sub})")


if __name__ == "__main__":
    main()
