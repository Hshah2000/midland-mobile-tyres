#!/usr/bin/env python3
"""
Builds every HTML page of the Midland Mobile Tyres site.

You do NOT need this to run the site: the finished .html files are already
in the folder. Use it only if you want to change something that appears on
every page (phone number, web address, towns) in one go:

    1. Edit the SETTINGS block below.
    2. Run:  python3 tools/build_site.py
    3. Upload the changed files to GitHub.
"""
import json
from pathlib import Path

# ============================ SETTINGS ============================
BUSINESS = "Midland Mobile Tyres"
PHONE_DISPLAY = "07376 023691"
PHONE_INTL = "+447376023691"          # used for tel: links
WHATSAPP = "447376023691"             # no + or spaces
# Your live web address, no slash at the end. Change when you get a domain.
BASE_URL = "https://YOUR-USERNAME.github.io/midland-mobile-tyres"
# Swap for the Google Business Profile "read reviews" link when you have it.
GOOGLE_REVIEWS_URL = "https://www.google.com/search?q=Midland+Mobile+Tyres+reviews"
# ==================================================================

ROOT = Path(__file__).resolve().parent.parent
TEL = f"tel:{PHONE_INTL}"
WA = f"https://wa.me/{WHATSAPP}?text=" + "Hi%2C%20I%20need%20help%20with%20a%20tyre.%20My%20location%20is%3A%20"

# ----------------------------- icons ------------------------------
def ico(body, fill=False):
    attrs = ('fill="currentColor"' if fill else
             'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"')
    return f'<svg viewBox="0 0 24 24" {attrs} aria-hidden="true" focusable="false">{body}</svg>'

I = {
    "phone": ico('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "chat": ico('<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/><path d="M9.5 9.5c.5 2 2 3.5 4 4l1-1 1.5.6v1.4c-3.5.3-7.2-3.4-6.9-6.9h1.4l.6 1.5z" fill="currentColor" stroke="none"/>'),
    "tyre": ico('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6.5"/><circle cx="12" cy="12" r="2"/><path d="M12 5.5v4.5M12 14v4.5M5.5 12H10M14 12h4.5"/>'),
    "wrench": ico('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'),
    "battery": ico('<rect x="2" y="7" width="20" height="13" rx="2"/><path d="M6 7V4.5h3V7M15 7V4.5h3V7"/><path d="m13 10-3 4h4l-3 4" />'),
    "warning": ico('<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
    "home": ico('<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>'),
    "pin": ico('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "check": ico('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/>'),
    "menu": ico('<path d="M3 6h18M3 12h18M3 18h18"/>'),
}

LOGO_MARK = ('<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
             '<circle cx="24" cy="24" r="20" fill="none" stroke="#ffd400" stroke-width="6" stroke-dasharray="6 2.4"/>'
             '<circle cx="24" cy="24" r="12.5" fill="none" stroke="#ffd400" stroke-width="3"/>'
             '<circle cx="24" cy="24" r="5" fill="#ffd400"/></svg>')

# ----------------------------- areas ------------------------------
AREAS = [
    {
        "slug": "telford", "name": "Telford",
        "nearby": "Madeley, Dawley, Hadley, Donnington, Ironbridge and Priorslee",
        "intro": [
            "Stuck with a flat in Telford? Midland Mobile Tyres comes to you, whether you're parked at home, at work on one of the town's business parks, or on the hard shoulder near the M54. We bring the tyres and the kit and fit them on the spot, so you don't need to find a garage.",
            "We cover the whole borough, day and night, including Telford town centre and the surrounding estates. Call, tell us your tyre size and where you are, and we'll give you an ETA there and then.",
        ],
        "faq": [
            ("Do you cover the M54 around Telford?", "Yes. If it's safe to work where you've stopped, we'll come out to you. If you're on a motorway, get yourself and your passengers to a safe place behind the barrier first, then call us."),
            ("Can you fit tyres at my workplace in Telford?", "Yes. Give us the address and where the car is parked and we'll fit the tyres while you carry on working."),
        ],
    },
    {
        "slug": "shrewsbury", "name": "Shrewsbury",
        "nearby": "Harlescott, Battlefield, Monkmoor, Meole Brace and Bayston Hill",
        "intro": [
            "Midland Mobile Tyres fits tyres anywhere in and around Shrewsbury: on your drive, in your work car park, or at the roadside on the A5 and A49. You won't need to limp to a tyre centre on a damaged tyre.",
            "We're on call 24/7. Ring us with your tyre size and location and we'll tell you when we can be there.",
        ],
        "faq": [
            ("Do you come out to villages around Shrewsbury?", "Yes. We cover the town and the surrounding villages. Call us with your postcode and we'll confirm."),
            ("Can you fix a puncture instead of replacing the tyre?", "Often, yes. If the damage is in the repairable area of the tread we'll repair it. If it isn't safe to repair, we'll tell you and fit a new tyre."),
        ],
    },
    {
        "slug": "wellington", "name": "Wellington",
        "nearby": "Admaston, Leegomery, Arleston, Ketley and The Wrekin area",
        "intro": [
            "Midland Mobile Tyres covers Wellington and the villages around The Wrekin. We'll come to your home, your work or the roadside and change your tyre where the car is.",
            "Flat tyre first thing in the morning? Battery dead after a cold night? Call us at any hour and we'll get you moving again.",
        ],
        "faq": [
            ("How quickly can you get to Wellington?", "It depends on where we are and how busy it is. Call and we'll give you an honest ETA before we set off."),
            ("Do you help with flat batteries in Wellington?", "Yes. We offer battery assistance as well as tyres and puncture repairs."),
        ],
    },
    {
        "slug": "newport", "name": "Newport",
        "nearby": "Edgmond, Church Aston, Chetwynd and Lilleshall",
        "intro": [
            "Midland Mobile Tyres provides mobile tyre fitting in Newport, Shropshire, and the villages around it. Whether you're at home, at work or stuck on the A41, we bring the tyres to you.",
            "Our 24/7 service means you're not stuck waiting for a garage to open. Call, tell us your tyre size, and we'll do the rest.",
        ],
        "faq": [
            ("Do you cover rural roads around Newport?", "Yes. Send us your location (a WhatsApp location pin is perfect) and we'll find you."),
            ("What do I need to tell you when I call?", "Your tyre size from the sidewall (for example 205/55 R16), where you are, and the make and model of the car."),
        ],
    },
    {
        "slug": "bridgnorth", "name": "Bridgnorth",
        "nearby": "High Town, Low Town, Tasley, Oldbury and Alveley",
        "intro": [
            "Midland Mobile Tyres fits tyres in Bridgnorth, in both High Town and Low Town, and on the A442 and A458. We come to you with the tyres and the equipment to fit them.",
            "Punctures don't wait for opening hours, so neither do we. Call any time, day or night.",
        ],
        "faq": [
            ("Can you come to me if I'm parked on a hill in Bridgnorth?", "In most cases, yes. We'll check the spot is safe to jack the car up when we arrive. If it isn't, we'll talk you through the options."),
            ("Do you stock budget and premium tyres?", "Tell us your size when you call and we'll go through the tyres we can get for you."),
        ],
    },
    {
        "slug": "oakengates", "name": "Oakengates",
        "nearby": "St Georges, Wrockwardine Wood, Trench, Ketley Bank and Priorslee",
        "intro": [
            "Need a tyre in Oakengates? Midland Mobile Tyres comes to your door, your workplace or the roadside, and fits the new tyre on the spot.",
            "We're local to Telford, so Oakengates and the neighbouring estates are right on our doorstep. Call 24/7 for tyres, punctures, batteries and roadside help.",
        ],
        "faq": [
            ("Do you cover St Georges and Trench as well?", "Yes, along with all of the surrounding Telford estates."),
            ("Can I send you a photo of my tyre?", f"Yes. Send a photo of the tyre sidewall on WhatsApp to {PHONE_DISPLAY} and we'll take it from there."),
        ],
    },
]

SERVICES = [
    ("tyre", "Tyre Changes", "New tyres fitted at your home, work or roadside. Tell us your tyre size and we'll bring the right tyre to you."),
    ("wrench", "Puncture Repairs", "Nails, screws and slow punctures repaired on the spot where it's safe to do so. If it can't be repaired, we'll replace it."),
    ("battery", "Battery Assistance", "Flat battery? We can get you started and help you sort out a replacement if your battery has had it."),
    ("warning", "Roadside Assistance", "Stuck at the roadside? We come out 24/7 to get you moving again, whatever the time."),
]

HOME_FAQ = [
    ("Do you really come to my home or work?", "Yes. That's what we do. We change tyres at your house, at work or wherever you've broken down. Just give us a call."),
    ("Are you open 24 hours?", f"Yes. Midland Mobile Tyres is available 24/7, including evenings, weekends and bank holidays. Call {PHONE_DISPLAY}."),
    ("Which areas do you cover?", "The Midlands and Shropshire, including Telford, Shrewsbury, Wellington, Newport, Bridgnorth and Oakengates. If you're not sure we cover you, call us and ask."),
    ("What information do you need when I call?", "Your location, the make and model of your car, and your tyre size. The size is printed on the side of the tyre and looks like 205/55 R16."),
    ("Can my puncture be repaired?", "Many punctures in the main tread can be repaired safely. Damage to the sidewall or shoulder, or a tyre that's been driven on flat, usually means it needs replacing. We'll check and tell you honestly."),
    ("Can I message you instead of calling?", f"Yes. Message us on WhatsApp at {PHONE_DISPLAY}. Sending your location and a photo of the tyre sidewall helps us quote quickly."),
]

# --------------------------- page parts ---------------------------
def head(title, desc, path, root, extra_ld):
    canonical = f"{BASE_URL}/{path}"
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in extra_ld)
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0b0b0b">
<meta name="geo.region" content="GB-SHR">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="{BUSINESS}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/images/flyer.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&amp;family=Montserrat:ital,wght@1,800;1,900&amp;display=swap">
<link rel="stylesheet" href="{root}css/styles.css">
{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(root, current=""):
    def cur(k):
        return ' aria-current="page"' if k == current else ""
    home = f"{root}index.html" if root else ""
    return f"""<div class="topbar">
  <div class="container">
    <span class="tb-services">Tyres &bull; Punctures &bull; Batteries &bull; Roadside Assistance</span>
    <a href="{TEL}">Available 24/7 &mdash; Call {PHONE_DISPLAY}</a>
  </div>
</div>
<header class="site-header">
  <div class="container">
    <a class="logo" href="{root}index.html" aria-label="{BUSINESS} home">
      {LOGO_MARK}
      <span class="logo-text"><span class="l1">Midland</span><span class="l2">Mobile Tyres</span></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">{I["menu"]}</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
        <li><a href="{home}#services"{cur("services")}>Services</a></li>
        <li><a href="{home}#how-it-works">How It Works</a></li>
        <li><a href="{home}#areas"{cur("areas")}>Areas</a></li>
        <li><a href="{home}#faq">FAQ</a></li>
        <li><a class="btn btn-yellow" href="{TEL}">{I["phone"]} {PHONE_DISPLAY}</a></li>
      </ul>
    </nav>
  </div>
</header>
"""


def cta_band():
    return f"""<section class="cta-band" aria-label="Call us">
  <div class="container">
    <div class="cta-phone-icon">{I["phone"]}</div>
    <div class="cta-text">
      <p class="head">Call now &bull; Available 24/7</p>
      <a class="number" href="{TEL}">{PHONE_DISPLAY}</a>
    </div>
    <div class="btn-row">
      <a class="btn btn-black" href="{WA}" rel="noopener" target="_blank">{I["chat"]} WhatsApp us</a>
    </div>
  </div>
  <div class="tread" aria-hidden="true"></div>
</section>
"""


def footer(root):
    area_items = "\n".join(f'<li><a href="{root}areas/{a["slug"]}.html">Mobile tyres {a["name"]}</a></li>' for a in AREAS)
    home = f"{root}index.html"
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{home}" aria-label="{BUSINESS} home">
          {LOGO_MARK}
          <span class="logo-text"><span class="l1">Midland</span><span class="l2">Mobile Tyres</span></span>
        </a>
        <p>24/7 mobile tyre services and roadside assistance across the Midlands and Shropshire.</p>
      </div>
      <div>
        <h3>Services</h3>
        <ul>
          <li><a href="{home}#services">Tyre changes</a></li>
          <li><a href="{home}#services">Puncture repairs</a></li>
          <li><a href="{home}#services">Battery assistance</a></li>
          <li><a href="{home}#services">Roadside assistance</a></li>
        </ul>
      </div>
      <div>
        <h3>Areas we cover</h3>
        <ul>
{area_items}
        </ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="{TEL}">Call {PHONE_DISPLAY}</a></li>
          <li><a href="{WA}" rel="noopener" target="_blank">WhatsApp {PHONE_DISPLAY}</a></li>
          <li>Open 24 hours, 7 days a week</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">&copy; <span id="year">2026</span> {BUSINESS}. All rights reserved.</div>
  </div>
</footer>
<nav class="mobile-bar" aria-label="Quick contact">
  <a class="call" href="{TEL}">{I["phone"]} Call Now</a>
  <a class="wa" href="{WA}" rel="noopener" target="_blank">{I["chat"]} WhatsApp</a>
</nav>
<a class="wa-float" href="{WA}" rel="noopener" target="_blank" aria-label="Message us on WhatsApp">{I["chat"]}</a>
<script src="{root}js/main.js" defer></script>
</body>
</html>
"""


def faq_html(items):
    return "\n".join(
        f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "AutoRepair",
        "@id": f"{BASE_URL}/#business",
        "name": BUSINESS,
        "description": "24/7 mobile tyre fitting, puncture repairs, battery assistance and roadside assistance across the Midlands and Shropshire.",
        "url": f"{BASE_URL}/",
        "telephone": PHONE_INTL,
        "image": f"{BASE_URL}/images/flyer.jpg",
        "logo": f"{BASE_URL}/favicon.svg",
        "priceRange": "££",
        "address": {"@type": "PostalAddress", "addressRegion": "Shropshire", "addressCountry": "GB"},
        "areaServed": [{"@type": "City", "name": a["name"]} for a in AREAS]
        + [{"@type": "AdministrativeArea", "name": "Shropshire"}, {"@type": "AdministrativeArea", "name": "West Midlands"}],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00", "closes": "23:59"}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Mobile tyre services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES]},
    }


def service_cards():
    return "\n".join(f"""<article class="card">
        <div class="icon-circle">{I[icon]}</div>
        <h3>{title}</h3>
        <p>{text}</p>
      </article>""" for icon, title, text in SERVICES)


def area_links(root, exclude=None):
    return "\n".join(
        f'<li><a href="{root}areas/{a["slug"]}.html">{I["pin"]} {a["name"]}</a></li>'
        for a in AREAS if a["slug"] != exclude)


# ------------------------------ pages -----------------------------
def build_home():
    title = "24/7 Mobile Tyre Fitting Shropshire | Midland Mobile Tyres"
    desc = (f"24/7 mobile tyre fitting, puncture repairs, battery and roadside assistance in Telford, "
            f"Shrewsbury and across the Midlands & Shropshire. We come to you. Call {PHONE_DISPLAY}.")
    html = head(title, desc, "", "", [business_ld(), faq_ld(HOME_FAQ)])
    html += header("")
    html += f"""<main id="main">
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="badge-247"><span class="circle">24/7</span> Mobile tyre services &amp; roadside assistance</div>
      <h1>Mobile Tyre Fitting in <span class="hl">Telford, Shropshire</span> &amp; the Midlands</h1>
      <ul class="service-tags"><li>Tyres</li><li>Punctures</li><li>Batteries</li><li>Roadside Assistance</li></ul>
      <p class="lead">Flat tyre, puncture or dead battery? We come to you, at home, at work or at the roadside, day or night, and get you back on the road.</p>
      <div class="btn-row">
        <a class="btn btn-yellow" href="{TEL}">{I["phone"]} Call {PHONE_DISPLAY}</a>
        <a class="btn btn-outline" href="{WA}" rel="noopener" target="_blank">{I["chat"]} WhatsApp us</a>
      </div>
    </div>
    <div class="hero-media">
      <div class="frame">
        <img src="images/van.jpg" width="622" height="430" alt="Midland Mobile Tyres black and yellow mobile tyre fitting van with new tyres" fetchpriority="high">
      </div>
      <div class="sticker"><small>Call now &bull; 24/7</small><a href="{TEL}">{PHONE_DISPLAY}</a></div>
    </div>
  </div>
</section>

<div class="brush">
  <div class="container">
    {I["home"]}
    <p>We can change tyres at your house, work or wherever you may be. Just give us a call.</p>
  </div>
</div>

<section class="section" id="services" aria-labelledby="services-title">
  <div class="container">
    <div class="section-head">
      <span class="kicker">What we do</span>
      <h2 id="services-title">Mobile Tyre <span class="hl">Services</span></h2>
      <p>Everything is done where your car is. No garage queues, no driving on a damaged tyre.</p>
    </div>
    <div class="cards">
      {service_cards()}
    </div>
  </div>
</section>

<section class="section section-yellow" id="how-it-works" aria-labelledby="how-title">
  <div class="container">
    <div class="section-head">
      <span class="kicker" style="color:#0b0b0b">Simple as 1, 2, 3</span>
      <h2 id="how-title">How It Works</h2>
      <p>Getting help takes one phone call or message.</p>
    </div>
    <ol class="steps">
      <li><h3>Call or WhatsApp</h3><p>Tell us where you are, your car, and your tyre size. We'll give you an ETA.</p></li>
      <li><h3>We come to you</h3><p>Our fully equipped van comes to your home, workplace or roadside location.</p></li>
      <li><h3>Back on the road</h3><p>We fit the tyre or fix the problem on the spot, and you're on your way.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="why-us" aria-labelledby="why-title">
  <div class="container why-grid">
    <div>
      <span class="kicker">Why choose us</span>
      <h2 id="why-title">Local, Mobile &amp; <span class="hl">Available 24/7</span></h2>
      <ul class="ticks">
        <li>{I["check"]}<div><strong>Open 24 hours, 7 days a week</strong>Nights, weekends and bank holidays. Call whenever it happens.</div></li>
        <li>{I["check"]}<div><strong>We come to you</strong>Home, work or roadside. No need to drive on a flat.</div></li>
        <li>{I["check"]}<div><strong>Tyres, punctures &amp; batteries</strong>One call covers the most common breakdown problems.</div></li>
        <li>{I["check"]}<div><strong>Local to the Midlands &amp; Shropshire</strong>We know the area, so we can find you fast.</div></li>
      </ul>
      <a class="btn btn-yellow" href="{TEL}">{I["phone"]} Call {PHONE_DISPLAY}</a>
      <div class="tip"><strong>Quick tip:</strong> your tyre size is printed on the side of the tyre and looks like <strong>205/55 R16</strong>. Have it ready when you call, or send us a photo on WhatsApp.</div>
    </div>
    <div class="flyer-frame">
      <img src="images/flyer.jpg" width="1200" height="675" loading="lazy" alt="Midland Mobile Tyres flyer: puncture repairs, tyre changes and battery assistance, available 24/7 across the Midlands and Shropshire">
    </div>
  </div>
</section>

<section class="section section-yellow" id="areas" aria-labelledby="areas-title">
  <div class="container areas-grid">
    <div class="section-head">
      <span class="kicker" style="color:#0b0b0b">Areas we cover</span>
      <h2 id="areas-title">The Midlands &amp; Shropshire</h2>
      <p>Based around Telford, we cover towns and villages across Shropshire and the wider Midlands. Not on the list? Call us and ask, as we probably cover you too.</p>
    </div>
    <ul class="area-links">
      {area_links("")}
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="reviews-title">
  <div class="container">
    <div class="reviews-box">
      <div>
        <div class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <h2 id="reviews-title">Read Our <span class="hl">Reviews</span></h2>
        <p>See what our customers say about Midland Mobile Tyres on Google.</p>
      </div>
      <a class="btn btn-yellow" href="{GOOGLE_REVIEWS_URL}" rel="noopener" target="_blank">Read reviews on Google</a>
    </div>
  </div>
</section>

<section class="section section-alt" id="faq" aria-labelledby="faq-title">
  <div class="container">
    <div class="section-head">
      <span class="kicker">FAQ</span>
      <h2 id="faq-title">Frequently Asked <span class="hl">Questions</span></h2>
    </div>
    <div class="faq">
      {faq_html(HOME_FAQ)}
    </div>
  </div>
</section>
</main>
"""
    html += cta_band() + footer("")
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def build_area(a):
    name = a["name"]
    path = f"areas/{a['slug']}.html"
    title = f"Mobile Tyre Fitting {name} | 24/7 | Midland Mobile Tyres"
    desc = (f"24/7 mobile tyre fitting in {name}. Tyre changes, puncture repairs, battery and roadside "
            f"assistance at your home, work or roadside. Call {PHONE_DISPLAY}.")
    service_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Mobile tyre fitting in {name}",
        "serviceType": "Mobile tyre fitting",
        "provider": {"@id": f"{BASE_URL}/#business", "@type": "AutoRepair", "name": BUSINESS, "telephone": PHONE_INTL},
        "areaServed": {"@type": "City", "name": name},
    }
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
        {"@type": "ListItem", "position": 2, "name": f"Mobile Tyres {name}", "item": f"{BASE_URL}/{path}"}]}
    faq = a["faq"] + [HOME_FAQ[1], HOME_FAQ[3]]
    html = head(title, desc, path, "../", [service_ld, crumbs, faq_ld(faq)])
    html += header("../", "areas")
    intro = "\n".join(f"<p>{p}</p>" for p in a["intro"])
    services_list = "\n".join(f"<li>{I['check']}<div><strong>{t}</strong>{d}</div></li>" for _, t, d in SERVICES)
    html += f"""<main id="main">
<section class="page-hero">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="../index.html">Home</a></li><li aria-current="page">Mobile Tyres {name}</li></ol></nav>
    <div class="badge-247"><span class="circle">24/7</span> Mobile tyre fitting {name}</div>
    <h1>Mobile Tyre Fitting <span class="hl">{name}</span></h1>
    <p class="lead">Tyres, punctures, batteries and roadside assistance in {name}, 24 hours a day. We come to you.</p>
    <div class="btn-row">
      <a class="btn btn-yellow" href="{TEL}">{I["phone"]} Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline" href="{WA}" rel="noopener" target="_blank">{I["chat"]} WhatsApp us</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container why-grid">
    <div class="prose">
      <h2>Mobile Tyres in <span class="hl">{name}</span>, Day or Night</h2>
      {intro}
      <p>We also cover nearby areas, including {a["nearby"]}.</p>
      <h2>Our Services in {name}</h2>
      <ul class="ticks">
        {services_list}
      </ul>
    </div>
    <div class="hero-media">
      <div class="frame"><img src="../images/van.jpg" width="622" height="430" loading="lazy" alt="Midland Mobile Tyres van providing mobile tyre fitting in {name}"></div>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="faq-title">
  <div class="container">
    <div class="section-head"><span class="kicker">FAQ</span><h2 id="faq-title">{name} <span class="hl">Questions</span></h2></div>
    <div class="faq">
      {faq_html(faq)}
    </div>
  </div>
</section>

<section class="section section-yellow" aria-labelledby="other-areas">
  <div class="container">
    <div class="section-head"><h2 id="other-areas">Other Areas We Cover</h2><p>We cover the Midlands and Shropshire. These are some of the places we visit most.</p></div>
    <ul class="area-links">
      {area_links("../", exclude=a["slug"])}
    </ul>
  </div>
</section>
</main>
"""
    html += cta_band() + footer("../")
    (ROOT / path).write_text(html, encoding="utf-8")


def build_404():
    from urllib.parse import urlparse
    r = (urlparse(BASE_URL).path.rstrip("/") + "/")  # e.g. /midland-mobile-tyres/ or /
    html = head("Page Not Found | Midland Mobile Tyres", "Page not found. Call Midland Mobile Tyres 24/7.", "404.html", r, [])
    html = html.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">')
    html += header(r)
    html += f"""<main id="main"><section class="page-hero"><div class="container">
<h1>Page <span class="hl">Not Found</span></h1>
<p class="lead">Sorry, that page doesn't exist. Need a tyre? We're available 24/7.</p>
<div class="btn-row"><a class="btn btn-yellow" href="{TEL}">{I["phone"]} Call {PHONE_DISPLAY}</a>
<a class="btn btn-outline" href="{r}">Back to home</a></div>
</div></section></main>
"""
    html += footer(r)
    (ROOT / "404.html").write_text(html, encoding="utf-8")


def build_seo_files():
    urls = [""] + [f"areas/{a['slug']}.html" for a in AREAS]
    items = "\n".join(
        f"  <url><loc>{BASE_URL}/{u}</loc><changefreq>monthly</changefreq><priority>{'1.0' if not u else '0.8'}</priority></url>"
        for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="10" fill="#0b0b0b"/>'
        + LOGO_MARK.split(">", 1)[1].replace("</svg>", "") + "</svg>\n", encoding="utf-8")


if __name__ == "__main__":
    (ROOT / "areas").mkdir(exist_ok=True)
    build_home()
    for area in AREAS:
        build_area(area)
    build_404()
    build_seo_files()
    print("Built index.html, 404.html,", len(AREAS), "area pages, sitemap.xml, robots.txt, favicon.svg")
