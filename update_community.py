#!/usr/bin/env python3
"""
Génère 4 cartes individuelles cliquables dans assets/community/ :
followers, stars, watchers, committers rank.
GITHUB_TOKEN fourni automatiquement par GitHub Actions.
"""
import os
import re
import json
import urllib.request

USERNAME = "sidi-maadh"
COUNTRY = "mauritania"
COUNTRY_LABEL = "Mauritania"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "profile-stats",
        "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def fetch_stats():
    user = api(f"https://api.github.com/users/{USERNAME}")
    followers = user.get("followers", 0)
    stars = watchers = 0
    page = 1
    while True:
        repos = api(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}")
        if not repos:
            break
        for repo in repos:
            stars += repo.get("stargazers_count", 0)
            watchers += repo.get("watchers_count", 0)
        if len(repos) < 100:
            break
        page += 1
    return followers, stars, watchers


def fetch_rank():
    try:
        url = f"https://user-badge.committers.top/{COUNTRY}/{USERNAME}.svg"
        req = urllib.request.Request(url, headers={"User-Agent": "profile-stats"})
        with urllib.request.urlopen(req, timeout=20) as r:
            svg = r.read().decode("utf-8", errors="replace")
        m = re.search(r"#?\s*(\d+)", svg)
        return m.group(1) if m else "—"
    except Exception:
        return "—"


def card(label, value, color, icon_svg, width=210):
    return f'''<svg width="{width}" height="80" viewBox="0 0 {width} 80" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="{width-2}" height="78" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="{width-2}" height="4" rx="2" fill="{color}"/>
  <circle cx="30" cy="44" r="16" fill="{color}" fill-opacity="0.15"/>
  {icon_svg}
  <text x="56" y="36" fill="#8b93a7" font-size="11" font-weight="600" letter-spacing="0.5">{label}</text>
  <text x="56" y="58" fill="#f0f3f9" font-size="20" font-weight="700">{value}</text>
</svg>
'''


def main():
    try:
        followers, stars, watchers = fetch_stats()
    except Exception as e:
        print(f"Avertissement stats: {e}")
        followers, stars, watchers = 0, 0, 0
    rank = fetch_rank()

    os.makedirs("assets/community", exist_ok=True)

    icons = {
        "followers": '<path d="M30 36 c-3 0 -5.4 2.4 -5.4 5.4 c0 2.1 1.2 4 3 4.8 c-3.6 1.2 -6 4.2 -6 7.8 l16.8 0 c0 -3.6 -2.4 -6.6 -6 -7.8 c1.8 -0.9 3 -2.7 3 -4.8 c0 -3 -2.4 -5.4 -5.4 -5.4 z" fill="#a78bfa"/>',
        "stars": '<path d="M30 34 l3.1 6.7 l7.2 0.8 l-5.3 5 l1.3 7.2 l-6.3 -3.4 l-6.3 3.4 l1.3 -7.2 l-5.3 -5 l7.2 -0.8 z" fill="#60a5fa"/>',
        "watchers": '<ellipse cx="30" cy="44" rx="11" ry="7" fill="none" stroke="#34d399" stroke-width="2"/><circle cx="30" cy="44" r="3.5" fill="#34d399"/>',
        "rank": '<path d="M22 36 l16 0 l0 4 l3 0 l0 2 c0 4 -3 5.5 -5.2 5.8 c-0.9 2.2 -2.6 3.4 -4.3 3.7 l0 2.5 l3.5 0 l0 2.8 l-10 0 l0 -2.8 l3.5 0 l0 -2.5 c-1.7 -0.3 -3.4 -1.5 -4.3 -3.7 c-2.2 -0.3 -5.2 -1.8 -5.2 -5.8 l0 -2 l3 0 z" fill="#fbbf24"/>',
    }

    cards = {
        "followers": card("FOLLOWERS", str(followers), "#8b5cf6", icons["followers"]),
        "stars": card("STARS EARNED", str(stars), "#3b82f6", icons["stars"]),
        "watchers": card("WATCHERS", str(watchers), "#34d399", icons["watchers"]),
        "rank": card("COMMITTERS RANK", f"{COUNTRY_LABEL} #{rank}", "#f59e0b", icons["rank"], width=270),
    }
    for name, svg in cards.items():
        with open(f"assets/community/{name}.svg", "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"OK — {followers} followers, {stars} stars, {watchers} watchers, rank #{rank}")


if __name__ == "__main__":
    main()
