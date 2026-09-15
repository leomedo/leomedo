# -*- coding: utf-8 -*-
"""Generates the bespoke animated hero banner for the GitHub profile README.

Two themed variants (dark / light) are rendered from a single template so the
banner stays in sync with whatever GitHub theme the visitor is using.
"""
import math
import pathlib

THEMES = {
    "dark": dict(
        bg0="#080C18", bg1="#111A33", bg2="#0A1024",
        grid="#7C8DB5", grid_op="0.10",
        name="#F2F6FF", muted="#93A2C6", sub="#DCE4F7",
        a1="#6C8CFF", a2="#35D6A4", a3="#FFB86B",
        glow_op="0.30", card_stroke="#2A3557",
        chip="#141D38", chip_stroke="#2C3A62",
    ),
    "light": dict(
        bg0="#FBFCFF", bg1="#E9EEFB", bg2="#F5F7FE",
        grid="#41527E", grid_op="0.12",
        name="#0C1430", muted="#5A688F", sub="#22305A",
        a1="#3355E8", a2="#0E9E72", a3="#C2701A",
        glow_op="0.18", card_stroke="#C9D3EC",
        chip="#FFFFFF", chip_stroke="#D3DCF0",
    ),
}

ROTATING = [
    "Python  ·  Frappe Framework  ·  ERPNext",
    "Multi-Tenant SaaS  ·  Stripe Billing  ·  Entitlements",
    "E-Invoicing Compliance  ·  ETA Egypt  ·  ZATCA KSA",
    "REST APIs  ·  React  ·  MariaDB  ·  PostgreSQL",
]

W, H = 1200, 340
CYCLE = 13.2                      # full subtitle rotation, seconds
STEP = CYCLE / len(ROTATING)
HUB_X, HUB_Y, RING_R = 1012.0, 170.0, 74.0


def build(t):
    # rotating subtitle lines -------------------------------------------------
    rot = "\n      ".join(
        '<text class="f rot" x="74" y="228" style="animation-delay:{:.2f}s">{}</text>'.format(
            i * STEP, txt
        )
        for i, txt in enumerate(ROTATING)
    )

    # background grid ---------------------------------------------------------
    grid = "".join(
        ['<line x1="{0}" y1="0" x2="{0}" y2="{1}"/>'.format(x, H) for x in range(0, W + 80, 40)]
        + ['<line x1="-40" y1="{0}" x2="{1}" y2="{0}"/>'.format(y, W + 40) for y in range(0, H + 40, 40)]
    )

    # multi-tenant constellation: one hub, six tenants, data flowing inward ----
    spokes, nodes = [], []
    for i in range(6):
        ang = math.radians(-90 + i * 60)
        nx, ny = HUB_X + RING_R * math.cos(ang), HUB_Y + RING_R * math.sin(ang)
        spokes.append(
            '<line class="spoke" x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" '
            'style="animation-delay:{:.2f}s"/>'.format(HUB_X, HUB_Y, nx, ny, i * 0.45)
        )
        nodes.append(
            '<circle class="node" cx="{:.1f}" cy="{:.1f}" r="7" '
            'style="animation-delay:{:.2f}s"/>'.format(nx, ny, i * 0.45)
        )
    net = "".join(spokes) + "".join(nodes)

    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Mohamed Khaled Shoaib - Backend Software Engineer">
  <title>Mohamed Khaled Shoaib &#8212; Backend Software Engineer</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg0}"/>
      <stop offset="55%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{a1}"/>
      <stop offset="50%" stop-color="{a2}"/>
      <stop offset="100%" stop-color="{a3}"/>
    </linearGradient>
    <radialGradient id="glowA" cx="50%" cy="50%">
      <stop offset="0%" stop-color="{a1}" stop-opacity="{glow_op}"/>
      <stop offset="100%" stop-color="{a1}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="50%" cy="50%">
      <stop offset="0%" stop-color="{a2}" stop-opacity="{glow_op}"/>
      <stop offset="100%" stop-color="{a2}" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <style>
      .f {{ font-family: 'Segoe UI', Inter, system-ui, Ubuntu, 'Helvetica Neue', Arial, sans-serif; }}
      .m {{ font-family: ui-monospace, 'Cascadia Code', 'SF Mono', Menlo, Consolas, monospace; }}
      .name {{ fill:{name}; font-size:57px; font-weight:700; letter-spacing:-0.6px; }}
      .eyebrow {{ fill:{a2}; font-size:14px; font-weight:600; letter-spacing:4.4px; }}
      .rot {{ fill:{sub}; font-size:20.5px; font-weight:500; opacity:0;
              animation: cyc {CYCLE}s ease-in-out infinite; }}
      .meta {{ fill:{muted}; font-size:14.5px; letter-spacing:0.4px; }}
      .chip {{ fill:{chip}; stroke:{chip_stroke}; stroke-width:1; }}
      .chipt {{ fill:{muted}; font-size:12.5px; font-weight:600; letter-spacing:0.8px; }}
      .grid line {{ stroke:{grid}; stroke-width:1; stroke-opacity:{grid_op}; }}
      .drift {{ animation: drift 9s linear infinite; }}
      .spoke {{ stroke:url(#accent); stroke-width:2; stroke-opacity:.8;
                stroke-dasharray:6 10; animation: flow 2.6s linear infinite; }}
      .node {{ fill:{a1}; animation: pulse 2.6s ease-in-out infinite; }}
      .hub {{ fill:none; stroke:{a2}; stroke-width:2; }}
      .halo {{ fill:none; stroke:{a2}; stroke-width:1.4; stroke-opacity:.45;
               animation: halo 3.4s ease-out infinite; transform-origin:{HUB_X}px {HUB_Y}px; }}
      .sweep {{ animation: sweep 5.5s ease-in-out infinite; }}
      .orb {{ animation: breathe 7s ease-in-out infinite; }}
      @keyframes cyc {{
        0%   {{ opacity:0; transform: translateY(9px); }}
        3.5% {{ opacity:1; transform: translateY(0); }}
        21%  {{ opacity:1; transform: translateY(0); }}
        25%  {{ opacity:0; transform: translateY(-9px); }}
        100% {{ opacity:0; transform: translateY(-9px); }}
      }}
      @keyframes drift {{ from {{ transform: translateX(0); }} to {{ transform: translateX(40px); }} }}
      @keyframes flow {{ to {{ stroke-dashoffset:-32; }} }}
      @keyframes pulse {{ 0%,100% {{ opacity:.45; r:6; }} 50% {{ opacity:1; r:8; }} }}
      @keyframes halo {{ 0% {{ transform:scale(.55); opacity:.7; }} 100% {{ transform:scale(1.7); opacity:0; }} }}
      @keyframes sweep {{ 0%,100% {{ opacity:.35; }} 50% {{ opacity:1; }} }}
      @keyframes breathe {{ 0%,100% {{ opacity:.65; }} 50% {{ opacity:1; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .rot, .drift, .spoke, .node, .halo, .sweep, .orb {{ animation:none; }}
        .rot {{ opacity:0; }}
        .rot:first-of-type {{ opacity:1; }}
      }}
    </style>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <g class="grid drift">{grid_lines}</g>
    <ellipse class="orb" cx="130" cy="60" rx="330" ry="210" fill="url(#glowA)"/>
    <ellipse class="orb" cx="1010" cy="280" rx="300" ry="200" fill="url(#glowB)" style="animation-delay:2.5s"/>

    <g filter="url(#soft)">
      {net}
      <circle class="halo" cx="{HUB_X}" cy="{HUB_Y}" r="30"/>
      <circle class="hub" cx="{HUB_X}" cy="{HUB_Y}" r="21"/>
      <circle cx="{HUB_X}" cy="{HUB_Y}" r="9" fill="{a2}"/>
    </g>

    <rect x="74" y="72" width="34" height="3" rx="1.5" fill="url(#accent)" class="sweep"/>
    <text class="f eyebrow" x="120" y="79">BACKEND SOFTWARE ENGINEER</text>
    <text class="f name" x="70" y="152">Mohamed Khaled Shoaib</text>
    <text class="m" x="74" y="228" font-size="20.5" fill="{a3}" opacity=".9">&#9656;</text>
    <g transform="translate(24,0)">
      {rot}
    </g>
    <text class="f meta" x="74" y="272">Giza, Egypt   &#183;   3+ years shipping production Python   &#183;   Open to remote</text>

    <g transform="translate(772,296)">
      <rect class="chip" x="0" y="0" width="96" height="26" rx="13"/><text class="m chipt" x="48" y="17" text-anchor="middle">PYTHON</text>
      <rect class="chip" x="106" y="0" width="90" height="26" rx="13"/><text class="m chipt" x="151" y="17" text-anchor="middle">FRAPPE</text>
      <rect class="chip" x="206" y="0" width="100" height="26" rx="13"/><text class="m chipt" x="256" y="17" text-anchor="middle">ERPNEXT</text>
      <rect class="chip" x="316" y="0" width="86" height="26" rx="13"/><text class="m chipt" x="359" y="17" text-anchor="middle">SAAS</text>
    </g>

    <rect x="0" y="{footer_y}" width="{W}" height="4" fill="url(#accent)" class="sweep"/>
    <rect width="{W}" height="{H}" rx="18" fill="none" stroke="{card_stroke}" stroke-width="1.5"/>
  </g>
</svg>
""".format(W=W, H=H, CYCLE=CYCLE, HUB_X=HUB_X, HUB_Y=HUB_Y,
           footer_y=H - 4, grid_lines=grid, net=net, rot=rot, **t)


def main():
    out = pathlib.Path("assets")
    out.mkdir(exist_ok=True)
    for theme_name, theme in THEMES.items():
        path = out / "hero-{}.svg".format(theme_name)
        path.write_text(build(theme), encoding="utf-8")
        print("wrote {}  ({:,} bytes)".format(path, path.stat().st_size))


if __name__ == "__main__":
    main()
