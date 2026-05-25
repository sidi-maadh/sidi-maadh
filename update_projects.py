#!/usr/bin/env python3
"""
Génère 3 cartes projet individuelles cliquables dans assets/projects/.
Récupère les 3 repos les plus récemment mis à jour (API GitHub).
Écrit aussi assets/projects/urls.txt avec les liens (pour le README).
"""
import os
import json
import urllib.request

USERNAME = "sidi-maadh"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

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
    repos = api(f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=20")
    own = [r for r in repos if not r.get("fork")]
    return own[:3]


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, max_chars=40):
    text = text or "No description provided."
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
        if len(lines) == 2:
            break
    if cur and len(lines) < 2:
        lines.append(cur)
    if not lines:
        lines = [text[:max_chars]]
    if len(lines) == 2 and len(lines[1]) >= max_chars - 1:
        lines[1] = lines[1][:max_chars - 1] + "…"
    return lines


def card(repo):
    name = esc(repo.get("name", ""))
    if len(name) > 24:
        name = name[:23] + "…"
    desc_lines = wrap(repo.get("description"))
    lang = repo.get("language") or "—"
    lang_color = LANG_COLORS.get(lang, "#8b5cf6")
    stars = repo.get("stargazers_count", 0)

    desc_svg = ""
    dy = 60
    for ln in desc_lines:
        desc_svg += f'<text x="20" y="{dy}" fill="#8b93a7" font-size="12">{esc(ln)}</text>'
        dy += 18

    return f'''<svg width="288" height="130" viewBox="0 0 288 130" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="286" height="128" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="286" height="4" rx="2" fill="{lang_color}"/>
  <path d="M20 30 a2 2 0 0 1 2 -2 h7 l2 2 h7 a2 2 0 0 1 2 2 v7 a2 2 0 0 1 -2 2 h-16 a2 2 0 0 1 -2 -2 z" fill="{lang_color}" fill-opacity="0.6"/>
  <text x="48" y="38" fill="#e6eaf2" font-size="14" font-weight="700">{name}</text>
  {desc_svg}
  <circle cx="24" cy="108" r="5" fill="{lang_color}"/>
  <text x="34" y="112" fill="#8b93a7" font-size="11">{esc(lang)}</text>
  <text x="268" y="112" fill="#fbbf24" font-size="11" text-anchor="end">★ {stars}</text>
</svg>
'''


def main():
    try:
        repos = fetch_repos()
    except Exception as e:
        print(f"Avertissement projets: {e}")
        repos = []
    os.makedirs("assets/projects", exist_ok=True)
    urls = []
    for i, repo in enumerate(repos, 1):
        with open(f"assets/projects/p{i}.svg", "w", encoding="utf-8") as f:
            f.write(card(repo))
        urls.append(repo.get("html_url", ""))
    with open("assets/projects/urls.txt", "w") as f:
        f.write("\n".join(urls))
    print(f"OK — {len(repos)} projets: " + ", ".join(r.get("name", "") for r in repos))


if __name__ == "__main__":
    main()
