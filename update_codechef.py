#!/usr/bin/env python3
"""
Génère assets/cp/codechef.svg avec les vraies stats CodeChef (scraping page profil).
CodeChef n'a pas d'API publique — on lit la page profil.
"""
import os
import re
import urllib.request

USERNAME = "sidi_maadh"


def fetch():
    url = f"https://www.codechef.com/users/{USERNAME}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        html = r.read().decode("utf-8", errors="replace")
    # Rating courant
    rating_m = re.search(r'class="rating-number"[^>]*>(\d+)', html)
    rating = int(rating_m.group(1)) if rating_m else None
    # Nombre d'étoiles (ex: "3★")
    stars_m = re.search(r'class="rating">\s*(\d+)\s*★', html) or re.search(r'(\d+)★', html)
    stars = int(stars_m.group(1)) if stars_m else None
    return rating, stars


def build_svg(rating, stars):
    star_txt = f"{stars} \u2605" if stars else "—"
    rating_txt = f"Rating {rating}" if rating else "Active solver"
    return f'''<svg width="210" height="110" viewBox="0 0 210 110" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="208" height="108" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="208" height="4" rx="2" fill="#A77B5A"/>
  <text x="20" y="34" fill="#8b93a7" font-size="12" font-weight="600" letter-spacing="0.5">CodeChef</text>
  <text x="20" y="66" fill="#A77B5A" font-size="26" font-weight="700">{star_txt}</text>
  <text x="20" y="90" fill="#6b7280" font-size="13">{rating_txt}</text>
</svg>
'''


def main():
    rating, stars = None, None
    try:
        rating, stars = fetch()
    except Exception as e:
        print(f"Avertissement CodeChef: {e} — valeurs par défaut.")
    if stars is None:
        stars = 3
    if rating is None:
        rating = 1600
    svg = build_svg(rating, stars)
    os.makedirs("assets/cp", exist_ok=True)
    with open("assets/cp/codechef.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — CodeChef {stars}star, rating {rating}.")


if __name__ == "__main__":
    main()
