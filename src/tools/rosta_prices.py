"""Update site prices from a Rosta export (made by rosta_pull.py).

    python src/tools/rosta_prices.py ROSTA_EXPORT.json

Each catalog row is linked to Rosta items in data/rosta-map.json. The row gets the lowest retail
price of its linked items. Rows with no link or no Rosta price keep their previous price
(0 means "по запросу"). Writes data/prices.json and prints what changed. Stock is not exported.
"""
import json, os, sys
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
rosta = {x['id']: x for x in json.load(open(sys.argv[1], encoding='utf-8-sig'))['items'] if not x.get('is_removed')}
cat = json.load(open(os.path.join(HERE, 'cat.json')))
link = json.load(open(os.path.join(HERE, 'rosta-map.json')))
pf = os.path.join(HERE, 'prices.json')
if os.path.exists(pf):
    old = json.load(open(pf))
else:
    old = [x['price_kzt'] for x in json.load(open(os.path.join(HERE, 'satu-prices.json')))]
old += [0] * (len(cat) - len(old))
new, changed = [], 0
for r, row in enumerate(cat):
    ps = [rosta[i]['price'] for i in link.get(str(r), []) if i in rosta and rosta[i].get('price')]
    p = min(ps) if ps else old[r]
    if p != old[r]:
        changed += 1
        print('%4d  %-55s %10s -> %s' % (r, row[1][:55], old[r] or 'по запросу', p))
    new.append(p)
json.dump(new, open(pf, 'w'))
print(changed, 'prices changed,', sum(1 for p in new if not p), 'rows без цены')
