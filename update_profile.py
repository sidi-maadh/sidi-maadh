#!/usr/bin/env python3
"""
Régénère assets/header.svg, assets/about.svg, assets/techstack.svg
à partir de profile.json. Édite profile.json — pas les SVG.
"""
import os
import json


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ───────────────────────── HEADER ─────────────────────────
def build_header(h):
    meta = h.get("meta", [])
    meta_svg = ""
    x = 0
    for i, m in enumerate(meta):
        meta_svg += f'<text x="{x}" y="12">{esc(m)}</text>'
        # avancer selon la longueur réelle du texte (approx) + marge
        x += int(len(m) * 7.2) + 28
        if i < len(meta) - 1:
            meta_svg += f'<text x="{x-18}" y="12" fill="#4b5263">|</text>'
    return f'''<svg width="900" height="240" viewBox="0 0 900 240" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8b5cf6"/><stop offset="0.5" stop-color="#6366f1"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
    <radialGradient id="glow" cx="0.85" cy="0.2" r="0.6"><stop offset="0" stop-color="#6366f1" stop-opacity="0.18"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0 L0 0 0 30" fill="none" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/></pattern>
  </defs>
  <rect width="900" height="240" rx="16" fill="url(#hbg)"/>
  <rect width="900" height="240" rx="16" fill="url(#grid)"/>
  <rect width="900" height="240" rx="16" fill="url(#glow)"/>
  <rect x="0.5" y="0.5" width="899" height="239" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  <rect x="0" y="0" width="900" height="3" rx="1.5" fill="url(#accent)"/>
  <g transform="translate(56, 50)">
    <rect width="220" height="28" rx="14" fill="#8b5cf6" fill-opacity="0.12" stroke="#8b5cf6" stroke-opacity="0.35"/>
    <circle cx="18" cy="14" r="4" fill="#34d399"/>
    <circle cx="18" cy="14" r="4" fill="#34d399" opacity="0.4"><animate attributeName="r" values="4;8;4" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.4;0;0.4" dur="2s" repeatCount="indefinite"/></circle>
    <text x="32" y="19" fill="#c4b5fd" font-size="12" font-weight="600" letter-spacing="0.3">{esc(h.get("availability",""))}</text>
  </g>
  <text x="56" y="120" fill="#f0f3f9" font-size="38" font-weight="700" letter-spacing="-0.5">{esc(h.get("name",""))}</text>
  <text x="57" y="152" fill="#8b93a7" font-size="17" font-weight="400">
    <tspan fill="#a78bfa" font-weight="600">{esc(h.get("role_accent",""))}</tspan>
    <tspan fill="#4b5263"> · </tspan>
    <tspan>{esc(h.get("role_rest",""))}</tspan>
  </text>
  <g transform="translate(56, 184)" font-size="13" fill="#6b7280">{meta_svg}</g>
  <g transform="translate(744, 70)">
    <rect width="100" height="100" rx="22" fill="#16191f" stroke="#8b5cf6" stroke-opacity="0.3" stroke-width="1.5"/>
    <rect x="14" y="14" width="72" height="72" rx="14" fill="url(#accent)" fill-opacity="0.12"/>
    <text x="50" y="64" text-anchor="middle" fill="url(#accent)" font-size="40" font-weight="700">{esc(h.get("monogram","SM"))}</text>
  </g>
</svg>
'''


# ───────────────────────── ABOUT ─────────────────────────
def build_about(a):
    summary = a.get("summary", [])
    sum_svg = ""
    sy = 0
    for ln in summary:
        sum_svg += f'<tspan x="40" dy="{sy}">{esc(ln)}</tspan>'
        sy = 24
    return f'''<svg width="900" height="290" viewBox="0 0 900 290" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="abg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="aacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="290" rx="16" fill="url(#abg)"/>
  <rect x="0.5" y="0.5" width="899" height="289" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
  <text x="40" y="52" fill="#aab2c5" font-size="14" font-weight="400">{sum_svg}</text>
  <line x1="40" y1="120" x2="860" y2="120" stroke="#ffffff" stroke-opacity="0.07"/>
  <g transform="translate(40, 140)">
    <text x="0" y="0" fill="#6b7280" font-size="11" font-weight="600" letter-spacing="1">FOCUS</text>
    <text x="0" y="22" fill="#e6eaf2" font-size="14" font-weight="500">{esc(a.get("focus",""))}</text>
  </g>
  <g transform="translate(480, 140)">
    <text x="0" y="0" fill="#6b7280" font-size="11" font-weight="600" letter-spacing="1">AI SKILLS</text>
    <text x="0" y="22" fill="#e6eaf2" font-size="14" font-weight="500">{esc(a.get("ai_skills",""))}</text>
  </g>
  <g transform="translate(40, 192)">
    <text x="0" y="0" fill="#6b7280" font-size="11" font-weight="600" letter-spacing="1">ALGORITHMS</text>
    <text x="0" y="22" fill="#e6eaf2" font-size="14" font-weight="500">{esc(a.get("algorithms",""))}</text>
  </g>
  <g transform="translate(480, 192)">
    <text x="0" y="0" fill="#6b7280" font-size="11" font-weight="600" letter-spacing="1">CURRENTLY</text>
    <text x="0" y="22" fill="#e6eaf2" font-size="14" font-weight="500">Building <tspan fill="#a78bfa">{esc(a.get("currently",""))}</tspan></text>
  </g>
  <g transform="translate(40, 238)">
    <rect width="820" height="34" rx="10" fill="#8b5cf6" fill-opacity="0.08" stroke="#8b5cf6" stroke-opacity="0.2"/>
    <text x="16" y="22" fill="#6b7280" font-size="12" font-weight="600" letter-spacing="0.5">SEEKING</text>
    <text x="92" y="22" fill="#c4b5fd" font-size="13" font-weight="500">{esc(a.get("seeking",""))}</text>
  </g>
</svg>
'''


# ───────────────────────── TECH STACK ─────────────────────────
def text_width(s):
    # estimation grossière de largeur en px pour police 12
    return len(s) * 7.0


def build_techstack(ts):
    cat_colors = ["#a78bfa", "#60a5fa", "#34d399", "#fbbf24", "#f472b6"]
    body = ""
    y = 40
    for idx, (cat, chips) in enumerate(ts.items()):
        color = cat_colors[idx % len(cat_colors)]
        label_w = text_width(cat) + 10
        body += f'<text x="40" y="{y}" fill="{color}" font-size="11" font-weight="700" letter-spacing="1.5">{esc(cat)}</text>'
        body += f'<line x1="{40+label_w+8}" y1="{y-4}" x2="860" y2="{y-4}" stroke="#ffffff" stroke-opacity="0.06"/>'
        y += 12
        cx = 40
        for chip in chips:
            name = chip["name"]
            w = int(text_width(name)) + 36
            body += f'''<g transform="translate({cx}, {y})">
    <rect width="{w}" height="28" rx="8" fill="#16191f" stroke="#2a2f3a"/>
    <circle cx="15" cy="14" r="4" fill="{chip["color"]}"/>
    <text x="26" y="18" fill="#cfd6e4" font-size="12" font-weight="500">{esc(name)}</text>
  </g>'''
            cx += w + 10
        y += 56

    svg_h = y - 28
    return f'''<svg width="900" height="{svg_h}" viewBox="0 0 900 {svg_h}" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="sacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="{svg_h}" rx="16" fill="url(#sbg)"/>
  <rect x="0.5" y="0.5" width="899" height="{svg_h-1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>

{body}</svg>
'''


def build_certifications(c):
    completed = c.get("completed", [])
    in_progress = c.get("in_progress", [])
    planned = c.get("planned", [])

    def plat_color(p):
        p = (p or "").lower()
        if "aws" in p:
            return "#fbbf24"
        if "coursera" in p:
            return "#60a5fa"
        return "#8b93a7"

    body = ""
    y = 40

    def status_label(color, label):
        return (f'<g transform="translate(40, {y})">'
                f'<rect width="11" height="11" rx="3" fill="{color}"/>'
                f'<text x="22" y="10" fill="{color}" font-size="12" font-weight="700" letter-spacing="0.8">{label}</text></g>')

    # COMPLETED
    body += status_label("#34d399", "COMPLETED")
    y += 16
    for i, cert in enumerate(completed):
        bg = "#13161c" if i % 2 == 0 else "#1c2128"
        body += (f'<g transform="translate(40, {y})">'
                 f'<rect width="820" height="40" rx="10" fill="{bg}" stroke="#222831"/>'
                 f'<rect x="0" y="0" width="3" height="40" rx="1.5" fill="#34d399"/>'
                 f'<text x="20" y="25" fill="#e6eaf2" font-size="13.5" font-weight="600">{esc(cert["name"])}</text>'
                 f'<text x="420" y="25" fill="#8b93a7" font-size="12.5">{esc(cert.get("issuer",""))}</text>'
                 f'<text x="660" y="25" fill="{plat_color(cert.get("platform"))}" font-size="12.5">{esc(cert.get("platform",""))}</text>'
                 f'<text x="800" y="25" fill="#6b7280" font-size="12.5" text-anchor="end">{esc(cert.get("year",""))}</text></g>')
        y += 46

    # IN PROGRESS
    y += 16
    body += status_label("#a78bfa", "IN PROGRESS")
    y += 16
    for i, cert in enumerate(in_progress):
        bg = "#13161c" if i % 2 == 0 else "#1c2128"
        body += (f'<g transform="translate(40, {y})">'
                 f'<rect width="820" height="40" rx="10" fill="{bg}" stroke="#222831"/>'
                 f'<rect x="0" y="0" width="3" height="40" rx="1.5" fill="#a78bfa"/>'
                 f'<text x="20" y="25" fill="#e6eaf2" font-size="13.5" font-weight="600">{esc(cert["name"])}</text>'
                 f'<text x="420" y="25" fill="#8b93a7" font-size="12.5">{esc(cert.get("issuer",""))}</text>'
                 f'<text x="660" y="25" fill="{plat_color(cert.get("platform"))}" font-size="12.5">{esc(cert.get("platform",""))}</text>'
                 f'<text x="800" y="25" fill="#6b7280" font-size="12.5" text-anchor="end">{esc(cert.get("year",""))}</text></g>')
        y += 46

    # PLANNED
    y += 16
    body += status_label("#6b7280", "PLANNED")
    y += 16
    px = 40
    for cert in planned:
        body += (f'<g transform="translate({px}, {y})">'
                 f'<rect width="404" height="36" rx="10" fill="#0f1217" stroke="#1c222b"/>'
                 f'<text x="18" y="23" fill="#8b93a7" font-size="13" font-weight="500">{esc(cert["name"])}</text>'
                 f'<text x="386" y="23" fill="#5a6270" font-size="12" text-anchor="end">{esc(cert.get("platform",""))}</text></g>')
        px = 456 if px == 40 else 40
        if px == 40:
            y += 44
    if len(planned) % 2 == 1:
        y += 44
    svg_h = y + 16

    return f'''<svg width="900" height="{svg_h}" viewBox="0 0 900 {svg_h}" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0c10"/><stop offset="1" stop-color="#10131a"/></linearGradient>
    <linearGradient id="cacc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
  </defs>
  <rect width="900" height="{svg_h}" rx="16" fill="url(#cbg)"/>
  <rect x="0.5" y="0.5" width="899" height="{svg_h-1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>

  <g transform="translate(620, 28)" font-size="12">
    <circle cx="6" cy="8" r="4" fill="#34d399"/><text x="16" y="12" fill="#8b93a7">{len(completed)} done</text>
    <circle cx="86" cy="8" r="4" fill="#a78bfa"/><text x="96" y="12" fill="#8b93a7">{len(in_progress)} active</text>
    <circle cx="176" cy="8" r="4" fill="#6b7280"/><text x="186" y="12" fill="#8b93a7">{len(planned)} planned</text>
  </g>
{body}</svg>
'''


def main():
    with open("profile.json", encoding="utf-8") as f:
        cfg = json.load(f)
    os.makedirs("assets", exist_ok=True)
    with open("assets/header.svg", "w", encoding="utf-8") as f:
        f.write(build_header(cfg["header"]))
    with open("assets/about.svg", "w", encoding="utf-8") as f:
        f.write(build_about(cfg["about"]))
    with open("assets/techstack.svg", "w", encoding="utf-8") as f:
        f.write(build_techstack(cfg["techstack"]))
    if "certifications" in cfg:
        with open("assets/certifications.svg", "w", encoding="utf-8") as f:
            f.write(build_certifications(cfg["certifications"]))
    print("OK — header, about, techstack, certifications régénérés depuis profile.json")


if __name__ == "__main__":
    main()
