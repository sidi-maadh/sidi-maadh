#!/usr/bin/env python3
"""
Génère des bannières de titre de section (SVG) cohérentes avec le thème.
Chaque bannière : barre d'accent verticale + titre + icône thématique à gauche.
"""
import os


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# Icône thématique par section (placée à translate(28,16), ~26x26)
ICONS = {
    "projects": '''<path d="M3 7 a2 2 0 0 1 2 -2 h6 l2.5 2.5 h7.5 a2 2 0 0 1 2 2 v11 a2 2 0 0 1 -2 2 h-23 a2 2 0 0 1 -2 -2 z" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linejoin="round"/>''',
    "community": '''<circle cx="9" cy="9" r="4" fill="none" stroke="#a78bfa" stroke-width="2"/><path d="M2 23 c0 -5 4 -8 7 -8 c3 0 7 3 7 8" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round"/><circle cx="19" cy="11" r="3" fill="none" stroke="#60a5fa" stroke-width="2"/><path d="M16 23 c0 -4 3 -6 5 -6" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round"/>''',
    "analytics": '''<rect x="2" y="14" width="5" height="10" rx="1.5" fill="#a78bfa"/><rect x="10" y="7" width="5" height="17" rx="1.5" fill="#60a5fa"/><rect x="18" y="2" width="5" height="22" rx="1.5" fill="#34d399"/>''',
    "competitive": '''<path d="M6 3 h13 v4 c0 4 -3 7 -6.5 7 S6 11 6 7 z M3 4 h3 v3 c0 1.5 -1.5 2 -3 2 z M19 4 h3 v2 c0 2 -1.5 2.5 -3 2.5 z M12.5 14 v4 M8 22 h9 l-1 -3 h-7 z" fill="none" stroke="#fbbf24" stroke-width="1.8" stroke-linejoin="round"/>''',
    "problem": '''<path d="M13 2 L23 8 V18 L13 24 L3 18 V8 Z" fill="none" stroke="#60a5fa" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 12 l3 3 l5 -6" stroke="#60a5fa" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    "cyber": '''<path d="M13 2 L23 5 V12 C23 19 18 23 13 25 C8 23 3 19 3 12 V5 Z" fill="none" stroke="#34d399" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 13 l3 3 l5 -6" stroke="#34d399" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    "ai": '''<rect x="6" y="8" width="14" height="12" rx="3" fill="none" stroke="#a78bfa" stroke-width="1.8"/><circle cx="10.5" cy="14" r="1.6" fill="#a78bfa"/><circle cx="15.5" cy="14" r="1.6" fill="#a78bfa"/><path d="M13 3 v5 M9 20 v3 M17 20 v3 M20 11 h3 M3 11 h3" stroke="#a78bfa" stroke-width="1.8" stroke-linecap="round"/><circle cx="13" cy="3" r="1.6" fill="#60a5fa"/>''',
    "snake": '''<path d="M3 8 q0 -5 5 -5 h6 q5 0 5 5 t-5 5 h-4 q-5 0 -5 5 t5 5 h8" fill="none" stroke="#34d399" stroke-width="2.2" stroke-linecap="round"/><circle cx="22" cy="23" r="2" fill="#34d399"/>''',
    "about": '''<circle cx="13" cy="9" r="5" fill="none" stroke="#a78bfa" stroke-width="2"/><path d="M3 24 c0 -6 5 -9 10 -9 c5 0 10 3 10 9" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round"/>''',
    "techstack": '''<path d="M9 7 l-6 6 l6 6 M17 7 l6 6 l-6 6 M14 4 l-3 18" stroke="#60a5fa" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    "certifications": '''<circle cx="13" cy="10" r="7" fill="none" stroke="#fbbf24" stroke-width="2"/><path d="M9 14 l-2 9 l6 -3 l6 3 l-2 -9" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linejoin="round"/><path d="M10 10 l2 2 l4 -4" stroke="#fbbf24" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    "education": '''<path d="M13 4 L24 10 L13 16 L2 10 Z" fill="none" stroke="#34d399" stroke-width="2" stroke-linejoin="round"/><path d="M7 12 v6 c0 2 12 2 12 0 v-6 M24 10 v7" stroke="#34d399" stroke-width="2" fill="none" stroke-linecap="round"/>''',
}


def banner(title, icon_key, accent="#8b5cf6"):
    icon = ICONS.get(icon_key, "")
    return f'''<svg width="900" height="64" viewBox="0 0 900 64" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#10131a"/><stop offset="1" stop-color="#0a0c10"/></linearGradient>
    <linearGradient id="hacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="64" rx="14" fill="url(#hbg)"/>
  <rect x="0.5" y="0.5" width="899" height="63" rx="14" fill="none" stroke="#ffffff" stroke-opacity="0.07"/>
  <rect x="0" y="0" width="5" height="64" rx="2.5" fill="url(#hacc)"/>
  <g transform="translate(28, 19)">{icon}</g>
  <text x="72" y="40" fill="#f0f3f9" font-size="21" font-weight="700" letter-spacing="-0.2">{esc(title)}</text>
</svg>
'''


SECTIONS = {
    "title_projects":    ("Latest Projects", "projects"),
    "title_community":   ("Community", "community"),
    "title_analytics":   ("GitHub Analytics", "analytics"),
    "title_competitive": ("Competitive Programming", "competitive"),
    "title_problem":     ("Problem Solving", "problem"),
    "title_cyber":       ("Cybersecurity", "cyber"),
    "title_ai":          ("Artificial Intelligence", "ai"),
    "title_snake":       ("Contribution Graph", "snake"),
    "title_about":          ("About", "about"),
    "title_techstack":      ("Tech Stack", "techstack"),
    "title_certifications": ("Certifications", "certifications"),
    "title_education":      ("Self Education", "education"),
}


def main():
    os.makedirs("assets/titles", exist_ok=True)
    for fname, (title, icon) in SECTIONS.items():
        with open(f"assets/titles/{fname}.svg", "w", encoding="utf-8") as f:
            f.write(banner(title, icon))
    print(f"OK — {len(SECTIONS)} bannières de titre générées")


if __name__ == "__main__":
    main()
