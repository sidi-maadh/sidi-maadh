#!/usr/bin/env python3
"""
Génère assets/cp/leetcode.svg avec les vraies stats LeetCode (API GraphQL publique).
"""
import os
import json
import urllib.request

USERNAME = "sidi_maadh"


def fetch():
    query = {
        "query": """
        query userProfile($username: String!) {
          matchedUser(username: $username) {
            submitStatsGlobal { acSubmissionNum { difficulty count } }
          }
        }""",
        "variables": {"username": USERNAME},
    }
    data = json.dumps(query).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://leetcode.com/u/{USERNAME}/",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        resp = json.loads(r.read().decode())
    user = resp.get("data", {}).get("matchedUser")
    if not user:
        raise RuntimeError("Utilisateur LeetCode introuvable")
    total = 0
    for item in user["submitStatsGlobal"]["acSubmissionNum"]:
        if item["difficulty"] == "All":
            total = item["count"]
    return total


def build_svg(solved):
    return f'''<svg width="210" height="110" viewBox="0 0 210 110" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', system-ui, sans-serif">
  <rect x="1" y="1" width="208" height="108" rx="12" fill="#13161c" stroke="#222831"/>
  <rect x="1" y="1" width="208" height="4" rx="2" fill="#FFA116"/>
  <text x="20" y="34" fill="#8b93a7" font-size="12" font-weight="600" letter-spacing="0.5">LeetCode</text>
  <text x="20" y="66" fill="#FFA116" font-size="26" font-weight="700">{solved}+</text>
  <text x="20" y="90" fill="#6b7280" font-size="13">Problems solved</text>
</svg>
'''


def main():
    try:
        solved = fetch()
        # arrondi à la dizaine inférieure pour le "+"
        display = (solved // 10) * 10 if solved >= 10 else solved
    except Exception as e:
        print(f"Avertissement LeetCode: {e} — valeur par défaut conservée.")
        display = 500
    svg = build_svg(display)
    os.makedirs("assets/cp", exist_ok=True)
    with open("assets/cp/leetcode.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"OK — LeetCode {display}+ résolus.")


if __name__ == "__main__":
    main()
