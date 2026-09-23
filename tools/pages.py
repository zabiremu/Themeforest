"""Builds every page in HTML/ from shared parts, so header, footer and components stay identical.
This is an authoring tool only; buyers edit the finished HTML files directly.
Run from the repo root: python3 tools/pages.py
"""
import os
import re

OUT = os.environ.get("OHMLY_OUT") or os.path.join(os.path.dirname(__file__), "..", "HTML")
DEMO = os.path.join(os.path.dirname(__file__), "..", "HTML", "assets", "images", "demo")
# Set OHMLY_PLACEHOLDERS=1 to ignore demo photos (used when packaging for ThemeForest).
USE_PHOTOS = os.environ.get("OHMLY_PLACEHOLDERS") != "1"


# Live-demo photos from Unsplash (free under the Unsplash License). Hotlinked, never bundled:
# the ThemeForest package is built with OHMLY_PLACEHOLDERS=1 and keeps the SVG artwork.
# A local file in assets/images/demo/<folder>/<name>.jpg wins over the entry here.
UNSPLASH = {
    "products/headphones": "photo-1618366712010-f4ae9c647dcb",
    "products/headphones-side": "photo-1583394838336-acd977736f90",
    "products/headphones-case": "photo-1599669454515-1b2e0173f302",
    "products/headphones-detail": "photo-1590658268037-6bf12165a8df",
    "products/earbuds": "photo-1632200004922-bc18602c79fc",
    "products/phone": "photo-1511707171634-5f897ff02aa9",
    "products/laptop": "photo-1496181133206-80ce9b88a853",
    "products/watch": "photo-1624096104992-9b4fa3a279dd",
    "products/speaker": "photo-1608043152269-423dbba4e7e1",
    "products/controller": "photo-1683137813509-e107c398d02b",
    "products/tablet": "photo-1544244015-0df4b3ffc6b0",
    "products/camera": "photo-1526170375885-4d8ecf77b99f",
    "products/keyboard": "photo-1587829741301-dc798b83add3",
    "products/powerbank": "photo-1745889763764-a13bc5028c4d",
    "products/monitor": "photo-1527443224154-c4a3942d3acf",
    "categories/audio": "photo-1618366712010-f4ae9c647dcb",
    "categories/phones": "photo-1511707171634-5f897ff02aa9",
    "categories/laptops": "photo-1496181133206-80ce9b88a853",
    "categories/wearables": "photo-1624096104992-9b4fa3a279dd",
    "categories/gaming": "photo-1683137813509-e107c398d02b",
    "categories/cameras": "photo-1526170375885-4d8ecf77b99f",
    "hero/hero-headphones": "photo-1585298723682-7115561c51b7",
    "hero/laptop-on-dark": "photo-1496181133206-80ce9b88a853",
    "hero/headphones-on-color": "photo-1583394838336-acd977736f90",
    "blog/blog-1": "photo-1505740420928-5e560c06d30e",
    "blog/blog-2": "photo-1496181133206-80ce9b88a853",
    "blog/blog-3": "photo-1527443224154-c4a3942d3acf",
    "blog/blog-4": "photo-1579586337278-3befd40fd17a",
    "blog/blog-5": "photo-1526170375885-4d8ecf77b99f",
    "blog/blog-6": "photo-1546435770-a3e426bf472b",
}


PORTRAIT = {"hero/headphones-on-color"}  # slots shown in a tall frame


def unsplash(photo_id, folder, name=""):
    size = "w=1200&h=750" if folder in ("blog", "hero") else "w=800&h=800"
    if f"{folder}/{name}" in PORTRAIT:
        size = "w=900&h=1100"
    return f"https://images.unsplash.com/{photo_id}?{size}&fit=crop&crop=entropy&auto=format&q=75"


def use_demo_photos(html):
    """Swap placeholder SVGs for real photos on the live demo.
    The SVG stays as data-fallback, so a photo that fails to load shows the artwork instead."""
    if not USE_PHOTOS:
        return html

    def swap(m):
        folder, name = m.group(1), m.group(2)
        svg = m.group(0)
        for ext in ("webp", "jpg", "jpeg", "png", "avif"):
            if os.path.exists(os.path.join(DEMO, folder, f"{name}.{ext}")):
                return f'src="assets/images/demo/{folder}/{name}.{ext}" data-photo data-fallback="{svg[5:-1]}"'
        key = f"{folder}/{name}"
        if key in UNSPLASH:
            return f'src="{unsplash(UNSPLASH[key], folder, name).replace("&", "&amp;")}" data-photo data-fallback="{svg[5:-1]}"'
        return svg
    html = re.sub(r'(?<![-\w])src="assets/images/(products|categories|hero|blog)/([a-z0-9-]+)\.svg"', swap, html)

    def swap_gallery(m):  # gallery thumbnails carry the big image in data-src
        key = f"{m.group(1)}/{m.group(2)}"
        return f'data-src="{unsplash(UNSPLASH[key], m.group(1)).replace("&", "&amp;")}"' if key in UNSPLASH else m.group(0)
    return re.sub(r'data-src="assets/images/(products)/([a-z0-9-]+)\.svg"', swap_gallery, html)
BRAND = "Ohmly"
IMG = "assets/images"


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true"><use href="#i-{name}"></use></svg>'


# ---------------------------------------------------------------- data
P = {
    "aero": dict(name="Aero Wireless Headphones", cat="Headphones", img="headphones", price=119, was=149, badge="-20%", rating=4.7, reviews=128,
                 specs=[("Battery", "30 h"), ("Weight", "250 g")], desc="Adaptive noise cancelling and 40 mm drivers in a light, foldable frame."),
    "pulse": dict(name="Pulse Earbuds", cat="Earbuds", img="earbuds", price=79, badge="New", rating=4.5, reviews=96,
                  specs=[("Battery", "8 h + 24 h"), ("Water", "IPX4")], desc="Compact earbuds with active noise cancelling and a pocket-size case."),
    "nova": dict(name="Nova X Phone", cat="Phones", img="phone", price=699, rating=4.8, reviews=212,
                 specs=[("Screen", "6.4 in"), ("Storage", "256 GB")], desc="A bright 120 Hz display, all-day battery and a triple camera."),
    "slate": dict(name="Slate 14 Laptop", cat="Laptops", img="laptop", price=1149, was=1299, badge="-12%", rating=4.6, reviews=74,
                  specs=[("Memory", "16 GB"), ("Weight", "1.3 kg")], desc="A 14-inch laptop with an 8-core processor and a full-day battery."),
    "orbit": dict(name="Orbit Smartwatch", cat="Wearables", img="watch", price=249, rating=4.4, reviews=58,
                  specs=[("Battery", "7 days"), ("Case", "44 mm")], desc="Heart rate, sleep and GPS tracking with a week between charges."),
    "echo": dict(name="Echo Mini Speaker", cat="Speakers", img="speaker", price=89, was=109, badge="-18%", rating=4.5, reviews=143,
                 specs=[("Battery", "12 h"), ("Output", "20 W")], desc="A water-resistant speaker with full, clear sound for its size."),
    "vector": dict(name="Vector Controller", cat="Gaming", img="controller", price=59, rating=4.3, reviews=87,
                   specs=[("Latency", "4 ms"), ("Battery", "40 h")], desc="Low-latency wireless controller for PC, console and mobile."),
    "lumen": dict(name="Lumen Tablet 11", cat="Tablets", img="tablet", price=429, badge="New", rating=4.6, reviews=65,
                  specs=[("Screen", "11 in"), ("Storage", "128 GB")], desc="An 11-inch tablet for reading, drawing and streaming."),
    "frame": dict(name="Frame M6 Camera", cat="Cameras", img="camera", price=899, rating=4.7, reviews=39,
                  specs=[("Sensor", "26 MP"), ("Video", "4K 60p")], desc="A mirrorless camera with fast autofocus and in-body stabilization."),
    "key75": dict(name="Key75 Keyboard", cat="Accessories", img="keyboard", price=129, rating=4.5, reviews=51,
                  specs=[("Layout", "75%"), ("Switches", "Linear")], desc="A compact mechanical keyboard with hot-swappable switches."),
    "drift": dict(name="Drift Power Bank", cat="Accessories", img="powerbank", price=49, was=59, badge="-17%", rating=4.4, reviews=110,
                  specs=[("Capacity", "20,000 mAh"), ("Output", "65 W")], desc="Charges a laptop, phone and earbuds at the same time."),
    "arc": dict(name="Arc 27 Monitor", cat="Monitors", img="monitor", price=329, rating=4.6, reviews=47,
                specs=[("Size", "27 in"), ("Refresh", "165 Hz")], desc="A 27-inch QHD monitor with a height-adjustable stand."),
}
ALL = list(P)
POSTS = [
    ("How to choose noise-cancelling headphones", "Guides", "blog-1", "Sep 12, 2026", "6 min read",
     "What the numbers on the box mean, and which ones you can ignore."),
    ("Laptop specs explained: what actually matters", "Guides", "blog-2", "Sep 5, 2026", "8 min read",
     "Processor, memory and storage in plain language, with real examples."),
    ("A two-monitor desk that stays tidy", "Setups", "blog-3", "Aug 28, 2026", "5 min read",
     "Cable routing, stands and the one adapter that fixed everything."),
    ("Smartwatch battery life, tested for 7 days", "Reviews", "blog-4", "Aug 21, 2026", "7 min read",
     "We wore four watches for a week and logged every charge."),
    ("Mirrorless cameras for beginners", "Guides", "blog-5", "Aug 14, 2026", "9 min read",
     "Sensor size, lenses and the settings to learn first."),
    ("The power bank that charges a laptop", "Reviews", "blog-6", "Aug 7, 2026", "4 min read",
     "Why 65 W output matters, and how long a charge really lasts."),
]


def fmt(n):
    return f"${n:,.2f}" if n % 1 else f"${n:,}"


# ---------------------------------------------------------------- components
def stars(rating):
    full = round(rating)
    s = "".join(icon("star", "" if i < full else "is-empty") for i in range(5))
    return f'<span class="rating__stars" aria-hidden="true">{s}</span>'


def rating_line(p):
    return (f'<p class="rating">{stars(p["rating"])}<span>{p["rating"]}<span class="visually-hidden"> out of 5,</span> '
            f'({p["reviews"]}<span class="visually-hidden"> reviews</span>)</span></p>')


def price(p, size=""):
    cls = "price" + (" price--sale" if p.get("was") else "") + (f" price--{size}" if size else "")
    was = f'<del class="price__was"><span class="visually-hidden">Original price: </span>{fmt(p["was"])}</del>' if p.get("was") else ""
    label = '<span class="visually-hidden">Sale price: </span>' if p.get("was") else ""
    return f'<p class="{cls}"><ins class="price__now">{label}{fmt(p["price"])}</ins>{was}</p>'


def spec_list(specs, cls="spec-list"):
    rows = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in specs)
    return f'<dl class="{cls}">{rows}</dl>'


def badge(p):
    b = p.get("badge")
    if not b:
        return ""
    kind = "new" if b == "New" else "sale"
    return f'<span class="badge badge--{kind}">{b}</span>'


def card(key):
    p = P[key]
    return f"""
<!-- Product Card Start -->
<article class="product-card">
  <a class="product-card__media" href="product-details.html" tabindex="-1">
    <img src="{IMG}/products/{p['img']}.svg" alt="{p['name']}" width="400" height="400" loading="lazy">
    {badge(p)}
  </a>
  <div class="product-card__actions">
    <button class="icon-btn" type="button" data-wishlist aria-pressed="false" aria-label="Save {p['name']} to wishlist">{icon('heart')}</button>
    <button class="icon-btn" type="button" data-quick-view aria-label="Quick view: {p['name']}">{icon('eye')}</button>
    <a class="icon-btn" href="compare.html" aria-label="Compare {p['name']}">{icon('compare')}</a>
  </div>
  <div class="product-card__body">
    <p class="product-card__cat">{p['cat']}</p>
    <h3 class="product-card__title"><a href="product-details.html">{p['name']}</a></h3>
    {rating_line(p)}
    <p class="product-card__desc">{p['desc']}</p>
    {spec_list(p['specs'])}
    <div class="product-card__footer">
      {price(p)}
      <button class="btn btn--primary btn--sm" type="button" data-add-to-cart>Add to cart</button>
    </div>
  </div>
</article>
<!-- Product Card End -->"""


def grid(keys, cls="product-grid", extra=""):
    return f'<div class="{cls}"{extra}>' + "".join(card(k) for k in keys) + "</div>"


def breadcrumb(items):
    lis = []
    for label, href in items[:-1]:
        lis.append(f'<li><a href="{href}">{label}</a></li>')
    lis.append(f'<li><span aria-current="page">{items[-1][0]}</span></li>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def page_banner(title, crumbs, text=""):
    t = f"<p>{text}</p>" if text else ""
    return f"""
<!-- Page Banner Start -->
<section class="page-banner">
  <div class="container">
    {breadcrumb([('Home', 'index.html')] + crumbs + [(title, '')])}
    <h1>{title}</h1>
    {t}
  </div>
</section>
<!-- Page Banner End -->"""


def qty(value=1, small=False, label="Quantity"):
    s = " qty--sm" if small else ""
    return (f'<div class="qty{s}" data-qty><button type="button" data-qty-minus aria-label="Decrease quantity">{icon("minus")}</button>'
            f'<input type="number" value="{value}" min="1" max="99" inputmode="numeric" aria-label="{label}">'
            f'<button type="button" data-qty-plus aria-label="Increase quantity">{icon("plus")}</button></div>')


def field(id_, label, type_="text", required=True, auto="", extra="", full=False, hint=""):
    req = ' <span class="req" aria-hidden="true">*</span>' if required else ""
    r = " required" if required else ""
    a = f' autocomplete="{auto}"' if auto else ""
    f = " full" if full else ""
    h = f'<p class="field-hint" id="{id_}-hint">{hint}</p>' if hint else ""
    db = f' aria-describedby="{id_}-hint"' if hint else ""
    if type_ == "textarea":
        ctl = f'<textarea class="form-control" id="{id_}" name="{id_}" rows="5"{r}{extra}></textarea>'
    else:
        ctl = f'<input class="form-control" id="{id_}" name="{id_}" type="{type_}"{a}{r}{db}{extra}>'
    return f'<div class="field{f}"><label class="field-label" for="{id_}">{label}{req}</label>{ctl}{h}</div>'


def section_head(title, text="", right="", tag="h2", id_="", eyebrow=""):
    i = f' id="{id_}"' if id_ else ""
    t = f"<p>{text}</p>" if text else ""
    e = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f'<div class="section-head"><div>{e}<{tag}{i}>{title}</{tag}>{t}</div>{right}</div>'


def services():
    items = [("truck", "Free shipping over $99", "Delivered in 2 to 4 business days."),
             ("return", "30-day returns", "Changed your mind? Send it back for free."),
             ("shield", "2-year warranty", "Every product, repaired or replaced."),
             ("support", "Real product advice", "Talk to our team 7 days a week.")]
    lis = "".join(f'<div class="services__item">{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in items)
    return f"""
<!-- Services Start -->
<section class="section section--tight section--surface" aria-label="Store services">
  <div class="container"><div class="services">{lis}</div></div>
</section>
<!-- Services End -->"""


def brands():
    names = [("norvik", "Norvik"), ("aurelo", "Aurelo"), ("halden", "Halden"), ("tovera", "Tovera"), ("pellan", "Pellan"), ("vesso", "Vesso")]
    items = "".join(f'<a href="shop.html"><img src="{IMG}/brands/{s}.svg" alt="{n}" width="240" height="80" loading="lazy"></a>' for s, n in names)
    return f"""
<!-- Brands Start -->
<section class="section section--tight" aria-labelledby="brands-title">
  <div class="container">
    {section_head('Brands we carry', right='<a class="text-btn" href="shop.html">Shop by brand</a>', id_='brands-title', eyebrow='Official retailer')}
    <div class="brands">{items}</div>
  </div>
</section>
<!-- Brands End -->"""


def ticker(items=None):
    items = items or ["Free shipping over $99", "2-year warranty", "30-day returns", "Specs on every card", "Price match promise", "Pay in 4 at checkout"]
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"""
<!-- Ticker Start -->
<div class="ticker" aria-label="Store promises"><div class="ticker__track"><ul>{lis}</ul><ul aria-hidden="true">{lis}</ul></div></div>
<!-- Ticker End -->"""


def newsletter_band():
    return f"""
<!-- Newsletter Start -->
<section class="section section--tight" aria-labelledby="newsletter-title">
  <div class="container">
    <div class="newsletter-band">
      <div>
        <p class="eyebrow eyebrow--dark">Newsletter</p>
        <h2 id="newsletter-title">Get <span class="mark">10% off</span> your first order</h2>
        <p>New arrivals, honest reviews and member-only deals, twice a month.</p>
      </div>
      <form class="newsletter-form" action="#" data-validate data-success="Thanks for subscribing. Your code is on its way.">
        <label class="visually-hidden" for="band-email">Email address</label>
        <input class="form-control" id="band-email" name="email" type="email" autocomplete="email" placeholder="Email address" required>
        <button class="btn btn--primary" type="submit">Subscribe</button>
      </form>
    </div>
  </div>
</section>
<!-- Newsletter End -->"""


def post_card(post, heading="h3"):
    title, cat, img, date, read, excerpt = post
    return f"""
<article class="post-card">
  <a class="post-card__media" href="blog-details.html" tabindex="-1"><img src="{IMG}/blog/{img}.svg" alt="" width="1200" height="750" loading="lazy"></a>
  <p class="post-card__meta"><a href="blog.html">{cat}</a><span>{date}</span><span>{read}</span></p>
  <{heading}><a href="blog-details.html">{title}</a></{heading}>
  <p>{excerpt}</p>
</article>"""


# ---------------------------------------------------------------- shell
SPRITE = """<svg class="sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
  <symbol id="i-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/></symbol>
  <symbol id="i-heart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7.5-4.4-7.5-10A4.2 4.2 0 0 1 12 7.6 4.2 4.2 0 0 1 19.5 10c0 5.6-7.5 10-7.5 10z"/></symbol>
  <symbol id="i-bag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 8h13l-1 12.5h-11z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></symbol>
  <symbol id="i-user" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></symbol>
  <symbol id="i-chevron-down" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></symbol>
  <symbol id="i-chevron-left" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></symbol>
  <symbol id="i-chevron-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></symbol>
  <symbol id="i-arrow-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5.5l6.5 6.5-6.5 6.5"/></symbol>
  <symbol id="i-arrow-up" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5.5 11.5L12 5l6.5 6.5"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></symbol>
  <symbol id="i-minus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M5 12h14"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3l-5.6 2.9 1.1-6.2L3 9.6l6.2-.9z"/></symbol>
  <symbol id="i-eye" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/></symbol>
  <symbol id="i-compare" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4v16M4 7l3-3 3 3M17 20V4M14 17l3 3 3-3"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
  <symbol id="i-truck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6.5h11v10H3zM14 10h4l3 3.5v3h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/></symbol>
  <symbol id="i-return" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 1 0 2.5-5.8"/><path d="M4 4.5v4.5h4.5"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 8.1-8 9-4.6-.9-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></symbol>
  <symbol id="i-support" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><path d="M4 14h3v6H5.5A1.5 1.5 0 0 1 4 18.5zM20 14h-3v6h1.5a1.5 1.5 0 0 0 1.5-1.5z"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></symbol>
  <symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h3.5l2 5-2.5 1.5a11 11 0 0 0 5.5 5.5L15 13.5l5 2V19a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2z"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
  <symbol id="i-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7.5a4 4 0 0 1 8 0V11"/></symbol>
  <symbol id="i-grid" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></symbol>
  <symbol id="i-list" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r=".75" fill="currentColor"/><circle cx="4.5" cy="12" r=".75" fill="currentColor"/><circle cx="4.5" cy="18" r=".75" fill="currentColor"/></symbol>
  <symbol id="i-trash" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></symbol>
  <symbol id="i-filter" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 6h16M7 12h10M10 18h4"/></symbol>
  </defs>
</svg>"""


def nav(current):
    def link(href, label):
        ac = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{ac}>{label}</a>'

    def top(href, label):
        ac = ' aria-current="page"' if href == current else ""
        return f'<a class="main-nav__link" href="{href}"{ac}>{label}</a>'

    def toggle(label):
        return f'<button class="submenu-toggle" type="button" aria-expanded="false" aria-label="Show {label} menu">{icon("chevron-down")}</button>'

    homes = "".join(f"<li>{link(h, l)}</li>" for h, l in [("index.html", "Home 1: Annotated hero"), ("index-2.html", "Home 2: Editorial"), ("index-3.html", "Home 3: Category mosaic")])
    pages = "".join(f"<li>{link(h, l)}</li>" for h, l in [
        ("about.html", "About"), ("faq.html", "FAQ"), ("order-tracking.html", "Order tracking"), ("compare.html", "Compare"),
        ("wishlist.html", "Wishlist"), ("my-account.html", "My account"), ("login.html", "Log in"), ("register.html", "Register"),
        ("forgot-password.html", "Forgot password"), ("order-complete.html", "Order complete"), ("404.html", "404"), ("coming-soon.html", "Coming soon")])
    cols = [("Audio", ["Headphones", "Earbuds", "Speakers", "Soundbars"]), ("Mobile", ["Phones", "Tablets", "Smartwatches", "Chargers"]),
            ("Computing", ["Laptops", "Monitors", "Keyboards", "Storage"]), ("Shop pages", None)]
    mega = ""
    for title, items in cols:
        if items:
            lis = "".join(f'<li><a href="shop.html">{i}</a></li>' for i in items)
        else:
            lis = "".join(f"<li>{link(h, l)}</li>" for h, l in [("shop.html", "Shop grid"), ("shop-list.html", "Shop list"), ("shop-fullwidth.html", "Shop full width"),
                                                              ("product-details.html", "Product details"), ("cart.html", "Cart"), ("checkout.html", "Checkout")])
        mega += f'<div><p class="mega-menu__title">{title}</p><ul>{lis}</ul></div>'
    mega += (f'<a class="mega-promo" href="product-details.html"><img src="{IMG}/products/headphones.svg" alt="" width="400" height="400" loading="lazy">'
             f'<span><strong>Aero Wireless Headphones</strong><span class="text-muted">30 h battery, now $119</span></span></a>')
    return f"""
<nav class="main-nav" aria-label="Main">
  <ul class="main-nav__list">
    <li class="main-nav__item has-dropdown">{top('index.html', 'Home')}{toggle('Home')}<ul class="dropdown">{homes}</ul></li>
    <li class="main-nav__item has-mega">{top('shop.html', 'Shop')}{toggle('Shop')}<div class="mega-menu">{mega}</div></li>
    <li class="main-nav__item has-dropdown"><a class="main-nav__link" href="about.html">Pages</a>{toggle('Pages')}<ul class="dropdown">{pages}</ul></li>
    <li class="main-nav__item">{top('blog.html', 'Blog')}</li>
    <li class="main-nav__item">{top('contact.html', 'Contact')}</li>
  </ul>
</nav>"""


def header(current):
    return f"""
<!-- Header Start -->
<header class="site-header">
  <div class="top-bar">
    <div class="container top-bar__inner">
      <p>Free shipping on orders over $99</p>
      <ul class="top-bar__links">
        <li><a href="order-tracking.html">Track order</a></li>
        <li><a href="faq.html">Help</a></li>
      </ul>
    </div>
  </div>
  <div class="site-header__main">
    <div class="container site-header__inner">
      <button class="icon-btn menu-toggle" type="button" data-open-drawer="mobile-menu" aria-label="Open menu">{icon('menu')}</button>
      <a class="site-header__logo" href="index.html"><img src="{IMG}/logo.svg" alt="{BRAND} home" width="132" height="36"></a>
      {nav(current)}
      <div class="header-actions">
        <form class="header-search" action="shop.html" role="search">
          <label class="visually-hidden" for="header-search-input">Search products</label>
          <input id="header-search-input" type="search" name="q" placeholder="Search products">
          <button type="submit" aria-label="Search">{icon('search')}</button>
        </form>
        <button class="icon-btn search-toggle" type="button" data-search-toggle aria-expanded="false" aria-label="Show search">{icon('search')}</button>
        <a class="icon-btn account-link" href="my-account.html" aria-label="My account">{icon('user')}</a>
        <a class="icon-btn" href="wishlist.html" aria-label="Wishlist">{icon('heart')}<span class="count" data-wishlist-count>3</span></a>
        <a class="icon-btn" href="cart.html" data-open-cart aria-label="Cart">{icon('bag')}<span class="count" data-cart-count>3</span></a>
      </div>
    </div>
  </div>
</header>
<!-- Header End -->"""


def footer():
    shop = "".join(f'<li><a href="shop.html">{i}</a></li>' for i in ["Headphones", "Phones", "Laptops", "Wearables", "Gaming", "Deals"])
    help_ = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in [("order-tracking.html", "Track your order"), ("faq.html", "Shipping and returns"),
                                                                 ("faq.html#warranty", "Warranty"), ("contact.html", "Contact us"), ("my-account.html", "My account")])
    return f"""
<!-- Footer Start -->
<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div class="footer-widget">
        <img class="footer-logo" src="{IMG}/logo-light.svg" alt="{BRAND}" width="132" height="36" loading="lazy">
        <p>Electronics picked, tested and explained, with specs you can compare at a glance.</p>
        <ul class="social-links">
          <li><a href="#">Instagram</a></li><li><a href="#">YouTube</a></li><li><a href="#">Facebook</a></li><li><a href="#">X</a></li>
        </ul>
      </div>
      <div class="footer-widget"><h2>Shop</h2><ul>{shop}</ul></div>
      <div class="footer-widget"><h2>Help</h2><ul>{help_}</ul></div>
      <div class="footer-widget">
        <h2>Stay in the loop</h2>
        <p>New arrivals and deals, twice a month.</p>
        <form class="newsletter-form" action="#" data-validate data-success="Thanks for subscribing.">
          <label class="visually-hidden" for="footer-email">Email address</label>
          <input class="form-control" id="footer-email" name="email" type="email" autocomplete="email" placeholder="Email address" required>
          <button class="btn btn--primary" type="submit">Subscribe</button>
        </form>
        <ul class="footer-contact">
          <li>{icon('phone')}<a href="tel:+15550142000">+1 (555) 014-2000</a></li>
          <li>{icon('mail')}<a href="mailto:hello@example.com">hello@example.com</a></li>
        </ul>
      </div>
    </div>
  </div>
  <p class="site-footer__wordmark" aria-hidden="true">{BRAND.lower()}</p>
  <div class="container site-footer__bottom">
    <p>&copy; 2026 {BRAND}. All rights reserved.</p>
    <p class="secure-note">{icon('lock')}Secure checkout</p>
    <ul><li><a href="faq.html">Privacy</a></li><li><a href="faq.html">Terms</a></li></ul>
  </div>
</footer>
<!-- Footer End -->"""


def mini_cart():
    items = [("aero", 1), ("pulse", 1), ("drift", 1)]
    lis = "".join(f'<li class="mini-cart-item" data-price="{P[k]["price"] * q}"><a class="mini-cart-item__media" href="product-details.html"><img src="{IMG}/products/{P[k]["img"]}.svg" alt="" width="400" height="400" loading="lazy"></a>'
                  f'<div class="mini-cart-item__info"><h3><a href="product-details.html">{P[k]["name"]}</a></h3><p>Qty {q}</p></div>'
                  f'<div class="mini-cart-item__end"><strong>{fmt(P[k]["price"] * q)}</strong>'
                  f'<button class="mini-cart-item__remove" type="button" data-remove-item aria-label="Remove {P[k]["name"]}">{icon("trash")}</button></div></li>' for k, q in items)
    return f"""
<!-- Mini Cart Start -->
<div class="drawer cart-drawer" id="cart-drawer" role="dialog" aria-modal="true" aria-labelledby="cart-drawer-title">
  <div class="drawer__head">
    <h2 id="cart-drawer-title">Your cart <span class="cart-drawer__count" data-cart-count>3</span></h2>
    <button class="icon-btn cart-drawer__close" type="button" data-close aria-label="Close cart">{icon('close')}</button>
  </div>
  <div class="drawer__body">
    <div class="free-shipping">
      {icon('truck')}
      <div><p><strong>Free shipping unlocked.</strong> Your order ships free.</p><div class="meter"><span class="w-100"></span></div></div>
    </div>
    <ul class="mini-cart">{lis}</ul>
    <p class="mini-cart-empty" data-mini-empty hidden>Your cart is empty. <a class="text-btn" href="shop.html">Start shopping</a></p>
  </div>
  <div class="drawer__foot">
    <p class="summary-row summary-row--total"><span>Subtotal</span><span data-mini-subtotal>$247.00</span></p>
    <p class="cart-drawer__note">Taxes and shipping are calculated at checkout.</p>
    <div class="cart-drawer__actions">
      <a class="btn btn--light" href="cart.html">View cart</a>
      <a class="btn btn--primary" href="checkout.html">Checkout{icon('arrow-right')}</a>
    </div>
  </div>
</div>
<!-- Mini Cart End -->"""


def layers(newsletter=False):
    popup = ""
    if newsletter:
        popup = f"""
<!-- Newsletter Popup Start -->
<div class="modal modal--sm" id="newsletter-modal" role="dialog" aria-modal="true" aria-labelledby="popup-title">
  <div class="modal__dialog">
    <button class="icon-btn modal__close" type="button" data-close aria-label="Close">{icon('close')}</button>
    <div class="newsletter-popup">
      <h2 id="popup-title">Take 10% off your first order</h2>
      <p>Join the list for new arrivals and member-only deals. We send two emails a month.</p>
      <form class="newsletter-form" action="#" data-validate data-success="Check your inbox for your code.">
        <label class="visually-hidden" for="popup-email">Email address</label>
        <input class="form-control" id="popup-email" name="email" type="email" autocomplete="email" placeholder="Email address" required>
        <button class="btn btn--primary" type="submit">Get my code</button>
      </form>
      <button class="text-btn" type="button" data-close>No thanks</button>
    </div>
  </div>
</div>
<!-- Newsletter Popup End -->"""
    a = P["aero"]
    return f"""
<!-- Mobile Menu Start -->
<div class="drawer drawer--left mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-labelledby="mobile-menu-title">
  <div class="drawer__head mobile-menu__head">
    <h2 class="visually-hidden" id="mobile-menu-title">Menu</h2>
    <a href="index.html"><img src="{IMG}/logo.svg" alt="{BRAND} home" width="132" height="36"></a>
    <button class="icon-btn mobile-menu__close" type="button" data-close aria-label="Close menu">{icon('close')}</button>
  </div>
  <div class="drawer__body mobile-menu__body">
    <form class="mobile-menu__search" action="shop.html" role="search">
      <label class="visually-hidden" for="mobile-search">Search products</label>
      <input id="mobile-search" type="search" name="q" placeholder="Search 1,200 products">
      <button type="submit" aria-label="Search">{icon('search')}</button>
    </form>
    <nav class="mobile-nav" aria-label="Mobile"></nav>
    <div class="mobile-menu__tiles">
      <a class="mobile-menu__tile mobile-menu__tile--accent" href="index-3.html#deals-title"><span class="mono">Up to 20% off</span><strong>Deals</strong></a>
      <a class="mobile-menu__tile" href="order-tracking.html"><span class="mono">Where is it?</span><strong>Track order</strong></a>
    </div>
    <div class="mobile-menu__extra">
      <a class="btn btn--primary" href="login.html">Log in</a>
      <a class="btn btn--light" href="register.html">Create account</a>
    </div>
  </div>
  <div class="mobile-menu__foot">
    <a href="tel:+15550142000">{icon('phone')}+1 (555) 014-2000</a>
    <ul class="mobile-menu__social"><li><a href="#">Instagram</a></li><li><a href="#">YouTube</a></li><li><a href="#">X</a></li></ul>
  </div>
</div>
<!-- Mobile Menu End -->
{mini_cart()}

<!-- Quick View Start -->
<div class="modal" id="quick-view" role="dialog" aria-modal="true" aria-labelledby="qv-title">
  <div class="modal__dialog">
    <button class="icon-btn modal__close" type="button" data-close aria-label="Close quick view">{icon('close')}</button>
    <div class="quick-view">
      <div class="quick-view__media"><img data-qv-img src="{IMG}/products/{a['img']}.svg" alt="{a['name']}" width="400" height="400" loading="lazy"></div>
      <div class="quick-view__body">
        <h2 id="qv-title" data-qv-title>{a['name']}</h2>
        <div data-qv-price class="price">{price(a)[len('<p class="price price--sale">'):-4]}</div>
        <dl class="spec-list" data-qv-specs>{spec_list(a['specs'])[len('<dl class="spec-list">'):-5]}</dl>
        <div class="btn-row">{qty()}<button class="btn btn--primary" type="button" data-add-to-cart>Add to cart</button></div>
        <a class="text-btn" href="product-details.html" data-qv-link>View full details</a>
      </div>
    </div>
  </div>
</div>
<!-- Quick View End -->
{popup}
<div class="overlay"></div>
<div class="toast-region" aria-live="polite"></div>
<button class="back-to-top" type="button" aria-label="Back to top">{icon('arrow-up')}</button>"""


def page(filename, title, desc, body, current=None, body_class="", newsletter=False, bare=False):
    current = current or filename
    fonts = '<link rel="preload" href="assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>'
    cls = f' class="{body_class}"' if body_class else ""
    if bare:
        content = body
    else:
        content = f"""{header(current)}

<!-- Main Content Start -->
<main class="main-content" id="main">
{body}
</main>
<!-- Main Content End -->
{footer()}
{layers(newsletter)}"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {BRAND}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0D0E12">
<link rel="icon" href="{IMG}/favicon.svg" type="image/svg+xml">
{fonts}
<link rel="stylesheet" href="assets/css/style.css">
<noscript><style>.preloader {{ display: none; }}</style></noscript>
</head>
<body{cls}>
<a class="skip-link" href="#main">Skip to content</a>
{SPRITE}
<div class="preloader" aria-hidden="true"><div class="preloader__bar"></div></div>
{content}

<script src="assets/js/main.js"></script>
</body>
</html>
"""
    html = use_demo_photos(html)
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)


# ---------------------------------------------------------------- shared sections
def tabs_products(prefix, tabs):
    buttons, panels = "", ""
    for i, (label, keys) in enumerate(tabs):
        sel = "true" if i == 0 else "false"
        ti = "0" if i == 0 else "-1"
        hidden = "" if i == 0 else " hidden"
        tid, pid = f"{prefix}-tab-{i}", f"{prefix}-panel-{i}"
        buttons += f'<button class="tabs__tab" id="{tid}" type="button" role="tab" aria-selected="{sel}" aria-controls="{pid}" tabindex="{ti}">{label}</button>'
        panels += f'<div class="tabs__panel" id="{pid}" role="tabpanel" aria-labelledby="{tid}"{hidden}>{grid(keys)}</div>'
    return f'<div class="tabs tabs--pill" data-tabs><div class="tabs__list" role="tablist" aria-label="Product collections">{buttons}</div>{panels}</div>'


def categories_row():
    cats = [("audio", "Audio", 48), ("phones", "Phones", 36), ("laptops", "Laptops", 24), ("wearables", "Wearables", 18), ("gaming", "Gaming", 31), ("cameras", "Cameras", 12)]
    tiles = "".join(f'<a class="category-tile" href="shop.html"><img src="{IMG}/categories/{s}.svg" alt="" width="400" height="400" loading="lazy">'
                    f'<span><strong>{n}</strong><span>{c} products</span></span></a>' for s, n, c in cats)
    return f"""
<!-- Categories Start -->
<section class="section" aria-labelledby="categories-title">
  <div class="container">
    {section_head('Shop by category', right='<a class="text-btn" href="shop.html">All products</a>', id_='categories-title', eyebrow='Categories')}
    <div class="category-row">{tiles}</div>
  </div>
</section>
<!-- Categories End -->"""


def deal_section():
    s = P["slate"]
    return f"""
<!-- Deal Start -->
<section class="section" aria-labelledby="deal-title">
  <div class="container">
    <div class="deal">
      <div class="deal__media">
        <img src="{IMG}/products/laptop.svg" alt="Slate 14 Laptop" width="400" height="400" loading="lazy">
        <span class="badge badge--sale">Save $150</span>
      </div>
      <div class="deal__body">
        <p class="eyebrow">Deal of the week</p>
        <h2 id="deal-title">Slate 14 Laptop</h2>
        {spec_list([('Processor', '8-core, 4.4 GHz'), ('Memory', '16 GB'), ('Storage', '512 GB SSD'), ('Battery', 'Up to 14 h'), ('Weight', '1.3 kg')])}
        {price(s, 'lg')}
        <div class="countdown" data-countdown="+3d">Ends Sunday at midnight</div>
        <div class="deal__stock"><p>62 of 100 sold</p><div class="meter"><span></span></div></div>
        <div class="btn-row">
          <button class="btn btn--primary" type="button" data-add-to-cart>Add to cart</button>
          <a class="btn btn--light" href="product-details.html">View details</a>
        </div>
      </div>
    </div>
  </div>
</section>
<!-- Deal End -->"""


def compare_strip():
    cols = [("Aero Wireless", "headphones"), ("Pulse Earbuds", "earbuds"), ("Aero Studio", "headphones-side")]
    head = "".join(f'<th scope="col"><img src="{IMG}/products/{img}.svg" alt="" width="400" height="400" loading="lazy"><a href="product-details.html">{n}</a></th>' for n, img in cols)
    rows = [("Type", ["Over-ear", "In-ear", "Over-ear"], None), ("Battery", ["30 h", "8 h + 24 h case", "40 h"], 2),
            ("Noise cancelling", ["Adaptive", "Active", "Adaptive"], None), ("Weight", ["250 g", "5 g per bud", "290 g"], 1),
            ("Price", ["$119", "$79", "$199"], 1)]
    body = ""
    for label, vals, best in rows:
        tds = "".join(f'<td class="is-best">{v}<span class="visually-hidden"> (best)</span></td>' if i == best else f"<td>{v}</td>" for i, v in enumerate(vals))
        body += f'<tr><th scope="row">{label}</th>{tds}</tr>'
    return f"""
<!-- Compare Strip Start -->
<section class="section section--surface" id="compare" aria-labelledby="compare-title">
  <div class="container">
    {section_head('Compare our audio range', 'Three models, the same five specs. Best values are highlighted.', '<a class="text-btn" href="compare.html">Open full comparison</a>', id_='compare-title', eyebrow='Side by side')}
    <div class="table-scroll">
      <table class="compare-table">
        <caption class="visually-hidden">Headphone and earbud comparison</caption>
        <thead><tr><td></td>{head}</tr></thead>
        <tbody>{body}</tbody>
      </table>
    </div>
  </div>
</section>
<!-- Compare Strip End -->"""


# ---------------------------------------------------------------- pages
def home1():
    notes = [(1, "Noise cancelling", True), (2, "40 mm drivers", False), (3, "30 h battery", False), (4, "USB-C fast charge", True)]
    lis = "".join(f'<li class="annotated__note annotated__note--{n}{" annotated__note--flip" if flip else ""}"><span class="annotated__line"></span>'
                  f'<span class="annotated__label">{t}</span></li>' for n, t, flip in notes)
    body = f"""
<!-- Hero Start -->
<section class="hero" aria-labelledby="hero-title">
  <div class="container">
    <div class="hero__stage">
      <div class="hero__copy">
        <p class="eyebrow eyebrow--dark">New &middot; Aero Wireless</p>
        <h1 id="hero-title">Hear every <span class="mark">detail.</span> Nothing else.</h1>
        <p class="lead">Adaptive noise cancelling, 40 mm drivers and a 10-minute USB-C charge that plays for 5 hours.</p>
        <div class="btn-row">
          <a class="btn btn--accent" href="product-details.html">Shop Aero from $119{icon('arrow-right')}</a>
          <a class="btn btn--ghost-light" href="#compare">Compare models</a>
        </div>
        <dl class="hero__stats">
          <div><dt>Battery</dt><dd>30<small>h</small></dd></div>
          <div><dt>Drivers</dt><dd>40<small>mm</small></dd></div>
          <div><dt>Weight</dt><dd>250<small>g</small></dd></div>
        </dl>
      </div>
      <div class="annotated">
        <img class="annotated__img" src="{IMG}/hero/hero-headphones.svg" alt="Aero Wireless Headphones in silver" width="600" height="450">
        <ul class="annotated__notes">{lis}</ul>
      </div>
    </div>
    <ul class="hero__facts">
      <li>{icon('truck')}Free shipping over $99</li>
      <li>{icon('shield')}2-year warranty</li>
      <li>{icon('return')}30-day returns</li>
      <li>{icon('support')}Real product advice, 7 days a week</li>
    </ul>
  </div>
</section>
<!-- Hero End -->
{ticker()}
{categories_row()}

<!-- Featured Products Start -->
<section class="section section--surface" aria-labelledby="picks-title">
  <div class="container">
    {section_head("This week's picks", right='<a class="text-btn" href="shop.html">View all</a>', id_='picks-title', eyebrow='Curated weekly')}
    {tabs_products('picks', [('Best sellers', ['aero', 'nova', 'echo', 'orbit']), ('New arrivals', ['pulse', 'lumen', 'key75', 'arc']), ('On sale', ['slate', 'drift', 'echo', 'aero'])])}
  </div>
</section>
<!-- Featured Products End -->
{deal_section()}
{compare_strip()}
{services()}
{brands()}
{newsletter_band()}"""
    page("index.html", "Electronics Store", "Shop headphones, phones, laptops and wearables with specs you can compare at a glance.", body, newsletter=True)


def home2():
    new = ["pulse", "lumen", "arc", "key75", "frame", "vector", "orbit", "nova"]
    track = "".join(card(k) for k in new)
    ranked = ""
    for k in ["aero", "nova", "echo", "slate", "drift", "orbit", "vector", "key75"]:
        p = P[k]
        ranked += (f'<li><img src="{IMG}/products/{p["img"]}.svg" alt="" width="400" height="400" loading="lazy">'
                   f'<div><h3><a href="product-details.html">{p["name"]}</a></h3><p>{p["specs"][0][0]} {p["specs"][0][1]}</p></div>{price(p)}</li>')
    posts = "".join(post_card(p) for p in POSTS[:3])
    body = f"""
<!-- Hero Start -->
<section class="hero-split" aria-labelledby="hero-title">
  <div class="container hero-split__grid">
    <div class="hero-split__main">
      <div>
        <p class="eyebrow eyebrow--dark">Workspace edit 2026</p>
        <h1 id="hero-title">Your desk, <span class="mark">upgraded.</span></h1>
        <p>Laptops, monitors and keyboards that work well together, chosen by people who use them all day.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn--accent" href="shop.html">Shop computing{icon('arrow-right')}</a>
        <a class="btn btn--ghost-light" href="index-3.html#bundle">See the desk bundle</a>
      </div>
      <img src="{IMG}/hero/laptop-on-dark.svg" alt="Slate 14 Laptop" width="400" height="400">
    </div>
    <div class="hero-split__side">
      <a class="promo-tile promo-tile--tint" href="product-details.html">
        <span><span class="h2-like"><strong>Nova X Phone</strong></span><span class="promo-tile__text">From $699, or $58 a month for 12 months.</span><span class="text-btn">Shop phones</span></span>
        <img src="{IMG}/products/phone.svg" alt="" width="400" height="400">
      </a>
      <a class="promo-tile" href="product-details.html">
        <span><span class="h2-like"><strong>Orbit Smartwatch</strong></span><span class="promo-tile__text">A week of battery in a 44 mm case.</span><span class="text-btn">Shop wearables</span></span>
        <img src="{IMG}/products/watch.svg" alt="" width="400" height="400">
      </a>
    </div>
  </div>
</section>
<!-- Hero End -->
{ticker(["Laptops", "Monitors", "Keyboards", "Docks and hubs", "Webcams", "Desk lamps", "Chargers"])}

<!-- New Arrivals Start -->
<section class="section" aria-labelledby="new-title">
  <div class="container carousel" data-carousel>
    {section_head('New arrivals', 'Fresh stock from this month, with full specs on every card.', f'<div class="carousel__nav"><button class="icon-btn" type="button" data-carousel-prev aria-label="Previous products">{icon("chevron-left")}</button><button class="icon-btn" type="button" data-carousel-next aria-label="Next products">{icon("chevron-right")}</button></div>', id_='new-title', eyebrow='Just landed')}
    <div class="carousel__track">{track}</div>
  </div>
</section>
<!-- New Arrivals End -->

<!-- Promo Pair Start -->
<section class="section section--tight" aria-label="Featured collections">
  <div class="container promo-pair">
    <a class="promo-tile" href="shop.html">
      <span><span class="h2-like"><strong>Gaming gear</strong></span><span class="promo-tile__text">Low-latency controllers and headsets for every platform.</span><span class="text-btn">Shop gaming</span></span>
      <img src="{IMG}/products/controller.svg" alt="" width="400" height="400" loading="lazy">
    </a>
    <a class="promo-tile promo-tile--tint" href="shop.html">
      <span><span class="h2-like"><strong>Power on the go</strong></span><span class="promo-tile__text">65 W power banks that can charge a laptop.</span><span class="text-btn">Shop charging</span></span>
      <img src="{IMG}/products/powerbank.svg" alt="" width="400" height="400" loading="lazy">
    </a>
  </div>
</section>
<!-- Promo Pair End -->

<!-- Best Sellers Start -->
<section class="section section--surface" aria-labelledby="best-title">
  <div class="container">
    {section_head('Best sellers this month', right='<a class="text-btn" href="shop.html">See all</a>', id_='best-title', eyebrow='Top 8')}
    <ol class="ranked">{ranked}</ol>
  </div>
</section>
<!-- Best Sellers End -->

<!-- Journal Start -->
<section class="section" aria-labelledby="journal-title">
  <div class="container">
    {section_head('Guides and reviews', 'Plain-language advice before you buy.', '<a class="text-btn" href="blog.html">Read the journal</a>', id_='journal-title', eyebrow='The journal')}
    <div class="post-grid">{posts}</div>
  </div>
</section>
<!-- Journal End -->
{newsletter_band()}"""
    page("index-2.html", "Home 2", "Laptops, monitors, phones and accessories, chosen and tested by the Ohmly team.", body, newsletter=True)


def home3():
    tiles = [("audio", "Audio", 48), ("phones", "Phones", 36), ("laptops", "Laptops", 24), ("wearables", "Wearables", 18)]
    t = "".join(f'<a class="mosaic__tile" href="shop.html"><h2>{n}</h2><span>{c} products</span>'
                f'<img src="{IMG}/categories/{s}.svg" alt="" width="400" height="400"></a>' for s, n, c in tiles)
    bundle_items = ["arc", "key75", "drift"]
    b = ""
    for i, k in enumerate(bundle_items):
        p = P[k]
        b += (f'<div class="bundle__item"><img src="{IMG}/products/{p["img"]}.svg" alt="" width="400" height="400" loading="lazy">'
              f'<div><h3><a href="product-details.html">{p["name"]}</a></h3><p>{fmt(p["price"])}</p></div></div>')
        if i < 2:
            b += f'<span class="bundle__plus">{icon("plus")}</span>'
        else:
            b += '<span class="bundle__plus bundle__plus--eq" aria-hidden="true">=</span>'
    quotes = [("The spec tables made it easy to pick between two monitors. It arrived in two days.", "Maya R.", "Arc 27 Monitor"),
              ("Honest battery numbers. My Orbit really does last a week between charges.", "Daniel K.", "Orbit Smartwatch"),
              ("Returned a keyboard that was too loud and swapped it the same week. No hassle.", "Sara L.", "Key75 Keyboard")]
    q = "".join(f'<figure><blockquote><p>{txt}</p></blockquote><figcaption><strong>{n}</strong>, bought the {prod}</figcaption></figure>' for txt, n, prod in quotes)
    body = f"""
<!-- Category Mosaic Start -->
<section class="mosaic" aria-labelledby="hero-title">
  <div class="container mosaic__grid">
    <div class="mosaic__tile mosaic__tile--lead">
      <div>
        <p class="eyebrow">1,200+ products</p>
        <h1 id="hero-title">Tech for work, play and everything between.</h1>
        <p>Browse 1,200 products by category, compare specs side by side, and get free shipping over $99.</p>
      </div>
      <a class="btn btn--primary" href="shop.html">Shop all products{icon('arrow-right')}</a>
      <img src="{IMG}/hero/headphones-on-color.svg" alt="" width="400" height="400">
    </div>
    {t}
  </div>
</section>
<!-- Category Mosaic End -->

<!-- Deals Start -->
<section class="section" aria-labelledby="deals-title">
  <div class="container">
    {section_head('Deals ending soon', 'Prices return to normal when the timer runs out.', '<div class="countdown" data-countdown="+2d">Ends in 2 days</div>', id_='deals-title', eyebrow='Limited time')}
    {grid(['slate', 'echo', 'drift', 'aero'])}
  </div>
</section>
<!-- Deals End -->

<!-- Bundle Start -->
<section class="section section--surface" id="bundle" aria-labelledby="bundle-title">
  <div class="container">
    {section_head('Complete your desk setup', 'Buy the monitor, keyboard and power bank together and save $48.', id_='bundle-title', eyebrow='Bundle and save')}
    <div class="bundle">
      {b}
      <div class="bundle__total">
        <p class="price"><ins class="price__now"><span class="visually-hidden">Bundle price: </span>$459</ins><del class="price__was"><span class="visually-hidden">Separately: </span>$507</del></p>
        <p class="save">You save $48</p>
        <button class="btn btn--primary btn--block" type="button" data-add-to-cart>Add all 3 to cart</button>
      </div>
    </div>
  </div>
</section>
<!-- Bundle End -->

<!-- Popular Products Start -->
<section class="section" aria-labelledby="popular-title">
  <div class="container">
    {section_head('Popular right now', right='<a class="text-btn" href="shop.html">View all</a>', id_='popular-title', eyebrow='Trending')}
    {grid(['nova', 'orbit', 'frame', 'pulse', 'lumen', 'vector', 'key75', 'arc'])}
  </div>
</section>
<!-- Popular Products End -->

<!-- Reviews Start -->
<section class="section section--surface" aria-labelledby="quotes-title">
  <div class="container">
    {section_head('What customers say', 'Rated 4.8 out of 5 from 3,400 verified reviews.', id_='quotes-title', eyebrow='4.8 / 5 rating')}
    <div class="quotes">{q}</div>
  </div>
</section>
<!-- Reviews End -->
{brands()}
{newsletter_band()}"""
    page("index-3.html", "Home 3", "Shop electronics by category: audio, phones, laptops, wearables, gaming and more.", body, newsletter=True)


def filters(full=False):
    cats = [("Headphones", 24), ("Earbuds", 18), ("Speakers", 12), ("Phones", 36), ("Laptops", 24), ("Wearables", 18)]
    brands_ = [("Norvik", 32), ("Aurelo", 21), ("Halden", 17), ("Tovera", 14), ("Pellan", 9)]
    cb = "".join(f'<label class="check"><input type="checkbox" name="category" value="{c}"{" checked" if c == "Headphones" else ""}>{c}<span class="count">{n}</span></label>' for c, n in cats)
    br = "".join(f'<label class="check"><input type="checkbox" name="brand" value="{c}">{c}<span class="count">{n}</span></label>' for c, n in brands_)
    rt = "".join(f'<label class="check"><input type="radio" name="rating" value="{r}"{" checked" if r == 4 else ""}>{r} stars and up</label>' for r in [4, 3, 2])

    def group(id_, title, content):
        return (f'<div class="filter-group accordion__item"><h3><button class="accordion__trigger" type="button" aria-expanded="true" aria-controls="{id_}">'
                f'{title}{icon("plus")}</button></h3><div class="accordion__panel" id="{id_}">{content}</div></div>')

    pr = f"""<div class="price-range" data-price-range>
      <div class="price-range__track">
        <label class="visually-hidden" for="price-min">Minimum price</label>
        <input class="range-min" id="price-min" type="range" min="0" max="2000" step="10" value="50">
        <label class="visually-hidden" for="price-max">Maximum price</label>
        <input class="range-max" id="price-max" type="range" min="0" max="2000" step="10" value="1500">
      </div>
      <p class="price-range__values"><span data-min-output>$50</span><span data-max-output>$1500</span></p>
    </div>"""
    av = ('<label class="check"><input type="checkbox" name="stock" checked>In stock<span class="count">142</span></label>'
          '<label class="check"><input type="checkbox" name="sale">On sale<span class="count">28</span></label>')
    body = group("f-cat", "Category", cb) + group("f-price", "Price", pr) + group("f-brand", "Brand", br) + group("f-rating", "Rating", rt) + group("f-stock", "Availability", av)
    return f"""
<!-- Shop Filters Start -->
<aside class="shop-sidebar drawer drawer--left" id="shop-filters" aria-labelledby="filters-title">
  <div class="drawer__head">
    <h2 id="filters-title">Filters</h2>
    <button class="icon-btn" type="button" data-close aria-label="Close filters">{icon('close')}</button>
  </div>
  <div class="drawer__body"><div data-accordion>{body}</div></div>
  <div class="drawer__foot">
    <button class="btn btn--primary btn--block" type="button" data-close>Show 48 products</button>
    <button class="btn btn--light btn--block" type="button">Clear all</button>
  </div>
</aside>
<!-- Shop Filters End -->"""


def shop_page(filename, title, list_view=False, full=False):
    keys = ALL
    grid_cls = "product-grid" + ("" if full else " product-grid--3") + (" is-list" if list_view else "")
    layout = "shop-layout" + (" shop-layout--full" if full else "")
    body = f"""{page_banner(title, [('Shop', 'shop.html')] if title != 'Shop' else [], '1,248 products across audio, mobile, computing and gaming.')}

<!-- Shop Start -->
<section class="section section--tight">
  <div class="container {layout}">
    {filters(full)}
    <div class="shop-main">
      <h2 class="visually-hidden">Products</h2>
      <div class="shop-toolbar">
        <button class="btn btn--light btn--sm filter-toggle" type="button" data-open-drawer="shop-filters">{icon('filter')}Filters</button>
        <p>Showing 1&ndash;12 of 48 products</p>
        <label class="visually-hidden" for="sort">Sort products</label>
        <select class="form-control" id="sort" name="sort">
          <option>Most popular</option><option>Newest</option><option>Price: low to high</option><option>Price: high to low</option><option>Top rated</option>
        </select>
        <div class="view-toggle">
          <button type="button" data-view="grid" aria-pressed="{'false' if list_view else 'true'}" aria-label="Grid view">{icon('grid')}</button>
          <button type="button" data-view="list" aria-pressed="{'true' if list_view else 'false'}" aria-label="List view">{icon('list')}</button>
        </div>
      </div>
      <div class="active-filters">
        <button type="button">Headphones {icon('close')}<span class="visually-hidden">Remove filter</span></button>
        <button type="button">4 stars and up {icon('close')}<span class="visually-hidden">Remove filter</span></button>
        <button type="button">In stock {icon('close')}<span class="visually-hidden">Remove filter</span></button>
      </div>
      {grid(keys, grid_cls, ' data-product-grid')}
      <nav class="pagination" aria-label="Pagination">
        <ul>
          <li><a href="#" aria-label="Previous page">{icon('chevron-left')}</a></li>
          <li><span aria-current="page">1</span></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><a href="#">4</a></li>
          <li><a href="#" aria-label="Next page">{icon('chevron-right')}</a></li>
        </ul>
      </nav>
    </div>
  </div>
</section>
<!-- Shop End -->"""
    page(filename, title, "Browse electronics with filters, spec tables and side-by-side comparison.", body, current=filename)


def product_details():
    a = P["aero"]
    thumbs = [("headphones", "Aero Wireless Headphones, front"), ("headphones-side", "Aero Wireless Headphones, side"),
              ("headphones-case", "Aero Wireless travel case"), ("headphones-detail", "Aero Wireless ear cushion detail")]
    th = "".join(f'<li><button type="button" data-src="{IMG}/products/{s}.svg" data-alt="{alt}" aria-current="{"true" if i == 0 else "false"}" aria-label="Show image {i + 1}">'
                 f'<img src="{IMG}/products/{s}.svg" alt="" width="400" height="400"></button></li>' for i, (s, alt) in enumerate(thumbs))
    colors = [("Graphite", "graphite"), ("Silver", "silver"), ("Cobalt", "cobalt"), ("Sand", "sand")]
    col = "".join(f'<label class="variant__chip"><input type="radio" name="color" value="{c}"{" checked" if i == 0 else ""}><span><i class="dot--{d}"></i>{c}</span></label>'
                  for i, (c, d) in enumerate(colors))
    ed = ('<label class="variant__chip"><input type="radio" name="edition" value="Standard" checked><span>Standard</span></label>'
          '<label class="variant__chip"><input type="radio" name="edition" value="With travel case (+$20)"><span>With travel case (+$20)</span></label>')
    full_specs = [("Driver", "40 mm dynamic"), ("Frequency response", "20 Hz to 40 kHz"), ("Noise cancelling", "Adaptive, 3 levels"),
                  ("Battery", "30 h with ANC on, 45 h off"), ("Charging", "USB-C, 10 min for 5 h"), ("Bluetooth", "5.3, multipoint"),
                  ("Codecs", "SBC, AAC, LDAC"), ("Microphones", "6, with wind reduction"), ("Weight", "250 g"), ("In the box", "Headphones, case, USB-C cable, 3.5 mm cable")]
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in full_specs)
    bars = [(5, 72), (4, 18), (3, 5), (2, 3), (1, 2)]
    bl = "".join(f'<li><span>{s} stars</span><span class="meter"><span class="w-{w}"></span></span><span>{w}%</span></li>' for s, w in bars)
    reviews = [("Maya R.", 5, "Aug 30, 2026", "Light enough to forget you are wearing them", "I use these on a 3-hour commute. The noise cancelling handles train noise well and the battery lasts all week."),
               ("Tom B.", 4, "Aug 18, 2026", "Great sound, case is bulky", "Clear, balanced sound and very comfortable. The travel case takes more room in my bag than I expected."),
               ("Priya S.", 5, "Aug 2, 2026", "Fast charge actually works", "Ten minutes on the charger before a flight gave me the whole trip. Multipoint switching is seamless.")]
    rv = "".join(f'<li class="review"><div class="review__head"><h3>{t}</h3><small>{d}</small></div>'
                 f'<p class="rating">{stars(r)}<span>{r} out of 5, by {n}</span></p><p>{body}</p></li>' for n, r, d, t, body in reviews)
    body = f"""
<!-- Product Start -->
<section class="section section--tight">
  <div class="container">
    {breadcrumb([('Home', 'index.html'), ('Shop', 'shop.html'), ('Headphones', 'shop.html'), (a['name'], '')])}
    <div class="product-detail">
      <div class="gallery" data-gallery>
        <div class="gallery__main"><img src="{IMG}/products/headphones.svg" alt="Aero Wireless Headphones, front" width="400" height="400"></div>
        <ul class="gallery__thumbs">{th}</ul>
      </div>
      <div class="product-info">
        <div class="product-info__meta"><a class="text-muted" href="shop.html">Headphones</a><span class="badge badge--stock">In stock</span><span class="text-muted">SKU AR-100</span></div>
        <h1>{a['name']}</h1>
        <p class="rating">{stars(a['rating'])}<a class="link" href="#reviews" data-tab-link>{a['rating']} out of 5 ({a['reviews']} reviews)</a></p>
        {price(a, 'lg')}
        <p class="product-info__summary">Adaptive noise cancelling that adjusts to your surroundings, 40 mm drivers tuned for detail, and a foldable frame that weighs 250 grams.</p>
        <fieldset class="variant" data-variant><legend>Color: <span data-variant-value>Graphite</span></legend><div class="variant__options">{col}</div></fieldset>
        <fieldset class="variant" data-variant><legend>Edition: <span data-variant-value>Standard</span></legend><div class="variant__options">{ed}</div></fieldset>
        <div class="product-info__buy">
          {qty()}
          <button class="btn btn--primary" type="button" data-add-to-cart>{icon('bag')}Add to cart</button>
          <button class="icon-btn btn--light" type="button" data-wishlist aria-pressed="false" aria-label="Save to wishlist">{icon('heart')}</button>
        </div>
        <div class="product-info__links">
          <a href="compare.html">{icon('compare')}Compare</a>
          <a href="contact.html">{icon('support')}Ask a question</a>
        </div>
        {spec_list([('Drivers', '40 mm'), ('Battery', '30 h (ANC on)'), ('Fast charge', '10 min = 5 h'), ('Weight', '250 g')])}
        <div class="delivery-note">
          <div>{icon('truck')}<p>Free delivery<span>Arrives in 2 to 4 business days</span></p></div>
          <div>{icon('return')}<p>30-day returns<span>Free return label included</span></p></div>
          <div>{icon('shield')}<p>2-year warranty<span>Repair or replacement, your choice</span></p></div>
        </div>
      </div>
    </div>
  </div>
</section>
<!-- Product End -->

<!-- Product Tabs Start -->
<section class="section section--surface" aria-label="Product information">
  <div class="container tabs" data-tabs>
    <div class="tabs__list" role="tablist" aria-label="Product information">
      <button class="tabs__tab" id="tab-desc" type="button" role="tab" aria-selected="true" aria-controls="panel-desc" tabindex="0">Description</button>
      <button class="tabs__tab" id="tab-specs" type="button" role="tab" aria-selected="false" aria-controls="panel-specs" tabindex="-1">Specifications</button>
      <button class="tabs__tab" id="tab-reviews" type="button" role="tab" aria-selected="false" aria-controls="reviews" tabindex="-1">Reviews (128)</button>
    </div>
    <div class="tabs__panel prose" id="panel-desc" role="tabpanel" aria-labelledby="tab-desc">
      <p>Aero Wireless is built for long days. Six microphones measure the noise around you and adjust the cancelling level on their own, so you hear less of the train and more of what you are listening to.</p>
      <h2>Made for travel</h2>
      <p>The ear cups fold flat into a slim case, and the 30-hour battery covers a return flight with time to spare. When you are low, a 10-minute charge gives you 5 more hours.</p>
      <ul><li>Multipoint Bluetooth connects to your laptop and phone at once</li><li>Wear detection pauses music when you take them off</li><li>Replaceable ear cushions extend the life of the headphones</li></ul>
    </div>
    <div class="tabs__panel" id="panel-specs" role="tabpanel" aria-labelledby="tab-specs" hidden>
      <div class="table-scroll"><table class="spec-table"><caption class="visually-hidden">Full specifications</caption><tbody>{rows}</tbody></table></div>
    </div>
    <div class="tabs__panel" id="reviews" role="tabpanel" aria-labelledby="tab-reviews" hidden>
      <div class="reviews">
        <div class="reviews__summary">
          <strong>4.7</strong>
          <p class="rating">{stars(4.7)}<span>Based on 128 reviews</span></p>
          <ul class="reviews__bars">{bl}</ul>
        </div>
        <div>
          <ul class="reviews__list">{rv}</ul>
          <form class="review-form form-card" action="#" data-validate data-success="Thanks, your review will appear after moderation.">
            <h2>Write a review</h2>
            <div class="form-grid">
              {field('review-name', 'Name', auto='name')}
              {field('review-email', 'Email', 'email', auto='email', hint='Not published.')}
              <div class="field full"><label class="field-label" for="review-rating">Rating <span class="req" aria-hidden="true">*</span></label>
                <select class="form-control" id="review-rating" name="review-rating" required><option value="">Choose a rating</option><option>5 stars</option><option>4 stars</option><option>3 stars</option><option>2 stars</option><option>1 star</option></select></div>
              {field('review-text', 'Your review', 'textarea', full=True)}
            </div>
            <div class="btn-row"><button class="btn btn--primary" type="submit">Submit review</button></div>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>
<!-- Product Tabs End -->

<!-- Related Products Start -->
<section class="section" aria-labelledby="related-title">
  <div class="container">
    {section_head('You might also like', id_='related-title')}
    {grid(['pulse', 'echo', 'orbit', 'drift'])}
  </div>
</section>
<!-- Related Products End -->"""
    page("product-details.html", a["name"], "Aero Wireless Headphones: 30 h battery, adaptive noise cancelling, 250 g.", body)


def cart_page():
    rows = ""
    for k in ["aero", "pulse", "drift"]:
        p = P[k]
        rows += (f'<tr data-price="{p["price"]}"><td><div class="cart-product"><img src="{IMG}/products/{p["img"]}.svg" alt="" width="400" height="400">'
                 f'<div><a href="product-details.html">{p["name"]}</a><small>{p["specs"][0][0]}: {p["specs"][0][1]}</small></div></div></td>'
                 f'<td data-label="Price">{fmt(p["price"])}</td><td data-label="Quantity">{qty(1, True, "Quantity for " + p["name"])}</td>'
                 f'<td data-label="Total" data-line-total>{fmt(p["price"])}</td>'
                 f'<td><button class="remove-btn" type="button" data-remove-row aria-label="Remove {p["name"]}">{icon("trash")}</button></td></tr>')
    body = f"""{page_banner('Your cart', [], '3 items ready for checkout.')}

<!-- Cart Start -->
<section class="section section--tight">
  <div class="container cart-layout">
    <div>
      <div class="table-scroll" data-cart-page>
        <table class="data-table cart-table">
          <caption class="visually-hidden">Items in your cart</caption>
          <thead><tr><th scope="col">Product</th><th scope="col">Price</th><th scope="col">Quantity</th><th scope="col">Total</th><th scope="col"><span class="visually-hidden">Remove</span></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="cart-empty" data-cart-empty hidden>
        <h2>Your cart is empty</h2>
        <p class="text-muted">Browse the shop to add products.</p>
        <a class="btn btn--primary" href="shop.html">Start shopping</a>
      </div>
      <div class="cart-actions">
        <form class="coupon" action="#" data-validate data-success="Coupon applied.">
          <label class="visually-hidden" for="coupon">Coupon code</label>
          <input class="form-control" id="coupon" name="coupon" type="text" placeholder="Coupon code" required>
          <button class="btn btn--dark" type="submit">Apply</button>
        </form>
        <a class="btn btn--light" href="shop.html">Continue shopping</a>
      </div>
    </div>
    <aside class="summary-card" aria-labelledby="summary-title">
      <h2 id="summary-title">Order summary</h2>
      <p class="summary-row"><span>Subtotal</span><span data-subtotal>$247.00</span></p>
      <p class="summary-row"><span>Shipping</span><span data-shipping>Free</span></p>
      <p class="summary-row"><span>Tax</span><span>Calculated at checkout</span></p>
      <hr>
      <p class="summary-row summary-row--total"><span>Total</span><span data-total>$247.00</span></p>
      <a class="btn btn--primary btn--block" href="checkout.html">Go to checkout</a>
      <p class="secure-note">{icon('lock')}Secure, encrypted checkout</p>
    </aside>
  </div>
</section>
<!-- Cart End -->"""
    page("cart.html", "Cart", "Review the items in your cart.", body)


def summary_items():
    return "".join(f'<li class="summary-item"><span class="thumb"><img src="{IMG}/products/{P[k]["img"]}.svg" alt="" width="400" height="400"><b>1</b></span>'
                   f'<span>{P[k]["name"]}<small>{P[k]["specs"][0][1]}</small></span><span>{fmt(P[k]["price"])}</span></li>' for k in ["aero", "pulse", "drift"])


def checkout_page():
    country = '<option value="">Choose a country</option><option>United States</option><option>Canada</option><option>United Kingdom</option><option>Australia</option><option>Bangladesh</option>'
    body = f"""{page_banner('Checkout', [('Cart', 'cart.html')])}

<!-- Checkout Start -->
<section class="section section--tight">
  <form class="container checkout-layout" action="order-complete.html" method="get" data-validate>
    <div>
      <div class="checkout-step">
        <h2><span>1</span>Contact</h2>
        <div class="form-grid">
          {field('co-email', 'Email', 'email', auto='email', hint='For your receipt and delivery updates.')}
          {field('co-phone', 'Phone', 'tel', required=False, auto='tel')}
          <label class="check full"><input type="checkbox" name="news">Email me new arrivals and deals</label>
        </div>
      </div>
      <div class="checkout-step">
        <h2><span>2</span>Shipping address</h2>
        <div class="form-grid">
          {field('co-first', 'First name', auto='given-name')}
          {field('co-last', 'Last name', auto='family-name')}
          {field('co-address', 'Street address', auto='address-line1', full=True)}
          {field('co-apt', 'Apartment, suite (optional)', required=False, auto='address-line2', full=True)}
          {field('co-city', 'City', auto='address-level2')}
          {field('co-zip', 'Postal code', auto='postal-code')}
          <div class="field full"><label class="field-label" for="co-country">Country <span class="req" aria-hidden="true">*</span></label>
            <select class="form-control" id="co-country" name="co-country" autocomplete="country-name" required>{country}</select></div>
        </div>
      </div>
      <div class="checkout-step">
        <h2><span>3</span>Delivery</h2>
        <fieldset class="radio-stack"><legend class="visually-hidden">Delivery method</legend>
          <label class="radio-card check"><input type="radio" name="delivery" value="standard" checked><span>Standard<small>2 to 4 business days</small></span><span class="radio-card__meta">Free</span></label>
          <label class="radio-card check"><input type="radio" name="delivery" value="express"><span>Express<small>Next business day</small></span><span class="radio-card__meta">$14.90</span></label>
        </fieldset>
      </div>
      <div class="checkout-step">
        <h2><span>4</span>Payment</h2>
        <fieldset class="radio-stack"><legend class="visually-hidden">Payment method</legend>
          <label class="radio-card check"><input type="radio" name="payment" value="card" checked><span>Credit or debit card<small>All major cards accepted</small></span></label>
          <label class="radio-card check"><input type="radio" name="payment" value="wallet"><span>Digital wallet<small>Pay with your saved wallet</small></span></label>
          <label class="radio-card check"><input type="radio" name="payment" value="cod"><span>Cash on delivery<small>Pay when your order arrives</small></span></label>
        </fieldset>
        <div class="form-grid checkout-card">
          {field('co-card', 'Card number', required=False, auto='cc-number', extra=' inputmode="numeric" placeholder="1234 5678 9012 3456"', full=True)}
          {field('co-exp', 'Expiry (MM/YY)', required=False, auto='cc-exp', extra=' placeholder="MM/YY"')}
          {field('co-cvc', 'Security code', required=False, auto='cc-csc', extra=' inputmode="numeric"')}
        </div>
        <p class="field-hint">This template does not process payments. Connect a payment provider to take real orders.</p>
      </div>
    </div>
    <aside class="summary-card" aria-labelledby="co-summary-title">
      <h2 id="co-summary-title">Order summary</h2>
      <ul class="summary-items">{summary_items()}</ul>
      <hr>
      <p class="summary-row"><span>Subtotal</span><span>$247.00</span></p>
      <p class="summary-row"><span>Shipping</span><span>Free</span></p>
      <p class="summary-row"><span>Tax</span><span>$19.76</span></p>
      <hr>
      <p class="summary-row summary-row--total"><span>Total</span><span>$266.76</span></p>
      <label class="check"><input type="checkbox" name="terms" required data-error="Please accept the terms to continue.">I agree to the terms and returns policy</label>
      <button class="btn btn--primary btn--block" type="submit">Place order</button>
      <p class="secure-note">{icon('lock')}Secure, encrypted checkout</p>
    </aside>
  </form>
</section>
<!-- Checkout End -->"""
    page("checkout.html", "Checkout", "Enter your details to complete your order.", body)


def order_complete():
    body = f"""
<!-- Order Complete Start -->
<section class="section">
  <div class="container order-complete">
    <span class="check-circle">{icon('check')}</span>
    <h1>Thanks, your order is placed.</h1>
    <p class="lead">We have emailed a confirmation to you@example.com. You will get tracking details when it ships.</p>
    <dl class="order-meta">
      <div><dt>Order number</dt><dd>OH-20481</dd></div>
      <div><dt>Date</dt><dd>Sep 23, 2026</dd></div>
      <div><dt>Total</dt><dd>$266.76</dd></div>
      <div><dt>Payment</dt><dd>Card ending 4242</dd></div>
    </dl>
    <div class="summary-card">
      <h2>Order details</h2>
      <ul class="summary-items">{summary_items()}</ul>
      <hr>
      <p class="summary-row summary-row--total"><span>Total</span><span>$266.76</span></p>
    </div>
    <div class="btn-row">
      <a class="btn btn--primary" href="order-tracking.html">Track your order</a>
      <a class="btn btn--light" href="shop.html">Continue shopping</a>
    </div>
  </div>
</section>
<!-- Order Complete End -->"""
    page("order-complete.html", "Order complete", "Your order has been placed.", body)


def wishlist_page():
    rows = ""
    for k, stock in [("orbit", True), ("frame", True), ("arc", False)]:
        p = P[k]
        st = '<span class="badge badge--stock">In stock</span>' if stock else '<span class="badge badge--out">Out of stock</span>'
        btn = ('<button class="btn btn--primary btn--sm" type="button" data-add-to-cart>Add to cart</button>' if stock
               else '<button class="btn btn--light btn--sm" type="button" disabled>Notify me</button>')
        rows += (f'<tr><td><div class="cart-product"><img src="{IMG}/products/{p["img"]}.svg" alt="" width="400" height="400">'
                 f'<div><a href="product-details.html">{p["name"]}</a><small>{p["cat"]}</small></div></div></td>'
                 f'<td data-label="Price">{fmt(p["price"])}</td><td data-label="Stock">{st}</td><td>{btn}</td>'
                 f'<td><button class="remove-btn" type="button" data-remove-item aria-label="Remove {p["name"]} from wishlist">{icon("trash")}</button></td></tr>')
    body = f"""{page_banner('Wishlist', [], 'Products you saved for later.')}

<!-- Wishlist Start -->
<div class="section section--tight">
  <div class="container">
    <div class="table-scroll" data-wishlist-page>
      <table class="data-table cart-table">
        <caption class="visually-hidden">Saved products</caption>
        <thead><tr><th scope="col">Product</th><th scope="col">Price</th><th scope="col">Stock</th><th scope="col"><span class="visually-hidden">Add to cart</span></th><th scope="col"><span class="visually-hidden">Remove</span></th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</div>
<!-- Wishlist End -->"""
    page("wishlist.html", "Wishlist", "Products you saved for later.", body)


def compare_page():
    keys = ["aero", "pulse", "echo"]
    head = "".join(f'<th scope="col"><img src="{IMG}/products/{P[k]["img"]}.svg" alt="" width="400" height="400"><a href="product-details.html">{P[k]["name"]}</a>'
                   f'<br><button class="text-btn" type="button" data-remove-item aria-label="Remove {P[k]["name"]} from comparison">Remove</button></th>' for k in keys)
    rows = [("Price", ["$119", "$79", "$89"]), ("Rating", ["4.7 (128)", "4.5 (96)", "4.5 (143)"]), ("Type", ["Over-ear headphones", "In-ear earbuds", "Portable speaker"]),
            ("Battery", ["30 h", "8 h + 24 h case", "12 h"]), ("Noise cancelling", ["Adaptive", "Active", "Not applicable"]),
            ("Water resistance", ["None", "IPX4", "IP67"]), ("Weight", ["250 g", "5 g per bud", "540 g"]), ("Bluetooth", ["5.3", "5.3", "5.2"]),
            ("Availability", ["In stock", "In stock", "In stock"])]
    body = "".join(f'<tr><th scope="row">{l}</th>' + "".join(f"<td>{v}</td>" for v in vals) + "</tr>" for l, vals in rows)
    body += '<tr><th scope="row"><span class="visually-hidden">Add to cart</span></th>' + "".join('<td><button class="btn btn--primary btn--sm" type="button" data-add-to-cart>Add to cart</button></td>' for _ in keys) + "</tr>"
    content = f"""{page_banner('Compare products', [], 'The same specs, side by side.')}

<!-- Compare Start -->
<div class="section section--tight">
  <div class="container">
    <div class="table-scroll">
      <table class="compare-table">
        <caption class="visually-hidden">Product comparison</caption>
        <thead><tr><td></td>{head}</tr></thead>
        <tbody>{body}</tbody>
      </table>
    </div>
  </div>
</div>
<!-- Compare End -->"""
    page("compare.html", "Compare products", "Compare product specs side by side.", content)


def auth_page(filename, title, intro, form, alt):
    body = f"""
<!-- Auth Start -->
<section class="auth-wrap">
  <div class="container">
    <div class="auth-card">
      <h1>{title}</h1>
      <p>{intro}</p>
      {form}
      <p class="auth-alt">{alt}</p>
    </div>
  </div>
</section>
<!-- Auth End -->"""
    page(filename, title, intro, body)


def auth_pages():
    auth_page("login.html", "Log in", "Welcome back. Log in to track orders and see your wishlist.", f"""
      <form class="form-stack" action="my-account.html" method="get" data-validate>
        {field('login-email', 'Email', 'email', auto='email')}
        {field('login-password', 'Password', 'password', auto='current-password', extra=' minlength="8"')}
        <div class="auth-row"><label class="check"><input type="checkbox" name="remember">Remember me</label><a class="link" href="forgot-password.html">Forgot password?</a></div>
        <button class="btn btn--primary btn--block" type="submit">Log in</button>
      </form>""", 'New to Ohmly? <a href="register.html">Create an account</a>')
    auth_page("register.html", "Create an account", "Save your details for faster checkout and track every order.", f"""
      <form class="form-stack" action="my-account.html" method="get" data-validate>
        {field('reg-name', 'Full name', auto='name')}
        {field('reg-email', 'Email', 'email', auto='email')}
        {field('reg-password', 'Password', 'password', auto='new-password', extra=' minlength="8"', hint='At least 8 characters.')}
        {field('reg-confirm', 'Confirm password', 'password', auto='new-password', extra=' data-match="#reg-password" data-error="Passwords do not match."')}
        <label class="check"><input type="checkbox" name="terms" required data-error="Please accept the terms to continue.">I agree to the terms and privacy policy</label>
        <button class="btn btn--primary btn--block" type="submit">Create account</button>
      </form>""", 'Already have an account? <a href="login.html">Log in</a>')
    auth_page("forgot-password.html", "Reset your password", "Enter the email you signed up with and we will send you a reset link.", f"""
      <form class="form-stack" action="#" data-validate data-success="If an account exists for that email, a reset link is on its way.">
        {field('reset-email', 'Email', 'email', auto='email')}
        <button class="btn btn--primary btn--block" type="submit">Send reset link</button>
      </form>""", 'Remembered it? <a href="login.html">Back to log in</a>')


def account_page():
    orders = [("OH-20481", "Sep 23, 2026", "progress", "Shipped", "$266.76"), ("OH-19872", "Aug 30, 2026", "success", "Delivered", "$129.00"),
              ("OH-19210", "Jul 14, 2026", "success", "Delivered", "$699.00"), ("OH-18544", "Jun 2, 2026", "muted", "Returned", "$59.00")]

    def order_rows(items):
        return "".join(f'<tr><td>{o}</td><td>{d}</td><td><span class="status status--{s}">{st}</span></td><td>{t}</td><td><a class="link" href="order-tracking.html">View<span class="visually-hidden"> order {o}</span></a></td></tr>' for o, d, s, st, t in items)

    def table(items, cap):
        return (f'<div class="table-scroll"><table class="data-table"><caption class="visually-hidden">{cap}</caption><thead><tr><th scope="col">Order</th><th scope="col">Date</th>'
                f'<th scope="col">Status</th><th scope="col">Total</th><th scope="col"><span class="visually-hidden">Actions</span></th></tr></thead><tbody>{order_rows(items)}</tbody></table></div>')

    tabs = [("dashboard", "Dashboard"), ("orders", "Orders"), ("addresses", "Addresses"), ("details", "Account details")]
    tb = "".join(f'<button class="tabs__tab" id="acc-tab-{k}" type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="acc-{k}" tabindex="{0 if i == 0 else -1}">{l}</button>' for i, (k, l) in enumerate(tabs))
    body = f"""{page_banner('My account', [], 'Signed in as Sara Lee.')}

<!-- Account Start -->
<section class="section section--tight">
  <div class="container account-layout" data-tabs>
    <div class="account-nav">
      <div class="tabs__list" role="tablist" aria-orientation="vertical" aria-label="Account sections">{tb}</div>
      <a class="logout" href="login.html">Log out</a>
    </div>
    <div>
      <div class="account-panel" id="acc-dashboard" role="tabpanel" aria-labelledby="acc-tab-dashboard">
        <h2>Hello, Sara</h2>
        <p class="text-muted">From here you can check recent orders, manage your addresses and update your details.</p>
        <dl class="stat-row"><div><dt>Orders</dt><dd>12</dd></div><div><dt>Wishlist</dt><dd>3</dd></div><div><dt>Reward points</dt><dd>1,240</dd></div></dl>
        <h3>Recent orders</h3>
        {table(orders[:2], 'Recent orders')}
      </div>
      <div class="account-panel" id="acc-orders" role="tabpanel" aria-labelledby="acc-tab-orders" hidden>
        <h2>Orders</h2>
        {table(orders, 'All orders')}
      </div>
      <div class="account-panel" id="acc-addresses" role="tabpanel" aria-labelledby="acc-tab-addresses" hidden>
        <h2>Addresses</h2>
        <div class="address-grid">
          <div class="address-card"><h3>Shipping address</h3><span class="badge badge--new">Default</span><address>Sara Lee<br>221 Market Street, Apt 4<br>San Francisco, CA 94105<br>United States</address><div class="btn-row"><button class="btn btn--light btn--sm" type="button">Edit</button></div></div>
          <div class="address-card"><h3>Billing address</h3><address>Sara Lee<br>221 Market Street, Apt 4<br>San Francisco, CA 94105<br>United States</address><div class="btn-row"><button class="btn btn--light btn--sm" type="button">Edit</button></div></div>
        </div>
      </div>
      <div class="account-panel" id="acc-details" role="tabpanel" aria-labelledby="acc-tab-details" hidden>
        <h2>Account details</h2>
        <form class="form-grid" action="#" data-validate data-success="Your details have been saved.">
          {field('acc-first', 'First name', auto='given-name', extra=' value="Sara"')}
          {field('acc-last', 'Last name', auto='family-name', extra=' value="Lee"')}
          {field('acc-email', 'Email', 'email', auto='email', extra=' value="sara@example.com"', full=True)}
          {field('acc-current', 'Current password', 'password', required=False, auto='current-password', hint='Only needed to change your password.')}
          {field('acc-new', 'New password', 'password', required=False, auto='new-password', extra=' minlength="8"')}
          <div class="full"><button class="btn btn--primary" type="submit">Save changes</button></div>
        </form>
      </div>
    </div>
  </div>
</section>
<!-- Account End -->"""
    page("my-account.html", "My account", "Manage your orders, addresses and account details.", body)


def tracking_page():
    steps = [("is-done", "Order placed", "Sep 23, 10:14"), ("is-done", "Packed", "Sep 23, 16:40"), ("is-current", "Shipped", "Sep 24, 09:02, with FastParcel"),
             ("", "Out for delivery", "Expected Sep 26"), ("", "Delivered", "Expected Sep 26")]
    ol = "".join(f'<li class="{c}"><div><h3>{t}</h3><p>{d}</p></div></li>' for c, t, d in steps)
    body = f"""{page_banner('Track your order', [], 'Enter your order number and email to see where your order is.')}

<!-- Tracking Start -->
<section class="section section--tight">
  <div class="container tracking-layout">
    <div class="form-card">
      <h2>Find your order</h2>
      <p>Your order number starts with OH and is in your confirmation email.</p>
      <form class="form-stack" action="#" data-validate data-success="Showing the latest status for your order.">
        {field('track-order', 'Order number', extra=' placeholder="OH-20481"')}
        {field('track-email', 'Email', 'email', auto='email')}
        <button class="btn btn--primary btn--block" type="submit">Track order</button>
      </form>
    </div>
    <div>
      <h2>Order OH-20481</h2>
      <p class="text-muted">Estimated delivery: Saturday, Sep 26</p>
      <ol class="timeline">{ol}</ol>
    </div>
  </div>
</section>
<!-- Tracking End -->"""
    page("order-tracking.html", "Track your order", "Check the delivery status of your order.", body)


def about_page():
    steps = [("Shortlist", "We start with what customers ask for, then pick the models worth testing."),
             ("Live with it", "Every product is used daily by our team for at least two weeks."),
             ("Measure it", "We check battery, weight and noise claims against the box."),
             ("Publish the numbers", "The specs you see on each card are the ones we measured.")]
    li = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps)
    body = f"""{page_banner('About Ohmly', [], 'An electronics store that shows its working.')}

<!-- Story Start -->
<section class="section">
  <div class="container split">
    <div class="split__media"><img src="{IMG}/products/laptop.svg" alt="" width="400" height="400"></div>
    <div class="split__copy">
      <h2>We test electronics so you can compare them honestly.</h2>
      <p>Ohmly started in 2019 with a simple idea: product pages should tell you what a device actually does, not what the marketing says it might.</p>
      <p>Today we stock around 1,200 products. Each one has been used by our team before it goes on sale, and every card in the shop shows the specs that matter most for that kind of product.</p>
      <dl class="facts-row"><div><dt>Founded</dt><dd>2019</dd></div><div><dt>Products tested</dt><dd>1,200+</dd></div><div><dt>Team</dt><dd>42 people</dd></div><div><dt>Ships to</dt><dd>30 countries</dd></div></dl>
    </div>
  </div>
</section>
<!-- Story End -->

<!-- Process Start -->
<section class="section section--surface" aria-labelledby="process-title">
  <div class="container">
    {section_head('How we choose what we sell', id_='process-title')}
    <ol class="process">{li}</ol>
  </div>
</section>
<!-- Process End -->
{services()}
{newsletter_band()}"""
    page("about.html", "About", "Learn how Ohmly chooses and tests the electronics we sell.", body)


def contact_page():
    body = f"""{page_banner('Contact us', [], 'Questions about an order or a product? We reply within one business day.')}

<!-- Contact Start -->
<section class="section section--tight">
  <div class="container contact-layout">
    <div>
      <h2>Get in touch</h2>
      <p class="text-muted">Our product team can help you choose, and our support team can help with orders, returns and warranty claims.</p>
      <ul class="contact-list">
        <li><span class="icon">{icon('pin')}</span><p>Visit<span>221 Market Street, San Francisco, CA 94105</span></p></li>
        <li><span class="icon">{icon('phone')}</span><p>Call<span><a href="tel:+15550142000">+1 (555) 014-2000</a></span></p></li>
        <li><span class="icon">{icon('mail')}</span><p>Email<span><a href="mailto:hello@example.com">hello@example.com</a></span></p></li>
        <li><span class="icon">{icon('clock')}</span><p>Hours<span>Monday to Sunday, 9:00 to 18:00</span></p></li>
      </ul>
      <!-- Map: change the address after "q=" in both links (use + for spaces) -->
      <div class="map-card">
        <iframe class="map-card__frame" title="Map showing the Ohmly store at 221 Market Street, San Francisco"
          src="https://maps.google.com/maps?q=221+Market+Street,+San+Francisco,+CA+94105&amp;z=15&amp;output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        <div class="map-card__info">
          <span class="map-card__pin">{icon('pin')}</span>
          <p><strong>Ohmly Store</strong><span>221 Market Street, San Francisco</span></p>
          <a class="btn btn--primary btn--sm" href="https://www.google.com/maps/dir/?api=1&amp;destination=221+Market+Street,+San+Francisco,+CA+94105" target="_blank" rel="noopener">Directions</a>
        </div>
      </div>
    </div>
    <div class="form-card">
      <h2>Send us a message</h2>
      <p>Fields marked with * are required.</p>
      <form class="form-grid" action="#" data-validate data-success="Thanks, we will reply within one business day.">
        {field('contact-name', 'Name', auto='name')}
        {field('contact-email', 'Email', 'email', auto='email')}
        {field('contact-phone', 'Phone', 'tel', required=False, auto='tel')}
        <div class="field"><label class="field-label" for="contact-topic">Topic</label>
          <select class="form-control" id="contact-topic" name="contact-topic"><option>Order question</option><option>Product advice</option><option>Returns</option><option>Warranty</option><option>Other</option></select></div>
        {field('contact-message', 'Message', 'textarea', full=True)}
        <div class="full"><button class="btn btn--primary" type="submit">Send message</button></div>
      </form>
    </div>
  </div>
</section>
<!-- Contact End -->"""
    page("contact.html", "Contact", "Contact the Ohmly team about orders, products, returns or warranty.", body)


def faq_page():
    groups = [("orders", "Orders", [("How do I change or cancel my order?", "Contact us within 1 hour of ordering and we will update or cancel it before it is packed."),
                                     ("Can I order by phone?", "Yes. Call our team during opening hours and we will place the order for you.")]),
              ("shipping", "Shipping", [("How long does delivery take?", "Standard delivery takes 2 to 4 business days. Express orders placed before 14:00 arrive the next business day."),
                                        ("Do you ship internationally?", "We ship to 30 countries. Duties and taxes are shown at checkout.")]),
              ("returns", "Returns", [("What is your returns policy?", "You can return any product within 30 days for a full refund. The return label is free."),
                                      ("When will I get my refund?", "Refunds are issued within 3 business days of your return arriving.")]),
              ("warranty", "Warranty", [("What does the 2-year warranty cover?", "Any fault that is not caused by accidental damage. We repair or replace the product, your choice."),
                                        ("How do I make a warranty claim?", "Send us your order number and a short description of the fault from the contact page.")])]
    nav_ = "".join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in groups)
    content = ""
    n = 0
    for k, t, qs in groups:
        items = ""
        for q, a in qs:
            n += 1
            items += (f'<div class="accordion__item"><h3><button class="accordion__trigger" type="button" aria-expanded="{"true" if n == 1 else "false"}" aria-controls="faq-{n}">{q}{icon("plus")}</button></h3>'
                      f'<div class="accordion__panel" id="faq-{n}"{"" if n == 1 else " hidden"}><p>{a}</p></div></div>')
        content += f'<div class="faq-group" id="{k}"><h2>{t}</h2><div class="accordion" data-accordion>{items}</div></div>'
    body = f"""{page_banner('Frequently asked questions', [], 'Answers about orders, shipping, returns and warranty.')}

<!-- FAQ Start -->
<section class="section section--tight">
  <div class="container faq-layout">
    <nav aria-label="FAQ topics"><ul>{nav_}</ul></nav>
    <div>{content}</div>
  </div>
</section>
<!-- FAQ End -->"""
    page("faq.html", "FAQ", "Answers to common questions about orders, shipping, returns and warranty.", body)


def blog_sidebar():
    recent = "".join(f'<li><img src="{IMG}/blog/{p[2]}.svg" alt="" width="1200" height="750" loading="lazy"><div><a href="blog-details.html">{p[0]}</a><small>{p[3]}</small></div></li>' for p in POSTS[:3])
    return f"""
<aside class="sidebar" aria-label="Blog sidebar">
  <div class="widget">
    <h2>Search</h2>
    <form class="search-pill" action="blog.html" role="search">
      <label class="visually-hidden" for="blog-search">Search articles</label>
      <input id="blog-search" type="search" name="q" placeholder="Search articles">
      <button type="submit" aria-label="Search">{icon('search')}</button>
    </form>
  </div>
  <div class="widget"><h2>Categories</h2><ul class="cat-list"><li><a href="blog.html">Guides</a><span>14</span></li><li><a href="blog.html">Reviews</a><span>22</span></li><li><a href="blog.html">Setups</a><span>8</span></li><li><a href="blog.html">News</a><span>11</span></li></ul></div>
  <div class="widget"><h2>Recent posts</h2><ul class="recent-posts">{recent}</ul></div>
  <div class="widget"><h2>Tags</h2><ul class="tag-list"><li><a href="blog.html">Headphones</a></li><li><a href="blog.html">Laptops</a></li><li><a href="blog.html">Battery</a></li><li><a href="blog.html">Desk setup</a></li><li><a href="blog.html">Cameras</a></li></ul></div>
</aside>"""


def blog_page():
    posts = "".join(post_card(p, "h2") for p in POSTS)
    body = f"""{page_banner('Journal', [], 'Buying guides, reviews and setup ideas from the Ohmly team.')}

<!-- Blog Start -->
<div class="section section--tight">
  <div class="container blog-layout">
    <div>
      <div class="post-grid post-grid--2">{posts}</div>
      <nav class="pagination" aria-label="Pagination"><ul><li><span aria-current="page">1</span></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><a href="#" aria-label="Next page">{icon('chevron-right')}</a></li></ul></nav>
    </div>
    {blog_sidebar()}
  </div>
</div>
<!-- Blog End -->"""
    page("blog.html", "Journal", "Buying guides, reviews and setup ideas for electronics.", body)


def blog_details():
    p = POSTS[0]
    body = f"""
<!-- Article Start -->
<div class="section section--tight">
  <div class="container">
    {breadcrumb([('Home', 'index.html'), ('Journal', 'blog.html'), (p[0], '')])}
  </div>
  <div class="container blog-layout">
    <article>
      <header class="article-head">
        <p class="post-card__meta"><a href="blog.html">{p[1]}</a><span>{p[3]}</span><span>{p[4]}</span></p>
        <h1>{p[0]}</h1>
        <p class="lead">{p[5]}</p>
      </header>
      <div class="article-cover"><img src="{IMG}/blog/{p[2]}.svg" alt="Over-ear headphones on a blue background" width="1200" height="750"></div>
      <div class="prose">
        <p>Noise cancelling has gone from a premium extra to a standard feature. That makes choosing harder, because every box now promises the same thing. Here is how to read the specs and what to test in the store.</p>
        <h2>Start with where you will wear them</h2>
        <p>Commuters need strong low-frequency cancelling for engines and trains. Office workers benefit more from cancelling in the mid range, where voices sit. Adaptive modes switch between the two automatically.</p>
        <blockquote><p>Battery claims are usually measured with noise cancelling off. Look for the number with it on.</p></blockquote>
        <h2>The three specs that matter</h2>
        <ul><li><strong>Battery with ANC on:</strong> 25 hours or more covers a long-haul flight.</li><li><strong>Weight:</strong> under 260 g is comfortable for all-day wear.</li><li><strong>Multipoint:</strong> connects to your phone and laptop at the same time.</li></ul>
        <h2>What you can ignore</h2>
        <p>Frequency response ranges beyond 20 kHz and driver sizes above 40 mm rarely change what you hear. Comfort and fit matter far more.</p>
      </div>
      <footer class="article-foot">
        <ul class="tag-list"><li><a href="blog.html">Headphones</a></li><li><a href="blog.html">Buying guide</a></li></ul>
        <p class="text-muted">Share: <a class="link" href="#">X</a>, <a class="link" href="#">Facebook</a>, <a class="link" href="#">Email</a></p>
      </footer>
      <div class="author-box"><span class="avatar">JM</span><div><strong>Jamie Moss</strong><p>Audio editor at Ohmly. Has tested over 200 pairs of headphones.</p></div></div>
      <section class="comments" aria-labelledby="comments-title">
        <h2 id="comments-title">2 comments</h2>
        <ol>
          <li class="comment"><span class="avatar avatar--sm">RK</span><div><strong>Rahul K.</strong><small>Sep 13, 2026</small><p>Really useful point about battery life with ANC on. I had no idea the box numbers were measured with it off.</p></div></li>
          <li class="comment comment--reply"><span class="avatar avatar--sm">JM</span><div><strong>Jamie Moss</strong><small>Sep 13, 2026</small><p>Thanks Rahul. Most brands list both if you check the full spec sheet.</p></div></li>
        </ol>
        <form class="form-card review-form" action="#" data-validate data-success="Thanks, your comment will appear after moderation.">
          <h2>Leave a comment</h2>
          <div class="form-grid">
            {field('comment-name', 'Name', auto='name')}
            {field('comment-email', 'Email', 'email', auto='email', hint='Not published.')}
            {field('comment-text', 'Comment', 'textarea', full=True)}
          </div>
          <div class="btn-row"><button class="btn btn--primary" type="submit">Post comment</button></div>
        </form>
      </section>
    </article>
    {blog_sidebar()}
  </div>
</div>
<!-- Article End -->"""
    page("blog-details.html", p[0], p[5], body)


def error_page():
    body = f"""
<!-- 404 Start -->
<section class="error-page">
  <div class="container error-page__inner">
    <p class="code">404</p>
    <h1>This page is missing</h1>
    <p>The link may be broken, or the page may have moved. Try searching, or head back to the shop.</p>
    <form class="search-pill" action="shop.html" role="search">
      <label class="visually-hidden" for="error-search">Search products</label>
      <input id="error-search" type="search" name="q" placeholder="Search products">
      <button type="submit" aria-label="Search">{icon('search')}</button>
    </form>
    <div class="btn-row"><a class="btn btn--primary" href="index.html">Back to home</a><a class="btn btn--light" href="shop.html">Browse the shop</a></div>
  </div>
</section>
<!-- 404 End -->"""
    page("404.html", "Page not found", "The page you are looking for could not be found.", body)


def coming_soon():
    body = f"""
<div class="coming-soon">
  <!-- Header Start -->
  <header>
    <a href="index.html"><img src="{IMG}/logo.svg" alt="{BRAND} home" width="120" height="32"></a>
    <a class="link" href="contact.html">Contact</a>
  </header>
  <!-- Header End -->
  <!-- Main Content Start -->
  <main id="main">
    <div class="coming-soon__inner">
      <h1>Something new is almost here.</h1>
      <p class="lead">We are getting the store ready. Leave your email and we will tell you the moment it opens.</p>
      <div class="countdown" data-countdown="+12d">Opening soon</div>
      <form class="newsletter-form" action="#" data-validate data-success="You are on the list. See you soon.">
        <label class="visually-hidden" for="soon-email">Email address</label>
        <input class="form-control" id="soon-email" name="email" type="email" autocomplete="email" placeholder="Email address" required>
        <button class="btn btn--primary" type="submit">Notify me</button>
      </form>
    </div>
  </main>
  <!-- Main Content End -->
  <!-- Footer Start -->
  <footer><p>&copy; 2026 {BRAND}</p><p><a href="#">Instagram</a> &nbsp; <a href="#">YouTube</a></p></footer>
  <!-- Footer End -->
</div>
<div class="toast-region" aria-live="polite"></div>"""
    page("coming-soon.html", "Coming soon", "The store is opening soon.", body, bare=True)


if __name__ == "__main__":
    home1(); home2(); home3()
    shop_page("shop.html", "Shop")
    shop_page("shop-list.html", "Shop list", list_view=True)
    shop_page("shop-fullwidth.html", "Shop full width", full=True)
    product_details(); cart_page(); checkout_page(); order_complete(); wishlist_page(); compare_page()
    auth_pages(); account_page(); tracking_page(); about_page(); contact_page(); faq_page()
    blog_page(); blog_details(); error_page(); coming_soon()
    print(len([f for f in os.listdir(OUT) if f.endswith('.html')]), "pages written")
