# -*- coding: utf-8 -*-
"""Generates the architecture diagram for the profile README.

One picture of the system this profile keeps talking about: tenants entering a
single Frappe/ERPNext deployment, an entitlement engine deciding what each of
them may touch, and a compliance path out to two tax authorities.

Shares its palette with gen_hero.py so both banners read as one design.
"""
import pathlib

from gen_hero import THEMES

W, H = 1200, 406

# ---- layout -----------------------------------------------------------------
COLS = [
    dict(x=56,  w=168, label="TENANTS"),
    dict(x=294, w=250, label="PLATFORM"),
    dict(x=614, w=226, label="CONTROL PLANE"),
    dict(x=910, w=234, label="EXTERNAL"),
]
TOP = 96            # first card's top edge
BOT = 290           # last card's bottom edge


def card(x, y, w, h, t, title, sub=None, accent=None, mono_title=False):
    """One rounded node box."""
    stroke = accent or t["card_stroke"]
    parts = [
        '<rect x="{}" y="{}" width="{}" height="{}" rx="10" fill="{}" stroke="{}" '
        'stroke-width="1.4"/>'.format(x, y, w, h, t["chip"], stroke)
    ]
    cls = "m" if mono_title else "f"
    if sub:
        parts.append('<text class="{} ct" x="{}" y="{}">{}</text>'.format(
            cls, x + w / 2, y + h / 2 - 4, title))
        parts.append('<text class="m cs" x="{}" y="{}">{}</text>'.format(
            x + w / 2, y + h / 2 + 14, sub))
    else:
        parts.append('<text class="{} ct" x="{}" y="{}">{}</text>'.format(
            cls, x + w / 2, y + h / 2 + 5, title))
    return "".join(parts)


def link(x1, y1, x2, y2, delay=0.0, curve=True):
    """Animated dashed connector; gentle S-curve between columns."""
    if curve and abs(y1 - y2) > 2:
        mx = (x1 + x2) / 2
        d = "M{},{} C{},{} {},{} {},{}".format(x1, y1, mx, y1, mx, y2, x2, y2)
    else:
        d = "M{},{} L{},{}".format(x1, y1, x2, y2)
    return ('<path class="wire" d="{}" style="animation-delay:{:.2f}s" '
            'marker-end="url(#arrow)"/>'.format(d, delay))


def build(t, key):
    c1, c2, c3, c4 = COLS

    # column 1 - three tenants
    tenants = []
    ty = TOP
    for i, name in enumerate(("Tenant A", "Tenant B", "Tenant C")):
        tenants.append(card(c1["x"], ty, c1["w"], 54, t, name, mono_title=True))
        ty += 70

    # column 2 - the single deployment everyone shares
    core = card(c2["x"], TOP, c2["w"], BOT - TOP, t, "", accent=t["a2"])
    core += (
        '<text class="f nt" x="{cx}" y="{y1}">Frappe / ERPNext</text>'
        '<text class="m ns" x="{cx}" y="{y2}">one deployment</text>'
        '<rect x="{bx}" y="{by}" width="{bw}" height="46" rx="8" fill="{a2f}" stroke="{a2}" stroke-width="1.2"/>'
        '<text class="f bt" x="{cx}" y="{bty}">SaaS Control Layer</text>'
    ).format(
        cx=c2["x"] + c2["w"] / 2, y1=TOP + 56, y2=TOP + 78,
        bx=c2["x"] + 24, by=TOP + 108, bw=c2["w"] - 48,
        bty=TOP + 136, a2=t["a2"], a2f=t["a2fill"],
    )

    # column 3 - the two things the control layer actually does
    ent = card(c3["x"], TOP, c3["w"], 89, t, "Entitlement Engine",
               "plans - modules - features", accent=t["a1"])
    inv = card(c3["x"], 201, c3["w"], 89, t, "E-Invoicing Gateway",
               "serialise - sign - reconcile", accent=t["a3"])

    # column 4 - everything outside the box
    stripe = card(c4["x"], TOP, c4["w"], 89, t, "Stripe",
                  "subscriptions - webhooks", accent=t["a1"])
    eta = card(c4["x"], 201, c4["w"], 38, t, "ETA - Egypt", mono_title=True, accent=t["a3"])
    zat = card(c4["x"], 252, c4["w"], 38, t, "ZATCA - Saudi Arabia", mono_title=True, accent=t["a3"])

    # wires
    c1r, c2l = c1["x"] + c1["w"], c2["x"]
    c2r, c3l = c2["x"] + c2["w"], c3["x"]
    c3r, c4l = c3["x"] + c3["w"], c4["x"]
    mid = (TOP + BOT) / 2
    wires = "".join([
        link(c1r, TOP + 27, c2l, mid - 30, 0.0),
        link(c1r, TOP + 97, c2l, mid, 0.35),
        link(c1r, TOP + 167, c2l, mid + 30, 0.70),
        link(c2r, mid - 34, c3l, TOP + 44, 0.20),
        link(c2r, mid + 34, c3l, 245, 0.55),
        link(c3r, TOP + 44, c4l, TOP + 44, 0.40, curve=False),
        link(c3r, 245, c4l, 220, 0.75),
        link(c3r, 245, c4l, 271, 0.95),
    ])

    labels = "".join(
        '<text class="m eyebrow" x="{}" y="68">{}</text>'.format(c["x"], c["label"])
        for c in COLS
    )

    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Architecture: tenants enter one Frappe/ERPNext deployment; a SaaS control layer applies entitlements and routes signed invoices to the Egyptian ETA and Saudi ZATCA portals">
  <title>Multi-tenant SaaS and e-invoicing architecture</title>
  <defs>
    <linearGradient id="bgA{key}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg0}"/><stop offset="60%" stop-color="{bg1}"/><stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">
      <path d="M0,1 L9,5 L0,9 z" fill="{a2}"/>
    </marker>
    <clipPath id="fr{key}"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <style>
      .f {{ font-family:'Segoe UI', Inter, system-ui, Ubuntu, 'Helvetica Neue', Arial, sans-serif; }}
      .m {{ font-family: ui-monospace,'Cascadia Code','SF Mono', Menlo, Consolas, monospace; }}
      .eyebrow {{ fill:{muted}; font-size:11px; font-weight:600; letter-spacing:2.6px; }}
      .ct {{ fill:{name}; font-size:14px; font-weight:600; text-anchor:middle; }}
      .cs {{ fill:{muted}; font-size:10.5px; text-anchor:middle; letter-spacing:.3px; }}
      .nt {{ fill:{name}; font-size:19px; font-weight:700; text-anchor:middle; }}
      .ns {{ fill:{muted}; font-size:11px; text-anchor:middle; letter-spacing:.6px; }}
      .bt {{ fill:{a2}; font-size:14.5px; font-weight:700; text-anchor:middle; }}
      .note {{ fill:{muted}; font-size:12.5px; }}
      .accent {{ fill:{a2}; font-size:12.5px; font-weight:600; }}
      .wire {{ fill:none; stroke:{a2}; stroke-width:1.7; stroke-opacity:.75;
               stroke-dasharray:5 9; animation: flow 2.4s linear infinite; }}
      @keyframes flow {{ to {{ stroke-dashoffset:-28; }} }}
      @media (prefers-reduced-motion: reduce) {{ .wire {{ animation:none; }} }}
    </style>
  </defs>
  <g clip-path="url(#fr{key})">
    <rect width="{W}" height="{H}" fill="url(#bgA{key})"/>
    {labels}
    {wires}
    {tenants}{core}{ent}{inv}{stripe}{eta}{zat}
    <text class="f note" x="56" y="352">Every gate above is enforced <tspan class="accent">server-side</tspan>. Hiding a button in the UI is not access control.</text>
    <text class="m note" x="56" y="380" font-size="11.5">one deployment &#183; N tenants &#183; per-tenant entitlements &#183; two tax authorities &#183; zero trust in the browser</text>
    <rect width="{W}" height="{H}" rx="18" fill="none" stroke="{card_stroke}" stroke-width="1.5"/>
  </g>
</svg>
""".format(W=W, H=H, key=key, labels=labels, wires=wires, tenants="".join(tenants),
           core=core, ent=ent, inv=inv, stripe=stripe, eta=eta, zat=zat, **t)


def main():
    out = pathlib.Path("assets")
    out.mkdir(exist_ok=True)
    for key, theme in THEMES.items():
        t = dict(theme)
        # translucent fill behind the control-layer pill
        t["a2fill"] = "#11301F" if key == "dark" else "#E4F6EE"
        p = out / "architecture-{}.svg".format(key)
        p.write_text(build(t, key), encoding="utf-8")
        print("wrote {}  ({:,} bytes)".format(p, p.stat().st_size))


if __name__ == "__main__":
    main()
