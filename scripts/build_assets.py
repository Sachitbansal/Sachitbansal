"""Builds the static animated SVGs in assets/ (header, terminal, footer).

The text in these SVGs is content, so it lives here as data: edit the constants
below and run `python scripts/build_assets.py` to regenerate. Everything is pure
SVG + CSS/SMIL so it animates inside GitHub's <img> sandbox (no JS, no web fonts).
"""

from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG = "#0d1117"
PANEL = "#0b0f14"
CYAN = "#00f7ff"
MAGENTA = "#ff2bd6"
GREEN = "#3fb950"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,Arial,sans-serif"

# ---------------------------------------------------------------- header

# Fixed node layout for the background "neural net" (x, y) in a 1000x280 box.
NODES = [
    (60, 75), (140, 200), (210, 110), (110, 225), (360, 75), (330, 230),
    (690, 50), (720, 235), (790, 140), (860, 60), (930, 200), (960, 110),
    (820, 215), (40, 150), (250, 255), (760, 80), (620, 260), (420, 250),
]


def header() -> str:
    edges = []
    for i, (x1, y1) in enumerate(NODES):
        for x2, y2 in NODES[i + 1:]:
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 < 150 ** 2:
                edges.append((x1, y1, x2, y2))

    edge_svg = "\n    ".join(
        f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="edge" style="animation-delay:{(i * 0.37) % 3:.2f}s"/>'
        for i, (a, b, c, d) in enumerate(edges)
    )
    node_svg = "\n    ".join(
        f'<circle cx="{x}" cy="{y}" r="3" class="node" style="animation-delay:{(i * 0.29) % 2.4:.2f}s"/>'
        for i, (x, y) in enumerate(NODES)
    )

    name = "SACHIT BANSAL"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 280" width="1000" height="280" role="img" aria-label="Sachit Bansal: agentic AI, retrieval, robotics, security">
  <title>Sachit Bansal</title>
  <defs>
    <linearGradient id="title" x1="0" x2="1">
      <stop offset="0" stop-color="{CYAN}"/>
      <stop offset="0.55" stop-color="#7f8cff"/>
      <stop offset="1" stop-color="{MAGENTA}"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CYAN}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.6">
      <stop offset="0" stop-color="#0f2a3a"/>
      <stop offset="1" stop-color="{BG}"/>
    </radialGradient>
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <path d="M25 0H0V25" fill="none" stroke="{CYAN}" stroke-opacity="0.06"/>
    </pattern>
    <clipPath id="frame"><rect width="1000" height="280" rx="16"/></clipPath>
  </defs>
  <style>
    .edge {{ stroke:{CYAN}; stroke-opacity:.28; stroke-width:1; stroke-dasharray:4 6; animation:flow 3s linear infinite; }}
    .node {{ fill:{CYAN}; animation:pulse 2.4s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }}
    .name {{ font:800 64px {SANS}; letter-spacing:8px; }}
    .glitch {{ font:800 64px {SANS}; letter-spacing:8px; opacity:0; }}
    .g1 {{ fill:{CYAN}; animation:g1 4s steps(1) infinite; }}
    .g2 {{ fill:{MAGENTA}; animation:g2 4s steps(1) infinite; }}
    .sub {{ font:600 15px {MONO}; letter-spacing:5px; fill:{TEXT}; }}
    .hud {{ font:12px {MONO}; fill:{MUTED}; letter-spacing:1px; }}
    .live {{ fill:{GREEN}; animation:blink 1.2s steps(2) infinite; }}
    .scan {{ animation:scan 5s linear infinite; }}
    .rule {{ stroke:url(#title); stroke-width:2; stroke-dasharray:420; stroke-dashoffset:420; animation:draw 1.4s .3s ease-out forwards; }}
    .fade {{ opacity:0; animation:fade .8s ease-out forwards; }}
    @keyframes flow {{ to {{ stroke-dashoffset:-20; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.25; transform:scale(.8); }} 50% {{ opacity:1; transform:scale(1.5); }} }}
    @keyframes blink {{ 50% {{ opacity:0; }} }}
    @keyframes scan {{ from {{ transform:translateY(-120px); }} to {{ transform:translateY(300px); }} }}
    @keyframes draw {{ to {{ stroke-dashoffset:0; }} }}
    @keyframes fade {{ to {{ opacity:1; }} }}
    @keyframes g1 {{
      0%,100% {{ opacity:0; }}
      86% {{ opacity:.8; transform:translate(-4px,0); clip-path:inset(10% 0 60% 0); }}
      88% {{ opacity:.8; transform:translate(3px,0); clip-path:inset(55% 0 20% 0); }}
      90% {{ opacity:.8; transform:translate(-2px,0); clip-path:inset(30% 0 45% 0); }}
      92% {{ opacity:0; }}
    }}
    @keyframes g2 {{
      0%,100% {{ opacity:0; }}
      87% {{ opacity:.8; transform:translate(4px,0); clip-path:inset(65% 0 10% 0); }}
      89% {{ opacity:.8; transform:translate(-3px,0); clip-path:inset(20% 0 55% 0); }}
      91% {{ opacity:.8; transform:translate(2px,0); clip-path:inset(45% 0 30% 0); }}
      93% {{ opacity:0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} .fade {{ opacity:1; }} .rule {{ stroke-dashoffset:0; }} }}
  </style>

  <g clip-path="url(#frame)">
    <rect width="1000" height="280" fill="url(#glow)"/>
    <rect width="1000" height="280" fill="url(#grid)"/>
    {edge_svg}
    {node_svg}
    <rect class="scan" width="1000" height="120" fill="url(#scan)"/>
  </g>
  <rect x=".5" y=".5" width="999" height="279" rx="16" fill="none" stroke="{CYAN}" stroke-opacity=".25"/>

  <!-- HUD corners -->
  <path d="M20 44V20h24M956 20h24v24M980 236v24h-24M44 260H20v-24" fill="none" stroke="{CYAN}" stroke-width="2" stroke-opacity=".7"/>
  <text x="34" y="40" class="hud fade" style="animation-delay:.2s">// IIT MANDI <tspan fill="{CYAN}">→</tspan> LEIBNIZ UNI HANNOVER</text>
  <g class="fade" style="animation-delay:.2s">
    <circle cx="874" cy="36" r="4" class="live"/>
    <text x="884" y="40" class="hud">ONLINE · DE</text>
  </g>
  <text x="34" y="252" class="hud fade" style="animation-delay:1.2s">52.37°N  9.73°E</text>
  <text x="966" y="252" class="hud fade" text-anchor="end" style="animation-delay:1.2s">status: <tspan fill="{CYAN}">compiling…</tspan></text>

  <!-- name with glitch layers -->
  <g class="fade">
    <text x="500" y="148" text-anchor="middle" class="name" fill="url(#title)">{name}</text>
    <text x="500" y="148" text-anchor="middle" class="glitch g1">{name}</text>
    <text x="500" y="148" text-anchor="middle" class="glitch g2">{name}</text>
  </g>
  <line x1="290" y1="172" x2="710" y2="172" class="rule"/>
  <text x="500" y="204" text-anchor="middle" class="sub fade" style="animation-delay:.9s">AGENTIC AI · RETRIEVAL · ROBOTICS · SECURITY</text>
</svg>
"""


# -------------------------------------------------------------- terminal

# 5x7 pixel glyphs for the neofetch logo.
GLYPHS = {
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
}

NEOFETCH = [
    ("sachit", "@", "github"),
    None,  # separator
    ("Uni", "IIT Mandi · B.Tech General Engg (AI & Robotics)"),
    ("Exchange", "Leibniz Universität Hannover · Oct '26 → Mar '27"),
    ("Focus", "agentic AI · RAG · robotics · security"),
    ("Langs", "Python · C++ · TypeScript · Solidity · Dart"),
    ("Infra", "Docker · Redis · Postgres · NATS · FAISS · Qdrant"),
    ("Side", "CTFs (rev · crypto · pwn) · competitive programming"),
    ("Org", "SBSSDigital LLP"),
]

NOW = [
    ("shipping", "researchAgent", "agentic RAG over arXiv, every claim NLI-checked"),
    ("running", "XBot", "LLM content radar with a Telegram approval loop"),
    ("studying", "@ Hannover", "ML + robotics, one semester in Germany"),
    ("looking", "Werkstudent", "AI / ML engineering roles in DE, DMs open"),
]

CHAR_W = 9.0  # approx advance of a 15px monospace glyph
LINE_H = 24


def typed(text_svg: str, x: float, y: float, chars: int, begin: float, uid: str) -> str:
    """Wrap a text line in a clip that reveals it one character at a time."""
    steps = ";".join(f"{i * CHAR_W:.0f}" for i in range(chars + 1)) + ";1000"
    dur = 0.045 * (chars + 1)
    return f"""<clipPath id="{uid}"><rect x="{x}" y="{y - 18}" height="{LINE_H}" width="0">
      <animate attributeName="width" values="{steps}" calcMode="discrete" dur="{dur:.2f}s" begin="{begin:.2f}s" fill="freeze"/>
    </rect></clipPath>
    <g clip-path="url(#{uid})">{text_svg}</g>"""


def appear(svg: str, begin: float) -> str:
    return f"""<g opacity="0">{svg}<set attributeName="opacity" to="1" begin="{begin:.2f}s" fill="freeze"/></g>"""


def prompt(x: float, y: float) -> str:
    return (
        f'<text x="{x}" y="{y}" class="t"><tspan fill="{GREEN}">sachit@hannover</tspan>'
        f'<tspan fill="{TEXT}">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{TEXT}">$</tspan></text>'
    )


def terminal() -> str:
    W = 1000
    x0, y = 28, 78
    px = 13  # logo pixel size
    out = []
    t = 0.6
    prompt_w = len("sachit@hannover:~$ ") * CHAR_W

    # $ neofetch
    out.append(appear(prompt(x0, y), t))
    cmd = "neofetch"
    out.append(typed(f'<text x="{x0 + prompt_w}" y="{y}" class="t">{cmd}</text>', x0 + prompt_w, y, len(cmd), t + 0.3, "c1"))
    t += 0.3 + 0.045 * (len(cmd) + 1) + 0.35
    y += LINE_H + 10

    # logo
    logo = []
    ox, oy = x0 + 6, y - 4
    col = 0
    for gi, ch in enumerate("SB"):
        for r, row in enumerate(GLYPHS[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    gx = ox + (col + c) * px
                    gy = oy + r * px
                    delay = t + (col + c) * 0.035
                    logo.append(
                        f'<rect x="{gx}" y="{gy}" width="{px - 2}" height="{px - 2}" rx="2" fill="url(#logo)" opacity="0">'
                        f'<set attributeName="opacity" to="1" begin="{delay:.2f}s" fill="freeze"/></rect>'
                    )
        col += 6
    out.append('<g filter="url(#soft)">' + "".join(logo) + "</g>")

    # info column
    ix = x0 + 190
    iy = y
    for i, row in enumerate(NEOFETCH):
        bt = t + 0.15 + i * 0.12
        if row is None:
            out.append(appear(f'<text x="{ix}" y="{iy}" class="t" fill="{MUTED}">{"─" * 20}</text>', bt))
        elif len(row) == 3:
            out.append(appear(
                f'<text x="{ix}" y="{iy}" class="t b"><tspan fill="{CYAN}">{row[0]}</tspan>'
                f'<tspan fill="{TEXT}">{row[1]}</tspan><tspan fill="{CYAN}">{row[2]}</tspan></text>', bt))
        else:
            key, val = row
            out.append(appear(
                f'<text x="{ix}" y="{iy}" class="t"><tspan fill="{CYAN}" class="b">{escape(key)}</tspan>'
                f'<tspan fill="{MUTED}">: </tspan><tspan x="{ix + 100}" fill="{TEXT}">{escape(val)}</tspan></text>', bt))
        iy += LINE_H
    # palette swatches
    bt = t + 0.15 + len(NEOFETCH) * 0.12
    sw = "".join(
        f'<rect x="{ix + i * 30}" y="{iy - 10}" width="26" height="14" rx="2" fill="{c}"/>'
        for i, c in enumerate(["#161b22", "#f85149", GREEN, "#d29922", "#58a6ff", MAGENTA, CYAN, TEXT])
    )
    out.append(appear(sw, bt))
    iy += LINE_H + 14
    t = bt + 0.5

    # $ cat now.log
    y = iy
    out.append(appear(prompt(x0, y), t))
    cmd = "cat ~/now.log"
    out.append(typed(f'<text x="{x0 + prompt_w}" y="{y}" class="t">{escape(cmd)}</text>', x0 + prompt_w, y, len(cmd), t + 0.3, "c2"))
    t += 0.3 + 0.045 * (len(cmd) + 1) + 0.35
    y += LINE_H + 4
    for i, (verb, what, desc) in enumerate(NOW):
        out.append(appear(
            f'<text x="{x0}" y="{y}" class="t"><tspan fill="{MAGENTA}">▸ </tspan>'
            f'<tspan fill="{MUTED}">[{verb}]</tspan><tspan x="{x0 + 120}" fill="{CYAN}" class="b">{escape(what)}</tspan>'
            f'<tspan x="{x0 + 270}" fill="{TEXT}">{escape(desc)}</tspan></text>', t + i * 0.25))
        y += LINE_H
    t += len(NOW) * 0.25 + 0.4
    y += 10

    # final prompt + cursor
    out.append(appear(prompt(x0, y) + f'<rect x="{x0 + prompt_w + 2}" y="{y - 14}" width="9" height="17" fill="{CYAN}" class="cursor"/>', t))
    H = y + 30

    body = "\n  ".join(out)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal running neofetch for Sachit Bansal">
  <title>sachit@hannover: neofetch</title>
  <defs>
    <linearGradient id="logo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAGENTA}"/>
    </linearGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    .t {{ font:15px {MONO}; fill:{TEXT}; white-space:pre; }}
    .b {{ font-weight:700; }}
    .cursor {{ animation:blink 1s steps(2) infinite; }}
    @keyframes blink {{ 50% {{ opacity:0; }} }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{PANEL}" stroke="#30363d"/>
  <path d="M.5 12.5a12 12 0 0 1 12-12h{W - 25}a12 12 0 0 1 12 12V40H.5z" fill="#161b22"/>
  <line x1="0" y1="40" x2="{W}" y2="40" stroke="#30363d"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>
  <text x="{W / 2}" y="25" text-anchor="middle" style="font:13px {MONO}" fill="{MUTED}">sachit@hannover: ~ — zsh</text>
  {body}
</svg>
"""


# ---------------------------------------------------------------- footer

def footer() -> str:
    # ECG-style trace across the width.
    pts = []
    x = 0
    while x < 1000:
        pts += [f"{x},40", f"{x + 70},40", f"{x + 80},30", f"{x + 90},40", f"{x + 100},40",
                f"{x + 108},52", f"{x + 118},8", f"{x + 128},66", f"{x + 136},40", f"{x + 160},40",
                f"{x + 172},32", f"{x + 186},40"]
        x += 200
    path = "M" + " L".join(pts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 110" width="1000" height="110" role="img" aria-label="End of transmission">
  <title>EOF</title>
  <defs>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{CYAN}"/>
      <stop offset="1" stop-color="{MAGENTA}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .trace {{ fill:none; stroke:url(#fade); stroke-width:2; stroke-dasharray:2600; stroke-dashoffset:2600; animation:run 4s linear infinite; }}
    .ghost {{ fill:none; stroke:{CYAN}; stroke-opacity:.08; stroke-width:2; }}
    .eof {{ font:13px {MONO}; fill:{MUTED}; letter-spacing:4px; }}
    @keyframes run {{ to {{ stroke-dashoffset:0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .trace {{ animation:none; stroke-dashoffset:0; }} }}
  </style>
  <path d="{path}" class="ghost"/>
  <path d="{path}" class="trace"/>
  <text x="500" y="100" text-anchor="middle" class="eof">── END OF TRANSMISSION ──</text>
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, build in [("header.svg", header), ("terminal.svg", terminal), ("footer.svg", footer)]:
        (ASSETS / name).write_text(build(), encoding="utf-8")
        print("wrote", ASSETS / name)
