"""Renders dist/stats.svg from the GitHub GraphQL API.

Run by .github/workflows/profile.yml. Self-hosted so the profile does not depend on
rate-limited public stats instances. Stdlib only.

    GITHUB_TOKEN=... python scripts/stats_card.py <login> <out.svg>
    python scripts/stats_card.py --sample <out.svg>   # offline preview
"""

import json
import os
import sys
import urllib.request
from datetime import date, datetime, timezone
from html import escape

BG = "#0b0f14"
CYAN = "#00f7ff"
MAGENTA = "#ff2bd6"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
BORDER = "#30363d"
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

# Notebook outputs and markup dwarf real code by bytes; leave them out of the language mix.
IGNORED_LANGS = {"Jupyter Notebook", "HTML", "CSS", "SCSS", "Makefile", "Dockerfile", "Shell", "Procfile"}
TOP_LANGS = 6

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""


def graphql(token: str, variables: dict) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def fetch(login: str, token: str) -> dict:
    cursor, repos, user = None, [], None
    while True:
        user = graphql(token, {"login": login, "cursor": cursor})
        page = user["repositories"]
        repos += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    langs: dict[str, list] = {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in IGNORED_LANGS:
                continue
            entry = langs.setdefault(name, [0, edge["node"]["color"] or MUTED])
            entry[0] += edge["size"]

    cc = user["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    return {
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": user["pullRequests"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "repos": user["repositories"]["totalCount"],
        "followers": user["followers"]["totalCount"],
        "langs": sorted(((n, s, c) for n, (s, c) in langs.items()), key=lambda x: -x[1]),
        "days": [(d["date"], d["contributionCount"]) for d in days],
    }


def streaks(days: list) -> tuple[int, int]:
    """Current and longest daily streak. Today not having a contribution yet doesn't break it."""
    counts = [c for _, c in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    return current, longest


def render(s: dict) -> str:
    W, H = 1000, 380
    current, longest = streaks(s["days"])
    metrics = [
        ("contributions / 1y", s["contributions"]), ("current streak", f"{current}d"),
        ("commits / 1y", s["commits"]), ("longest streak", f"{longest}d"),
        ("pull requests", s["prs"]), ("public repos", s["repos"]),
        ("stars earned", s["stars"]), ("followers", s["followers"]),
    ]
    out = []

    # metrics grid, two columns
    for i, (label, value) in enumerate(metrics):
        x = 32 + (i % 2) * 250
        y = 104 + (i // 2) * 40
        val = f"{value:,}" if isinstance(value, int) else value
        delay = 0.1 + i * 0.08
        out.append(
            f'<g class="in" style="animation-delay:{delay:.2f}s">'
            f'<text x="{x}" y="{y}" class="lbl">{label}</text>'
            f'<text x="{x + 220}" y="{y}" class="val" text-anchor="end">{val}</text>'
            f'<line x1="{x}" y1="{y + 10}" x2="{x + 220}" y2="{y + 10}" class="dash"/></g>'
        )

    # language bars
    top = s["langs"][:TOP_LANGS]
    total = sum(size for _, size, _ in s["langs"]) or 1
    bx, bw = 580, 300
    for i, (name, size, color) in enumerate(top):
        y = 112 + i * 28
        pct = size / total
        w = max(2.0, (bw - 110) * pct)
        delay = 0.3 + i * 0.1
        out.append(
            f'<g class="in" style="animation-delay:{delay:.2f}s">'
            f'<text x="{bx}" y="{y}" class="lbl">{escape(name)}</text>'
            f'<rect x="{bx + 110}" y="{y - 10}" width="{bw - 110}" height="10" rx="5" fill="#161b22"/>'
            f'<rect x="{bx + 110}" y="{y - 10}" width="0" height="10" rx="5" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{w:.1f}" dur="1s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>'
            f'<text x="{bx + bw + 12}" y="{y}" class="pct">{pct * 100:.1f}%</text></g>'
        )

    # contribution sparkline, last 26 weeks summed weekly
    days = s["days"][-26 * 7:]
    weeks = [sum(c for _, c in days[i:i + 7]) for i in range(0, len(days), 7)]
    peak = max(weeks) if weeks and max(weeks) else 1
    sx, sy, sh = 32, 352, 56
    bar_w = (W - 64) / max(len(weeks), 1)
    for i, wk in enumerate(weeks):
        h = max(2.0, sh * wk / peak)
        out.append(
            f'<rect x="{sx + i * bar_w + 2:.1f}" y="{sy - h:.1f}" width="{bar_w - 4:.1f}" height="{h:.1f}" rx="2" '
            f'fill="url(#spark)" class="bar" style="animation-delay:{0.6 + i * 0.03:.2f}s"/>'
        )

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = "\n  ".join(out)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub stats: {s['contributions']} contributions in the last year">
  <title>system diagnostics</title>
  <defs>
    <linearGradient id="spark" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" x2="1">
      <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/>
    </linearGradient>
  </defs>
  <style>
    .h {{ font:700 14px {MONO}; fill:{CYAN}; letter-spacing:3px; }}
    .sub {{ font:12px {MONO}; fill:{MUTED}; }}
    .lbl {{ font:14px {MONO}; fill:{MUTED}; }}
    .val {{ font:700 15px {MONO}; fill:{TEXT}; }}
    .pct {{ font:13px {MONO}; fill:{TEXT}; }}
    .dash {{ stroke:{BORDER}; stroke-dasharray:2 4; }}
    .in {{ opacity:0; animation:in .5s ease-out forwards; }}
    .bar {{ transform-box:fill-box; transform-origin:bottom; transform:scaleY(0); animation:grow .6s ease-out forwards; }}
    @keyframes in {{ from {{ opacity:0; transform:translateY(6px); }} to {{ opacity:1; transform:none; }} }}
    @keyframes grow {{ to {{ transform:scaleY(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .in, .bar {{ animation:none; opacity:1; transform:none; }} }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
  <text x="32" y="44" class="h">[ SYSTEM DIAGNOSTICS ]</text>
  <text x="{W - 32}" y="44" class="sub" text-anchor="end">last sync {updated}</text>
  <line x1="32" y1="58" x2="{W - 32}" y2="58" stroke="url(#rule)" stroke-opacity=".6"/>
  <text x="580" y="86" class="sub">// language mix (public repos, by bytes)</text>
  <text x="32" y="{sy - sh - 16}" class="sub">// weekly activity, last 26 weeks</text>
  {body}
</svg>
"""


def sample() -> dict:
    start = date(2026, 4, 1).toordinal()
    days = [(date.fromordinal(start + i).isoformat(), (i * 7 + i // 9) % 6 if i % 11 else 0) for i in range(365)]
    return {
        "contributions": 1287, "commits": 942, "prs": 38, "stars": 41, "repos": 52, "followers": 34,
        "langs": [("Python", 900, "#3572A5"), ("TypeScript", 600, "#3178c6"), ("C++", 300, "#f34b7d"),
                  ("Solidity", 120, "#AA6746"), ("JavaScript", 100, "#f1e05a"), ("Dart", 60, "#00B4AB"), ("C#", 20, "#178600")],
        "days": days,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    who, out_path = sys.argv[1], sys.argv[2]
    data = sample() if who == "--sample" else fetch(who, os.environ["GITHUB_TOKEN"])
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(data))
    print("wrote", out_path)
