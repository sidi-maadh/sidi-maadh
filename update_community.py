#!/usr/bin/env python3
"""
Génère assets/community.svg à partir de l'API GitHub + committers.top.
Récupère followers, total stars, watchers, et rang committers.top.
GITHUB_TOKEN est fourni automatiquement par GitHub Actions.
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
    stars = 0
    watchers = 0
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
    """Récupère le rang committers.top (texte 'rank N' dans le SVG badge)."""
    try:
        url = f"https://user-badge.committers.top/{COUNTRY}/{USERNAME}.svg"
        req = urllib.request.Request(url, headers={"User-Agent": "profile-stats"})
        with urllib.request.urlopen(req, timeout=20) as r:
            svg = r.read().decode("utf-8", errors="replace")
        m = re.search(r"#?\s*(\d+)", svg)
        return m.group(1) if m else "—"
    except Exception:
        return "—"


def build_svg(followers, stars, watchers, rank):
    return f'''<svg width="900" height="150" viewBox="0 0 900 150" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="gacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="150" rx="16" fill="url(#gbg)"/>
  <rect x="0.5" y="0.5" width="899" height="149" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  <g transform="translate(40, 40)">
    <rect x="0" y="-14" width="4" height="20" rx="2" fill="url(#gacc)"/>
    <text x="16" y="2" fill="#f0f3f9" font-size="16" font-weight="700">Community</text>
    <text x="118" y="2" fill="#4b5263" font-size="13">// live from GitHub</text>
  </g>
  <g transform="translate(40, 64)">
    <rect width="194" height="56" rx="12" fill="#13161c" stroke="#222831"/>
    <circle cx="32" cy="28" r="15" fill="#8b5cf6" fill-opacity="0.15"/>
    <path d="M32 21 c-2.4 0 -4.3 1.9 -4.3 4.3 c0 1.7 1 3.1 2.4 3.8 c-2.9 1 -4.8 3.3 -4.8 6.2 l13.4 0 c0 -2.9 -1.9 -5.2 -4.8 -6.2 c1.4 -0.7 2.4 -2.1 2.4 -3.8 c0 -2.4 -1.9 -4.3 -4.3 -4.3 z" fill="#a78bfa"/>
    <text x="58" y="25" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.5">FOLLOWERS</text>
    <text x="58" y="44" fill="#f0f3f9" font-size="17" font-weight="700">{followers}</text>
  </g>
  <g transform="translate(244, 64)">
    <rect width="194" height="56" rx="12" fill="#13161c" stroke="#222831"/>
    <circle cx="32" cy="28" r="15" fill="#3b82f6" fill-opacity="0.15"/>
    <path d="M32 20 l2.5 5.3 l5.7 0.7 l-4.2 4 l1 5.7 l-5 -2.7 l-5 2.7 l1 -5.7 l-4.2 -4 l5.7 -0.7 z" fill="#60a5fa"/>
    <text x="58" y="25" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.5">STARS</text>
    <text x="58" y="44" fill="#f0f3f9" font-size="17" font-weight="700">{stars}</text>
  </g>
  <g transform="translate(448, 64)">
    <rect width="194" height="56" rx="12" fill="#13161c" stroke="#222831"/>
    <circle cx="32" cy="28" r="15" fill="#34d399" fill-opacity="0.15"/>
    <ellipse cx="32" cy="28" rx="8.5" ry="5.5" fill="none" stroke="#34d399" stroke-width="2"/>
    <circle cx="32" cy="28" r="2.6" fill="#34d399"/>
    <text x="58" y="25" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.5">WATCHERS</text>
    <text x="58" y="44" fill="#f0f3f9" font-size="17" font-weight="700">{watchers}</text>
  </g>
  <g transform="translate(652, 64)">
    <rect width="208" height="56" rx="12" fill="#13161c" stroke="#222831"/>
    <circle cx="32" cy="28" r="15" fill="#f59e0b" fill-opacity="0.15"/>
    <path d="M27 22 l10 0 l0 2.5 l2.2 0 l0 1.2 c0 2.4 -1.8 3.4 -3.4 3.6 c-0.6 1.4 -1.7 2.1 -2.8 2.4 l0 1.8 l2.5 0 l0 1.9 l-7 0 l0 -1.9 l2.5 0 l0 -1.8 c-1.1 -0.3 -2.2 -1 -2.8 -2.4 c-1.6 -0.2 -3.4 -1.2 -3.4 -3.6 l0 -1.2 l2.2 0 z M25 25.7 l0 1 c0 1.1 0.8 1.5 1.5 1.6 l0 -2.6 z M37 25.7 l0 2.6 c0.7 -0.1 1.5 -0.5 1.5 -1.6 l0 -1 z" fill="#fbbf24"/>
    <text x="58" y="25" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.5">COMMITTERS RANK</text>
    <text x="58" y="44" fill="#f0f3f9" font-size="15" font-weight="700">{COUNTRY_LABEL} <tspan fill="#fbbf24">#{rank}</tspan></text>
  </g>
</svg>
'''


def main():
    followers, stars, watchers = fetch_stats()
    rank = fetch_rank()
    svg = build_svg(followers, stars, watchers, rank)
    os.makedirs("assets", exist_ok=True)
    with open("assets/community.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — {followers} followers, {stars} stars, {watchers} watchers, rank #{rank}.")


if __name__ == "__main__":
    main()
