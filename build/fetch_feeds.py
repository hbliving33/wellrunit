"""Pull security news headlines and Microsoft 365 public status into assets/data/news.json.

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

def m365():
    try:
        root = ET.fromstring(get(M365_FEED))
        it = root.find('.//item')
        status = (it.findtext('status') or '').strip() if it is not None else ''
        return {'status': status or 'Unknown', 'checked': dt.datetime.now(dt.timezone.utc).isoformat(), 'link': 'https://status.cloud.microsoft/'}
    except Exception as e:
        print('M365 status failed:', e)
        return {'status': 'Unknown', 'checked': dt.datetime.now(dt.timezone.utc).isoformat(), 'link': 'https://status.cloud.microsoft/'}

def aws():
    # AWS Health Dashboard public events (no sign-in needed).  An empty list means no open public events.
    url = 'https://health.aws.amazon.com/public/currentevents'
    try:
        raw = get(url).decode('utf-16') if get(url)[:2] in (b'\xff\xfe', b'\xfe\xff') else get(url).decode('utf-8-sig')
        ev = json.loads(raw or '[]')
        n = len(ev) if isinstance(ev, list) else 0
        return {'status': 'Available' if n == 0 else f'{n} open event' + ('' if n == 1 else 's'), 'link': 'https://health.aws.amazon.com/health/status'}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': 'https://health.aws.amazon.com/health/status'}, str(e)[:160]

def wasabi():
    # Wasabi's status page; this checks the standard status-page summary it publishes.
    try:
        d = json.loads(get('https://status.wasabi.com/api/v2/status.json'))
        ind = (d.get('status') or {}).get('indicator', '')
        desc = (d.get('status') or {}).get('description', '')
        return {'status': 'Available' if ind == 'none' else (desc or 'Unknown'), 'link': 'https://status.wasabi.com/'}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': 'https://status.wasabi.com/'}, str(e)[:160]

def statuspage(base):
    # Atlassian Statuspage sites publish a public summary at /api/v2/status.json (no sign-in needed).
    try:
        d = json.loads(get(base.rstrip('/') + '/api/v2/status.json'))
        ind = (d.get('status') or {}).get('indicator', '')
        desc = (d.get('status') or {}).get('description', '')
        return {'status': 'Available' if ind == 'none' else (desc or 'Unknown'), 'link': base}, None
    except Exception as e:
        return {'status': 'Unknown', 'link': base}, str(e)[:160]

EXTRA = [('zoom', 'Zoom status', 'https://status.zoom.us/'), ('netsuite', 'NetSuite status', 'https://status.netsuite.com/')]

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
    a, ae = aws(); w, we = wasabi()
    if ae: errors['AWS status'] = ae
    if we: errors['Wasabi status'] = we
    now = dt.datetime.now(dt.timezone.utc).isoformat(); a['checked'] = w['checked'] = now
    data = {'updated': now, 'm365': m365(), 'aws': a, 'wasabi': w, 'items': pick, 'errors': errors}
    for key, label, base in EXTRA:
        r, err = statuspage(base); r['checked'] = now; data[key] = r
        if err: errors[label] = err
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
    print('\n'.join(ok)); print('M365:', data['m365']['status'], '| headlines:', len(data['items']))

if __name__ == '__main__':
    main()
