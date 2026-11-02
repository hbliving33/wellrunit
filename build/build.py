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

SERVICES = C['SERVICES']
SVC = {s['slug']: s for s in SERVICES}
TOPICS = C['TOPICS2']; TOPIC_OF = C['TOPIC_OF']

def ver(rel):
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]

# ---------- brand ----------
CHECK = '<path d="M7 12.6l3.4 3.4L17.2 8.6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
def mark(fill='#1b2430', size=24):
    return f'<svg class="mk" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6.5" fill="{fill}"/>{CHECK}</svg>'

def logo(dark=False):
    return '<span class="wordmark">Well<b>Run</b><i>IT</i></span>'

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
      'business-applications': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 4v5"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

def plain(h):
    return re.sub(r'</?em>', '', h)

NAV = [('services.html', 'Services'), ('engagement.html', 'How We Work'), ('why-us.html', 'Why Us'), ('about.html', 'Our Story'), ('news.html', 'Cyber News')]
SVC_FILES = {s['slug'] + '.html' for s in SERVICES}

ORG_LD = json.dumps({"@context": "https://schema.org", "@type": "ProfessionalService", "name": BRAND, "url": DOMAIN, "logo": DOMAIN + "assets/brand/og.png",
    "description": "IT infrastructure and operations consulting for startups, small and growing companies: networks, servers and cloud, Microsoft 365, business applications, security and managed IT.",
    "address": {"@type": "PostalAddress", "addressLocality": "Huntington Beach", "addressRegion": "CA", "addressCountry": "US"}, "areaServed": "US"})

def page(fname, title, desc, body):
    css, js = ver('assets/css/site.css'), ver('assets/js/site.js')
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
    <div class="cols">
      <div><a class="brand" href="index.html" aria-label="{BRAND}, home">{logo(True)}</a><p>IT infrastructure and operations consulting for startups, small and growing companies.  Headquartered in Huntington Beach, California, serving clients across the United States.</p></div>
      <div><h4>Services</h4><ul>{svc_links}</ul></div>
      <div><h4>Company</h4><ul><li><a href="engagement.html">How we work</a></li><li><a href="why-us.html">Why us</a></li><li><a href="about.html">Our story</a></li><li><a href="testimonials.html">Testimonials</a></li><li><a href="news.html">Cybersecurity news</a></li></ul></div>
      <div><h4>Get in touch</h4><ul><li><a href="contact.html">Contact us</a></li><li><a href="why-us.html#check">Free IT health check</a></li><li><a href="privacy.html">Privacy</a></li></ul></div>
    </div>
    <div class="base"><span>&copy; {YEAR} {BRAND}</span><span>Huntington Beach, California.  Remote support in all 50 states.</span></div>
  </div>
</footer>
<script src="assets/js/site.js?v={js}" defer></script>
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
<div class="acts"><a class="btn" href="contact.html">Contact us</a><a class="link" href="why-us.html#check">Take the free IT health check</a></div></div></div></section>'''

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

FIT = [('Startups, small and growing companies', 'Our sweet spot is the business without a full IT department, or with one IT person stretched thin.  We have been part of a few startups ourselves.'),
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

PROOF = [('30 years', 'running IT operations, from data centers to Microsoft 365'), ('$4.5M', 'cut from one manufacturer’s IT costs over two years'),
         ('1 business day', 'to hear back from a senior consultant'), ('50 states', 'with remote support, on-site across California and Arizona')]

def proof():
    return '<div class="cards four">' + ''.join(f'<div class="card"><div class="stat" style="font-size:40px">{n}</div><p style="margin-top:10px">{t}</p></div>' for n, t in PROOF) + '</div>'

def fit_cards():
    return '<div class="cards">' + ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in FIT) + '</div>'

def quote_block(i=0):
    q, c = C['QUOTES'][i]
    return f'<section><div class="wrap"><figure class="quote"><blockquote>{q}</blockquote><figcaption>{c}.  <a class="link" href="testimonials.html">Read the testimonials</a></figcaption></figure></div></section>'

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
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace('  ', ' ')}} for q, a in FAQ]})
    return f'<section><div class="wrap"><div class="sec-head"><h2>Common questions.</h2></div><div class="faq">{items}</div></div></section><script type="application/ld+json">{ld}</script>'

# ---------- pages ----------
def home():
    body = f'''
<section class="hero"><div class="wrap">
  <span class="kicker">IT for startups, small and growing companies</span>
  <h1>Your IT, well run.</h1>
  <p class="lead">We design, build and run the systems your business depends on: networks, servers and cloud, Microsoft 365, business applications and security.  Thirty years of running IT operations, now working for you.</p>
  <div class="acts"><a class="btn" href="contact.html">Contact us</a><a class="link" href="why-us.html#check">Take the free 60-second IT health check</a></div>
  <p class="reach">Headquartered in Huntington Beach, California.  Remote support in all 50 states.</p>
</div></section>

<section style="padding-top:0"><div class="wrap">{tiles()}</div></section>

<section style="padding-top:24px"><div class="wrap"><div class="panel two">
  <div><h2>What well run looks like.</h2><p class="lead" style="margin-top:18px">Well-run IT is the IT nobody has to think about.  People sign in and get to work, the network stays up, and the bad days are short.  Under the hood, it comes down to a few things done every time.</p>
  <p style="margin-top:26px"><a class="link" href="why-us.html#check">See how your IT measures up</a></p></div>
  <ul class="checks">{''.join(f'<li>{x}</li>' for x in WELL_RUN)}</ul>
</div></div></section>

<section><div class="wrap"><div class="sec-head"><h2>Mom-and-pop care.  Enterprise experience.</h2><p class="lead">We're a small team, built for startups and small companies.  We don't chase large accounts; we'd rather be the IT partner a growing business can call by name.</p></div>{fit_cards()}</div></section>

<section class="dark"><div class="wrap"><div class="sec-head"><h2>Proof, not promises.</h2><p class="lead">A few numbers behind the work.  Client names are kept confidential.</p></div>{proof().replace('class="card"', 'class="card"')}</div></section>

<section><div class="wrap"><div class="sec-head"><h2>What we run.</h2><p class="lead">Our specialty is the core of IT: the infrastructure and the day-to-day operations that keep a business moving.  Facilities and compliance come along when the work calls for it.</p></div>
{sortable(['Area', 'What it covers'], RUN, 'What we run')}
<p style="margin-top:24px"><a class="link" href="services.html">See every service</a></p></div></section>

{quote_block(1)}
{cta()}
<script type="application/ld+json">{ORG_LD}</script>'''
    page('index.html', f'{BRAND} | IT infrastructure and operations, well run', 'IT infrastructure and operations for startups, small and growing companies: networks, servers and cloud, Microsoft 365, business applications and security.  Headquartered in California, serving clients nationwide.', body)

def services():
    cards = ''.join(f'<a class="tile" href="{s["slug"]}.html"><span class="ic">{icon(s["slug"])}</span><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="go">Learn more</span></a>' for s in SERVICES)
    body = phero('Everything IT, one team.', 'Bring us a single project or hand us the whole stack.  Every service is delivered by the same small, senior team.') + f'<section style="padding-top:0"><div class="wrap"><div class="tiles">{cards}</div></div></section>' + cta()
    page('services.html', f'Services | {BRAND}', 'Network, cloud, data center, Microsoft 365, business applications, AI, managed IT, IT strategy, cybersecurity, automation, access control and compliance.', body)

def service(i, s):
    sym = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in s['pains'])
    ct, cs, cl, co = s['case']
    prev, nxt = SERVICES[i - 1], SERVICES[(i + 1) % len(SERVICES)]
    note = s.get('case_note', 'Client names are kept confidential.')
    topic = quote(TOPIC_OF.get(s['slug'], 'A project or assessment')); msg = quote('About ' + s['name'] + ': ')
    body = phero(plain(s['h']), s['intro'], trail=f'<a href="services.html">Services</a> / {s["name"]}') + f'''
<section style="padding-top:0"><div class="wrap"><div class="sec-head"><h2>Sound familiar?</h2></div><div class="cards">{sym}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="panel two">
  <div><h2>What you get.</h2><ul class="ticks" style="margin-top:26px">{''.join(f'<li>{g}</li>' for g in s['get'])}</ul>
  <p style="margin-top:28px"><a class="btn" href="contact.html?topic={topic}&amp;msg={msg}">Talk to us about {s["name"]}</a></p></div>
  <div><article class="story"><p class="lbl">{s.get('case_label', 'From the field')}</p><h3>{ct}</h3><p>{cs}</p><ul class="ticks" style="margin-top:14px">{''.join(f'<li>{x}</li>' for x in cl)}</ul><div class="out">{co}</div></article>
  {f'<p class="fine">{note}</p>' if note else ''}
  <h3 style="margin-top:30px">Platforms and standards</h3><div class="pills">{''.join(f'<span>{p}</span>' for p in s['plat'])}</div></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap"><nav class="next-prev" aria-label="More services"><a href="{prev['slug']}.html"><small>Previous service</small><b>{prev['name']}</b></a><a href="{nxt['slug']}.html" style="text-align:right"><small>Next service</small><b>{nxt['name']}</b></a></nav></div></section>
'''
    page(s['slug'] + '.html', f'{s["name"]} | {BRAND}', s.get('desc') or f'{s["name"]} from {BRAND}.  {s["intro"].split("  ")[0]}', body)

def engagement():
    eng = ''.join(f'''<div class="card"><div class="num">{t}</div><h3>{sub}</h3><p>{how}</p><ul class="ticks" style="margin-top:16px">{''.join(f"<li>{x}</li>" for x in inc)}</ul>
<p style="margin-top:16px;font-size:15px"><b>Typical work:</b> {', '.join(work)}.</p><p style="margin-top:8px;font-size:15px"><b>Best for:</b> {best}.</p></div>''' for t, sub, how, inc, work, best in C['ENGAGE'])
    steps = [('Send us a message', "Tell us what's going on through the contact form.  We reply within one business day."), ('Get a written proposal', 'A clear scope, timeline and price, in plain English.'), ('Kick off', 'We get to work, keep you posted and document everything as we go.'), ('Hand-off or ongoing', 'Projects end with documentation you own.  Managed and fractional work continue month to month.')]
    st = ''.join(f'<div class="card"><div class="num">Step {n}</div><h3>{t}</h3><p>{d}</p></div>' for n, (t, d) in enumerate(steps, 1))
    std = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for _, t, d in C['STANDARD'])
    body = phero('Work with us the way that fits.', 'One job, a managed IT plan built around you, or a senior IT leader part time.  Start with one and add another later.') + f'''
<section style="padding-top:0"><div class="wrap"><div class="cards">{eng}</div></div></section>
<section class="dark"><div class="wrap"><div class="sec-head"><h2>How an engagement starts.</h2></div><div class="cards four">{st}</div></div></section>
<section><div class="wrap"><div class="sec-head"><h2>Our standard, in writing.</h2><p class="lead">Six commitments we hold ourselves to on every engagement, large or small.</p></div><div class="cards">{std}</div></div></section>
{faq()}
{cta()}'''
    page('engagement.html', f'How We Work | {BRAND}', 'Projects, a managed IT plan built around you, or fractional IT leadership.  Written scope and price before any work starts.', body)

def why():
    qs = ''.join(f'<li data-q="{i}"><p>{q}</p><div class="yn"><button type="button" data-v="1" aria-pressed="false">Yes</button><button type="button" data-v="0" aria-pressed="false">No</button></div></li>' for i, q in enumerate(C['QUESTIONS']))
    pains = ''.join(f'<li><a href="{s}.html"><span class="nm">{t}</span><span class="ds">{SVC[s]["name"]}</span></a></li>' for t, s in C['PAINS'])
    body = phero('Mom-and-pop care.  Enterprise experience.', "A small team for startups, small and growing companies.  You get people who know your name and your systems, backed by thirty years of running IT where downtime isn't an option.") + f'''
<section style="padding-top:0" id="check"><div class="wrap"><div class="panel">
  <h2>The 60-second IT health check.</h2><p class="lead" style="margin-top:14px">Six honest questions.  No email required, and your answers stay in your browser.</p>
  <div class="check" style="margin-top:34px"><ol class="questions" id="questions">{qs}</ol>
  <div class="score"><div class="n" id="gaugeNum">0<small> of {len(C['QUESTIONS'])}</small></div><h3 id="verdictTitle">Answer the questions</h3><p id="verdictText">Every "No" is a gap worth closing.  Most businesses have at least one.</p><a class="btn" id="checkCta" href="contact.html" hidden>Send us your results</a></div></div>
</div></div></section>
<section><div class="wrap">{fit_cards()}</div></section>
<section class="dark"><div class="wrap"><div class="sec-head"><h2>If you nodded at any of these, we should talk.</h2></div><ul class="pains">{pains}</ul></div></section>
{cta()}'''
    page('why-us.html', f'Why Us | {BRAND}', 'Mom-and-pop care, enterprise experience: a small IT team for startups, small and growing companies.  Take the free 60-second IT health check.', body)

def about():
    vals = ''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in [('Straight answers', "Plain English, no jargon.  If something doesn't need fixing, we'll say so."), ('Senior people', 'The people who scope your project are the ones who do the work.'), ('Documented', "Every change is written down, so you're never locked in to us."), ('Built to last', 'We design for the next five years, not the next invoice.')])
    notes = ''.join(f'<article class="note"><div class="where">{k}</div><div><h3>{t}</h3><p>{d}</p></div><div class="out">{b}</div></article>' for k, t, d, b in C['RESULTS'])
    body = phero('Our story.', 'Thirty years of running IT, and one idea we kept coming back to.') + f'''
<section style="padding-top:0"><div class="wrap"><div class="panel">
  <p class="big">Well-run IT is the IT nobody talks about.  People sign in and get to work.  The network stays up.  Backups restore when you need them.  The audit goes smoothly, and the person who left last Friday can't get back in.</p>
  <p class="lead" style="margin-top:26px;max-width:820px">That's the job, and it's the only promise we want to make.  So it's our name.</p>
</div></div></section>
<section><div class="wrap two">
  <div><h2>Where we come from.</h2><div style="margin-top:34px"><div class="stat">30</div><p class="stat-l">Years in IT leadership</p></div></div>
  <div class="prose">
    <p class="lead">Our team has spent three decades running IT operations: building and moving data centers and colocation facilities across the country, and running IT for medical device and diagnostics companies, manufacturers, startups and growing firms.</p>
    <p>We've moved headquarters and data centers, built labs, and been on the IT side of SOX and ISO audits and HIPAA reviews.  We handle networks, servers and cloud, data centers, Microsoft 365, business applications, cybersecurity, physical security and IT strategy.</p>
    <p>Some of our longest client relationships began at OC TechWorks LLC, the Orange County IT firm our founder co-owned from start to finish.  When it wound down, its clients came with us.</p>
    <p>We started out as Cali IT Consulting.  We're still headquartered in Huntington Beach, California, with remote offices in Arcata, California and Payson, Arizona.  But our clients are across the country, and our name should say what we do, not where we are.</p>
  </div>
</div></section>
<section class="dark"><div class="wrap"><div class="sec-head"><h2>What we stand for.</h2></div><div class="cards four">{vals}</div></div></section>
<section><div class="wrap"><div class="sec-head"><h2>Field notes.</h2><p class="lead">A few of the projects behind the numbers.  Client names are kept confidential.</p></div><div style="border-top:1px solid var(--line)">{notes}</div></div></section>
{quote_block(2)}
{cta()}'''
    page('about.html', f'Our Story | {BRAND}', 'Why we are called Well Run IT: thirty years of running IT operations for startups, small and growing companies.  Headquartered in Huntington Beach, serving clients nationwide.', body)

def testimonials():
    rows = ''.join(f'<figure class="tq"><figcaption class="who">{E(t["cap"][0])}<span>{E(t["cap"][1]) if len(t["cap"]) > 1 else ""}</span></figcaption><blockquote>{"".join(f"<p>{E(p)}</p>" for p in t["paras"])}</blockquote></figure>' for t in C['TESTIMONIALS'])
    body = phero('In their own words.', "What clients and colleagues have said about the work of our team's leader.  Quoted from LinkedIn recommendations, with names left out for privacy.") + f'<section style="padding-top:0"><div class="wrap" style="max-width:900px">{rows}</div></section>' + cta()
    page('testimonials.html', f'Testimonials | {BRAND}', f'What clients and colleagues say about working with the {BRAND} team.', body)

def status_panel():
    rows = ''.join(f'<a class="sp-row" data-status="{k}" href="{u}" target="_blank" rel="noopener"><span class="dot" aria-hidden="true"></span><b>{n}</b><span class="sp-t">Checking.</span></a>' for k, n, u in C['STATUS'])
    return f'<div class="status-panel"><p class="sp-h">Cloud service status</p>{rows}<p class="sp-note">From each provider\'s public status page, checked every hour.  Problems limited to one company\'s account show only in its own admin console.</p></div>'

def news_page():
    body = phero('Cybersecurity news, refreshed every hour.', 'Advisories from CISA and Microsoft, plus the stories security teams are reading.  We collect the headlines; every link goes to the original publisher.') + f'''
<section style="padding-top:0"><div class="wrap two">
  <ol class="news" id="newsList" data-limit="30"><li class="news-empty">Loading the latest headlines.</li></ol>
  <div>{status_panel()}</div>
</div></section>'''
    page('news.html', f'Cybersecurity News | {BRAND}', 'Cybersecurity headlines from CISA, Microsoft and the security press, plus Microsoft 365, AWS, Wasabi, Zoom and NetSuite service status, refreshed every hour.', body)

def contact():
    body = phero("Tell us what you're working on.", 'Fill out the form and a senior consultant will get back to you within one business day.') + f'''
<section style="padding-top:0"><div class="wrap two">
  <div><h2>Headquartered in California.  Clients nationwide.</h2><ul class="ticks" style="margin-top:26px"><li>Headquarters in Huntington Beach, California</li><li>Remote offices in Arcata, California and Payson, Arizona</li><li>On-site across California and Arizona</li><li>Remote support in all 50 states, with on-site travel as required</li><li>A reply from a senior consultant within one business day</li></ul></div>
  {form()}
</div></section>'''
    page('contact.html', f'Contact | {BRAND}', f'Contact {BRAND}.  Headquartered in California, serving clients nationwide.  A senior consultant replies within one business day.', body)

def thanks():
    page('thanks.html', f'Thank you | {BRAND}', 'Your message was sent.', phero('Thanks.  We got your message.', 'A senior consultant will reply within one business day.') + '<section style="padding-top:0"><div class="wrap"><a class="btn" href="index.html">Back to the home page</a></div></section>')

def privacy():
    prose = (ROOT / 'build' / 'privacy_src.html').read_text()
    page('privacy.html', f'Privacy | {BRAND}', f'How {BRAND} collects, uses and protects information sent through this website and its contact form.', phero('Privacy policy.', f'Effective November 1, {YEAR}.') + f'<section style="padding-top:0"><div class="wrap prose" style="max-width:820px">{prose}</div></section>')

def notfound():
    page('404.html', f'Page not found | {BRAND}', 'Page not found.', phero("This page isn't here.", "The page you're looking for may have moved.") + '<section style="padding-top:0"><div class="wrap"><div class="acts" style="margin-top:0"><a class="btn" href="index.html">Home page</a><a class="link" href="services.html">See our services</a></div></div></section>')

def redirect(fname, to):
    (ROOT / fname).write_text(f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{DOMAIN}{to}"><title>Moved</title><a href="{to}">This page has moved.</a>')

def extras():
    pages = ['', 'services.html', 'engagement.html', 'why-us.html', 'about.html', 'testimonials.html', 'news.html', 'contact.html', 'privacy.html'] + [s['slug'] + '.html' for s in SERVICES]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}{p}</loc></url>\n' for p in pages) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}sitemap.xml\n')
    (ROOT / 'CNAME').write_text('wellrunit.com\n')
    (ROOT / '.nojekyll').write_text('')
    (ROOT / 'assets' / 'brand' / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#1b2430"/><rect x="5.5" y="6" width="3.2" height="12" rx=".6" fill="#9bb6d3"/><rect x="10.3" y="6" width="9" height="3.2" rx=".6" fill="#9bb6d3"/><rect x="13.2" y="6" width="3.2" height="12" rx=".6" fill="#9bb6d3"/></svg>')
    for old, new in [('industries.html', 'services.html'), ('focus.html', 'services.html')]:
        redirect(old, new)

if __name__ == '__main__':
    home(); services(); [service(i, s) for i, s in enumerate(SERVICES)]; engagement(); why(); about(); testimonials(); news_page(); contact(); thanks(); privacy(); notfound(); extras()
    for n in ('thanks.html', '404.html'):
        f = ROOT / n; t = f.read_text()
        if 'name="robots"' not in t: f.write_text(t.replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n<meta name="theme-color"', 1))
    print('built Well Run IT')
