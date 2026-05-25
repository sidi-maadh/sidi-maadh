#!/usr/bin/env python3
"""
Génère des cartes plateforme avec logos officiels dessinés en SVG.
Chaque carte : 210x110, barre couleur, logo, nom, label, sous-texte.
"""

CARD_W = 210
CARD_H = 110


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ─── Logos officiels (dessinés à la main, placés à translate(20,18), ~28x28) ───
LOGOS = {
    # Codeforces : 3 barres (rouge, jaune, bleu)
    "codeforces": '''<g transform="translate(20,20)">
      <rect x="0" y="9" width="6" height="14" rx="2" fill="#f44336"/>
      <rect x="9" y="3" width="6" height="20" rx="2" fill="#ffc107"/>
      <rect x="18" y="13" width="6" height="10" rx="2" fill="#2196f3"/></g>''',
    # LeetCode : losange stylisé
    "leetcode": '''<g transform="translate(22,19)">
      <path d="M13 2 L4 11 a3 3 0 0 0 0 4 l9 9 l2.5 -2.5 l-8 -8 a0.7 0.7 0 0 1 0 -1 l8 -8 z" fill="#ffa116"/>
      <rect x="7" y="13" width="14" height="2.6" rx="1.3" fill="#b3b3b3"/></g>''',
    # CodeChef : chapeau de chef
    "codechef": '''<g transform="translate(20,20)">
      <path d="M5 16 c-3 0 -4 -2.5 -4 -4.5 c0 -2 1.5 -3.5 3.5 -3.5 c0 -3 2.5 -4.5 4.5 -4.5 c1.5 0 2.8 0.8 3.5 2 c0.7 -1.2 2 -2 3.5 -2 c2 0 4.5 1.5 4.5 4.5 c2 0 3.5 1.5 3.5 3.5 c0 2 -1 4.5 -4 4.5 z" fill="#a77b5a"/>
      <rect x="5" y="16" width="14" height="6" rx="1" fill="#5b4638"/></g>''',
    # HackerRank : "h" dans un carré
    "hackerrank": '''<g transform="translate(21,19)">
      <rect x="0" y="0" width="24" height="24" rx="6" fill="#2ec866"/>
      <path d="M8 6 v12 M16 6 v12 M8 12 h8" stroke="#0a0c10" stroke-width="2" fill="none" stroke-linecap="round"/></g>''',
    # Advent of Code : étoile + sapin
    "adventofcode": '''<g transform="translate(20,19)">
      <path d="M12 2 l2.4 5 l5.6 0.5 l-4.2 3.6 l1.2 5.4 l-5 -2.8 l-5 2.8 l1.2 -5.4 l-4.2 -3.6 l5.6 -0.5 z" fill="#ffd700"/>
      <circle cx="6" cy="20" r="1.6" fill="#00cc00"/><circle cx="18" cy="20" r="1.6" fill="#ff0000"/></g>''',
    # CSES : monospace brackets
    "cses": '''<g transform="translate(21,20)">
      <path d="M8 2 L2 12 L8 22 M16 2 L22 12 L16 22" stroke="#4a90d9" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>''',
    # CodeWars : ninja head
    "codewars": '''<g transform="translate(20,20)">
      <path d="M2 9 c0 -3 4 -5 10 -5 c6 0 10 2 10 5 l-3 1 c-4 -1.5 -10 -1.5 -14 0 z" fill="#b1361e"/>
      <path d="M2 11 c2 1 6 2 10 2 c4 0 8 -1 10 -2 l-1 4 c-2 1.5 -5.5 2.5 -9 2.5 c-3.5 0 -7 -1 -9 -2.5 z" fill="#ad2c27"/>
      <circle cx="9" cy="12.5" r="1.2" fill="#fff"/><circle cx="15" cy="12.5" r="1.2" fill="#fff"/></g>''',
    # GeeksforGeeks : "G" green
    "geeksforgeeks": '''<g transform="translate(21,19)">
      <circle cx="8" cy="12" r="6" fill="none" stroke="#2f8d46" stroke-width="2.4"/>
      <circle cx="17" cy="12" r="6" fill="none" stroke="#2f8d46" stroke-width="2.4"/>
      <path d="M8 12 h4 M17 12 h3" stroke="#2f8d46" stroke-width="2.4" stroke-linecap="round"/></g>''',
    # Edabit : hexagon
    "edabit": '''<g transform="translate(21,19)">
      <path d="M12 1 L22 6.5 V17.5 L12 23 L2 17.5 V6.5 Z" fill="none" stroke="#6c5ce7" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M8 12 l3 3 l5 -6" stroke="#6c5ce7" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>''',
    # Hack The Box : hexagon cube
    "hackthebox": '''<g transform="translate(21,18)">
      <path d="M12 2 L21 7 V17 L12 22 L3 17 V7 Z" fill="none" stroke="#9fef00" stroke-width="2" stroke-linejoin="round"/>
      <path d="M12 2 V12 M12 12 L3 7 M12 12 L21 7" stroke="#9fef00" stroke-width="1.6" fill="none"/></g>''',
    # TryHackMe : shield
    "tryhackme": '''<g transform="translate(21,18)">
      <path d="M12 2 L21 5 V12 C21 18 17 21 12 23 C7 21 3 18 3 12 V5 Z" fill="#c11111"/>
      <path d="M8 12 l3 3 l5 -6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>''',
    # CryptoHack : lock
    "cryptohack": '''<g transform="translate(22,19)">
      <rect x="2" y="10" width="16" height="12" rx="2.5" fill="#16c79a"/>
      <path d="M5 10 V7 a5 5 0 0 1 10 0 V10" fill="none" stroke="#16c79a" stroke-width="2.2"/>
      <circle cx="10" cy="15" r="1.8" fill="#0a0c10"/></g>''',
    # RootMe : terminal prompt
    "rootme": '''<g transform="translate(20,19)">
      <rect x="1" y="3" width="22" height="17" rx="3" fill="none" stroke="#e00911" stroke-width="2"/>
      <path d="M5 9 l3 2.5 l-3 2.5 M11 14 h5" stroke="#e00911" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>''',
    # Kaggle : "K" stylized
    "kaggle": '''<g transform="translate(23,19)">
      <path d="M2 2 V22 M2 14 L12 2 M5 11 L13 22" stroke="#20beff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>''',
    # Hugging Face : smiley face
    "huggingface": '''<g transform="translate(20,19)">
      <circle cx="12" cy="12" r="11" fill="#ffd21e"/>
      <circle cx="8" cy="10" r="1.6" fill="#0a0c10"/><circle cx="16" cy="10" r="1.6" fill="#0a0c10"/>
      <path d="M7 15 q5 4 10 0" stroke="#0a0c10" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>''',
}


def card(key, platform, big, sub, color, link=""):
    logo = LOGOS.get(key, "")
    return f'''<svg width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="{CARD_W-2}" height="{CARD_H-2}" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="{CARD_W-2}" height="4" rx="2" fill="{color}"/>
  {logo}
  <text x="60" y="36" fill="#8b93a7" font-size="12" font-weight="600" letter-spacing="0.3">{esc(platform)}</text>
  <text x="20" y="72" fill="{color}" font-size="21" font-weight="700">{esc(big)}</text>
  <text x="20" y="94" fill="#6b7280" font-size="12">{esc(sub)}</text>
</svg>
'''


# Définition des 15 cartes
CARDS = {
    # Competitive Programming
    "codeforces":   ("Codeforces", "Active", "Problems solved", "#1F8ACB"),
    "leetcode":     ("LeetCode", "Solving", "Problems solved", "#FFA116"),
    "codechef":     ("CodeChef", "3 \u2605", "Rating 1600+", "#A77B5A"),
    "hackerrank":   ("HackerRank", "Gold", "Problem solving", "#2EC866"),
    "adventofcode": ("Advent of Code", "Coder", "Yearly puzzles", "#FFD700"),
    # Problem Solving
    "cses":          ("CSES", "Solving", "Problem set", "#4A90D9"),
    "codewars":      ("CodeWars", "Active", "Kata challenges", "#B1361E"),
    "geeksforgeeks": ("GeeksforGeeks", "Active", "DSA practice", "#2F8D46"),
    "edabit":        ("Edabit", "Solving", "Coding challenges", "#6C5CE7"),
    # Cybersecurity
    "hackthebox": ("Hack The Box", "Hacker", "Pentesting labs", "#9FEF00"),
    "tryhackme":  ("TryHackMe", "Active", "Security rooms", "#FF5252"),
    "cryptohack": ("CryptoHack", "Active", "Crypto challenges", "#16C79A"),
    "rootme":     ("RootMe", "Active", "Hacking challenges", "#E00911"),
    # AI
    "kaggle":      ("Kaggle", "Contributor", "ML competitions", "#20BEFF"),
    "huggingface": ("Hugging Face", "Builder", "Models & datasets", "#FFD21E"),
}


# Emplacement de chaque carte (dossier par section)
FOLDERS = {
    "codeforces": "cp", "leetcode": "cp", "codechef": "cp",
    "hackerrank": "cp", "adventofcode": "cp",
    "cses": "problemsolving", "codewars": "problemsolving",
    "geeksforgeeks": "problemsolving", "edabit": "problemsolving",
    "hackthebox": "cyber", "tryhackme": "cyber",
    "cryptohack": "cyber", "rootme": "cyber",
    "kaggle": "ai", "huggingface": "ai",
}


def fetch_dynamic():
    """Récupère les vraies stats là où une API publique existe.
    Retourne un dict {key: (big, sub)} pour écraser les valeurs par défaut."""
    import json
    import urllib.request
    overrides = {}

    # --- Codeforces (problèmes résolus ou rang) ---
    try:
        def cf_api(u):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        info = cf_api("https://codeforces.com/api/user.info?handles=sidi_maadh")
        if info.get("status") == "OK":
            u = info["result"][0]
            if u.get("rating"):
                overrides["codeforces"] = (u.get("rank", "Rated").title(),
                                           f'Rating {u["rating"]}')
            else:
                st = cf_api("https://codeforces.com/api/user.status?handle=sidi_maadh&from=1&count=10000")
                if st.get("status") == "OK":
                    sosolved = {f'{s["problem"].get("contestId")}-{s["problem"].get("index")}'
                                for s in st["result"] if s.get("verdict") == "OK"}
                    overrides["codeforces"] = (f"{len(sosolved)}+", "Problems solved")
    except Exception as e:
        print(f"CF: {e}")

    # --- LeetCode (problèmes résolus) ---
    try:
        q = {"query": "query u($u:String!){matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}}",
             "variables": {"u": "sidi_maadh"}}
        req = urllib.request.Request("https://leetcode.com/graphql",
                                     data=json.dumps(q).encode(),
                                     headers={"Content-Type": "application/json",
                                              "User-Agent": "Mozilla/5.0",
                                              "Referer": "https://leetcode.com"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.loads(r.read().decode())
        m = d.get("data", {}).get("matchedUser")
        if m:
            for it in m["submitStatsGlobal"]["acSubmissionNum"]:
                if it["difficulty"] == "All":
                    n = it["count"]
                    overrides["leetcode"] = (f"{(n//10)*10}+" if n >= 10 else f"{n}",
                                             "Problems solved")
    except Exception as e:
        print(f"LC: {e}")

    # --- Hugging Face (models + datasets) ---
    try:
        req = urllib.request.Request("https://huggingface.co/api/users/sidiMaadh/overview",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.loads(r.read().decode())
        models = d.get("numModels", 0)
        datasets = d.get("numDatasets", 0)
        if models or datasets:
            overrides["huggingface"] = (str(models + datasets),
                                        f"{models} models · {datasets} datasets")
    except Exception as e:
        print(f"HF: {e}")

    return overrides


def main():
    import os
    overrides = fetch_dynamic()
    for key, (platform, big, sub, color) in CARDS.items():
        if key in overrides:
            big, sub = overrides[key]
        folder = FOLDERS.get(key, "cp")
        os.makedirs(f"assets/{folder}", exist_ok=True)
        with open(f"assets/{folder}/{key}.svg", "w", encoding="utf-8") as f:
            f.write(card(key, platform, big, sub, color))
    print(f"OK — {len(CARDS)} cartes générées (dont {len(overrides)} dynamiques)")


if __name__ == "__main__":
    main()
