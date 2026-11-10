# Lixiangshop.kz

Статический сайт магазина запчастей для Li Auto L6, L7, L8, L9 в Алматы. Сервера и базы нет, только HTML, CSS и картинки.

## Что где лежит

- `site/` готовый сайт. Его и публикует хостинг.
- `src/` исходники, из которых собирается `site/`:
  - `build.py` сборщик страниц;
  - `content.py`, `content2.py`, `content3.py` тексты разделов, статей и моделей;
  - `data/cat.json` каталог (название, модели, OEM), `data/satu-prices.json` цены, `data/satu-parsed.json` описания;
  - `site.css`, `site.js`, `fonts/`, `icons/`, картинки в `img-base/`, `img-parts/`, `img-cars/`, `photos/`, `pimg/` (фото товаров, файл = номер строки каталога).
- `vercel.json` настройки для Vercel: отдавать папку `site/`, кэш картинок, запрет индексации на адресах `*.vercel.app`.

## Публикация на Vercel

1. vercel.com → Add New → Project → Import репозитория `lixiangshopkz`.
2. Framework Preset: Other. Build Command и Install Command оставить пустыми, всё уже задано в `vercel.json`.
3. Deploy. Дальше каждый push в `main` публикуется сам.

## Домен lixiangshop.kz

1. В проекте Vercel: Settings → Domains → добавить `lixiangshop.kz` и `www.lixiangshop.kz` (www поставить редиректом на основной).
2. У регистратора домена (ps.kz, hoster.kz и т. п.) в DNS прописать:
   - `A` для `@` → `76.76.21.21`
   - `CNAME` для `www` → `cname.vercel-dns.com`
   Если Vercel в Domains покажет другие значения, берите их.
3. Через 15–60 минут Vercel сам выпустит HTTPS-сертификат.
4. После этого добавить сайт в Google Search Console и Яндекс Вебмастер и отправить `https://lixiangshop.kz/sitemap.xml`.

## Как сайт опубликован сейчас

Хостинг PS.kz (Plesk), подписка viton.kz, домен lixiangshop.kz.

- Plesk → Git: репозиторий `https://github.com/theonlyalibek/lixiangshopkz.git`, ветка `main`, автоматическое развёртывание в `/lixiangshop.kz`.
- На GitHub стоит вебхук Plesk, поэтому каждый push в `main` сразу выкладывается на сервер.
- Корневая папка домена: `lixiangshop.kz/site`. Наружу видна только папка `site/`, исходники из `src/` закрыты.
- SSL: Let's Encrypt на lixiangshop.kz и www, продлевается сам. www перенаправляет на lixiangshop.kz.
- `site/.htaccess` отдаёт страницу 404 и типы файлов.

Если репозиторий станет приватным, в Plesk нужно перейти на SSH-адрес `git@github.com:theonlyalibek/lixiangshopkz.git` и добавить ключ из Plesk в Settings → Deploy keys.

## Цены и товары из Rosta

Каталог сверен с учётной системой Rosta (группа «Lixiangshop.kz»). Связь строк каталога с товарами Rosta лежит в `src/data/rosta-map.json`, цены сайта в `src/data/prices.json`.

Обновить цены:

```
set ROSTA_KEY=ключ_из_Rosta
python src/tools/rosta_pull.py C:\путь\вне\репозитория\rosta.json
python src/tools/rosta_prices.py C:\путь\вне\репозитория\rosta.json
python src/build.py
```

Потом commit и push. Ключ и выгрузку из Rosta в репозиторий не кладите: там остатки и внутренние данные. Наличие на сайте не показывается.

## Как менять сайт

Нужен Python 3 и Pillow (`pip install pillow`).

```
python src/build.py
```

Команда пересобирает `site/` целиком. Затем commit и push, Vercel опубликует сам.

- Цена товара: `src/data/prices.json`, по порядку строк каталога, обновляется из Rosta. `0` значит «по запросу».
- Новый товар: строка в `src/data/cat.json` (`[раздел, название, модели, OEM]`) и номер строки в `rows` нужной детали в `content.py` или `content3.py`. Фото кладите в `src/pimg/<номер строки>.webp`.
- Тексты страниц деталей и статей: `content.py`.

Цены показываются только на страницах товаров и в корзине. Сайт не называет себя официальным дилером Li Auto.

## IndexNow

После каждого пуша с изменениями в `site/` GitHub Actions (`.github/workflows/indexnow.yml`) ждёт деплой и отправляет изменённые страницы в IndexNow (Bing, Яндекс). Отправить весь sitemap вручную: Actions → IndexNow → Run workflow → «Отправить все страницы».
