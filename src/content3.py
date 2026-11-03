# Items added from the owner's full catalog (xlsx, 3 Nov 2026)
import json, os
_N = json.load(open(os.path.join(os.path.dirname(__file__), 'new-rows.json')))
NEW_PARTS = [
 {"slug": "fary", "sys": "elektronika", "name": "Фары: корпус и стекло", "short": "Фары",
  "sym": ["Трещина или скол на стекле фары", "Фара запотевает изнутри", "Сломаны крепления корпуса после удара"],
  "check": "Пришлите фото фары и VIN в WhatsApp. Подберём корпус или стекло по номеру, установку проведут наши партнёры.",
  "note": "У L7 две версии фар: старая и новая. Версию подтверждаем по VIN.", "faq": []},
 {"slug": "parktroniki", "sys": "elektronika", "name": "Парктроники", "short": "Парктроники",
  "sym": ["Ошибка парковочных датчиков на панели", "Сигнал без препятствия", "Датчик не работает после удара или мойки"],
  "check": "Пришлите фото ошибки и VIN в WhatsApp. Подберём датчик по номеру, установку проведут наши партнёры.", "note": "", "faq": []},
 {"slug": "datchiki-davleniya-shin", "sys": "elektronika", "name": "Датчики давления в шинах", "short": "Датчики шин",
  "sym": ["Ошибка давления в шинах на панели", "Не показывается давление одного колеса", "Датчик повреждён при шиномонтаже"],
  "check": "Пришлите фото ошибки и VIN в WhatsApp. Подберём датчик по номеру, установку проведут наши партнёры.", "note": "", "faq": []},
 {"slug": "svechi-zazhiganiya", "sys": "dvigatel", "name": "Свечи зажигания", "short": "Свечи",
  "sym": ["Пропуски зажигания", "Двигатель-генератор работает неровно", "Подошёл срок замены по ТО"],
  "check": "Подберём свечи по VIN и заменим на подъёмнике VibroTest, можно вместе с ТО.", "note": "", "faq": []},
 {"slug": "klapannaya-kryshka", "sys": "dvigatel", "name": "Клапанная крышка", "short": "Клапанная крышка",
  "sym": ["Течь масла по крышке", "Трещина на корпусе крышки", "Запах масла под капотом"],
  "check": "Осматриваем двигатель на подъёмнике, проверяем крышку и прокладку. Подберём по VIN и заменим на месте.", "note": "", "faq": []},
]
def apply(C):
    by = {p['slug']: p for p in C.PARTS}
    for np in NEW_PARTS:
        if np['slug'] in by: continue
        np = dict(np, rows=[])
        last = max(i for i, p in enumerate(C.PARTS) if p['sys'] == np['sys'])
        C.PARTS.insert(last + 1, np); by[np['slug']] = np
    for slug, rows in _N['add'].items():
        for r in rows:
            if r not in by[slug]['rows']: by[slug]['rows'].append(r)
    cam = by.get('perednyaya-kamera')
    if cam: cam.update(name='Передние камеры', short='Камеры', note='')
