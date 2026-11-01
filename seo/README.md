# Централизованный сбор семантики 1000 Frameworks

Этот каталог живёт в GitHub рядом с AI Skills. `seo/pages.json` — реестр страниц и стартовых фраз. Сбор запускает **точные копии** существующих локальных модулей `src/wordstat.py`, `src/cluster_keywords.py` и `src/analyze_intent.py`, без изменения их SEO-логики. Ручной запуск GitHub Actions сохраняет для выбранной страницы:

- `seo/data/<page-id>/wordstat.json` — исходные ответы Wordstat и параметры сбора;
- `seo/data/<page-id>/keywords.json` — кластеры, вопросы, исключённые запросы и частотности по существующему алгоритму;
- `seo/data/<page-id>/intent.json` — предварительный поисковый интент по существующему алгоритму;
- `seo/data/<page-id>/manifest.json` — URL, регион, исходные фразы и дата сбора;
- `seo/data/<page-id>/README.md` — читаемая таблица первых 100 запросов.

Репозиторий предназначен для приватного использования владельцем. API-ключ хранится **только** в GitHub Actions Secrets и никогда не попадает в коммиты, Issues, логи или результаты.

## Настройка один раз

1. Откройте **Settings → Secrets and variables → Actions → New repository secret**.
2. Добавьте `YANDEX_CLOUD_API_KEY` и `YANDEX_CLOUD_FOLDER_ID`.
3. Убедитесь, что для сервисного аккаунта включена роль `search-api.webSearch.user`, а у ключа область `yc.search-api.execute`.
4. В **Settings → Actions → General → Workflow permissions** разрешите **Read and write permissions**, чтобы workflow сохранял результаты в репозитории.

## Сбор

Откройте **Actions → Collect Wordstat semantics → Run workflow**. Укажите `page_id` из `seo/pages.json`, например `odi`; регион `225` для России или пустое значение для всех регионов. Один запуск собирает одну тему и расходует API-запросы для её исходных фраз.

Чтобы добавить страницу, внесите её URL, название и 1–8 исходных фраз в `seo/pages.json`, затем запустите workflow с её ID. Не добавляйте ключи API в этот файл.

Частотность и группировка Wordstat не доказывают релевантность или сложность ранжирования. `keywords.json` и `intent.json` содержат предварительные результаты существующих алгоритмов; `manifest.json` сохраняет редакционный статус `needs_review`, пока редактор не проверит выдачу, шум, каннибализацию и место запроса на странице. Сбор не меняет HTML сайта автоматически.

## Запуск из любого чата GPT

Подключите GitHub к чату и дайте ему доступ к приватному репозиторию. Для запуска GPT должен создать Issue в `daniil-tv/1000-frameworks-skills`:

- заголовок: `[semantics] <page-id>`, например `[semantics] odi`;
- тело: `region: 225`.

Workflow принимает такие заявки только от владельца репозитория, запускает Wordstat, сохраняет результат в `seo/data/<page-id>/`, оставляет ссылку на запуск и закрывает Issue. После завершения попросите GPT прочитать `keywords.json`, `intent.json` и `manifest.json`. API-ключ чату не передаётся.

Новые результаты находятся в GitHub, а не на компьютере, где запущен Codex.

API: [Yandex Wordstat GetTop](https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop).
