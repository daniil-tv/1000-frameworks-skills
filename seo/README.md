# Централизованный сбор семантики 1000 Frameworks

Этот каталог живёт в GitHub рядом с AI Skills. `seo/pages.json` — реестр страниц и стартовых фраз. Ручной запуск GitHub Actions сохраняет для каждой страницы:

- `seo/data/<page-id>/wordstat.json` — исходные ответы Wordstat и параметры сбора;
- `seo/data/<page-id>/semantics.json` — все уникальные запросы, частотность, предварительный тип интента и поля для редакционной проверки;
- `seo/data/<page-id>/README.md` — читаемая таблица первых 100 запросов.

Данные публичны в репозитории. API-ключ хранится **только** в GitHub Actions Secrets и никогда не попадает в коммиты.

## Настройка один раз

1. Откройте **Settings → Secrets and variables → Actions → New repository secret**.
2. Добавьте `YANDEX_CLOUD_API_KEY` и `YANDEX_CLOUD_FOLDER_ID`.
3. Убедитесь, что для сервисного аккаунта включена роль `search-api.webSearch.user`, а у ключа область `yc.search-api.execute`.
4. В **Settings → Actions → General → Workflow permissions** разрешите **Read and write permissions**, чтобы workflow сохранял результаты в репозитории.

## Сбор

Откройте **Actions → Collect Wordstat semantics → Run workflow**. Укажите `page_id` из `seo/pages.json` либо `all`, регион `225` для России или пустое значение для всех регионов. Сначала запустите `jtbd` и проверьте результат; `all` потребует больше API-запросов.

Чтобы добавить страницу, внесите её URL, название и 1–8 исходных фраз в `seo/pages.json`, затем запустите workflow с её ID. Не добавляйте ключи API в этот файл.

Частотность и группировка Wordstat не доказывают релевантность или сложность ранжирования. Тип интента в `semantics.json` — предварительная эвристика; поле `review` остаётся `pending`, пока редактор не проверит выдачу, шум, каннибализацию и место запроса на странице. Сбор не меняет HTML сайта автоматически.

В другом чате ChatGPT подключите этот GitHub-репозиторий и попросите прочитать `seo/pages.json` и `seo/data/<page-id>/semantics.json`. Новые результаты находятся в GitHub, а не на компьютере, где запущен Codex.

API: [Yandex Wordstat GetTop](https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop).
