"""One-off check (temporary branch): Okta's RSS feed structure."""
import urllib.request, re
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36', 'Accept': '*/*'}
with urllib.request.urlopen(urllib.request.Request('https://feeds.feedburner.com/OktaStatusRSS', headers=UA), timeout=25) as r: t = r.read().decode('utf-8', 'replace')
print('P items', t.count('<item'), 'entries', t.count('<entry'))
for blk in re.findall(r'<(?:item|entry)\b.*?</(?:item|entry)>', t, re.S)[:4]:
    b = re.sub(r'\s+', ' ', blk)
    title = re.search(r'<title[^>]*>(.*?)</title>', b); date = re.search(r'<(pubDate|updated|published)>(.*?)<', b)
    print('P ITEM', (title.group(1) if title else '')[:160], '|', date.group(2) if date else '', '|', re.sub(r'<[^>]+>|&lt;[^&]*&gt;', ' ', b)[:400])
