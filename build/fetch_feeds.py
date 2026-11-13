"""Pull security news headlines and cloud service status (15 providers) into assets/data/news.json.

Runs on a schedule in GitHub Actions (.github/workflows/feeds.yml).  Only headlines, sources,
dates and links are kept, so the site links out to each publisher instead of copying articles.
Uses only the Python standard library.
"""
import json, re, html, pathlib, urllib.request, email.utils, datetime as dt
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'data' / 'news.json'
HIST = ROOT / 'assets' / 'data' / 'news-history.json'   # two weeks of headlines for news-history.html
FEEDS = [
    ('CISA', 'https://www.cisa.gov/cybersecurity-advisories/all.xml'),
    ('Microsoft Security Blog', 'https://www.microsoft.com/en-us/security/blog/feed/'),
    ('BleepingComputer', 'https://www.bleepingcomputer.com/feed/'),
    ('The Hacker News', 'https://feeds.feedburner.com/TheHackersNews'),
    ('SecurityWeek', 'https://www.securityweek.com/feed/'),
    ('Krebs on Security', 'https://krebsonsecurity.com/feed/'),
    ('Dark Reading', 'https://www.darkreading.com/rss.xml'),
]
KEV_JSON = 'https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json'   # CISA's official KEV catalog on GitHub
M365_FEED = 'https://status.cloud.microsoft/api/feed/mac'
PER_SOURCE, TOTAL = 12, 60
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 wellrunit-news/1.0',
      'Accept': 'application/rss+xml, application/atom+xml, application/xml;q=0.9, */*;q=0.8'}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return r.read()

def text(el, *names):
    for n in names:
        x = el.find(n)
        if x is not None:
            if x.text and x.text.strip(): return x.text.strip()
            if x.get('href'): return x.get('href').strip()
    return ''

def when(s):
    if not s: return None
    try: return email.utils.parsedate_to_datetime(s).astimezone(dt.timezone.utc)
    except Exception: pass
    try: return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(dt.timezone.utc)
    except Exception: return None

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()

def parse(source, raw):
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:   # some feeds ship a stray & or control character; repair and retry
        t = raw.decode('utf-8', 'replace')
        t = re.sub(r'&(?!(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);)', '&amp;', t)
        t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', t)
        root = ET.fromstring(t.encode('utf-8'))
    for el in root.iter():           # drop namespaces so RSS and Atom read the same
        if isinstance(el.tag, str) and '}' in el.tag: el.tag = el.tag.split('}', 1)[1]
    items = root.findall('.//item') or root.findall('.//entry')
    out = []
    for it in items:
        title, link = clean(text(it, 'title')), text(it, 'link', 'guid')
        d = when(text(it, 'pubDate', 'published', 'updated', 'date'))
        if title and link.startswith('http') and d:
            out.append({'title': title[:180], 'link': link, 'source': source, 'date': d.isoformat()})
    out.sort(key=lambda x: x['date'], reverse=True)
    return out[:PER_SOURCE]

# ---------- cloud service status (Cloud Status page) ----------
# Each check returns ({status, link, notes}, error).  status is "Available" when nothing is open,
# "Unknown" when the check failed, or the provider's own wording.  notes lists what's open right now (max 5).
def _clip(t, n=220):
    t = clean(t or '')
    return t if len(t) <= n else t[:n - 3].rstrip() + '...'

def m365():
    link = 'https://status.cloud.microsoft/'
    try:
        root = ET.fromstring(get(M365_FEED))
        items = root.findall('.//item')
        raw = (items[0].findtext('status') or '').strip() if items else ''
        if not raw: return {'status': 'Unknown', 'link': link, 'notes': []}, None
        if re.search(r'operational|restored|resolved', raw, re.I): return {'status': 'Available', 'link': link, 'notes': []}, None
        status = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', raw).capitalize()   # "ServiceDegradation" -> "Service degradation"
        # each feed item is one affected service and its state, e.g. "Exchange Online: Service degradation"
        words = lambda v: re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', v).capitalize()
        notes = [_clip(f"{it.findtext('title').strip()}: {words((it.findtext('status') or '').strip())}") for it in items
                 if it.findtext('title') and not re.search(r'operational|restored|resolved', it.findtext('status') or '', re.I)][:5]
        return {'status': status, 'link': link, 'notes': notes}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': link, 'notes': []}, str(e)[:160]

def aws():
    # AWS Health Dashboard public events (no sign-in needed).  An empty list means no open public events.
    link, url = 'https://health.aws.amazon.com/health/status', 'https://health.aws.amazon.com/public/currentevents'
    try:
        b = get(url)
        raw = b.decode('utf-16') if b[:2] in (b'\xff\xfe', b'\xfe\xff') else b.decode('utf-8-sig')
        ev = json.loads(raw or '[]')
        ev = ev if isinstance(ev, list) else []
        notes = []
        for x in ev[:5]:
            if isinstance(x, dict):
                name = x.get('service_name') or x.get('service') or ''
                summ = x.get('summary') or ''
                notes.append(_clip(' '.join(p for p in [name, summ] if p)))
        n = len(ev)
        return {'status': 'Available' if n == 0 else f'{n} open event' + ('' if n == 1 else 's'), 'link': link, 'notes': [x for x in notes if x]}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': link, 'notes': []}, str(e)[:160]

def statuspage(base):
    # Atlassian Statuspage sites publish a public summary at /api/v2/summary.json (no sign-in needed).
    try:
        d = json.loads(get(base.rstrip('/') + '/api/v2/summary.json'))
        ind = (d.get('status') or {}).get('indicator', ''); desc = (d.get('status') or {}).get('description', '')
        open_ = [i for i in d.get('incidents', []) if i.get('status') not in ('resolved', 'postmortem')]
        maint = [m for m in d.get('scheduled_maintenances', []) if m.get('status') == 'in_progress']
        notes = [_clip(i.get('name')) for i in open_][:4] + [_clip('Maintenance: ' + (m.get('name') or '')) for m in maint][:2]
        return {'status': 'Available' if ind == 'none' else (desc or 'Unknown'), 'link': base, 'notes': notes[:5]}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': base, 'notes': []}, str(e)[:160]

def google():
    link = 'https://www.google.com/appsstatus/dashboard/'
    try:
        inc = json.loads(get('https://www.google.com/appsstatus/dashboard/incidents.json'))
        open_ = [i for i in inc if isinstance(i, dict) and not i.get('end')]
        notes = [_clip(i.get('external_desc') or (i.get('most_recent_update') or {}).get('text')) for i in open_][:5]
        n = len(open_)
        return {'status': 'Available' if n == 0 else f'{n} open incident' + ('' if n == 1 else 's'), 'link': link, 'notes': notes}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': link, 'notes': []}, str(e)[:160]

def azure():
    # Azure's public RSS feed lists the incidents that are open right now; an empty feed means none.
    link = 'https://azure.status.microsoft/en-us/status'
    try:
        root = ET.fromstring(get('https://azure.status.microsoft/en-us/status/feed/'))
        items = root.findall('.//item')
        notes = [_clip(it.findtext('title')) for it in items[:5] if it.findtext('title')]
        n = len(items)
        return {'status': 'Available' if n == 0 else f'{n} open incident' + ('' if n == 1 else 's'), 'link': link, 'notes': notes}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': link, 'notes': []}, str(e)[:160]

def slack():
    link = 'https://slack-status.com/'
    try:
        d = json.loads(get('https://slack-status.com/api/v2.0.0/current'))
        act = d.get('active_incidents') or []
        notes = [_clip(i.get('title')) for i in act if isinstance(i, dict)][:5]
        ok = (d.get('status') == 'ok') and not act
        return {'status': 'Available' if ok else (f'{len(act)} open incident' + ('' if len(act) == 1 else 's') if act else str(d.get('status') or 'Unknown')), 'link': link, 'notes': notes}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': link, 'notes': []}, str(e)[:160]

def salesforce():
    # Salesforce runs many separate instances; most incidents hit only some of them.
    link = 'https://status.salesforce.com/'
    try:
        act = json.loads(get('https://api.status.salesforce.com/v1/incidents/active'))
        act = act if isinstance(act, list) else []
        n = len(act)
        notes = []
        for i in act[:5]:
            inst = i.get('instanceKeys') or []
            notes.append(_clip(('Affects all instances' if i.get('affectsAll') else f'Affects {len(inst)} instance' + ('' if len(inst) == 1 else 's') + (': ' + ', '.join(inst[:6]) if inst else '')) + (' (core service)' if i.get('isCore') else '')))
        return {'status': 'Available' if n == 0 else f'{n} open incident' + ('' if n == 1 else 's'), 'link': link, 'notes': notes}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': link, 'notes': []}, str(e)[:160]

STATUSPAGES = [('wasabi', 'https://status.wasabi.com/'), ('zoom', 'https://status.zoom.us/'), ('netsuite', 'https://status.netsuite.com/'),
               ('cloudflare', 'https://www.cloudflarestatus.com/'), ('dropbox', 'https://status.dropbox.com/'), ('box', 'https://status.box.com/'),
               ('goto', 'https://status.goto.com/'), ('quickbooks', 'https://status.quickbooks.intuit.com/')]
CHECKS = [('m365', m365), ('aws', aws), ('google', google), ('azure', azure), ('slack', slack), ('salesforce', salesforce)] + \
         [(k, (lambda b=b: statuspage(b))) for k, b in STATUSPAGES]

def main():
    prev = {}
    if OUT.exists():
        try: prev = json.loads(OUT.read_text())
        except Exception: prev = {}
    items, ok, errors = [], [], {}
    for source, url in FEEDS:
        try:
            got = parse(source, get(url)); items += got; ok.append(f'{source}: {len(got)}')
        except Exception as e:
            print(f'{source} failed: {e}'); errors[source] = str(e)[:160]
            items += [x for x in prev.get('items', []) if x.get('source') == source]   # keep last good headlines
    if not any(x['source'] == 'CISA' for x in items):   # CISA's site often blocks cloud runners; use its KEV catalog instead
        try:
            kev = json.loads(get(KEV_JSON)).get('vulnerabilities', [])
            kev.sort(key=lambda v: v.get('dateAdded', ''), reverse=True)
            for v in kev[:PER_SOURCE]:
                d = dt.datetime.fromisoformat(v['dateAdded']).replace(tzinfo=dt.timezone.utc)
                items.append({'title': clean(f"Actively exploited: {v.get('vendorProject', '')} {v.get('product', '')} ({v['cveID']})"), 'link': f"https://nvd.nist.gov/vuln/detail/{v['cveID']}", 'source': 'CISA', 'date': d.isoformat()})
            errors.pop('CISA', None); ok.append('CISA KEV: %d' % min(len(kev), PER_SOURCE))
        except Exception as e:
            errors['CISA KEV'] = str(e)[:160]
    seen, uniq = set(), []
    for x in sorted(items, key=lambda x: x['date'], reverse=True):
        k = x['title'].lower()
        if k not in seen: seen.add(k); uniq.append(x)
    # every source gets its two newest headlines in, then the rest fill by date
    first = [x for src, _ in FEEDS for x in [y for y in uniq if y['source'] == src][:2]]
    rest = [x for x in uniq if x not in first]
    pick = sorted(first + rest[:max(0, TOTAL - len(first))], key=lambda x: x['date'], reverse=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    data = {'updated': now, 'items': pick, 'errors': errors}
    for key, fn in CHECKS:
        r, err = fn(); r['checked'] = now; data[key] = r
        if err: errors[key + ' status'] = err; print(key, 'status failed:', err)
    # Okta publishes no public feed (its status data needs a sign-in), so the page links to it instead.
    data['okta'] = {'status': 'Link only', 'link': 'https://status.okta.com/', 'notes': [], 'checked': now}
    if not data['items'] and prev.get('items'): data['items'] = prev['items']
    OUT.write_text(json.dumps(data, indent=1))
    # history: everything seen in the last 14 days, kept between runs, newest first
    try: hist = json.loads(HIST.read_text()).get('items', []) if HIST.exists() else []
    except Exception: hist = []
    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)).isoformat()
    keep, seen_h = [], set()
    for x in sorted(uniq + hist, key=lambda x: x['date'], reverse=True):
        k = x['title'].lower()
        if x['date'] >= cutoff and k not in seen_h: seen_h.add(k); keep.append(x)
    HIST.write_text(json.dumps({'updated': now, 'items': keep[:600]}, indent=1))
    print('\n'.join(ok)); print(' | '.join(f"{k}: {data[k]['status']}" for k, _ in CHECKS), '|', '| headlines:', len(data['items']))

if __name__ == '__main__':
    main()
