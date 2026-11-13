"""One-off check (temporary branch): is Okta's overall status in the page as served?"""
import urllib.request, re
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36', 'Accept': 'text/html'}
with urllib.request.urlopen(urllib.request.Request('https://status.okta.com/', headers=UA), timeout=25) as r: t = r.read().decode('utf-8', 'replace')
for pat in [r'system__status_today_status.{0,200}', r'today_icon.{0,40}', r'icon-(Success|Warning|Error|Info|Disruption|Outage)[^"]{0,20}', r'js-render-modal.{0,120}']:
    m = re.findall(pat, t, re.S)
    print('P', repr(pat[:30]), len(m), repr(re.sub(r'\s+', ' ', str(m[0]))[:260]) if m else '')
