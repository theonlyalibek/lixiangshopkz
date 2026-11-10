"""Collect changed pages from git diff (or the whole sitemap) and send them to IndexNow."""
import json, os, re, subprocess, urllib.error, urllib.request

DOMAIN = 'https://lixiangshop.kz'
KEY = os.environ['KEY']
before = os.environ.get('BEFORE', '')

def all_urls():
    return re.findall(r'<loc>(.*?)</loc>', open('site/sitemap.xml', encoding='utf-8').read())

if os.environ.get('ALL') == 'true' or not before or set(before) == {'0'}:
    urls = all_urls()
else:
    out = subprocess.run(['git', 'diff', '--name-only', before, 'HEAD', '--', 'site/'],
                         capture_output=True, text=True, check=True).stdout.split()
    urls = []
    for f in out:
        if f == 'site/index.html':
            urls.append(DOMAIN + '/')
        elif f.endswith('/index.html') and not f.startswith('site/assets/'):
            urls.append(DOMAIN + '/' + f[len('site/'):-len('index.html')])
    urls = sorted(set(urls))

print(len(urls), 'urls')
if not urls:
    raise SystemExit(0)
body = json.dumps({'host': 'lixiangshop.kz', 'key': KEY, 'keyLocation': f'{DOMAIN}/{KEY}.txt',
                   'urlList': urls[:10000]}).encode()
for ep in ('https://api.indexnow.org/indexnow', 'https://yandex.com/indexnow'):
    req = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(ep, r.status)
    except urllib.error.HTTPError as e:
        print(ep, 'HTTP', e.code, e.read()[:300])
