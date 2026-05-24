#!/usr/bin/env python3
"""
Génère assets/projects.svg avec les 3 derniers repos mis à jour (API GitHub).
Affiche nom, description, langage principal, et étoiles.
GITHUB_TOKEN est fourni automatiquement par GitHub Actions.
"""
import os
import json
import urllib.request

USERNAME = "sidi-maadh"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Couleurs officielles des langages
LANG_COLORS = {
    "Python": "#3776ab", "Java": "#ed8b00", "C++": "#00599c", "C": "#555555",
    "JavaScript": "#f7df1e", "TypeScript": "#007acc", "HTML": "#e34c26",
    "CSS": "#563d7c", "Dart": "#02569b", "PHP": "#777bb4", "Jupyter Notebook": "#da5b0b",
    "Shell": "#89e051", "Go": "#00add8", "Rust": "#dea584", "Kotlin": "#a97bff",
}


def api(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "profile-stats",
        "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def fetch_repos():
    # Triés par date de push (activité récente), exclut les forks
    repos = api(f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=20")
    own = [r for r in repos if not r.get("fork")]
    return own[:3]


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, max_chars=44):
    text = text or "No description provided."
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
    if not lines:
        lines = [text[:max_chars]]
    if len(lines) == 2 and len(lines[1]) >= max_chars - 1:
        lines[1] = lines[1][:max_chars - 1] + "…"
    return lines


def card(repo, x):
    name = esc(repo.get("name", ""))
    if len(name) > 22:
        name = name[:21] + "…"
    desc_lines = wrap(repo.get("description"))
    lang = repo.get("language") or "—"
    lang_color = LANG_COLORS.get(lang, "#8b5cf6")
    stars = repo.get("stargazers_count", 0)

    desc_svg = ""
    dy = 56
    for ln in desc_lines:
        desc_svg += f'<text x="20" y="{dy}" fill="#8b93a7" font-size="12">{esc(ln)}</text>'
        dy += 18

    return f'''  <g transform="translate({x}, 64)">
    <rect width="272" height="120" rx="12" fill="#13161c" stroke="#222831"/>
    <rect x="0" y="0" width="272" height="4" rx="2" fill="{lang_color}"/>
    <path d="M16 24 a2 2 0 0 1 2 -2 h6 l2 2 h6 a2 2 0 0 1 2 2 v6 a2 2 0 0 1 -2 2 h-14 a2 2 0 0 1 -2 -2 z" fill="{lang_color}" fill-opacity="0.6"/>
    <text x="42" y="32" fill="#e6eaf2" font-size="14" font-weight="700">{name}</text>
    {desc_svg}
    <circle cx="22" cy="98" r="5" fill="{lang_color}"/>
    <text x="32" y="102" fill="#8b93a7" font-size="11">{esc(lang)}</text>
    <text x="252" y="102" fill="#fbbf24" font-size="11" text-anchor="end">★ {stars}</text>
  </g>'''


def build_svg(repos):
    cards = ""
    xs = [40, 324, 608]
    for repo, x in zip(repos, xs):
        cards += card(repo, x) + "\n"
    return f'''<svg width="900" height="210" viewBox="0 0 900 210" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="pacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="210" rx="16" fill="url(#pbg)"/>
  <rect x="0.5" y="0.5" width="899" height="209" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  <g transform="translate(40, 40)">
    <rect x="0" y="-14" width="4" height="20" rx="2" fill="url(#pacc)"/>
    <text x="16" y="2" fill="#f0f3f9" font-size="16" font-weight="700">Latest Projects</text>
    <text x="170" y="2" fill="#4b5263" font-size="13">// most recently updated</text>
  </g>
{cards}</svg>
'''


def main():
    repos = fetch_repos()
    svg = build_svg(repos)
    os.makedirs("assets", exist_ok=True)
    with open("assets/projects.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    # Sauvegarde les URLs pour les liens cliquables dans le README
    urls = [r.get("html_url", "") for r in repos]
    with open("assets/projects_urls.txt", "w") as f:
        f.write("\n".join(urls))
    print(f"OK — {len(repos)} projets: " + ", ".join(r.get("name", "") for r in repos))


if __name__ == "__main__":
    main()
