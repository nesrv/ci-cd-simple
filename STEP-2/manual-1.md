# Практическое занятие
## Изучение CI/CD

## Часть 2 Continius Delivery (CD)

## Цели

- Объяснить процесс деплоя
- Дать практические задания для закрепления знаний.

## Цели методички

- ...
- Объяснить ...
- Дать практические задания для закрепления знаний.

## Структура проекта (корневая)

- `main.py` — основное FastAPI приложение
- `shop.json` — данные товаров
- `requirements.txt` — зависимости (fastapi, uvicorn, pydantic, pytest, httpx, black)
- `railway.json` — конфиг Railway (команда запуска, билдер)
- `test_main.py` — тесты (pytest)
- `.github/workflows/deploy.yml` — CI/CD: тесты + деплой на Railway (отдельного `ci.yml` нет)


## Деплой на Railway

Railway — это платформа для деплоя приложений прямо с GitHub (простой и бесплатный вариант для учебных проектов).

### Шаг 0: Как Railway узнаёт, как запускать приложение

**Вариант A — Procfile.** Создайте файл `Procfile` в корне (без расширения):

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Вариант B — railway.json (используется в текущем проекте).** В корне есть `railway.json` с полем `deploy.startCommand`:

```json
"startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

В обоих случаях `$PORT` — переменная окружения, которую Railway выделяет приложению.

### Шаг 1: Создать аккаунт на Railway

1. Перейдите на [railway.app](https://railway.app)
2. Нажмите `Start New Project`
3. Выберите `Deploy from GitHub Repo`
4. Авторизуйте GitHub (дайте Railway доступ к вашим репозиториям)

### Шаг 2: Выбрать репозиторий и ветку

1. Выберите свой репозиторий `name_repo`
2. Выберите ветку `main`
3. Railway автоматически обнаружит что это Python проект

### Шаг 3: Добавить requirements.txt (важно!)

Railway нужно знать, какие зависимости установить. В текущем проекте в корне уже есть `requirements.txt`, например:

```
fastapi==0.110.0
uvicorn==0.28.0
pydantic==2.8.0
pytest==7.4.4
httpx==0.25.2
black==24.10.0
```

### Шаг 4: Добавить переменные окружения (опционально)

На странице проекта в Railway:

- Нажмите `Variables`
- Добавьте переменные (если нужны, например для логирования)

### Шаг 5: Дождитесь деплоя

1. Railway автоматически запустит деплой
2. Включит ваше приложение на публичный URL
3. Вы увидите что-то вроде: `https://your-app-xxxx.railway.app`

### Проверка

После деплоя приложение будет доступно по URL:

```
https://your-app-xxxx.railway.app/health
```

А документация (Swagger UI):

```
https://your-app-xxxx.railway.app/docs
```

### Автоматический деплой

После первого деплоя: каждый пуш в `main` автоматически обновит приложение на Railway!

### Деплой через GitHub Actions (как в текущем проекте)

В проекте используется `.github/workflows/deploy.yml`: сначала запускаются тесты, затем деплой через Railway CLI.

**Содержимое workflow (актуально для проекта):**

- **Job `test`:** checkout → Python 3.13 → установка зависимостей → `pytest -v test_main.py`.
- **Job `deploy`:** зависит от `test`, ставит Node.js → устанавливает `@railway/cli` → выполняет `railway up --service <имя_сервиса>`.

Пример шага деплоя:

```yaml
- name: Deploy to Railway
  run: |
    railway up --service ${{ secrets.RAILWAY_SERVICE || 'web' }}
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

**Секреты в GitHub (Settings → Secrets and variables → Actions):**

1. **RAILWAY_TOKEN** (обязательно) — токен с Railway: Settings → Tokens → Create Token.
2. **RAILWAY_SERVICE** (необязательно) — имя сервиса в проекте Railway. Если не задан, подставляется `web` (как при выборе сервиса в `railway link`).

**Важно:** у команды `railway up` обязательно должен быть аргумент `--service <SERVICE>`. Имя сервиса (например `web`) выбирается при `railway link` в консоли; проект (project) и сервис (service) в Railway — разные сущности.

---

## Советы и замечания

- В текущем учебном проекте корзина и заказы хранятся в памяти — данные теряются при перезапуске.
- Для продакшена используйте базу данных и хранение секретов через `GH Secrets` или переменные окружения.
- ID товаров — индекс в `shop.json` (начинается с 0).

---

## Корректировки для текущего проекта

В этой методичке учтены отличия репозитория **CI-CD-SIMPLE**:

| В методичке (общее) | В текущем проекте |
|---------------------|-------------------|
| Отдельный CI workflow (`ci.yml`) | Единый `deploy.yml`: job **test** (pytest) + job **deploy** (Railway CLI). Отдельного `ci.yml` нет. |
| Запуск через Procfile | Запуск задаётся в `railway.json` (`deploy.startCommand`: uvicorn). Procfile не используется. |
| Деплой через `railwayapp/deploy-action` | Деплой через **Railway CLI**: `npm install -g @railway/cli`, затем `railway up --service …`. |
| Только RAILWAY_TOKEN в секретах | **RAILWAY_TOKEN** обязателен; **RAILWAY_SERVICE** опционален (по умолчанию `web`). Без `--service` деплой падает с ошибкой «a value is required for '--service'». |
| Проект = имя приложения | **Проект** (project) в Railway — например `luminous-curiosity`. **Сервис** (service) внутри проекта — например `web`. В `railway up` указывается имя **сервиса**. |

**Проверка перед деплоем:** в GitHub Actions перед деплоем запускаются тесты (`pytest -v test_main.py`). Для прохождения пайплайна код должен проходить тесты и (при использовании black в CI) соответствовать форматированию black.

---

3. Перенесите хранение корзины в файл или простую базу данных (например SQLite).
4. Добавьте логирование в приложение.

Если хотите, я могу расширить методичку: добавить раздел с примерами тестов (`pytest`), `requirements.txt`, и дополнить CI шагами для тестов и линтинга.

### Как это происходит (кратко)

- **Триггер:** пуш в ветку `main` или открытие/обновление Pull Request в `main` запускает workflow.
- **Шаги в CI:**
  - `actions/checkout` — получает код репозитория.
  - `actions/setup-python` — устанавливает Python 3.13.
  - Установка зависимостей через `pip` (FastAPI, Pydantic, Uvicorn).
  - `python -m py_compile main.py` — быстрая проверка синтаксиса.
  - `python -c "import main"` — пробный импорт модуля, чтобы убедиться, что импорт не падает.
- **Где смотреть результаты:** Зайди в вкладку `Actions` на GitHub, выбери workflow `CI` и открой последний запуск — там логи по каждому шагу.
- **Артефакты:** В минимальном варианте артефактов нет; можно добавить шаги для сохранения логов/результатов тестов при необходимости.


