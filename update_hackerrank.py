#!/usr/bin/env python3
"""
Génère assets/cp/hackerrank.svg avec les badges HackerRank.
HackerRank expose un endpoint REST public pour les badges.
"""
import os
import json
import urllib.request

USERNAME = "sidi_maadh"


def fetch():
    url = f"https://www.hackerrank.com/rest/hackers/{USERNAME}/badges"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode())
    models = data.get("models", [])
    if not models:
        return None, 0
    # Badge avec le plus d'étoiles
    best = max(models, key=lambda m: m.get("stars", 0))
    total_badges = len(models)
    return best, total_badges


def build_svg(top_stars, badge_name, total):
    if top_stars >= 5:
        level, color = "Gold", "#FFD700"
    elif top_stars >= 3:
        level, color = "Silver", "#C0C0C0"
    elif top_stars >= 1:
        level, color = "Bronze", "#CD7F32"
    else:
        level, color = "Active", "#2EC866"
    sub = f"{total} badges earned" if total else "Problem solving"
    return f'''<svg width="210" height="110" viewBox="0 0 210 110" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="208" height="108" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="208" height="4" rx="2" fill="#2EC866"/>
  <text x="20" y="34" fill="#8b93a7" font-size="12" font-weight="600" letter-spacing="0.5">HackerRank</text>
  <text x="20" y="66" fill="#2EC866" font-size="26" font-weight="700">{level}</text>
  <text x="20" y="90" fill="#6b7280" font-size="13">{sub}</text>
</svg>
'''


def main():
    top_stars, total, badge_name = 0, 0, ""
    try:
        best, total = fetch()
        if best:
            top_stars = best.get("stars", 0)
            badge_name = best.get("badge_name", "")
    except Exception as e:
        print(f"Avertissement HackerRank: {e} — valeur par défaut.")
        top_stars, total = 5, 0
    svg = build_svg(top_stars, badge_name, total)
    os.makedirs("assets/cp", exist_ok=True)
    with open("assets/cp/hackerrank.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — HackerRank {top_stars}stars, {total} badges.")


if __name__ == "__main__":
    main()
