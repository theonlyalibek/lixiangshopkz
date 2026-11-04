"""Pull products, groups and stock from the Rosta public API into one JSON file.

The key is never stored in the repo. Pass it in the ROSTA_KEY environment variable:
    set ROSTA_KEY=...            (Windows)   export ROSTA_KEY=...   (Linux/macOS)
    python src/tools/rosta_pull.py OUT.json
OUT.json holds stock and other internal data: keep it outside the repo.
"""
import json, os, sys, time, urllib.error, urllib.request

BASE = 'https://next.rosta.kz/api/client/public'
KEY = os.environ.get('ROSTA_KEY') or sys.exit('ROSTA_KEY is not set')


def call(path, body=None):
    req = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body).encode(),
                                 method='GET' if body is None else 'POST',
                                 headers={'Authorization': 'Bearer ' + KEY, 'Accept': 'application/json', 'Content-Type': 'application/json'})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                time.sleep(0.5)
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 7: raise
            time.sleep(int(e.headers.get('Retry-After') or 0) or 5 * (attempt + 1))


def pages(path, body=None):
    out, page = [], 1
    while True:
        sep = '&' if '?' in path else '?'
        j = call('%s%spage=%d' % (path, sep, page), body)
        out += j.get('data') or []
        if page >= (j.get('meta') or {}).get('last_page', 1):
            return out
        page += 1


items = pages('/items?page_size=500')
items = list({x['id']: x for x in items}.values())
groups = list({g['id']: g for g in pages('/items/groups?page_size=500')}.values())
warehouses = pages('/warehouses')
stock = {w['name']: pages('/warehouses/%s/items' % w['id'], {}) for w in warehouses}
json.dump({'items': items, 'groups': groups, 'warehouses': warehouses, 'stock': stock},
          open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(items), 'items,', len(groups), 'groups,', {k: len(v) for k, v in stock.items()})
