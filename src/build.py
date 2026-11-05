import glob
# -*- coding: utf-8 -*-
import json, os, sys, shutil, html, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C
import content2 as C2
import content3 as C3
import content4 as C4
C3.apply(C)
C4.apply(C)

MODE = sys.argv[1] if len(sys.argv) > 1 else 'deploy'   # preview | deploy
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'site')
DOMAIN = 'https://lixiangshop.kz'
WA = '77472194228'
PHONE = '+7 747 219 42 28'
GIS = 'https://2gis.kz/almaty/firm/70000001117356381'
GIS_VT = 'https://2gis.kz/almaty/firm/70000001104923303'
GIS_REV = GIS + '/tab/reviews'
GMAPS = 'https://www.google.com/maps/dir/?api=1&destination=43.251485%2C76.884787'
HOURS = 'Ежедневно 09:30–19:00'
LEGAL = 'ИП Новиков, ИИН 020317501018'
FOUNDER = {"@type": "Person", "@id": "https://viton.kz/#viktor", "name": "Виктор Новиков", "jobTitle": "Основатель Lixiangshop.kz, VITON.KZ и VibroTest", "image": "https://viton.kz/img/viktor-novikov.jpg", "url": "https://viton.kz/ru/"}
# part page photo: only a photo of exactly this part (part-<slug>.webp from the parts prompt)
PIMG = {}
for _f in glob.glob(os.path.join(HERE, 'img-parts', 'part-*.webp')):
    PIMG[os.path.basename(_f)[5:-5]] = 'part-' + os.path.basename(_f)[5:-5]
DATA = json.load(open(os.path.join(HERE, 'data', 'cat.json')))
PRICE = json.load(open(os.path.join(HERE, 'data', 'prices.json')))  # from Rosta, see tools/rosta_prices.py
PRICE += [0] * (len(DATA) - len(PRICE))
# Цены не показываем: их называет менеджер в WhatsApp. True вернёт цены на карточки, в корзину и разметку.
SHOW_PRICES = False
if not SHOW_PRICES: PRICE = [0] * len(PRICE)
NOTE_PRICE = 'Цену и наличие подскажет менеджер в WhatsApp, номер сверим по VIN.'
def rub(v): return f'{v:,}'.replace(',', '\u202f') + '\u00a0₸'
SATU = json.load(open(os.path.join(HERE, 'data', 'satu-parsed.json')))
SATU += [{}] * (len(DATA) - len(SATU))
_TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', ['a','b','v','g','d','e','e','zh','z','i','y','k','l','m','n','o','p','r','s','t','u','f','kh','ts','ch','sh','shch','','y','','e','yu','ya']))
def translit(t):
    t = ''.join(_TR.get(ch, ch) for ch in t.lower())
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t)).strip('-')
ROWPART = {}
def pslug(r):
    name, ms, oem = DATA[r][1], DATA[r][2], DATA[r][3]
    return translit(name + ' li ' + ' '.join('l' + m for m in ms) + ' ' + (oem or str(r)))
def pkey(r): return 'zapchasti/' + ROWPART[r]['slug'] + '/' + pslug(r)
def lc1(t): return t[:1].lower() + t[1:] if len(t) > 1 and t[1].islower() else t
def pimg(r): return 'img/p/%d.webp' % r if os.path.exists(os.path.join(HERE, 'pimg', '%d.webp' % r)) else None
SYS = {s['slug']: s for s in C.SYSTEMS}
for _p in C.PARTS:
    for _r in _p['rows']: ROWPART[_r] = _p
PART = {p['slug']: p for p in C.PARTS}
# the suspension article's cover repeats the Замена photo, so it goes last
C.ARTICLES = sorted(C.ARTICLES, key=lambda a: a['slug'] == 'stuchit-podveska-li')
ART = {a['slug']: a for a in C.ARTICLES}
MOD = ['6', '7', '8', '9']
BW = {'6': '62%', '7': '70%', '8': '78%', '9': '86%'}
SEATS = {m['m']: m['seats'] for m in C.MODELS}
UPD = '2026-11-04'
UPD_RU = '4 ноября 2026'
e = html.escape

def depth(key): return 0 if key == 'index' else key.count('/')
def href(cur, key, frag=''):
    if MODE == 'deploy':
        return ('/' if key == 'index' else '/' + key + '/') + frag
    return '../' * depth(cur) + ('index' if key == 'index' else key) + '.html' + frag
import hashlib as _h
VER = _h.md5(open(os.path.join(HERE, 'site.css'), 'rb').read() + open(os.path.join(HERE, 'site.js'), 'rb').read()).hexdigest()[:8]
def asset(cur, path):
    return ('/' if MODE == 'deploy' else '../' * depth(cur)) + path + ('?v=' + VER if path.endswith(('site.css', 'site.js')) else '')
def canon(key): return DOMAIN + ('/' if key == 'index' else '/' + key + '/')
METRIKA_ID = 114093598
METRIKA = '''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=114093598', 'ym');

    ym(114093598, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/114093598" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->'''
def wa(text): return 'https://wa.me/%s?text=%s' % (WA, __import__('urllib.parse').parse.quote(text))
def models_of(rows):
    ms = set()
    for r in rows: ms |= set(DATA[r][2])
    return [m for m in MOD if m in ms]
def sdesc(intro):
    d = intro + ' Подбор по VIN, замена в Алматы, Аносова 91.'
    return d if len(d) <= 160 else intro if len(intro) <= 160 else intro.split('. ')[0] + '. Подбор по VIN в Алматы.'
def mlabel(ms): return ', '.join('L' + m for m in ms) if ms else 'уточним по VIN'
def plural(n, a, b, c):
    n1, n2 = n % 10, n % 100
    return a if n1 == 1 and n2 != 11 else b if 2 <= n1 <= 4 and not 12 <= n2 <= 14 else c
def links_md(cur, text):
    return re.sub(r'\[\[([a-z0-9-]+)\]\]', lambda m: '<a href="%s">%s</a>' % (href(cur, 'zapchasti/' + m.group(1)), e(PART[m.group(1)]['short'].lower())), e(text))

ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="i-wa" viewBox="0 0 24 24"><path d="M12 2.2A9.7 9.7 0 0 0 3.6 16.8L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3Z"/></symbol></svg>'''

STORE = {
  "@context": "https://schema.org", "@type": "AutoPartsStore", "@id": DOMAIN + "/#store",
  "name": "Lixiangshop.kz", "url": DOMAIN + "/", "telephone": "+77472194228",
  "description": "Запчасти для Li L6, L7, L8, L9 в Алматы. Подбор по VIN, замена на подъёмнике в VibroTest.",
  "address": {"@type": "PostalAddress", "streetAddress": "ул. Аносова, 91", "addressLocality": "Алматы", "addressCountry": "KZ"},
  "areaServed": {"@type": "City", "name": "Алматы"}, "hasMap": GIS,
  "geo": {"@type": "GeoCoordinates", "latitude": 43.251485, "longitude": 76.884787},
  "openingHours": "Mo-Su 09:30-19:00",
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "09:30", "closes": "19:00"}],
  "image": [DOMAIN + "/img/vhod-1600.webp", DOMAIN + "/img/hero-desktop.webp"], "logo": DOMAIN + "/logo-512.png",
  "legalName": "ИП Новиков", "founder": FOUNDER,
  "sameAs": ["https://www.instagram.com/lixiangshop.kz/", GIS],
  "knowsAbout": ["Li Auto L6", "Li Auto L7", "Li Auto L8", "Li Auto L9", "запчасти Li Auto", "замена подвески"],
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Запчасти для Li L6, L7, L8, L9",
    "itemListElement": [{"@type": "OfferCatalog", "name": s["name"], "url": DOMAIN + "/katalog/" + s["slug"] + "/"} for s in C.SYSTEMS]}
}

def crumbs_html(cur, items):
    if not items: return ''
    parts = ['<a href="%s">Главная</a>' % href(cur, 'index')]
    for k, name in items[:-1]: parts.append('<a href="%s">%s</a>' % (href(cur, k), e(name)))
    parts.append('<span aria-current="page">%s</span>' % e(items[-1][1]))
    return '<nav class="crumbs wrap" aria-label="Навигация">' + '<i>/</i>'.join(parts) + '</nav>'

def crumbs_ld(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Главная", "item": canon('index')}]
    for i, (k, name) in enumerate(items): lst.append({"@type": "ListItem", "position": i + 2, "name": name, "item": canon(k)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}

def pthumb(cur, p):
    pim = PIMG.get(p['slug'])
    return f'<img class="pth" src="{asset(cur, "img/" + pim + "-t.webp")}" alt="{e(p['name'])} для Li" loading="lazy">' if pim else ''
def wide(i):
    return i + '-wide' if i.startswith(('cat-', 'part-')) else 'service-desktop'

def band_pic(cur, i, alt):
    return f'<picture><source media="(min-width:760px)" srcset="{asset(cur, "img/" + wide(i) + ".webp")}"><img src="{asset(cur, "img/" + i + ".webp")}" alt="{alt}"></picture>'

def layout(key, title, desc, body, crumbs=None, ld=None, home=False, og_img='img/hero-desktop.webp', bar=None):
    ld = list(ld or [])
    if len(title) > 70 and title.endswith(' | Lixiangshop.kz'): title = title[:-len(' | Lixiangshop.kz')]
    if crumbs: ld.append(crumbs_ld(crumbs))
    navs = [('katalog', 'Каталог'), ('katalog', 'Модели', '#modeli'), ('poleznoe', 'Полезное'), ('zamena', 'Замена'), ('kontakty', 'Контакты')]
    nav = ''.join('<a href="%s">%s</a>' % (href(key, n[0], n[2] if len(n) > 2 else ''), n[1]) for n in navs)
    foot_sys = ''.join('<a href="%s">%s</a>' % (href(key, 'katalog/' + s['slug']), s['name']) for s in C.SYSTEMS)
    foot_mod = ''.join('<a href="%s">Li L%s</a>' % (href(key, 'modeli/li-l' + m), m) for m in MOD)
    foot_art = ''.join('<a href="%s">%s</a>' % (href(key, 'poleznoe/' + a['slug']), e(a['title'])) for a in C.ARTICLES)
    fab = '<a class="fab" id="fab" href="%s" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">%s</a>' % (wa('Здравствуйте! Пишу с сайта Lixiangshop.kz.'), ICON_WA)
    intro = '' if not home else '''<div id="intro" aria-hidden="true"><div class="stage">
<div class="bloom"></div><div class="streak"></div><div class="beam g2"></div><div class="beam g1"></div><div class="beam core"></div><div class="beam refl"></div>
<div class="spark"></div><div class="head l"></div><div class="head"></div><div class="wm">LIXIANG<span>SHOP.KZ</span></div></div>
<button class="skip" id="skip" tabindex="-1" aria-label="Пропустить"></button></div>'''
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0a0b0d">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon(key)}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="Lixiangshop.kz">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon(key)}"><meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="robots" content="max-image-preview:large"><meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="KZ-75"><meta name="geo.placename" content="Алматы">
<link rel="preload" href="{asset(key, 'assets/fonts/geist-cyrillic-wght-normal.woff2')}" as="font" type="font/woff2" crossorigin><link rel="preload" href="{asset(key, 'assets/fonts/michroma-wordmark.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{asset(key, 'favicon.ico')}" sizes="any"><link rel="icon" href="{asset(key, 'icon-192.png')}" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{asset(key, 'apple-touch-icon.png')}"><link rel="manifest" href="{asset(key, 'site.webmanifest')}">
<link rel="stylesheet" href="{asset(key, 'assets/site.css')}">
{''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)}
{METRIKA if MODE == 'deploy' else ''}
</head>
<body class="{'home' if home else 'inner'}{' has-sbar' if bar else ''}" data-wa="{WA}" data-models='{json.dumps({m: href(key, "modeli/li-l" + m) for m in MOD})}'>
{intro}
<header class="top{'' if home else ' solid'}" id="top"><div class="wrap">
<a class="brand" href="{href(key, 'index')}">LIXIANG<span>SHOP.KZ</span></a>
<nav class="nav" aria-label="Разделы">{nav}</nav>
<div class="tb"><a class="mychip" id="mychip" href="#">Li</a><a class="ib" href="{wa('Здравствуйте! Пишу с сайта Lixiangshop.kz.')}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON_WA}</a>
<button class="ib burger" id="menuBtn" aria-label="Меню" aria-expanded="false" aria-controls="menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 9h16M4 15h10"/></svg></button></div>
</div></header>
<div id="menu" aria-hidden="true"><nav>{nav}</nav><p>Аносова 91, Алматы<br>{HOURS}<span class="ostat" data-open></span><br>{PHONE}</p></div>
<main>
{crumbs_html(key, crumbs) if crumbs else ''}
{body}
</main>
<footer class="foot"><div class="wrap fgrid">
<div><a class="brand" href="{href(key, 'index')}">LIXIANG<span>SHOP.KZ</span></a><p>Независимый магазин запчастей для Li L6, L7, L8, L9 в Алматы.<br>Аносова 91 · {HOURS}<br><a href="tel:+77472194228">{PHONE}</a></p><p class="fnear">На той же площадке: <a href="https://viton.kz/ru/" target="_blank" rel="noopener">Viton</a> и <a href="https://vibrotest.kz/ru/" target="_blank" rel="noopener">VibroTest</a></p><nav class="fnav" aria-label="Разделы">{nav}</nav></div>
<div class="fcol"><b>Каталог</b>{foot_sys}</div>
<div class="fcol"><b>Модели</b>{foot_mod}<b class="mt">Сервис</b><a href="{href(key, 'zamena')}">Замена на VibroTest</a><a href="{href(key, 'kontakty')}">Контакты</a></div>
<div class="fcol"><b>Полезное</b>{foot_art}</div>
</div><div class="wrap legal"><p class="dl"><span><span>© 2026 Lixiangshop.kz</span><span>{LEGAL}</span><a href="{href(key, 'privacy')}">Политика данных</a></span></p><p>Независимый магазин. Не является официальным дилером Li Auto. Li и названия моделей принадлежат их правообладателям.</p></div></footer>
{fab if home else ''}{bar or ''}
{SPRITE}
<script src="{asset(key, 'assets/site.js')}"></script>
</body>
</html>'''

def near(rows, title='Рядом на той же площадке', h='h2'):
    li = ''.join(f'<li><a href="{u}" target="_blank" rel="noopener"><b>{e(n)}</b><span>{e(d)}</span>{ICON_ARROW}</a></li>' for n, u, d in rows)
    return f'<div class="near"><{h} class="nh">{e(title)}</{h}><ul>{li}</ul></div>'

def waform(cur, need='', m=''):
    ms = ''.join(f'<label class="mopt"><input type="radio" name="m" value="{m}"><span>L{m}</span></label>' for m in MOD)
    return f'''<form class="waf" data-waf data-m="{m}" novalidate>
<fieldset class="mseg"><legend>Модель</legend><div class="mrow">{ms}</div></fieldset>
<label class="fld"><span>Деталь или симптом</span><input name="need" value="{e(need)}" placeholder="Например, стучит спереди" autocomplete="off"></label>
<label class="fld"><span>VIN <small>по желанию</small></span><input class="vinf" name="vin" maxlength="17" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="17 символов из техпаспорта"></label>
<div class="fend"><button class="btn pri" type="submit">{ICON_WA}Отправить в WhatsApp</button><span class="cnt" aria-hidden="true">0/17</span></div>
<p class="err" role="alert"></p></form>'''

def cta(cur, need='', m='', title='Подберём и заменим', text='Выберите модель и напишите, что нужно. Сообщение в WhatsApp соберётся само.'):
    return f'''<section class="cta wrap fsec"><h2>{e(title)}</h2><p>{e(text)}</p>{waform(cur, need, m)}</section>'''

def tile(cur, s):
    n = sum(1 for r in DATA if r[0] == s['cat'])
    return f'<a class="tile" href="{href(cur, "katalog/" + s["slug"])}"><img src="{asset(cur, "img/" + s["img"] + ".webp")}" alt="{e(s["name"])} Li" loading="lazy"><b>{e(s["name"])}</b><span>{n} {plural(n, "позиция", "позиции", "позиций")}</span></a>'

def car(cur, m):
    n = sum(1 for r in DATA if m in r[2])
    return f'<a class="mod" data-m="{m}" href="{href(cur, "modeli/li-l" + m)}"><b><small>Li</small>L{m}</b><span>{n} {plural(n, "позиция", "позиции", "позиций")}</span></a>'

SYMPTOMS = [('Стучит подвеска', 'poleznoe/stuchit-podveska-li'), ('Скрипят тормоза', 'poleznoe/skrip-pri-tormozhenii-li'), ('Течёт антифриз', 'poleznoe/ohlazhdenie-li'),
            ('Люфт в руле', 'katalog/rulevoe'), ('Вибрация на скорости', 'katalog/privody'), ('Пора на ТО', 'poleznoe/to-li-filtry')]
def symptoms(cur):
    chips = ''.join('<a href="%s">%s</a>' % (href(cur, k), t) for t, k in SYMPTOMS)
    return f'<section class="s wrap"><h2 class="h2">Что беспокоит?</h2><div class="chips big">{chips}</div></section>'

def art_card(cur, a):
    return f'<a class="acard" href="{href(cur, "poleznoe/" + a["slug"])}"><img src="{asset(cur, "img/" + wide(a["img"]) + ".webp")}" alt="{e(a["title"])}" loading="lazy"><b>{e(a["title"])}</b></a>'

pages = {}

# ---------- home
k = 'index'
body = f'''<section class="hero"><picture><source media="(min-width:760px)" srcset="{asset(k, 'img/hero-desktop.webp')}"><img src="{asset(k, 'img/hero-mobile.webp')}" alt="Li L9 ночью над Алматы" fetchpriority="high"></picture>
<div class="copy wrap"><h1 class="rise">Запчасти для Li<span class="sr"> в Алматы</span></h1><p class="hl rise">Алматы · подбор по VIN · замена на месте</p>
<div class="row2 rise" id="heroCta"><a class="btn pri" href="#vin">Подобрать по VIN</a><a class="btn sec" href="{href(k, 'katalog')}">Каталог</a></div></div></section>
<section class="s wrap"><h2 class="h2">Модели</h2><div class="mods">{''.join(car(k, m) for m in MOD)}</div></section>
<section class="s wrap"><div class="hrow"><h2 class="h2">Каталог</h2><a class="more-link" href="{href(k, 'katalog')}">Все детали {ICON_ARROW}</a></div><div class="tiles">{''.join(tile(k, s) for s in C.SYSTEMS)}</div></section>
{symptoms(k)}
<section class="s wrap fsec" id="vin"><h2 class="h2">Подбор в WhatsApp</h2><p class="sub">Модель, деталь или симптом, VIN по желанию. Сообщение соберётся само.</p>{waform(k)}</section>
<a class="full" href="{href(k, 'zamena')}"><picture><source media="(min-width:760px)" srcset="{asset(k, 'img/service-desktop.webp')}"><img src="{asset(k, 'img/service-mobile.webp')}" alt="Замена детали на подъёмнике" loading="lazy"></picture>
<div class="copy wrap"><h2 class="h2">Замена на месте</h2><p>Проверка на вибростенде и замена на подъёмнике VibroTest {ICON_ARROW}</p></div></a>
<section class="s wrap"><div class="hrow"><h2 class="h2">Полезное</h2><a class="more-link" href="{href(k, 'poleznoe')}">Все статьи {ICON_ARROW}</a></div><div class="arts">{''.join(art_card(k, a) for a in C.ARTICLES)}</div></section>
<section class="s wrap split"><div class="addr">Аносова 91</div><div><div class="lines"><span>Независимый магазин запчастей Li</span><span>Алматы, {HOURS.lower()}<span class="ostat" data-open></span></span><a href="tel:+77472194228">{PHONE}</a><a href="https://www.instagram.com/lixiangshop.kz/" target="_blank" rel="noopener">@lixiangshop.kz</a></div>
<div class="row2 left"><a class="btn pri" href="{wa('Здравствуйте! Пишу с сайта Lixiangshop.kz.')}" target="_blank" rel="noopener">WhatsApp</a><a class="btn sec" href="{href(k, 'kontakty', '#kak-nayti')}">Как добраться</a></div>
{near(C2.SITES, h='h3')}</div></section>'''
pages[k] = layout(k, 'Запчасти для Li (Lixiang) L6, L7, L8, L9 в Алматы | Lixiangshop.kz',
    'Запчасти для Li Auto L6, L7, L8, L9 в Алматы: подвеска, тормоза, охлаждение, рулевое. Подбор по VIN, проверка и замена на VibroTest, Аносова 91.',
    body, ld=[STORE, {"@context": "https://schema.org", "@type": "WebSite", "name": "Lixiangshop.kz", "url": DOMAIN + "/", "inLanguage": "ru"}], home=True)

# ---------- katalog
k = 'katalog'
groups = ''
for s in C.SYSTEMS:
    items = ''.join(f'<li data-m="{"".join(models_of(p["rows"]))}"><a href="{href(k, "zapchasti/" + p["slug"])}"><span>{e(p["name"])}</span><small>{len(p["rows"])} {plural(len(p["rows"]), "позиция", "позиции", "позиций")} · {mlabel(models_of(p["rows"]))}</small></a></li>' for p in C.PARTS if p['sys'] == s['slug'])
    npos = sum(len(p['rows']) for p in C.PARTS if p['sys'] == s['slug'])
    groups += f'<details class="grp"><summary><span>{e(s["name"])}</span><small>{npos} {plural(npos, "позиция", "позиции", "позиций")}</small></summary><ul class="plist">{items}</ul><a class="more-link gl" href="{href(k, "katalog/" + s["slug"])}">Весь раздел {ICON_ARROW}</a></details>'
search_data = [[DATA[r][1], DATA[r][3], DATA[r][2], p['slug'] + '/' + pslug(r), p['name']] for p in C.PARTS for r in p['rows']]
body = f'''<section class="ph wrap"><h1>Каталог запчастей Li</h1><p class="lede">{len(DATA)} позиций для L6, L7, L8 и L9. Подбор по VIN, замена на месте в Алматы.</p>
<div class="myli" data-myli></div><p class="fit" id="fit" data-scope="catalog"></p>
<input class="search" id="q" type="search" placeholder="Деталь или номер" aria-label="Поиск по каталогу" autocomplete="off"><ul class="list" id="results" hidden></ul></section>
<section class="s wrap" style="padding-top:40px"><div class="tiles">{''.join(tile(k, s) for s in C.SYSTEMS)}</div></section>
{symptoms(k)}
<section class="s wrap" id="modeli"><h2 class="h2">По модели</h2><div class="mods">{''.join(car(k, m) for m in MOD)}</div></section>
<section class="s wrap"><h2 class="h2">Все детали</h2><div class="groups">{groups}</div></section>
{cta(k)}
<script>window.SEARCH={json.dumps(search_data, ensure_ascii=False)};</script>'''
pages[k] = layout(k, 'Каталог запчастей Li (Lixiang) L6, L7, L8, L9 в Алматы | Lixiangshop.kz',
    f'Каталог: {len(DATA)} запчастей для Li Auto L6, L7, L8, L9. Подвеска, тормоза, охлаждение, рулевое, приводы, двигатель, фильтры. Алматы, Аносова 91.',
    body, crumbs=[('katalog', 'Каталог')])

# ---------- systems
for s in C.SYSTEMS:
    k = 'katalog/' + s['slug']
    plist = [p for p in C.PARTS if p['sys'] == s['slug']]
    cards = ''.join(f'''<a class="pcard" href="{href(k, 'zapchasti/' + p['slug'])}">{pthumb(k, p)}<div><b>{e(p['name'])}</b><span>{len(p['rows'])} {plural(len(p['rows']), 'позиция', 'позиции', 'позиций')} · {mlabel(models_of(p['rows']))}</span></div>{ICON_ARROW}</a>''' for p in plist)
    arts = [a for a in C.ARTICLES if any('[[%s]]' % p['slug'] in json.dumps(a['body'], ensure_ascii=False) for p in plist)]
    rel = ''.join(art_card(k, a) for a in arts)
    install = 'Устанавливают наши партнёры, подбор и заказ у нас.' if s['install'] == 'partner' else 'Меняем на подъёмнике в VibroTest, Аносова 91.'
    body = f'''<section class="band">{band_pic(k, s['img'], e(s['name']) + ' Li')}<div class="copy wrap"><h1>{e(s['h1'])}</h1><p>L6 · L7 · L8 · L9 · Алматы</p></div></section>
<section class="wrap art"><p class="lede">{e(s['intro'])}</p></section>
<section class="s wrap" style="padding-top:40px"><h2 class="h2">Детали</h2><div class="pcards">{cards}</div></section>
<section class="wrap art" style="padding-top:24px"><h2>Когда пора к нам</h2><ul class="sym">{''.join('<li>' + e(x) + '</li>' for x in s['sym'])}</ul>
{near([('VibroTest', C2.VT_DIAG[0], C2.VT_DIAG[1] + ' ходовой и рулевого')], 'Проверить перед заказом') if s['slug'] in ('podveska', 'rulevoe') else ''}</section>
{'<section class="s wrap"><h2 class="h2">Полезное</h2><div class="arts">' + rel + '</div></section>' if rel else ''}
{cta(k)}'''
    pages[k] = layout(k, f'{s["h1"]} L6, L7, L8, L9 в Алматы | Lixiangshop.kz',
        sdesc(s['intro']), body,
        crumbs=[('katalog', 'Каталог'), (k, s['name'])], og_img='img/' + wide(s['img']) + '.webp')

# ---------- parts
POPULAR = ['stoyki-stabilizatora', 'perednie-rychagi', 'tormoznye-kolodki', 'tormoznye-diski', 'rulevye-nakonechniki', 'zadnie-rychagi', 'stupicy', 'saylentbloki', 'privody', 'salonnyy-filtr', 'maslyanyy-filtr', 'vozdushnyy-filtr']
for p in C.PARTS:
    k = 'zapchasti/' + p['slug']
    s = SYS[p['sys']]
    ms = models_of(p['rows'])
    rows = ''
    for r in p['rows']:
        name, rm, oem = DATA[r][1], DATA[r][2], DATA[r][3]
        msg = f'Здравствуйте! Нужна деталь: {name}{" (" + oem + ")" if oem else ""}, Li{(" " + mlabel(list(rm))) if rm else ""}. Подскажите цену?'
        num = ('<code>' + e(oem) + '</code>') if oem else 'номер по VIN'
        pr = f'<span class="pp">{rub(PRICE[r])}</span>' if PRICE[r] else ''
        rows += f'<li data-m="{rm}" data-id="{r}" data-n="{e(name)}" data-o="{e(oem or "")}" data-l="{mlabel(list(rm)) if rm else ""}" data-p="{PRICE[r] or 0}"><a class="pn" href="{href(k, pkey(r))}"><b>{e(name)}</b></a>{pr}<span class="pm">{mlabel(list(rm))} · {num}</span><a class="pa" href="{wa(msg)}" target="_blank" rel="noopener" aria-label="В корзину: {e(name)}">В корзину</a></li>'
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in p['faq'])
    sib = ''.join(f'<a href="{href(k, "zapchasti/" + q["slug"])}">{e(q["short"])}</a>' for q in C.PARTS if q['sys'] == p['sys'] and q['slug'] != p['slug'])
    arts = [a for a in C.ARTICLES if '[[%s]]' % p['slug'] in json.dumps(a['body'], ensure_ascii=False)]
    install = ('Устанавливают наши партнёры, подбор и заказ у нас.' if s['install'] == 'partner'
               else ('' if 'Меняем' in p['check'] else 'Меняем там же, на подъёмнике VibroTest.'))
    nt = len(p['rows']); nn = sum(1 for r in p['rows'] if DATA[r][3])
    pos = f'{nt} {plural(nt, "позиция", "позиции", "позиций")}'
    numtxt = (', у всех указан номер OEM' if nn == nt else '' if nn == 0 else f', у {nn} указан номер OEM')
    where = ('устанавливают наши партнёры' if s['install'] == 'partner' else 'меняем на подъёмнике VibroTest на Аносова 91')
    short = f'{p["name"]} для Li{(" " + mlabel(ms)) if ms else ""} в Алматы: {pos}{numtxt}. Точный номер подбираем по VIN, {where}. Наличие подтверждаем в WhatsApp.'
    cz = C2.CAUSE.get(p['slug'])
    if cz:
        assert len(cz) == len(p['sym']), p['slug']
        symblock = ('<h2>Симптом и причина</h2><table class="stbl"><thead><tr><th scope="col">Симптом</th><th scope="col">Частая причина</th></tr></thead><tbody>'
                    + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in zip(p['sym'], cz)) + '</tbody></table>')
    else:
        symblock = '<h2>Когда менять</h2><ul class="sym">' + ''.join('<li>' + e(x) + '</li>' for x in p['sym']) + '</ul>'
    nrows = []
    if s['slug'] in ('podveska', 'rulevoe'):
        nrows.append(('VibroTest', C2.VT_DIAG[0], C2.VT_DIAG[1]))
        if p['slug'] in C2.VT_SERVICE:
            sv = C2.VT_SERVICE[p['slug']]; nrows.append(('VibroTest', C2.VT + sv[0] + '/', sv[1]))
    if p['slug'] == 'toplivnaya-sistema':
        nrows.append(('Viton', 'https://viton.kz/ru/', 'Проверка и чистка форсунок'))
    nearblock = near(nrows, 'На той же площадке', 'h3') if nrows else ''
    pim = PIMG.get(p['slug'])
    fig = f'<figure class="pimg sm"><img src="{asset(k, "img/" + wide(pim) + ".webp")}" alt="{e(p["name"])}" loading="lazy"></figure>' if pim else ''
    askmsg = 'Здравствуйте! Нужно: ' + p['name'].lower() + ' для Li. VIN: '
    bym = ('<div class="chips" style="margin-top:16px">' + ''.join(f'<a href="{href(k, "modeli/li-l" + m + "/" + p["slug"])}">{e(p["short"])} Li L{m}</a>' for m in MOD if any(m in DATA[r][2] for r in p['rows'])) + '</div>') if p['slug'] in POPULAR else ''
    bar = f'<div class="sbar"><a class="btn pri" href="{wa(askmsg)}" target="_blank" rel="noopener">{ICON_WA}Подобрать по VIN</a></div>'
    ld = []
    if p['faq']:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]})
    ld.append({"@context": "https://schema.org", "@type": "ItemList", "name": p['name'] + ' для Li', "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": DATA[r][1] + ' для Li', **({"mpn": DATA[r][3]} if DATA[r][3] else {}), **({"offers": {"@type": "Offer", "price": PRICE[r], "priceCurrency": "KZT", "seller": {"@type": "Organization", "name": "Lixiangshop"}}} if PRICE[r] else {})}} for i, r in enumerate(p['rows'])]})
    body = f'''<section class="ph wrap"><h1>{e(p['name'])} для Li{(" " + mlabel(ms)) if ms else ""}</h1><div class="short"><p class="lbl">Коротко</p><p>{e(short)}</p></div>
<div class="myli" data-myli></div><p class="fit" id="fit" data-scope="part"></p>
<div class="btns dsk"><a class="btn pri" href="{wa(askmsg)}" target="_blank" rel="noopener">{ICON_WA}Подобрать по VIN</a></div></section>
<section class="wrap art" style="padding-top:28px">
<ul class="prow">{rows}</ul>
{bym}<p class="pnote">{NOTE_PRICE}</p>
{('<p class="muted">' + e(p['note']) + '</p>') if p['note'] else ''}
{fig}
{symblock}
<h2>Проверка и замена</h2><p>{e(p['check'])}{(' ' + install) if install else ''}</p><a class="more-link" href="{href(k, 'zamena')}">Как проходит замена {ICON_ARROW}</a>
{nearblock}
{('<h2>Вопросы</h2><div class="faq">' + faq + '</div>') if faq else ''}
{('<h2>Читайте также</h2><ul class="sym">' + ''.join('<li><a href="%s">%s</a></li>' % (href(k, 'poleznoe/' + a['slug']), e(a['title'])) for a in arts) + '</ul>') if arts else ''}
{('<h2>Ещё в разделе «' + e(s['name']) + '»</h2><div class="chips">' + sib + '</div>') if sib else ''}
</section>'''
    pages[k] = layout(k, f'{p["name"]} для Li{(" " + mlabel(ms)) if ms else ""} в Алматы | Lixiangshop.kz',
        f'{p["name"]} для Li Auto (Lixiang){(" " + mlabel(ms)) if ms else ""}: {"номера деталей" if nn else "подбор по VIN"}, признаки износа, проверка на VibroTest и замена в Алматы, Аносова 91.',
        body, crumbs=[('katalog', 'Каталог'), ('katalog/' + s['slug'], s['name']), (k, p['short'])], ld=ld,
        og_img='img/' + wide(pim or s['img']) + '.webp', bar=bar)

# ---------- products
for p in C.PARTS:
    s = SYS[p['sys']]
    where = ('Установят наши партнёры.' if s['install'] == 'partner' else 'Заменим там же, на подъёмнике VibroTest.')
    for r in p['rows']:
        k = pkey(r)
        name, rm, oem = DATA[r][1], DATA[r][2], DATA[r][3]
        ml = mlabel(list(rm)) if rm else ''
        forli = 'Li' + (' ' + ml if ml else '')
        price = PRICE[r]
        img = pimg(r) or ('img/' + wide(PIMG[p['slug']]) + '.webp' if PIMG.get(p['slug']) else None)
        sat = SATU[r]
        maker = dict(sat.get('attrs') or []).get('Производитель', '')
        msg = f'Здравствуйте! Нужна деталь: {name}{" (" + oem + ")" if oem else ""}, {forli}. Подскажите цену?'
        data = f'data-m="{rm}" data-id="{r}" data-n="{e(name)}" data-o="{e(oem or "")}" data-l="{ml}" data-p="{price or 0}"'
        answer = (f'В Lixiangshop в Алматы. {name} для {forli}'
                  + (f', номер {oem}' if oem else '') + (f', цена {rub(price).replace(chr(0x202f), " ").replace(chr(0xa0), " ")}' if price else '')
                  + f'. Перед заказом сверяем номер по VIN. {where}')
        sibs = [x for x in p['rows'] if x != r]
        sib = ''.join(f'<li data-m="{DATA[x][2]}"><a href="{href(k, pkey(x))}"><span>{e(DATA[x][1])}</span><small>{mlabel(list(DATA[x][2]))}{(" · " + e(DATA[x][3])) if DATA[x][3] else ""}</small></a></li>' for x in sibs)
        spec = [('Номер OEM', f'<code>{e(oem)}</code>' if oem else 'подбираем по VIN'), ('Модели', e(forli)),
                ('Раздел', f'<a href="{href(k, "zapchasti/" + p["slug"])}">{e(p["name"])}</a>')]
        spec.insert(1, ('Марка', 'Li Auto (Lixiang, Лисян)'))
        if maker: spec.append(('Производитель', e(maker.title())))
        spec_html = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in spec)
        fig = (f'<figure class="pph"><img src="{asset(k, img)}" alt="{e(name)} для {e(forli)}{(", " + e(oem)) if oem else ""}" width="800" height="800" fetchpriority="high"></figure>' if img else '')
        body = f"""<section class="ph wrap prod" {data}>
<div class="pgrid">{fig}<div class="pinfo">
<h1>{e(name)} для {e(forli)}</h1>
{f'<p class="poem">OEM <code>{e(oem)}</code></p>' if oem else ''}
{f'<p class="pprice">{rub(price)}</p>' if price else '<p class="pprice na">Цена по запросу в WhatsApp</p>'}
<p class="pfit" data-fitm="{rm}">Подходит: {e(forli)}</p>
<div class="btns"><a class="btn pri pa" href="{wa(msg)}" target="_blank" rel="noopener" data-add>В корзину</a><a class="btn sec" href="{wa(msg)}" target="_blank" rel="noopener">{ICON_WA}Узнать цену</a></div>
<p class="pnote">{NOTE_PRICE}</p>
</div></div></section>
<section class="wrap art" style="padding-top:8px">
<h2>Где купить в Алматы</h2><p>{e(answer)}</p>
<table class="spec"><tbody>{spec_html}</tbody></table>
<h2>Когда менять</h2><ul class="sym">{''.join('<li>' + e(x) + '</li>' for x in p['sym'][:4])}</ul>
<h2>Проверка и замена</h2><p>{e(p['check'])}</p>
{('<h2>Другие позиции: ' + e(lc1(p['name'])) + '</h2><ul class="plist">' + sib + '</ul>') if sib else ''}
<a class="more-link" href="{href(k, "zapchasti/" + p["slug"])}">{e(p["name"])}: симптомы и замена {ICON_ARROW}</a>
</section>"""
        prod_ld = {"@context": "https://schema.org", "@type": "Product", "name": f'{name} для {forli}', "url": canon(k),
                   "description": f'{name} для Li Auto (Lixiang){(" " + ml) if ml else ""}{(", номер " + oem) if oem else ""}. Подбор по VIN и замена в Алматы.',
                   "category": p['name'], **({"mpn": oem, "sku": oem} if oem else {}),
                   **({"brand": {"@type": "Brand", "name": "Li Auto"}} if maker else {}),
                   **({"image": DOMAIN + '/' + img} if img else {}),
                   **({"offers": {"@type": "Offer", "url": canon(k), "price": price, "priceCurrency": "KZT", "seller": {"@id": DOMAIN + "/#store"}, "areaServed": {"@type": "City", "name": "Алматы"}}} if price else {})}
        bar = f'<div class="sbar" {data}><a class="btn pri pa" href="{wa(msg)}" target="_blank" rel="noopener" data-add>В корзину{(" · " + rub(price)) if price else ""}</a></div>'
        title = f'{name} для {forli} (Lixiang) купить в Алматы{(" · " + oem) if oem else ""}'
        if len(title) > 70: title = f'{name} для {forli} купить в Алматы{(" · " + oem) if oem else ""}'
        desc = f'{name} для Li Auto (Lixiang){(" " + ml) if ml else ""}{(", номер " + oem) if oem else ""}. Купить в Алматы: подбор по VIN, {"установка у партнёров" if s["install"] == "partner" else "замена на подъёмнике VibroTest"}.'
        if len(desc) > 160: desc = f'{name} для Li{(" " + ml) if ml else ""}{(", номер " + oem) if oem else ""}. Купить в Алматы: подбор по VIN, {"установка у партнёров" if s["install"] == "partner" else "замена на VibroTest"}.'
        pages[k] = layout(k, title, desc, body,
            crumbs=[('katalog', 'Каталог'), ('katalog/' + s['slug'], s['name']), ('zapchasti/' + p['slug'], p['short']), (k, name)],
            ld=[prod_ld], og_img=img or 'img/hero-desktop.webp', bar=bar)

# ---------- models
for mm in C.MODELS:
    m = mm['m']; k = 'modeli/li-l' + m
    tiles = ''; srcs = ''; total = 0
    for s in C.SYSTEMS:
        items = ''; n = 0
        for p in C.PARTS:
            if p['sys'] != s['slug']: continue
            rr = [r for r in p['rows'] if m in DATA[r][2]]
            if not rr: continue
            n += len(rr)
            items += f'<li><a href="{href(k, "zapchasti/" + p["slug"])}"><span>{e(p["name"])}</span><small>{len(rr)}</small>{ICON_ARROW}</a></li>'
        if not n: continue
        total += n
        tiles += f'<a class="tile" href="{href(k, "katalog/" + s["slug"])}" data-sheet="{s["slug"]}"><img src="{asset(k, "img/" + s["img"] + ".webp")}" alt="{e(s["name"])} Li L{m}" loading="lazy"><b>{e(s["name"])}</b><span>{n} {plural(n, "позиция", "позиции", "позиций")}</span></a>'
        note = '<p class="snote">Устанавливают партнёры, подбор у нас.</p>' if s['install'] == 'partner' else ''
        srcs += f'<div class="ssrc" id="src-{s["slug"]}" hidden data-title="{e(s["name"])}" data-img="{asset(k, "img/" + wide(s["img"]) + ".webp")}" data-all="{href(k, "katalog/" + s["slug"])}"><ul class="slist">{items}</ul>{note}</div>'
    pop = [x for x in POPULAR if any(m in DATA[r][2] for r in PART[x]['rows'])][:8]
    chips = ''.join(f'<a href="{href(k, "modeli/li-l" + m + "/" + x)}">{e(PART[x]["short"])}</a>' for x in pop)
    others = ''.join(f'<a href="{href(k, "modeli/li-l" + x)}">Li L{x}</a>' for x in MOD if x != m)
    sheet = f'''<div class="sheet" id="sheet" aria-hidden="true"><div class="sheet-bg" data-close></div>
<div class="sheet-panel" role="dialog" aria-modal="true" aria-labelledby="sheetT"><div class="grab" aria-hidden="true"></div>
<div class="shead"><h2 id="sheetT">Запчасти</h2><button class="ib" data-close aria-label="Закрыть"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>
<img class="simg" alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">
<div class="sbody"></div>
<div class="sfoot"><a class="btn pri" href="{wa('Здравствуйте! Нужна деталь для Li L' + m + '. VIN: ')}" target="_blank" rel="noopener">{ICON_WA}Не нашли? Подбор по VIN</a><a class="btn sec" data-all href="#">Вся система</a></div></div></div>'''
    body = f'''<section class="ph wrap"><h1>Запчасти для Li L{m} в Алматы</h1><p class="lede">{total} {plural(total, 'позиция', 'позиции', 'позиций')}. Выберите систему или пришлите VIN.</p><div class="myli" data-myli data-pick="{m}"></div></section>
<figure class="pimg wrap model"><img src="{asset(k, 'img/car-l' + m + '-wide.webp')}" alt="Li L{m}"></figure>
<section class="s wrap" style="padding-top:48px"><h2 class="h2">Что ищете?</h2><div class="tiles">{tiles}</div></section>
<section class="s wrap" style="padding-top:64px"><h2 class="h2">Быстро найти</h2><div class="chips big">{chips}</div></section>
<section class="s wrap" style="padding-top:64px"><h2 class="h2">Другие модели</h2><div class="chips">{others}</div></section>
{srcs}
{cta(k, m=m)}
{sheet}'''
    pages[k] = layout(k, f'Запчасти для Li L{m} (Lixiang L{m}) в Алматы | Lixiangshop.kz',
        f'Запчасти для Li Auto L{m} (Lixiang L{m}): подвеска, тормоза, охлаждение, рулевое, приводы, фильтры. Подбор по VIN и замена в Алматы.',
        body, crumbs=[('katalog', 'Каталог'), (k, 'Li L' + m)], og_img='img/car-l' + m + '-wide.webp')


# ---------- model × part landings: «тормозные колодки Li L6»
MP = {}
for p in C.PARTS:
    if p['slug'] not in POPULAR: continue
    for m in MOD:
        rr = [r for r in p['rows'] if m in DATA[r][2]]
        if rr: MP[(m, p['slug'])] = rr
for (m, sl), rr in MP.items():
    p = PART[sl]; s = SYS[p['sys']]; k = 'modeli/li-l' + m + '/' + sl
    nm = p['name']; low = lc1(nm)
    rows = ''
    for r in rr:
        name, rm, oem = DATA[r][1], DATA[r][2], DATA[r][3]
        msg = f'Здравствуйте! Нужна деталь: {name}{" (" + oem + ")" if oem else ""}, Li L{m}. Подскажите цену?'
        num = ('<code>' + e(oem) + '</code>') if oem else 'номер по VIN'
        rows += f'<li data-m="{rm}" data-id="{r}" data-n="{e(name)}" data-o="{e(oem or "")}" data-l="L{m}" data-p="0"><a class="pn" href="{href(k, pkey(r))}"><b>{e(name)}</b></a><span class="pm">{mlabel(list(rm))} · {num}</span><a class="pa" href="{wa(msg)}" target="_blank" rel="noopener" aria-label="В корзину: {e(name)}">В корзину</a></li>'
    nums = [DATA[r][3] for r in rr if DATA[r][3]]
    only = [r for r in rr if DATA[r][2] == m]
    shared = sorted({x for r in rr for x in DATA[r][2] if x != m})
    where = ('устанавливают наши партнёры' if s['install'] == 'partner' else 'меняем на подъёмнике VibroTest')
    n = len(rr)
    short = (f'{nm} для Li L{m} (Lixiang L{m}) в Lixiangshop.kz, Алматы: {n} {plural(n, "позиция", "позиции", "позиций")}'
             + (f', номера {", ".join(nums[:4])}' if nums else '') + f'. Номер сверяем по VIN, {where}. Цену подскажет менеджер в WhatsApp.')
    if only and len(only) == n: fit = f'Нет. Все позиции в этом разделе сделаны только под L{m}, детали от других Li не подойдут.'
    elif shared: fit = f'Часть позиций общая с {", ".join("L" + x for x in shared)}, часть своя. Какая стоит на вашей машине, сверим по VIN.'
    else: fit = f'Сверим по VIN: у разных лет выпуска L{m} номера могут отличаться.'
    faq = [(f'Где купить {low} на Li L{m} в Алматы?', f'В Lixiangshop.kz, независимом магазине запчастей для Li в Алматы. Номер сверяем по VIN, {where}. Напишите в WhatsApp, менеджер назовёт цену.'),
           (f'{nm} для Li L{m}: какой номер OEM?', ('; '.join(f'{DATA[r][1]}: {DATA[r][3]}' for r in rr if DATA[r][3]) + '.') if nums else 'Подбираем по VIN.'),
           (f'{"Подходят" if nm.split()[0][-1] in "иые" else "Подходит"} ли {low} от других моделей Li на L{m}?', fit)]
    faq_html = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    others = ''.join(f'<a href="{href(k, "modeli/li-l" + x + "/" + sl)}">Li L{x}</a>' for x in MOD if x != m and (x, sl) in MP)
    more = ''.join(f'<a href="{href(k, "modeli/li-l" + m + "/" + y)}">{e(PART[y]["short"])}</a>' for y in POPULAR if y != sl and (m, y) in MP)
    askmsg = f'Здравствуйте! Нужно: {low} для Li L{m}. VIN: '
    bar = f'<div class="sbar"><a class="btn pri" href="{wa(askmsg)}" target="_blank" rel="noopener">{ICON_WA}Подобрать по VIN</a></div>'
    body = f"""<section class="ph wrap"><h1>{e(nm)} для Li L{m} в Алматы</h1><div class="short"><p class="lbl">Коротко</p><p>{e(short)}</p></div>
<div class="btns dsk"><a class="btn pri" href="{wa(askmsg)}" target="_blank" rel="noopener">{ICON_WA}Подобрать по VIN</a></div></section>
<section class="wrap art" style="padding-top:28px">
<h2>{e(nm)} на L{m}</h2><ul class="prow">{rows}</ul>
<p class="pnote">{NOTE_PRICE}</p>
<h2>Когда менять</h2><ul class="sym">{''.join('<li>' + e(x) + '</li>' for x in p['sym'])}</ul>
<h2>Проверка и замена</h2><p>{e(p['check'])}</p>
<h2>Вопросы</h2><div class="faqh">{faq_html}</div>
{('<h2>' + e(nm) + ' для других Li</h2><div class="chips">' + others + '</div>') if others else ''}
<h2>Ещё для Li L{m}</h2><div class="chips">{more}<a href="{href(k, "modeli/li-l" + m)}">Все запчасти L{m}</a></div>
<a class="more-link" href="{href(k, "zapchasti/" + sl)}">{e(nm)} для всех Li {ICON_ARROW}</a>
</section>
{cta(k, m=m)}"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
          {"@context": "https://schema.org", "@type": "ItemList", "name": f'{nm} для Li L{m}', "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": canon(pkey(r)), "name": DATA[r][1] + f' для Li L{m}'} for i, r in enumerate(rr)]}]
    title = f'{nm} Li L{m} (Lixiang L{m}) купить в Алматы | Lixiangshop.kz'
    desc = f'{nm} для Li L{m} (Lixiang L{m}) в Алматы{(": " + ", ".join(nums[:2])) if nums else ""}. Подбор по VIN, {where}. Цена в WhatsApp.'
    if len(desc) > 160: desc = f'{nm} для Li L{m} (Lixiang L{m}) в Алматы. Подбор по VIN, {where}. Цена в WhatsApp.'
    pages[k] = layout(k, title, desc, body, crumbs=[('katalog', 'Каталог'), ('modeli/li-l' + m, 'Li L' + m), (k, nm)], ld=ld, bar=bar)

def art_parts(k, a):
    slugs = []
    for sl in re.findall(r'\[\[([a-z0-9-]+)', json.dumps(a['body'], ensure_ascii=False)):
        if sl not in slugs and any(q['slug'] == sl for q in C.PARTS): slugs.append(sl)
    if not slugs: return ''
    rows = ''
    for sl in slugs:
        q = [x for x in C.PARTS if x['slug'] == sl][0]; n = len(q['rows'])
        rows += f'<li><a href="{href(k, "zapchasti/" + sl)}"><span>{e(q["name"])}</span><small>{mlabel(models_of(q["rows"]))} · {n} {plural(n, "номер", "номера", "номеров")}</small></a></li>'
    return '<h2>Детали из статьи</h2><ul class="plist">' + rows + '</ul>'

# ---------- poleznoe
k = 'poleznoe'
body = f'''<section class="ph wrap"><h1>Полезное</h1><p class="lede">Что проверить, если на Li что-то стучит, скрипит или течёт, и как подобрать деталь.</p></section>
<section class="s wrap" style="padding-top:32px"><div class="arts big">{''.join(art_card(k, a) for a in C.ARTICLES)}</div></section>{cta(k)}'''
pages[k] = layout(k, 'Полезное о ремонте Li L6, L7, L8, L9 | Lixiangshop.kz', 'Статьи о подвеске, тормозах, охлаждении, ТО и подборе запчастей Li Auto: признаки, проверка на VibroTest и замена в Алматы.', body, crumbs=[('poleznoe', 'Полезное')])
for a in C.ARTICLES:
    k = 'poleznoe/' + a['slug']
    out = ''
    for t, v in a['body']:
        if t == 'p': out += '<p>' + links_md(k, v) + '</p>'
        elif t == 'h2': out += '<h2>' + e(v) + '</h2>'
        elif t == 'ul': out += '<ul class="sym">' + ''.join('<li>' + links_md(k, x) + '</li>' for x in v) + '</ul>'
        elif t == 'table': out += '<table class="spec"><tbody>' + ''.join('<tr><th>%s</th><td>%s</td></tr>' % (e(x), e(y)) for x, y in v) + '</tbody></table>'
    faqh = ''
    if a.get('faq'): faqh = '<h2>Вопросы</h2><div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>' for q, ans in a['faq']) + '</div>'
    body = f'''<article><section class="band">{band_pic(k, a['img'], e(a['title']))}<div class="copy wrap"><h1>{e(a['title'])}</h1></div></section>
<section class="wrap art"><p class="upd">Обновлено {UPD_RU}</p>{out}{art_parts(k, a)}{faqh}</section></article>{cta(k)}'''
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "inLanguage": "ru",
           "image": DOMAIN + '/img/' + wide(a['img']) + '.webp', "publisher": {"@id": DOMAIN + "/#store"}, "author": {"@type": "Organization", "name": "Lixiangshop.kz", "url": DOMAIN + "/"}, "datePublished": a.get('date', "2026-11-01"), "dateModified": UPD, "mainEntityOfPage": canon(k)}]
    if a.get('faq'): ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a['faq']]})
    pages[k] = layout(k, (a['title'].replace(' Li', ' Li (Lixiang)', 1) if 'Lixiang' not in a['title'] else a['title']) + ' | Lixiangshop.kz', a['desc'], body, crumbs=[('poleznoe', 'Полезное'), (k, a['title'])], ld=ld, og_img='img/' + wide(a['img']) + '.webp')

# ---------- zamena
k = 'zamena'
steps = [('Вибростенд', 'Ставим машину на вибростенд VibroTest. Он показывает состояние подвески по каждому колесу.'),
         ('Осмотр на подъёмнике', 'Поднимаем машину и смотрим узлы, на которые указал стенд: рычаги, стойки, ступицы, тормоза.'),
         ('Подбор и заказ', 'Подбираем деталь по VIN и номеру. Если её нет на складе, заранее говорим срок.'),
         ('Замена', 'Меняем на подъёмнике там же. Электронику устанавливают наши партнёры.')]
body = f'''<section class="band"><picture><source media="(min-width:760px)" srcset="{asset(k, 'img/service-desktop.webp')}"><img src="{asset(k, 'img/service-mobile.webp')}" alt="Замена детали на подъёмнике"></picture>
<div class="copy wrap"><h1>Проверка и замена на VibroTest</h1><p>Аносова 91, Алматы</p></div></section>
<section class="wrap art"><p class="lede">Lixiangshop находится в одном комплексе с VibroTest. Машину можно проверить, заказать деталь и заменить её в одном месте.</p>
<a class="rating" href="{GIS_VT}" target="_blank" rel="noopener"><b>4,8</b><span>VibroTest в 2ГИС<br>82 отзыва</span>{ICON_ARROW}</a>
<ol class="steps">{''.join('<li><b>' + e(t) + '</b><p>' + e(x) + '</p></li>' for t, x in steps)}</ol>
{near(C2.SITES)}
<h2>Что меняем на месте</h2><div class="chips">{''.join('<a href="%s">%s</a>' % (href(k, 'zapchasti/' + x), e(PART[x]['short'])) for x in ['stoyki-stabilizatora', 'perednie-rychagi', 'zadnie-rychagi', 'tormoznye-kolodki', 'tormoznye-diski', 'rulevye-nakonechniki', 'stupicy', 'privody'])}</div></section>
{cta(k, title='Записаться', text='Выберите модель и напишите, что беспокоит. Подскажем время.')}'''
pages[k] = layout(k, 'Проверка подвески и замена запчастей Li на VibroTest в Алматы | Lixiangshop.kz',
    'Проверка подвески Li на вибростенде VibroTest, осмотр на подъёмнике и замена запчастей в одном месте. Алматы, Аносова 91.', body,
    crumbs=[('zamena', 'Замена на VibroTest')], ld=[STORE, {"@context": "https://schema.org", "@type": "Service", "name": "Проверка подвески и замена запчастей Li", "serviceType": "Диагностика подвески на вибростенде и замена запчастей", "provider": {"@id": DOMAIN + "/#store"}, "areaServed": {"@type": "City", "name": "Алматы"}, "audience": {"@type": "Audience", "audienceType": "Владельцы Li L6, L7, L8, L9"}}], og_img='img/service-desktop.webp')

# ---------- kontakty
k = 'kontakty'
body = f'''<section class="ph wrap"><h1>Контакты</h1></section>
<section class="s wrap split" style="padding-top:24px"><div class="addr">Аносова 91</div><div><div class="lines"><span>Алматы, в одном комплексе с Viton и VibroTest</span><span>{HOURS}<span class="ostat" data-open></span></span><a href="tel:+77472194228">{PHONE}</a><a href="https://www.instagram.com/lixiangshop.kz/" target="_blank" rel="noopener">@lixiangshop.kz</a></div>
<div class="row2 left"><a class="btn pri" href="{wa('Здравствуйте! Пишу с сайта Lixiangshop.kz.')}" target="_blank" rel="noopener">WhatsApp</a><a class="btn sec" href="{GIS}" target="_blank" rel="noopener">2ГИС</a></div></div></section>
<section class="wrap art" id="kak-nayti" style="padding-top:64px"><h2>Как найти</h2>
<figure class="vhod"><picture><source media="(min-width:760px)" srcset="{asset(k, 'img/vhod-1600.webp')}"><img src="{asset(k, 'img/vhod-800.webp')}" width="800" height="600" alt="Вход на Аносова 91: вывески VIBROTEST.KZ, VITON и LIXIANG SHOP.KZ" loading="lazy"></picture></figure>
<ul class="sym"><li>Алматы, ул. Аносова, 91, мкр Тастак-3. Остановка «Розыбакиева» в 270 м.</li><li>Ищите синюю вывеску LIXIANG SHOP.KZ: она справа от VITON и VIBROTEST.KZ.</li><li>Заезд во двор узкий, на L8 и L9 заезжайте медленно.</li></ul>
<div class="row2 left"><a class="btn sec" href="{GIS}" target="_blank" rel="noopener">Маршрут в 2ГИС</a><a class="btn sec" href="{GMAPS}" target="_blank" rel="noopener">Google Карты</a></div></section>
<section class="wrap art" style="padding-top:64px"><h2>Кто мы</h2><p>Магазин основал Виктор Новиков, основатель Viton и VibroTest. Все три работают на одной площадке.</p>{near(C2.SITES)}</section>
<section class="wrap art" style="padding-top:64px"><h2>Написать</h2>{waform(k)}</section>'''
KFAQ = [('Вы официальный дилер Li Auto?', 'Нет. Lixiangshop.kz — независимый магазин запчастей для Li L6, L7, L8 и L9 в Алматы.'),
        ('Где поменять деталь?', 'Там же, на подъёмнике VibroTest: он в одном комплексе с магазином на Аносова 91. Электронику устанавливают наши партнёры.'),
        ('Как подобрать деталь?', 'Пришлите VIN в WhatsApp +7 747 219 42 28. Подберём по номеру детали.'),
        ('Где узнать цену и наличие?', 'Напишите в WhatsApp: менеджер назовёт цену и сверит номер по VIN.'),
        ('Подойдут ли детали к Li 2026 года?', 'В 2026 году вышли обновлённые L6, L8 и L9. Чтобы деталь точно подошла, подбираем по VIN.'),
        ('Во сколько вы работаете?', 'Каждый день с 09:30 до 19:00, без выходных.'),
        ('Как вас найти?', 'Алматы, ул. Аносова, 91, в одном комплексе с Viton и VibroTest. Остановка «Розыбакиева» в 270 м. Ищите синюю вывеску LIXIANG SHOP.KZ.'),
        ('Кто владелец магазина?', 'Магазин основал Виктор Новиков, он же основатель Viton и VibroTest. Магазин оформлен на ИП Новиков.')]
body += '<section class="wrap art" style="padding-top:64px"><h2>Вопросы</h2><div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in KFAQ) + '</div></section>'
body += f'''<section class="wrap art" style="padding-top:64px"><h2>Отзыв</h2><p>Покупали у нас или меняли деталь? Расскажите в 2ГИС, как всё прошло.</p><a class="btn sec" href="{GIS_REV}" target="_blank" rel="noopener">Оставить отзыв в 2ГИС</a></section>'''
pages[k] = layout(k, 'Контакты Lixiangshop.kz: Алматы, Аносова 91', 'Магазин запчастей для Li в Алматы: Аносова 91, ежедневно 09:30–19:00, +7 747 219 42 28, WhatsApp. Как найти и где оставить отзыв.', body, crumbs=[('kontakty', 'Контакты')], ld=[STORE, {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in KFAQ]}])

# ---------- privacy
k = 'privacy'
PRIV = [
 ('1. Общие положения', ['Эта политика описывает, как обрабатываются персональные данные посетителей сайта lixiangshop.kz и покупателей магазина Lixiangshop.kz. Она составлена в соответствии с Законом Республики Казахстан от 21 мая 2013 года № 94-V «О персональных данных и их защите».',
   'Оператор персональных данных: индивидуальный предприниматель Новиков, ИИН 020317501018, адрес: г. Алматы, ул. Аносова, 91, телефон +7 747 219 42 28.']),
 ('2. Какие данные мы получаем', [['Имя и номер телефона, когда вы пишете нам в WhatsApp или звоните.',
   'Сведения об автомобиле: модель, год выпуска, VIN, нужную деталь или описание неисправности, если вы их сообщаете.',
   'Технические данные: IP-адрес, тип браузера и устройства, страницы сайта, которые вы посетили, и файлы cookie, если на сайте работают сервисы веб-аналитики.'],
   'Форма на сайте не отправляет данные на сервер. Она только собирает текст сообщения и открывает WhatsApp. Данные мы получаем, когда вы сами отправите это сообщение.',
   'Выбранная модель Li запоминается в памяти вашего браузера, чтобы показывать подходящие детали. Она остаётся на вашем устройстве и нам не передаётся.',
   'Мы не запрашиваем данные удостоверения личности, банковских карт и другие сведения, которые не нужны для подбора и продажи запчастей.']),
 ('3. Зачем мы это делаем', [['Ответить на вопрос, подобрать деталь по VIN, сообщить цену и наличие.', 'Оформить заказ и записать на замену детали.', 'Понимать, какие страницы сайта полезны, и улучшать его.']]),
 ('4. Согласие на обработку', ['Отправляя сообщение в WhatsApp, в том числе собранное формой на сайте, или сообщая данные по телефону, вы даёте согласие на их сбор и обработку для целей из раздела 3. Согласие действует до достижения этих целей или до его отзыва.']),
 ('5. Где и сколько хранятся данные', ['Данные хранятся на территории Республики Казахстан. Мы храним их, пока это нужно для заказа и гарантийных обязательств, но не дольше 3 лет с последнего обращения, если более долгий срок не требует закон. После этого данные удаляются.']),
 ('6. Кому мы передаём данные', ['Мы не продаём и не передаём ваши данные третьим лицам, кроме случаев, предусмотренных законодательством Республики Казахстан. Если вы заказываете установку электроники у наших партнёров, мы передаём им модель автомобиля и описание задачи с вашего согласия.',
   'Если вы пишете нам в WhatsApp, переписка также обрабатывается этим мессенджером по его собственным правилам. Карты 2ГИС и Google открываются на их сайтах и работают по их правилам.']),
 ('7. Как мы защищаем данные', ['Доступ к данным есть только у сотрудников, которым они нужны для работы. Сайт работает по защищённому протоколу HTTPS. Мы принимаем организационные и технические меры против утраты, изменения и несанкционированного доступа к данным.']),
 ('8. Файлы cookie', ['Сайт может использовать файлы cookie, чтобы корректно работать и собирать обезличенную статистику посещений через Яндекс Метрику (включая запись действий на странице, Вебвизор). Вы можете отключить cookie в настройках браузера: сайт продолжит работать.']),
 ('9. Ваши права', [['Узнать, какие ваши данные у нас есть и как они используются.', 'Потребовать исправить, заблокировать или удалить данные.', 'Отозвать согласие на обработку.', 'Обжаловать наши действия в уполномоченном органе по защите персональных данных или в суде.'],
   'Чтобы воспользоваться этими правами, напишите или позвоните нам по номеру +7 747 219 42 28. Мы ответим в сроки, установленные законом.']),
 ('10. Изменения политики', ['Мы можем обновлять эту политику. Новая редакция действует с момента публикации на этой странице. Дата текущей редакции указана в начале документа.'])]
def _pblock(x): return ('<ul class="sym">' + ''.join('<li>' + e(i) + '</li>' for i in x) + '</ul>') if isinstance(x, list) else '<p>' + e(x) + '</p>'
body = '<section class="ph wrap"><h1>Политика обработки персональных данных</h1><p class="lede">Как ИП Новиков собирает, хранит и защищает данные посетителей сайта и покупателей Lixiangshop.kz.</p></section><section class="wrap art" style="padding-top:28px"><p class="upd">Редакция от 02.11.2026</p>' + \
       ''.join('<h2>' + e(h) + '</h2>' + ''.join(_pblock(x) for x in xs) for h, xs in PRIV) + '</section>'
pages[k] = layout(k, 'Политика обработки персональных данных | Lixiangshop.kz', 'Как ИП Новиков обрабатывает и защищает персональные данные посетителей сайта и покупателей Lixiangshop.kz.', body, crumbs=[('privacy', 'Политика данных')])

# ---------- 404
k = 'index'
nf = layout(k, 'Страница не найдена | Lixiangshop.kz', 'Такой страницы нет. Каталог запчастей для Li L6, L7, L8, L9 и подбор по VIN в WhatsApp.',
    f'''<section class="ph wrap nf"><p class="code">404</p><h1>Такой страницы нет</h1><p class="lede">Возможно, адрес изменился. Найдите деталь в каталоге или напишите нам.</p>
<div class="btns"><a class="btn pri" href="{href(k, 'katalog')}">Каталог</a><a class="btn sec" href="{href(k, 'index')}">Главная</a></div></section>
{cta(k, title='Подберём по VIN')}''')
nf = nf.replace('<link rel="canonical" href="%s">' % canon('index'), '<meta name="robots" content="noindex">')
if MODE == 'deploy': nf = re.sub(r'(href|src)="(?!/|https?:|#|tel:|data:)', r'\1="/', nf)

# ---------- write
if os.path.exists(OUT): shutil.rmtree(OUT)
for key, h in pages.items():
    path = os.path.join(OUT, 'index.html' if key == 'index' else (key + '/index.html' if MODE == 'deploy' else key + '.html'))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(h)
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
for f in ['site.css', 'site.js']: shutil.copy(os.path.join(HERE, f), os.path.join(OUT, 'assets', f))
shutil.copytree(os.path.join(HERE, 'fonts'), os.path.join(OUT, 'assets', 'fonts'))
for f in glob.glob(os.path.join(HERE, 'icons', '*')): shutil.copy(f, OUT)
for f in glob.glob(os.path.join(HERE, 'brand', '*')): shutil.copy(f, os.path.join(OUT, 'assets'))
open(os.path.join(OUT, '404.html'), 'w').write(nf)
open(os.path.join(OUT, 'site.webmanifest'), 'w').write(json.dumps({"name": "Lixiangshop.kz", "short_name": "Lixiangshop", "lang": "ru",
    "start_url": "/", "display": "minimal-ui", "background_color": "#0a0b0d", "theme_color": "#0a0b0d",
    "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, ensure_ascii=False, indent=1))
shutil.copytree(os.path.join(HERE, 'img-base'), os.path.join(OUT, 'img'))
if os.path.isdir(os.path.join(HERE, 'pimg')): shutil.copytree(os.path.join(HERE, 'pimg'), os.path.join(OUT, 'img', 'p'))
for f in glob.glob(os.path.join(HERE, 'img-parts', '*.webp')) + glob.glob(os.path.join(HERE, 'img-cars', '*.webp')) + glob.glob(os.path.join(HERE, 'photos', '*.webp')): shutil.copy(f, os.path.join(OUT, 'img'))
if MODE == 'deploy':
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (canon(k), UPD) for k in pages) + '</urlset>\n')
    open(os.path.join(OUT, '.htaccess'), 'w').write('ErrorDocument 404 /404.html\nDirectoryIndex index.html\nAddType application/manifest+json .webmanifest\nAddType font/woff2 .woff2\n<IfModule mod_headers.c>\n  <FilesMatch "\\.(webp|png|jpg|ico|woff2)$">\n    Header set Cache-Control "public, max-age=604800"\n  </FilesMatch>\n</IfModule>\n')
    open(os.path.join(OUT, 'e864aec0b98bbd3f6b2ffc80e169086f.txt'), 'w').write('e864aec0b98bbd3f6b2ffc80e169086f')  # IndexNow key (Bing, Yandex): tools/indexnow.py
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % DOMAIN)
L = ['# Lixiangshop.kz', '', '> Независимый магазин запчастей для Li Auto L6, L7, L8, L9 в Алматы. Не является официальным дилером Li Auto.', '',
     '- Адрес: Алматы, ул. Аносова, 91 (один комплекс с Viton и VibroTest)', '- Часы: ежедневно 09:30–19:00, без выходных', '- Как найти: остановка «Розыбакиева» в 270 м, синяя вывеска LIXIANG SHOP.KZ рядом с VITON и VIBROTEST.KZ', '- Основатель: Виктор Новиков (также основатель Viton и VibroTest). Продавец: ИП Новиков', '- Отзывы: ' + GIS_REV,
     '- Рядом на той же площадке: Viton (https://viton.kz/ru/), чистка форсунок и диагностика двигателя; VibroTest (https://vibrotest.kz/ru/), диагностика ходовой на вибростенде', '- Телефон и WhatsApp: ' + PHONE, '- Instagram: https://www.instagram.com/lixiangshop.kz/',
     '- Цену называет менеджер в WhatsApp. Подбор по VIN.', '- Проверка подвески на вибростенде VibroTest и замена механики на подъёмнике на месте. Электронику устанавливают партнёры.', '',
     '## Разделы', '- [Каталог](%s): %d позиций' % (canon('katalog'), len(DATA))] + ['- [%s](%s)' % (x['name'], canon('katalog/' + x['slug'])) for x in C.SYSTEMS] + \
    ['', '## Товары'] + ['- [%s для Li%s%s](%s)' % (DATA[r][1], (' ' + mlabel(list(DATA[r][2]))) if DATA[r][2] else '', (', ' + DATA[r][3]) if DATA[r][3] else '', canon(pkey(r))) for p in C.PARTS for r in p['rows']] + \
    ['', '## Модели'] + ['- [Запчасти для Li L%s](%s)' % (m, canon('modeli/li-l' + m)) for m in MOD] + \
    ['- [%s для Li L%s](%s)' % (PART[sl]['name'], m, canon('modeli/li-l' + m + '/' + sl)) for (m, sl) in MP] + \
    ['', '## Полезное'] + ['- [%s](%s): %s' % (a['title'], canon('poleznoe/' + a['slug']), a['desc']) for a in C.ARTICLES] + \
    ['', '## Сервис', '- [Проверка и замена на VibroTest](%s)' % canon('zamena'), '- [Контакты](%s)' % canon('kontakty'), '- [Политика данных](%s)' % canon('privacy')]
open(os.path.join(OUT, 'llms.txt'), 'w').write('\n'.join(L) + '\n')
# width/height on images (layout stability)
from PIL import Image as _Im
_dim = {}
def _wh(src, page):
    src = src.split('?')[0]
    f = os.path.join(OUT, src.lstrip('/')) if src.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(page), src))
    if f not in _dim:
        try: _dim[f] = _Im.open(f).size
        except Exception: _dim[f] = None
    return _dim[f]
for d_, _, fs_ in os.walk(OUT):
    for f_ in fs_:
        if not f_.endswith('.html'): continue
        pth = os.path.join(d_, f_); h = open(pth).read()
        def _fix(m):
            tag = m.group(0)
            if ' width=' in tag: return tag
            sm = re.search(r'src="([^"]+)"', tag)
            if not sm or sm.group(1).startswith('data:'): return tag
            wh = _wh(sm.group(1), pth)
            return tag if not wh else tag[:-1] + f' width="{wh[0]}" height="{wh[1]}">'
        h2 = re.sub(r'<img\b[^>]*>', _fix, h)
        if h2 != h: open(pth, 'w').write(h2)
print(len(pages), 'pages ->', OUT)
