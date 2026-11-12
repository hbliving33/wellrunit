"""Builds the Well Run IT website (wellrunit.com) from build/content.json.
Run from the repo root:  python3 build/build.py
Design: light and calm, Inter only, navy and steel blue, no animation.  No personal names on the site."""
import json, pathlib, html, hashlib, re
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = json.loads((ROOT / 'build' / 'content.json').read_text())
E = html.escape
YEAR = 2026
BRAND = 'Well Run IT'
DOMAIN = 'https://wellrunit.com/'
PRELAUNCH = True   # keeps every page out of search results until launch; set False on launch day and rebuild
PRE_META = '<meta name="robots" content="noindex, nofollow">\n' if PRELAUNCH else ''

SERVICE_ORDER = ['microsoft-365', 'business-applications', 'network', 'cybersecurity', 'it-strategy', 'managed-it', 'cloud', 'ai', 'data-center', 'business-automation', 'access-control', 'compliance']
SERVICES = sorted(C['SERVICES'], key=lambda x: SERVICE_ORDER.index(x['slug']) if x['slug'] in SERVICE_ORDER else 99)
# One-line answers to the questions people ask most, placed inside the service they belong to (Nov 2026: instead of Bernie answering questions)
SVC_NOTES = {
  'managed-it': ['No packages.  No tiers.  No paying for what you don\'t use.  Every plan is built around your business.', 'We can take over from your current MSP, and we support companies in all 50 states.'],
  'microsoft-365': ['From sign-in to SharePoint, Exchange and Teams, we support Microsoft 365 for companies of every size.'],
}
SVC = {s['slug']: s for s in SERVICES}
TOPICS = C['TOPICS2']; TOPIC_OF = C['TOPIC_OF']

def ver(rel):
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]

# ---------- brand ----------
CHECK = '<path d="M7 12.6l3.4 3.4L17.2 8.6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
def mark(fill='#1b2430', size=24):
    return f'<svg class="mk" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6.5" fill="{fill}"/>{CHECK}</svg>'

# Logo (picked Nov 1 2026, logo-refine.html number 2): the R in "Run" in stride, tipped 10 degrees with two motion marks.
# Drawn on a 100-unit cap height; the marks take the accent color, the R takes the text color.
STRIDE_W = 109
STRIDE_R = '''<rect x="12.2" y="26" width="22.0" height="9" rx="4.5" class="rm"/><rect x="15.7" y="46" width="15.0" height="9" rx="4.5" class="rm"/><g transform="skewX(-10) translate(46.6 0)"><rect x="0" y="0" width="21" height="100" fill="currentColor"/><path d="M10 10.5H39a22.5 22.5 0 010 45H10" fill="none" stroke="currentColor" stroke-width="21"/><path d="M27 56h22l21 44H47z" fill="currentColor"/></g>'''
def stride_r(cls='gl'):
    return f'<svg class="{cls}" viewBox="0 0 {STRIDE_W} 100" style="width:{STRIDE_W * .727 / 100:.4f}em" aria-hidden="true" overflow="visible">{STRIDE_R}</svg>'

def logo(dark=False):
    return f'<span class="wordmark">Well<b>{stride_r()}un</b><i>IT</i></span>'

def icon(name):
    p = {
      'infra': '<rect x="4" y="3" width="16" height="5" rx="1"/><rect x="4" y="10" width="16" height="5" rx="1"/><rect x="4" y="17" width="16" height="4" rx="1"/><path d="M8 5.5h.01M8 12.5h.01"/>',
      'ops': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      'microsoft-365': '<rect x="3" y="3" width="8" height="8"/><rect x="13" y="3" width="8" height="8"/><rect x="3" y="13" width="8" height="8"/><rect x="13" y="13" width="8" height="8"/>',
      'cybersecurity': '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
      'apps': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 4v5"/>',
      'ai': '<path d="M12 3l1.8 4.6L18.5 9l-4.7 1.6L12 15l-1.8-4.4L5.5 9l4.7-1.4z"/><path d="M18 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
      'network': '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M12 11.5L6.5 17M12 11.5l5.5 5.5"/>',
      'cloud': '<path d="M7 18a4.5 4.5 0 01-.6-9A6 6 0 0118 8.5a4.5 4.5 0 01-.5 9.5z"/>',
      'data-center': '<rect x="4" y="3" width="16" height="5" rx="1"/><rect x="4" y="10" width="16" height="5" rx="1"/><rect x="4" y="17" width="16" height="4" rx="1"/><path d="M8 5.5h.01M8 12.5h.01"/>',
      'compliance': '<path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4M10 13l2 2 4-4"/>',
      'access-control': '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/><circle cx="12" cy="15.5" r="1.5"/>',
      'business-automation': '<path d="M4 7h11M11 3l4 4-4 4M20 17H9M13 13l-4 4 4 4"/>',
      'it-strategy': '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
      'managed-it': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      'doc': '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
      'person': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
      'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l2 2M14 9l2 2"/>',
      'talk': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8"/>',
      'business-applications': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 4v5"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def plain(h):
    return re.sub(r'</?em>', '', h)

NAV = [('index.html', 'Home'), ('services.html', 'Services'), ('about.html', 'About Us'), ('news.html', 'Cyber News')]   # five pages with Contact (Nov 12 2026 trim)
SVC_FILES = {s['slug'] + '.html' for s in SERVICES}

ORG_LD = json.dumps({"@context": "https://schema.org", "@type": "ProfessionalService", "name": BRAND, "url": DOMAIN, "logo": DOMAIN + "assets/brand/og.png",
    "description": "IT infrastructure and operations consulting for startups, small businesses and companies preparing for growth: networks, servers and cloud, Microsoft 365, business applications, security and managed IT.",
    "address": {"@type": "PostalAddress", "addressLocality": "Huntington Beach", "addressRegion": "CA", "addressCountry": "US"}, "areaServed": "US"})

def page(fname, title, desc, body):
    css, js, bj = ver('assets/css/site.css'), ver('assets/js/site.js'), ver('assets/js/bernie.js')
    cur = lambda f: ' aria-current="page"' if f == fname or (fname in SVC_FILES and f == 'services.html') else ''
    nav = ''.join(f'<a href="{f}"{cur(f)}>{n}</a>' for f, n in NAV) + '<a class="talk" href="contact.html">Contact us</a>'
    svc_links = ''.join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    canon = '' if fname == 'index.html' else fname
    full = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{PRE_META}<meta name="theme-color" content="#f6f5f1">
<link rel="canonical" href="{DOMAIN}{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{DOMAIN}{canon}"><meta property="og:image" content="{DOMAIN}assets/brand/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/inter-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={css}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{BRAND}, home">{logo()}</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-row">
      <a class="brand" href="index.html" aria-label="{BRAND}, home">{logo(True)}</a>
      <nav class="foot-links" aria-label="Footer"><a href="services.html">Services</a><a href="about.html">About us</a><a href="news.html">Cyber news</a><a href="contact.html">Contact</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="app.html">Get the app</a></nav>
    </div>
    <div class="base"><span>&copy; {YEAR} {BRAND}</span><span>Supporting all 50 states</span></div>
  </div>
</footer>
<script src="assets/js/site.js?v={js}" defer></script>
<script src="assets/js/bernie.js?v={bj}" defer></script>
</body>
</html>
'''
    (ROOT / fname).write_text(full)

def phero(h1, lead, trail=None):
    tr = f'<div class="trail">{trail}</div>' if trail else ''
    return f'<section class="phero"><div class="wrap">{tr}<h1>{h1}</h1><p class="lead">{lead}</p></div></section>'

def sortable(cols, rows, caption):
    head = ''.join(f'<th scope="col"><button type="button">{c}<span class="arrow" aria-hidden="true"></span></button></th>' for c in cols)
    body = ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join(f'<td>{x}</td>' for x in r[1:]) + '</tr>' for r in rows)
    return f'<table class="sortable"><caption class="hp">{caption}.  Select a column heading to sort.</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'

def cta(title='Ready for IT that runs well?', lead="Tell us what's going on.  A senior consultant replies within one business day."):
    return f'''<section class="cta"><div class="wrap"><div class="panel"><h2>{title}</h2><p class="lead">{lead}</p>
<div class="acts"><a class="btn" href="contact.html">Contact us</a><a class="link" href="about.html#check">Take the free IT health check</a></div></div></div></section>'''

# ---------- shared blocks ----------
TILES = [('infra', 'Infrastructure', 'Networks, servers, storage, cloud and data centers, designed, built and kept running.', 'network.html'),
         ('ops', 'IT operations', 'Users, devices, patching, backups, vendors and onboarding, run the same way every time.', 'managed-it.html'),
         ('microsoft-365', 'Microsoft 365', 'Identity first, then email, files, Teams and devices, set up right and kept clean.', 'microsoft-365.html'),
         ('cybersecurity', 'Security', 'Penetration testing, phishing-resistant MFA, email security and a plan for a bad day.', 'cybersecurity.html'),
         ('apps', 'Business applications', 'ERP, HR and payroll, CRM and quality systems, each with an owner and single sign-on.', 'business-applications.html'),
         ('ai', 'AI', 'Copilot readiness, oversharing cleanup and practical automation, with guardrails.', 'ai.html')]
def tiles():
    return '<div class="tiles">' + ''.join(f'<a class="tile" href="{u}"><span class="ic">{icon(i)}</span><h3>{t}</h3><p>{d}</p><span class="go">Learn more</span></a>' for i, t, d, u in TILES) + '</div>'

WELL_RUN = ['Multi-factor sign-in on every account, including admins', 'Backups you have actually restored, not just run', 'People who leave lose access to everything the same day',
            'Firewalls, servers and laptops patched every month', 'Every license accounted for, with a name next to it', 'A written plan for the day ransomware hits',
            'Documentation and admin access that belong to you']

FIT = [('Startups, small businesses and companies preparing for growth', 'Our sweet spot is the business without a full IT department, or with one IT person stretched thin.  We have been part of a few startups ourselves.'),
       ('People who know your name', 'You talk to the same small team every time, people who know your setup and your people.'),
       ('Enterprise experience', 'Big-company know-how: secure, documented and audit-ready IT, sized and priced for a small business.')]

RUN = [('Core infrastructure', 'Servers, storage, virtualization, networks, Wi-Fi and the links between sites.  Data centers and colocation, designed, built, moved and kept running.'),
       ('IT operations', 'Users, devices, patching, monitoring, backups, onboarding and offboarding, vendors and documentation.  Run the same way every time, with written processes.'),
       ('Microsoft 365 and cloud', 'Identity first: Entra ID, phishing-resistant MFA and conditional access.  Then email, SharePoint, OneDrive, Teams and devices, plus Azure and hybrid servers.'),
       ('Business applications', 'ERP, HR and payroll, CRM and quality systems, each with an owner.  Single sign-on, access by role, and licenses and renewals kept in check.'),
       ('AI', 'Copilot readiness, oversharing cleanup before AI is switched on, plain-English AI policies, and automation that saves real time.'),
       ('Security', 'Penetration testing, phishing-resistant MFA, endpoint protection, email security, staff training and a written plan for a bad day.'),
       ('Facilities', 'When the building is part of the job: office moves and build-outs, server room power and cooling, badge access and cameras.'),
       ('Compliance', 'When audits come, the evidence is ready: SOX, HIPAA and ISO environments.')]

PROOF = [('30+ years', 'running IT operations, from data centers to Microsoft 365'), ('$4.5M', 'cut from one manufacturer’s IT costs over two years'),
         ('1 business day', 'to hear back from a senior consultant'), ('50 states', 'with remote support, on-site across California and Arizona')]

def proof():
    return '<div class="cards four">' + ''.join(f'<div class="card"><div class="stat" style="font-size:40px">{n}</div><p style="margin-top:10px">{t}</p></div>' for n, t in PROOF) + '</div>'

def fit_cards():
    return '<div class="cards">' + ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in FIT) + '</div>'

def quote_block(i=0):
    q, c = C['QUOTES'][i]
    return f'<section><div class="wrap"><figure class="quote"><blockquote>{q}</blockquote><figcaption>{c}.  <a class="link" href="about.html#testimonials">Read the testimonials</a></figcaption></figure></div></section>'

def form():
    opts = ''.join(f'<option>{E(t)}</option>' for t in TOPICS)
    sizes = ''.join(f'<option>{t}</option>' for t in ['1 to 10 people', '11 to 50 people', '51 to 200 people', '200+ people'])
    return f'''<form class="form" id="contactForm" novalidate>
  <div class="row"><div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required maxlength="120"></div><div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="200"></div></div>
  <div class="row"><div class="field"><label for="f-company">Company (optional)</label><input id="f-company" name="company" autocomplete="organization" maxlength="160"></div><div class="field"><label for="f-phone">Phone (optional)</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40"></div></div>
  <div class="row"><div class="field"><label for="f-topic">What can we help with?</label><select id="f-topic" name="topic" required><option value="">Choose one</option>{opts}</select></div><div class="field"><label for="f-size">Company size (optional)</label><select id="f-size" name="size"><option value="">Choose one</option>{sizes}</select></div></div>
  <div class="field"><label for="f-msg">Tell us what's going on</label><textarea id="f-msg" name="message" required maxlength="5000"></textarea></div>
  <div class="hp" aria-hidden="true"><label for="f-hp">Leave this empty</label><input id="f-hp" name="_honey" tabindex="-1" autocomplete="off"></div>
  <div><button class="btn" type="submit">Send message</button></div>
  <p class="form-msg" id="formMsg" role="alert" hidden></p>
  <p class="form-note">A senior consultant replies within one business day.  We only use your details to reply.  <a href="privacy.html">Privacy policy</a>.</p>
</form>'''

FAQ = C['FAQ']
def faq():
    # plain questions and answers, nothing to click open
    items = ''.join(f'<div class="qa"><h3>{q}</h3><p>{a}</p></div>' for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace('  ', ' ')}} for q, a in FAQ]})
    return f'<section class="band"><div class="wrap"><div class="sec-head"><h2>Common questions.</h2></div><div class="qas">{items}</div></div></section><script type="application/ld+json">{ld}</script>'

# ---------- pages ----------
def home():
    lines = ''.join(f'<a class="line" href="services.html#{x["slug"]}"><span class="li-ic">{icon(x["slug"])}</span><span><b>{x["name"]}</b><span>{x["short"]}</span></span></a>' for x in SERVICES[:6])
    stats = ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in PROOF)
    body = f'''
<section class="hero"><div class="wrap">
  <span class="kicker">IT for startups, small businesses and companies preparing for growth</span>
  <h1>Your IT, well run.</h1>
  <p class="lead">We set up your IT, keep it running and keep it safe.  So you can get back to work.</p>
  <div class="acts"><a class="btn" href="contact.html">Contact us</a><a class="link" href="about.html#check">Take the free 60-second IT health check</a></div>
  <p class="reach">Supporting companies in all 50 states.</p>
</div></section>

<section class="tight"><div class="wrap">
  <div class="split-head"><h2>What we run.</h2><a class="link" href="services.html">All services</a></div>
  <div class="lines">{lines}</div>
</div></section>

<section class="tight"><div class="wrap"><div class="panel two">
  <div><h2>What well run looks like.</h2><p class="lead" style="margin-top:18px">It just works.  People sign in, the network stays up, and problems get fixed fast.</p>
  <p style="margin-top:26px"><a class="link" href="about.html#check">See how your IT measures up</a></p></div>
  <ul class="checks">{''.join(f'<li>{x}</li>' for x in WELL_RUN)}</ul>
</div></div></section>

<section class="tight"><div class="wrap"><div class="statrow">{stats}</div></div></section>
{quote_block(1)}
{cta()}
<script type="application/ld+json">{ORG_LD}</script>'''
    page('index.html', f'{BRAND} | IT infrastructure and operations, well run', 'IT infrastructure and operations for startups, small businesses and companies preparing for growth: Microsoft 365, business applications, networks, cybersecurity and IT leadership.  Supporting companies in all 50 states.', body)

def ways():
    # Partnership page folded into Services (Nov 12 2026 trim)
    w = list(C['ENGAGE'])
    t, sub, how, inc, work, best = w[1]
    w[1] = (t, "No packages.  No tiers.  No paying for what you don't use.", "Every plan is built around your business.  We sit down with you, choose what we manage and how, and price it to fit, from a few key systems to the whole stack.  We can also take over from your current MSP.", inc, work, best)
    cols = ''.join(f'''<div class="way"><span class="way-t">{t}</span><h3>{sub}</h3><p>{how}</p><ul class="ticks">{''.join(f"<li>{x}</li>" for x in inc[:5])}</ul>
<p class="way-best"><b>Best for:</b> {best}.</p></div>''' for t, sub, how, inc, work, best in w)
    return f'''<section class="band" id="partnership"><div class="wrap"><div class="sec-head"><h2>Three ways to work with us.</h2><p class="lead">One job, a managed IT plan built around you, or a senior IT leader part time.  Start with one and add another later.  You get a written scope and price before any work starts.</p></div><div class="ways">{cols}</div></div></section>'''

def services():
    jump = ''.join(f'<a href="#{x["slug"]}">{x["name"]}</a>' for x in SERVICES)
    rows = ''
    for n, x in enumerate(SERVICES, 1):
        notes = ''.join(f'<p class="svc-note">{t}</p>' for t in SVC_NOTES.get(x['slug'], []))
        topic = quote(TOPIC_OF.get(x['slug'], 'A project or assessment')); msg = quote('About ' + x['name'] + ': ')
        rows += f'''<section class="svc{' alt' if n % 2 == 0 else ''}" id="{x["slug"]}"><div class="wrap svc-grid">
  <div class="svc-side"><span class="svc-num">{n:02d}</span><span class="svc-ic">{icon(x["slug"])}</span><h2>{x["name"]}</h2></div>
  <div class="svc-main"><p class="svc-h">{plain(x["h"])}</p><p class="svc-intro">{x["intro"]}</p>{notes}
    <ul class="svc-list">{''.join(f'<li>{g}</li>' for g in x["get"][:4])}</ul>
    <a class="btn" href="contact.html?topic={topic}&amp;msg={msg}">Talk to us about {x["name"]}</a></div>
</div></section>'''
    body = phero('Everything IT, one team.', 'Bring us a single project or hand us the whole stack.  Every service is delivered by the same small, senior team.') + f'<nav class="jump" aria-label="Services on this page"><div class="wrap">{jump}</div></nav>' + rows + ways() + faq() + cta()
    page('services.html', f'Services | {BRAND}', 'Microsoft 365, business applications, network, cybersecurity, IT strategy, managed IT, cloud, AI, data center, automation, access control and compliance.', body)

def service(i, s):
    redirect(s['slug'] + '.html', 'services.html#' + s['slug'])   # one Services page now, no sub-pages (Nov 2026)

def engagement():
    redirect('engagement.html', 'services.html#partnership')   # Partnership folded into Services, Nov 12 2026

def why():
    redirect('why-us.html', 'about.html')   # Why Us merged into About Us, Nov 2026

def about():
    std = ''.join(f'<li><span class="li-ic">{icon(k)}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for k, t, d in C['STANDARD'])
    tq = ''.join(f'<figure class="tq"><figcaption class="who">{E(t["cap"][0])}<span>{E(t["cap"][1]) if len(t["cap"]) > 1 else ""}</span></figcaption><blockquote>{"".join(f"<p>{E(p)}</p>" for p in t["paras"])}</blockquote></figure>' for t in C['TESTIMONIALS'])
    qs = ''.join(f'<li data-q="{i}"><p>{q}</p><div class="yn"><button type="button" data-v="1" aria-pressed="false">Yes</button><button type="button" data-v="0" aria-pressed="false">No</button></div></li>' for i, q in enumerate(C['QUESTIONS']))
    body = phero('Mom-and-pop care.  Enterprise experience.', 'A small, senior team for startups, small businesses and companies preparing for growth, backed by 30+ years of running IT.') + f'''
<section class="tight"><div class="wrap"><div class="panel">
  <p class="big">Well-run IT is the IT nobody talks about.  People sign in and get to work.  The network stays up.  Backups restore when you need them.  The audit goes smoothly, and the person who left last Friday can't get back in.</p>
  <p class="lead" style="margin-top:26px;max-width:820px">That's the job, and it's the only promise we want to make.  So it's our name.</p>
</div></div></section>
<section><div class="wrap two">
  <div><h2>Where we come from.</h2><div style="margin-top:34px"><div class="stat">30+</div><p class="stat-l">Years running IT</p></div></div>
  <div class="prose">
    <p class="lead">For more than three decades we've run IT from the help desk to the data center: service desk and IT operations, network infrastructure, physical and digital security, websites and business applications.</p>
    <p>We've built data centers and colocation facilities across the country and run IT for medical device and diagnostics companies, manufacturers, startups and growing firms, keeping them secure and ready for every audit and compliance review.</p>
    <p>Some of our longest client relationships began at OC TechWorks LLC, the Orange County IT firm our founder co-owned.  When it wound down, its clients came with us.  We started out as Cali IT Consulting, headquartered in Huntington Beach, with remote offices in Arcata, California and Payson, Arizona.  Our clients are now across the country, so our name says what we do, not where we are.</p>
  </div>
</div></section>
<section><div class="wrap"><div class="sec-head"><h2>Our standard, in writing.</h2><p class="lead">Six commitments we hold ourselves to on every engagement, large or small.</p></div><ul class="standards">{std}</ul></div></section>
<section id="testimonials" class="band"><div class="wrap" style="max-width:900px"><div class="sec-head"><h2>In their own words.</h2><p class="lead">What clients and colleagues have said about the work of our team's leader.  Quoted from LinkedIn recommendations, with names left out for privacy.</p></div>{tq}</div></section>
<section id="check"><div class="wrap"><div class="panel-check">
  <h2>The 60-second IT health check.</h2><p class="lead" style="margin-top:14px">Six honest questions.  No email required, and your answers stay in your browser.</p>
  <div class="check" style="margin-top:34px"><ol class="questions" id="questions">{qs}</ol>
  <div class="score"><div class="n" id="gaugeNum">0<small> of {len(C['QUESTIONS'])}</small></div><h3 id="verdictTitle">Answer the questions</h3><p id="verdictText">Every "No" is a gap worth closing.  Most businesses have at least one.</p><a class="btn" id="checkCta" href="contact.html" hidden>Send us your results</a></div></div>
</div></div></section>
{cta()}'''
    page('about.html', f'About Us | {BRAND}', 'Mom-and-pop care, enterprise experience: 30+ years of running IT for startups, small businesses and companies preparing for growth.  Take the free 60-second IT health check.', body)

def testimonials():
    redirect('testimonials.html', 'about.html#testimonials')   # folded into About Us, Nov 12 2026

def status_panel():
    rows = ''.join(f'<a class="sp-row" data-status="{k}" href="{u}" target="_blank" rel="noopener"><span class="dot" aria-hidden="true"></span><b>{n}</b><span class="sp-t">Checking.</span></a>' for k, n, u in C['STATUS'])
    return f'<div class="status-panel"><p class="sp-h">Cloud service status</p>{rows}<p class="sp-note">From each provider\'s public status page, checked every hour.  Problems limited to one company\'s account show only in its own admin console.</p></div>'

def news_page():
    body = phero('Cybersecurity news, last 48 hours.', 'Advisories from CISA and Microsoft, plus the stories security teams are reading.  We collect the headlines; every link goes to the original publisher.') + f'''
<section style="padding-top:0"><div class="wrap two">
  <div><ol class="news" id="newsList" data-hours="48"><li class="news-empty">Loading the latest headlines.</li></ol>
  <p style="margin-top:22px"><a class="link" href="news-history.html">Previous two weeks</a></p></div>
  <div>{status_panel()}</div>
</div></section>'''
    page('news.html', f'Cybersecurity News | {BRAND}', 'Cybersecurity headlines from the last 48 hours, from CISA, Microsoft and the security press, plus cloud service status, refreshed every hour.', body)

def news_history():
    body = phero('Cybersecurity news, previous two weeks.', 'Older headlines, newest first.  For the last 48 hours, see the <a href="news.html">main news page</a>.') + \
        '<section style="padding-top:0"><div class="wrap" style="max-width:900px"><div id="newsHistory"><p class="news-empty">Loading headlines.</p></div></div></section>'
    page('news-history.html', f'Cybersecurity News History | {BRAND}', 'Cybersecurity headlines from the previous two weeks.', body)

def contact():
    body = phero("Tell us what you're working on.", "Bernie fills out the form for you in a few quick questions, then a real person takes it from there.") + f'''
<section style="padding-top:0"><div class="wrap two">
  <div class="panel-lite"><h2>Two ways to reach us.</h2>
  <p class="lead" style="margin-top:18px">Ask Bernie, or email us directly.  Either way, a real person answers.</p>
  <div class="acts" style="margin-top:26px"><button class="btn" type="button" data-bernie>Ask Bernie</button><a class="link" href="mailto:support@wellrunit.com">support@wellrunit.com</a></div></div>
  <div><ul class="ticks"><li>Headquarters in Huntington Beach, California</li><li>Remote offices in Arcata, California and Payson, Arizona</li><li>On-site across California and Arizona</li><li>Remote support in all 50 states, with on-site travel as required</li><li>Callbacks weekdays, 7 a.m. to 4 p.m. Pacific</li></ul></div>
</div></section>'''
    page('contact.html', f'Contact | {BRAND}', f'Contact {BRAND}.  Headquartered in Huntington Beach, California, serving clients nationwide.', body)

def thanks():
    page('thanks.html', f'Thank you | {BRAND}', 'Your message was sent.', phero('Thanks.  We got your message.', 'A senior consultant will reply within one business day.') + '<section style="padding-top:0"><div class="wrap"><a class="btn" href="index.html">Back to the home page</a></div></section>')

def privacy():
    prose = (ROOT / 'build' / 'privacy_src.html').read_text()
    page('privacy.html', f'Privacy | {BRAND}', f'How {BRAND} collects, uses and protects information sent through this website.', phero('Privacy policy.', f'Effective November 12, {YEAR}.') + f'<section style="padding-top:0"><div class="wrap prose" style="max-width:820px">{prose}</div></section>')

def terms():
    prose = (ROOT / 'build' / 'terms_src.html').read_text()
    page('terms.html', f'Terms of Use | {BRAND}', f'The terms for using the {BRAND} website.', phero('Terms of use.', f'Effective November 2, {YEAR}.') + f'<section style="padding-top:0"><div class="wrap prose" style="max-width:820px">{prose}</div></section>')

def notfound():
    page('404.html', f'Page not found | {BRAND}', 'Page not found.', phero("This page isn't here.", "The page you're looking for may have moved.") + '<section style="padding-top:0"><div class="wrap"><div class="acts" style="margin-top:0"><a class="btn" href="index.html">Home page</a><a class="link" href="services.html">See our services</a></div></div></section>')

MIC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0M12 18v3M8 21h8"/></svg>'
OKMARK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

def app_page():
    # The Bernie app (Nov 12 2026): saved to a phone or desktop from the footer's "Get the app" link.
    # "Well Run IT" under the icon, "Bernie by Well Run IT" inside.  Look: option 2, Night (picked Nov 12 2026).
    css, js = ver('assets/css/app.css'), ver('assets/js/app.js')
    (ROOT / 'app.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Well Run IT</title>
<meta name="description" content="Bernie by Well Run IT.  Tap, talk and send an IT ticket to our support team.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1b2430">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Well Run IT">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="app.webmanifest">
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/brand/app-180.png">
<link rel="preload" href="assets/fonts/inter-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/app.css?v={css}">
</head>
<body>
<div class="app">
  <header class="head"><span class="wordmark" aria-label="Well Run IT">Well<b>{stride_r()}un</b><i>IT</i></span><span class="by">Bernie</span></header>

  <main class="screen" id="setup" hidden>
    <h1>Who are we helping?</h1>
    <p class="sub">Just once.  It's saved on this device only, so next time you just tap and talk.</p>
    <form class="card" id="setupForm" novalidate>
      <label>Your name<input id="s-name" autocomplete="name" maxlength="120" required></label>
      <label>Company<input id="s-company" autocomplete="organization" maxlength="160" required></label>
      <label>Best phone number<input id="s-phone" type="tel" autocomplete="tel" maxlength="40" required></label>
      <label>Email (optional)<input id="s-email" type="email" autocomplete="email" maxlength="200"></label>
      <p class="err" id="setupErr" role="alert" hidden></p>
      <button class="btn wide" type="submit">Save</button>
      <p class="note">We only use this to reply to you.  <a href="privacy.html">Privacy</a></p>
    </form>
  </main>

  <main class="screen" id="home" hidden>
    <h1>Tell Bernie<br>what's going on.</h1>
    <button class="talk" id="talk" type="button" aria-pressed="false">{MIC}<span id="talkLabel">Tap to talk</span><span class="t2" id="talkSub" hidden><span class="timer" id="timer">0:00</span></span></button>
    <p class="sub" id="homeHint" aria-live="polite">Tap again when you're done.  You'll see what Bernie heard before it's sent.</p>
    <p class="err" id="homeErr" role="alert" hidden></p>
    <div class="install" id="install" hidden><p id="installText"></p><button class="btn" id="installBtn" type="button" hidden>Install</button></div>
  </main>

  <main class="screen" id="working" hidden>
    <h1 id="workTitle">One moment.</h1>
    <p class="sub" id="workText" aria-live="polite"></p>
  </main>

  <main class="screen" id="review" hidden>
    <h1>Look right?</h1>
    <form class="card" id="reviewForm" novalidate>
      <p class="sub" id="reviewNote" style="max-width:none;text-align:center"></p>
      <label><span class="hp">What's going on</span><textarea id="r-text" maxlength="5000" aria-label="What's going on"></textarea></label>
      <p class="err" id="reviewErr" role="alert" hidden></p>
      <div class="row" style="max-width:none"><button class="btn ghost" id="redo" type="button">Start over</button><button class="btn" type="submit">Submit</button></div>
    </form>
  </main>

  <main class="screen" id="done" hidden>
    <span class="big-ok">{OKMARK}</span>
    <h1>Sent.</h1>
    <p class="sub">A real person on our team has it and will reach out.  You won't have to repeat any of this.</p>
    <button class="btn" id="again" type="button">Done</button>
  </main>

  <main class="screen" id="failed" hidden>
    <h1>That didn't go through.</h1>
    <p class="sub">Try again, or email us at <a id="mailLink" href="#">support@wellrunit.com</a>.</p>
    <div class="row"><button class="btn ghost" id="failedBack" type="button">Edit</button><button class="btn" id="retry" type="button">Try again</button></div>
  </main>

  <div id="botcheck"></div>
  <div class="foot"><button class="linkbtn" id="typeIt" type="button">Rather type it?</button><button class="linkbtn who" id="changeWho" type="button" aria-label="Change your details"><span id="who"></span></button></div>
</div>
<script src="assets/js/app.js?v={js}" defer></script>
</body>
</html>
''')

def redirect(fname, to):
    (ROOT / fname).write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{DOMAIN}{to}"><title>Moved</title><a href="{to}">This page has moved.</a>')

def extras():
    pages = ['', 'services.html', 'about.html', 'news.html', 'news-history.html', 'contact.html', 'privacy.html', 'terms.html']
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}{p}</loc></url>\n' for p in pages) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}sitemap.xml\n')
    (ROOT / 'CNAME').write_text('wellrunit.com\n')
    (ROOT / '.nojekyll').write_text('')
    (ROOT / 'assets' / 'brand' / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="8 -3 106 106"><style>svg{color:#1b2430}.rm{fill:#2f5580}@media (prefers-color-scheme:dark){svg{color:#fff}.rm{fill:#b9cde3}}</style>' + STRIDE_R + '</svg>')
    for old, new in [('industries.html', 'services.html'), ('focus.html', 'services.html')]:
        redirect(old, new)

if __name__ == '__main__':
    home(); services(); [service(i, s) for i, s in enumerate(SERVICES)]; engagement(); why(); about(); testimonials(); news_page(); news_history(); contact(); thanks(); privacy(); terms(); notfound(); app_page(); extras()
    for n in ('thanks.html', '404.html'):
        f = ROOT / n; t = f.read_text()
        if 'name="robots"' not in t: f.write_text(t.replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n<meta name="theme-color"', 1))
    print('built Well Run IT')
