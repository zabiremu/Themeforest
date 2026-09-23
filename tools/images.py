"""Generates the placeholder illustrations used by the demo (original artwork, free to redistribute).
Run from the repo root: python3 tools/images.py
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "HTML", "assets", "images")

# Fills point at gradients defined in defs(); every SVG file carries its own copy.
LIME = "#C6F432"
DARK = {"body": "url(#gb)", "mid": "url(#gm)", "deep": "url(#gd)", "screen": "url(#gs)", "line": "#3A4254", "accent": LIME}
LIGHT = DARK  # products keep one finish; backgrounds do the contrast work


def defs(tone="dark"):
    body = ("#4A5263", "#1A1D25") if tone == "dark" else ("#F4F5F7", "#B9BEC8")
    mid = ("#6B7385", "#2F3542") if tone == "dark" else ("#DDE0E6", "#9EA4B0")
    return ('<defs>'
            f'<linearGradient id="gb" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{body[0]}"/><stop offset="1" stop-color="{body[1]}"/></linearGradient>'
            f'<linearGradient id="gm" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="{mid[0]}"/><stop offset="1" stop-color="{mid[1]}"/></linearGradient>'
            '<linearGradient id="gd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20242E"/><stop offset="1" stop-color="#0B0D12"/></linearGradient>'
            '<linearGradient id="gs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#232937"/><stop offset="1" stop-color="#0E1117"/></linearGradient>'
            '<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#0B0D12" flood-opacity=".28"/></filter>'
            '</defs>')


def product(kind, tone="dark"):
    """Product art with depth: gradient finish, soft shadow and a top sheen."""
    art = draw(kind)
    return (defs(tone) + '<ellipse cx="200" cy="364" rx="118" ry="10" fill="#0B0D12" opacity=".14"/>'
            f'<g filter="url(#sh)">{art}</g>'
            f'<g opacity=".5" style="mix-blend-mode:screen">{art.replace("url(#gb)", "url(#gl)").replace("url(#gm)", "none").replace("url(#gd)", "none").replace("url(#gs)", "none")}</g>')


def draw(kind, c=DARK):
    b, m, d, s, l, a = c["body"], c["mid"], c["deep"], c["screen"], c["line"], c["accent"]
    if kind == "headphones":
        return (f'<path d="M112 214V178a88 88 0 0 1 176 0v36" fill="none" stroke="{b}" stroke-width="16" stroke-linecap="round"/>'
                f'<rect x="146" y="226" width="12" height="40" rx="5" fill="{m}"/><rect x="242" y="226" width="12" height="40" rx="5" fill="{m}"/>'
                f'<rect x="82" y="200" width="64" height="112" rx="28" fill="{b}"/><rect x="98" y="216" width="32" height="80" rx="16" fill="{m}"/>'
                f'<rect x="254" y="200" width="64" height="112" rx="28" fill="{b}"/><rect x="270" y="216" width="32" height="80" rx="16" fill="{m}"/>'
                f'<circle cx="300" cy="300" r="4" fill="{a}"/>')
    if kind == "headphones-side":
        return (f'<rect x="186" y="46" width="28" height="140" rx="14" fill="{m}"/>'
                f'<ellipse cx="200" cy="250" rx="86" ry="104" fill="{b}"/><ellipse cx="200" cy="250" rx="58" ry="72" fill="{m}"/>'
                f'<circle cx="200" cy="250" r="16" fill="{a}" opacity=".75"/>')
    if kind == "headphones-case":
        return (f'<rect x="64" y="110" width="272" height="190" rx="95" fill="{b}"/>'
                f'<path d="M90 205h220" stroke="{m}" stroke-width="6" stroke-dasharray="12 8" stroke-linecap="round"/>'
                f'<rect x="300" y="188" width="44" height="34" rx="10" fill="{m}"/><circle cx="200" cy="160" r="5" fill="{a}"/>')
    if kind == "headphones-detail":
        return (f'<circle cx="200" cy="200" r="140" fill="{b}"/><circle cx="200" cy="200" r="104" fill="{m}"/>'
                f'<circle cx="200" cy="200" r="70" fill="{d}"/><circle cx="200" cy="200" r="30" fill="{a}" opacity=".7"/>'
                f'<circle cx="182" cy="182" r="9" fill="#fff" opacity=".5"/>')
    if kind == "earbuds":
        bud = (f'<ellipse cx="0" cy="0" rx="38" ry="44" fill="{b}"/><rect x="-12" y="28" width="24" height="72" rx="12" fill="{b}"/>'
               f'<ellipse cx="0" cy="-10" rx="18" ry="20" fill="{m}"/>')
        return (f'<g transform="translate(150 130) rotate(-16)">{bud}</g><g transform="translate(250 130) rotate(16)">{bud}</g>'
                f'<rect x="106" y="252" width="188" height="104" rx="48" fill="{b}"/>'
                f'<path d="M112 294h176" stroke="{m}" stroke-width="3"/><circle cx="200" cy="326" r="5" fill="{a}"/>')
    if kind == "phone":
        return (f'<rect x="130" y="50" width="140" height="300" rx="28" fill="{b}"/><rect x="140" y="60" width="120" height="280" rx="20" fill="{s}"/>'
                f'<rect x="182" y="70" width="36" height="10" rx="5" fill="{b}"/><rect x="156" y="98" width="88" height="88" rx="16" fill="{a}" opacity=".85"/>'
                f'<rect x="156" y="204" width="72" height="8" rx="4" fill="{l}"/><rect x="156" y="220" width="52" height="8" rx="4" fill="{l}"/>'
                f'<rect x="156" y="296" width="88" height="24" rx="12" fill="{l}"/>')
    if kind == "laptop":
        return (f'<rect x="84" y="92" width="232" height="156" rx="12" fill="{b}"/><rect x="96" y="104" width="208" height="132" rx="4" fill="{s}"/>'
                f'<rect x="112" y="120" width="84" height="64" rx="8" fill="{a}" opacity=".85"/><rect x="208" y="122" width="80" height="8" rx="4" fill="{l}"/>'
                f'<rect x="208" y="138" width="60" height="8" rx="4" fill="{l}"/><rect x="112" y="198" width="176" height="8" rx="4" fill="{l}"/>'
                f'<path d="M56 256h288l-14 22a8 8 0 0 1-7 4H77a8 8 0 0 1-7-4z" fill="{m}"/><rect x="172" y="256" width="56" height="6" rx="3" fill="{b}"/>')
    if kind == "watch":
        return (f'<rect x="160" y="40" width="80" height="112" rx="16" fill="{m}"/><rect x="160" y="248" width="80" height="112" rx="16" fill="{m}"/>'
                f'<rect x="138" y="120" width="124" height="160" rx="40" fill="{b}"/><rect x="152" y="134" width="96" height="132" rx="28" fill="{d}"/>'
                f'<circle cx="200" cy="200" r="30" fill="none" stroke="{a}" stroke-width="8" stroke-dasharray="130 200" stroke-linecap="round"/>'
                f'<rect x="262" y="176" width="12" height="28" rx="4" fill="{m}"/>')
    if kind == "speaker":
        dots = "".join(f'<circle cx="{150 + x * 20}" cy="{130 + y * 20}" r="4" fill="{m}"/>' for x in range(6) for y in range(9))
        return (f'<rect x="128" y="70" width="144" height="260" rx="72" fill="{b}"/>{dots}'
                f'<rect x="178" y="308" width="44" height="5" rx="2.5" fill="{a}"/>')
    if kind == "controller":
        return (f'<path d="M120 150h160c40 0 64 32 72 82l8 52c4 28-26 44-46 22l-34-38H120l-34 38c-20 22-50 6-46-22l8-52c8-50 32-82 72-82z" fill="{b}"/>'
                f'<rect x="104" y="202" width="52" height="16" rx="5" fill="{m}"/><rect x="122" y="184" width="16" height="52" rx="5" fill="{m}"/>'
                f'<circle cx="276" cy="190" r="11" fill="{a}"/><circle cx="298" cy="212" r="11" fill="{m}"/><circle cx="254" cy="212" r="11" fill="{m}"/><circle cx="276" cy="234" r="11" fill="{m}"/>'
                f'<circle cx="168" cy="262" r="18" fill="{d}"/><circle cx="232" cy="262" r="18" fill="{d}"/>')
    if kind == "tablet":
        return (f'<rect x="96" y="56" width="208" height="288" rx="24" fill="{b}"/><rect x="108" y="68" width="184" height="264" rx="14" fill="{s}"/>'
                f'<rect x="126" y="88" width="148" height="100" rx="12" fill="{a}" opacity=".85"/><rect x="126" y="204" width="110" height="8" rx="4" fill="{l}"/>'
                f'<rect x="126" y="220" width="80" height="8" rx="4" fill="{l}"/><rect x="126" y="248" width="68" height="60" rx="10" fill="{l}"/><rect x="206" y="248" width="68" height="60" rx="10" fill="{l}"/>')
    if kind == "camera":
        return (f'<rect x="86" y="116" width="64" height="32" rx="8" fill="{m}"/><rect x="60" y="136" width="280" height="172" rx="24" fill="{b}"/>'
                f'<circle cx="212" cy="222" r="68" fill="{m}"/><circle cx="212" cy="222" r="50" fill="{d}"/><circle cx="212" cy="222" r="26" fill="{a}" opacity=".6"/>'
                f'<circle cx="198" cy="208" r="8" fill="#fff" opacity=".6"/><rect x="92" y="162" width="36" height="16" rx="4" fill="{m}"/>')
    if kind == "keyboard":
        keys = "".join(f'<rect x="{62 + col * 24}" y="{158 + row * 24}" width="18" height="18" rx="4" fill="{a if (row, col) == (0, 11) else m}"/>'
                       for row in range(3) for col in range(12))
        return (f'<rect x="44" y="140" width="312" height="124" rx="16" fill="{b}"/>{keys}'
                f'<rect x="62" y="230" width="42" height="18" rx="4" fill="{m}"/><rect x="110" y="230" width="162" height="18" rx="4" fill="{m}"/><rect x="278" y="230" width="60" height="18" rx="4" fill="{m}"/>')
    if kind == "powerbank":
        return (f'<rect x="146" y="60" width="108" height="280" rx="26" fill="{b}"/><rect x="186" y="68" width="28" height="6" rx="3" fill="{m}"/>'
                + "".join(f'<circle cx="{176 + i * 16}" cy="300" r="5" fill="{a if i < 3 else m}"/>' for i in range(4)))
    if kind == "monitor":
        return (f'<rect x="56" y="70" width="288" height="180" rx="12" fill="{b}"/><rect x="68" y="82" width="264" height="148" rx="4" fill="{s}"/>'
                f'<rect x="84" y="98" width="120" height="72" rx="8" fill="{a}" opacity=".85"/><rect x="216" y="100" width="96" height="8" rx="4" fill="{l}"/>'
                f'<rect x="216" y="116" width="70" height="8" rx="4" fill="{l}"/><rect x="84" y="186" width="228" height="8" rx="4" fill="{l}"/>'
                f'<path d="M184 250h32l10 58h-52z" fill="{m}"/><rect x="136" y="304" width="128" height="12" rx="6" fill="{b}"/>')
    raise ValueError(kind)


def svg(w, h, inner, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<title>{title}</title>{inner}</svg>\n')


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)


PRODUCTS = ["headphones", "headphones-side", "headphones-case", "headphones-detail", "earbuds", "phone", "laptop",
            "watch", "speaker", "controller", "tablet", "camera", "keyboard", "powerbank", "monitor"]

for k in PRODUCTS:
    write(f"products/{k}.svg", svg(400, 400, product(k), k.replace("-", " ").title() + " placeholder"))

for name, k in [("audio", "headphones"), ("phones", "phone"), ("laptops", "laptop"), ("wearables", "watch"),
                ("gaming", "controller"), ("cameras", "camera")]:
    write(f"categories/{name}.svg", svg(400, 400, product(k), name.title() + " category placeholder"))

# Hero art
write("hero/hero-headphones.svg", svg(600, 450, '<g transform="translate(300 225) scale(1.35) translate(-200 -200)">' + product("headphones", "light") + '</g>', "Headphones placeholder"))
write("hero/laptop-on-dark.svg", svg(400, 400, product("laptop", "light"), "Laptop placeholder"))
write("hero/headphones-on-color.svg", svg(400, 400, product("headphones"), "Headphones placeholder"))

# Blog covers
covers = [("blog-1", "headphones", "#E6F7B0"), ("blog-2", "laptop", "#E4E4DE"), ("blog-3", "monitor", "#DCDDE3"),
          ("blog-4", "watch", "#EFE9DF"), ("blog-5", "camera", "#E4E4DE"), ("blog-6", "powerbank", "#E6F7B0")]
for name, k, bg in covers:
    inner = (f'<rect width="1200" height="750" fill="{bg}"/><circle cx="600" cy="375" r="250" fill="#fff" opacity=".55"/>'
             f'<g transform="translate(600 385) scale(1.55) translate(-200 -200)">{product(k)}</g>')
    write(f"blog/{name}.svg", svg(1200, 750, inner, "Blog cover placeholder"))

# Fictional brand wordmarks
brands = [("norvik", "NORVIK", "700", "4"), ("aurelo", "aurelo", "600", "0"), ("halden", "Halden", "500", "1"),
          ("tovera", "TOVERA", "600", "6"), ("pellan", "pellan.", "700", "-1"), ("vesso", "Vesso", "400", "2")]
for slug, text, weight, spacing in brands:
    inner = (f'<text x="120" y="50" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="30" '
             f'font-weight="{weight}" letter-spacing="{spacing}" fill="#16181D">{text}</text>')
    write(f"brands/{slug}.svg", svg(240, 80, inner, text + " placeholder logo"))

# Logo
def logo(color, mark):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 32" width="120" height="32" role="img"><title>Ohmly</title>'
            f'<path d="M3 28h7v-3.2a10.5 10.5 0 1 1 10 0V28h7" fill="none" stroke="{mark}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="35" y="24" font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="700" letter-spacing="-0.5" fill="{color}">ohmly</text></svg>\n')
def logo2(text, tile, mark):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 36" width="132" height="36" role="img"><title>Ohmly</title>'
            f'<rect width="36" height="36" rx="11" fill="{tile}"/>'
            f'<path d="M8.5 27h5.5v-3a8.2 8.2 0 1 1 8 0v3h5.5" fill="none" stroke="{mark}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="44" y="26" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" letter-spacing="-1" fill="{text}">ohmly</text></svg>\n')
write("logo.svg", logo2("#0D0E12", "#0D0E12", LIME))
write("logo-light.svg", logo2("#FFFFFF", LIME, "#0D0E12"))
write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#0D0E12"/>'
      '<path d="M7 25h5v-2.6a8 8 0 1 1 8 0V25h5" fill="none" stroke="#C6F432" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>\n')
print("images written")
