#!/usr/bin/env python3
"""
Génère assets/education.svg à partir du Google Sheet publié en CSV.
Le SHEET_CSV_URL est lu depuis une variable d'environnement (GitHub secret).
"""
import os
import csv
import io
import urllib.request
from datetime import date

SHEET_CSV_URL = os.environ.get("SHEET_CSV_URL", "")

BIRTH_DATE = date(2002, 1, 10)
LIFE_EXPECTANCY_YEARS = 63

PURPLE = "#8b5cf6"


def hm_to_minutes(h, m):
    try:
        h = int(float(h)) if h not in ("", None) else 0
    except (ValueError, TypeError):
        h = 0
    try:
        m = int(float(m)) if m not in ("", None) else 0
    except (ValueError, TypeError):
        m = 0
    return h * 60 + m


def fmt_hm(total_min):
    return f"{total_min // 60}h {total_min % 60:02d}m"


def fetch_rows():
    req = urllib.request.Request(SHEET_CSV_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    return list(csv.reader(io.StringIO(text)))


def parse(rows):
    """Extrait les sujets (col 0 = nom, col 1 = heures, col 2 = minutes)."""
    subjects = []
    for r in rows[1:]:
        if len(r) < 3:
            continue
        name = r[0].strip()
        if not name or name.upper().startswith("TOTAL"):
            continue
        mins = hm_to_minutes(r[1], r[2])
        if mins > 0:
            subjects.append((name, mins))
    subjects.sort(key=lambda x: -x[1])
    total = sum(m for _, m in subjects)
    return subjects, total


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(subjects, total):
    top = subjects[:5]
    maxv = top[0][1] if top else 1
    n_fields = len(subjects)
    top_name = top[0][0].split(" - ")[0].split(" (")[0] if top else "-"
    top_hours = f"{top[0][1] // 60}h" if top else "0h"
    goal_min = 1200 * 60
    pct_goal = round(total / goal_min * 100) if goal_min else 0

    bars = []
    y = 168
    for name, mins in top:
        w = max(8, round(820 * mins / maxv))
        short = name.split(" (")[0]
        if len(short) > 46:
            short = short[:44] + "…"
        bars.append(f'''  <text x="40" y="{y}" fill="#cfd6e4" font-size="13" font-weight="500">{esc(short)}</text>
  <text x="860" y="{y}" fill="#e6eaf2" font-size="12" font-weight="600" text-anchor="end">{fmt_hm(mins)}</text>
  <rect x="40" y="{y+6}" width="820" height="8" rx="4" fill="#161a21"/>
  <rect x="40" y="{y+6}" width="{w}" height="8" rx="4" fill="url(#barg)"/>''')
        y += 34

    today = date.today().isoformat()

    # --- Progress calculations ---
    today_d = date.today()
    year_start = date(today_d.year, 1, 1)
    days_passed = (today_d - year_start).days
    days_in_year = 366 if (today_d.year % 4 == 0 and (today_d.year % 100 != 0 or today_d.year % 400 == 0)) else 365
    days_remaining = days_in_year - days_passed
    year_pct = round(days_passed / days_in_year * 100)

    life_days = (today_d - BIRTH_DATE).days
    age_years = life_days // 365
    age_months = life_days // 30
    life_pct = round(age_years / LIFE_EXPECTANCY_YEARS * 100)

    circ = 201
    year_offset = round(circ * (1 - days_passed / days_in_year))
    life_offset = round(circ * (1 - age_years / LIFE_EXPECTANCY_YEARS))

    rings_y = y + 30
    svg_h = rings_y + 64 + 24

    return f'''<svg width="900" height="{svg_h}" viewBox="0 0 900 {svg_h}" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="ebg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="eacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
    <linearGradient id="barg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#6366f1"/></linearGradient>
  </defs>
  <rect width="900" height="{svg_h}" rx="16" fill="url(#ebg)"/>
  <rect x="0.5" y="0.5" width="899" height="{svg_h-1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  <text x="40" y="36" fill="#8b93a7" font-size="13">Daily hours logged across scientific &amp; practical fields — updated {today}.</text>
  <g transform="translate(40, 52)"><rect width="194" height="62" rx="12" fill="#13161c" stroke="#222831"/><text x="16" y="22" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.8">TOTAL STUDIED</text><text x="16" y="46" fill="#f0f3f9" font-size="22" font-weight="700">{total//60}<tspan font-size="13" fill="#8b93a7" font-weight="500">h {total%60:02d}m</tspan></text></g>
  <g transform="translate(246, 52)"><rect width="194" height="62" rx="12" fill="#13161c" stroke="#222831"/><text x="16" y="22" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.8">YEARLY GOAL</text><text x="16" y="46" fill="#f0f3f9" font-size="22" font-weight="700">1200<tspan font-size="13" fill="#8b93a7" font-weight="500">h · {pct_goal}%</tspan></text></g>
  <g transform="translate(452, 52)"><rect width="194" height="62" rx="12" fill="#13161c" stroke="#222831"/><text x="16" y="22" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.8">TOP SUBJECT</text><text x="16" y="44" fill="#f0f3f9" font-size="14" font-weight="700">{esc(top_name)}</text><text x="170" y="44" fill="#a78bfa" font-size="11" text-anchor="end">{top_hours}</text></g>
  <g transform="translate(658, 52)"><rect width="202" height="62" rx="12" fill="#13161c" stroke="#222831"/><text x="16" y="22" fill="#6b7280" font-size="10" font-weight="600" letter-spacing="0.8">FIELDS TRACKED</text><text x="16" y="46" fill="#f0f3f9" font-size="22" font-weight="700">{n_fields}<tspan font-size="13" fill="#8b93a7" font-weight="500"> active areas</tspan></text></g>
  <text x="40" y="146" fill="#6b7280" font-size="11" font-weight="600" letter-spacing="1">HOURS BY FIELD</text>
  <line x1="158" y1="168" x2="860" y2="168" stroke="#ffffff" stroke-opacity="0.06"/>
{chr(10).join(bars)}
  <line x1="40" y1="{y+12}" x2="860" y2="{y+12}" stroke="#ffffff" stroke-opacity="0.07"/>
  <g transform="translate(40, {rings_y})">
    <circle cx="32" cy="32" r="32" fill="none" stroke="#161a21" stroke-width="8"/>
    <circle cx="32" cy="32" r="32" fill="none" stroke="#8b5cf6" stroke-width="8" stroke-linecap="round" stroke-dasharray="{circ}" stroke-dashoffset="{year_offset}" transform="rotate(-90 32 32)"/>
    <text x="32" y="38" text-anchor="middle" fill="#f0f3f9" font-size="16" font-weight="700">{year_pct}%</text>
    <text x="82" y="28" fill="#e6eaf2" font-size="16" font-weight="600">Year Progress</text>
    <text x="82" y="50" fill="#8b93a7" font-size="13">{days_passed} days passed · {days_remaining} remaining</text>
  </g>
  <g transform="translate(470, {rings_y})">
    <circle cx="32" cy="32" r="32" fill="none" stroke="#161a21" stroke-width="8"/>
    <circle cx="32" cy="32" r="32" fill="none" stroke="#3b82f6" stroke-width="8" stroke-linecap="round" stroke-dasharray="{circ}" stroke-dashoffset="{life_offset}" transform="rotate(-90 32 32)"/>
    <text x="32" y="38" text-anchor="middle" fill="#f0f3f9" font-size="16" font-weight="700">{life_pct}%</text>
    <text x="82" y="28" fill="#e6eaf2" font-size="16" font-weight="600">Life Progress</text>
    <text x="82" y="50" fill="#8b93a7" font-size="13">{age_years} years · {age_months} months — keep building</text>
  </g>
</svg>
'''


def main():
    if not SHEET_CSV_URL:
        raise SystemExit("SHEET_CSV_URL manquant (configure le secret GitHub).")
    rows = fetch_rows()
    subjects, total = parse(rows)
    svg = build_svg(subjects, total)
    os.makedirs("assets", exist_ok=True)
    with open("assets/education.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — {len(subjects)} sujets, {fmt_hm(total)} au total.")


if __name__ == "__main__":
    main()
