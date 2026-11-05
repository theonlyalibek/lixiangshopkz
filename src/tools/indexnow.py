"""Ping IndexNow (Bing, Yandex) with every URL from site/sitemap.xml.
Run after a deploy: python3 src/tools/indexnow.py"""
import json, os, re, urllib.request
KEY = 'e864aec0b98bbd3f6b2ffc80e169086f'
HERE = os.path.dirname(os.path.abspath(__file__))
urls = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(HERE, '..', '..', 'site', 'sitemap.xml')).read())
body = json.dumps({"host": "lixiangshop.kz", "key": KEY, "keyLocation": "https://lixiangshop.kz/%s.txt" % KEY, "urlList": urls}).encode()
for ep in ('https://api.indexnow.org/indexnow', 'https://yandex.com/indexnow'):
    req = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: print(ep, r.status, len(urls))
    except Exception as e: print(ep, 'error', e)
