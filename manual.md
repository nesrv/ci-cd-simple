manual.md

# Методичка: E-Shop FastAPI (минималистичный учебный проект)

## Цели методички
- Пошагово объяснить, как подготовить окружение и запустить `main.py` локально.
- Показать базовую структуру API и примеры вызовов.
- Объяснить минимальный CI (GitHub Actions) и как он запускается.
- Дать практические задания для закрепления знаний.

## Требования
- Python 3.13+
- Git (для работы с репозиторием и CI)
- Рекомендуется виртуальное окружение

## Структура проекта (корневая)
- `main.py` — основное FastAPI приложение
- `agents.py` — альтернативная копия (удобно для экспериментов)
- `shop.json` — данные товаров
- `.github/workflows/ci.yml` — минимальный CI workflow
- `README.md`, `manual.md` — документация

---

## Быстрая установка (локально)
1. Клонируйте репозиторий и перейдите в папку:

```bash
git clone <repo-url>
cd CI-CD-SIMPLE
```

2. Создайте и активируйте виртуальное окружение:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```bash
python -m pip install --upgrade pip
pip install fastapi uvicorn pydantic
```

---

## Запуск приложения
Для разработки с авто-перезагрузкой:

```bash
uvicorn main:app --reload
```

После запуска приложение доступно по адресу: `http://localhost:8000`.
Интерактивная документация: `http://localhost:8000/docs`.

---

## Короткое описание API (минимум)
- `GET /products` — получить список всех товаров
- `GET /product/{id}` — получить товар по ID (ID начинается с 0)
- `GET /search?q=...` — поиск по названию
- `GET /cart` — просмотр корзины (items + total)
- `POST /cart/add?pid={id}&qty={n}` — добавить в корзину
- `DELETE /cart` — очистить корзину
- `POST /checkout` — оформить заказ (из текущей корзины)
- `GET /orders` — список заказов
- `GET /health` — проверка состояния приложения

Примеры curl:

```bash
# Все товары
curl http://localhost:8000/products

# Поиск
curl "http://localhost:8000/search?q=RTX"

# Добавить в корзину
curl -X POST "http://localhost:8000/cart/add?pid=0&qty=2"

# Оформить заказ
curl -X POST http://localhost:8000/checkout
```

---



## Минимальный CI (GitHub Actions)
Файл workflow расположен в `.github/workflows/ci.yml`. Его задача — быстро проверить, что `main.py` не содержит синтаксических ошибок и успешно импортируется.

Триггеры:
- пуш в ветку `main`
- Pull Request в `main`

Основные шаги workflow:
1. `actions/checkout` — получить код репозитория.
2. `actions/setup-python` (Python 3.13).
3. Установка зависимостей (`pip install fastapi pydantic uvicorn`).
4. `python -m py_compile main.py` — проверка синтаксиса.
5. `python -c \"import main\"` — пробный импорт модуля.

Где смотреть прогон: вкладка `Actions` в GitHub → выбрать workflow `CI` → посмотреть логи.

Локальная проверка тех же шагов:

```bash
python -m pip install --upgrade pip
pip install fastapi pydantic uvicorn
python -m py_compile main.py
python -c "import main; print('imported OK')"
```

**Важно:** Если workflow запускается дважды на один пуш, причина — в `.github/workflows/ci.yml` указаны оба триггера (`push` и `pull_request`). Оставляем только `push`:

```yaml
on:
  push:
    branches: [ main ]
```

Это исключит дублирование для учебного проекта.

---

## Примеры ошибок для обучения (тестирование workflow)

Чтобы убедиться, что CI работает и ловит ошибки, можно специально добавить ошибку в `main.py`, запушить и посмотреть, как workflow её ловит.

### Пример 1: Синтаксическая ошибка

Откройте `main.py` и добавьте ошибку (например, забудьте закрыть скобку):

```python
@app.get("/products")
async def get_products() -> list[dict]
    return PRODUCTS  # Пропущена двоеточие выше
```

При пуше workflow выполнит `python -m py_compile main.py` и вернёт ошибку:
```
SyntaxError: invalid syntax
```

Посмотреть в: вкладка `Actions` → workflow `CI` → log с красной ошибкой.

### Пример 2: Ошибка импорта

Добавьте неправильный импорт в начало `main.py`:

```python
from nonexistent_module import something  # Этого модуля не существует
```

Workflow выполнит `python -c "import main"` и упадёт:
```
ModuleNotFoundError: No module named 'nonexistent_module'
```

### Пример 3: Проверка зависимостей

Если удалить `fastapi` из `pip install`, workflow понимает, что импорт невозможен:
```
ModuleNotFoundError: No module named 'fastapi'
```

### Как исправить после ошибки
1. Исправьте ошибку в коде локально.
2. Проверьте локально: `python -m py_compile main.py` и `python -c "import main"`.
3. Запушьте исправленный код.
4. Workflow снова запустится и должен пройти успешно (зелёная галочка).

---

## Деплой на Railway

Railway — это платформа для деплоя приложений прямо с GitHub (простой и бесплатный вариант для учебных проектов).

### Шаг 1: Создать аккаунт на Railway
1. Перейдите на [railway.app](https://railway.app)
2. Нажмите `Start New Project`
3. Выберите `Deploy from GitHub Repo`
4. Авторизуйте GitHub (дайте Railway доступ к вашим репозиториям)

### Шаг 2: Выбрать репозиторий и ветку
1. Выберите репозиторий `ci-cd-simple`
2. Выберите ветку `main`
3. Railway автоматически обнаружит что это Python проект

### Шаг 3: Добавить requirements.txt (важно!)
Railway нужно знать, какие зависимости установить. Создайте файл `requirements.txt` в корне:

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.6.0
```

**Важно:** используйте **новые версии** пакетов, совместимые с Python 3.13! Старые версии (например pydantic<2.6) содержат Rust компоненты, которые требуют компиляции на Railway и вызывают ошибки.

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

### Альтернатива: GitHub Actions для деплоя на Railway (опционально)

Если хотите больше контроля, добавьте workflow файл `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: railwayapp/deploy-action@v1
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

Для этого нужно:
1. На Railway: Settings → Tokens → создать новый токен
2. На GitHub: Settings → Secrets → добавить `RAILWAY_TOKEN` с полученным токеном
3. Пушить в `main` — деплой произойдёт автоматически

---

## Возможные проблемы и решения

### Проблема: `pydantic-core` не компилируется на Railway (Python 3.13)
**Ошибка:** `Failed building wheel for pydantic-core`

**Причина:** старые версии Pydantic (< 2.6) содержат Rust компоненты, которые требуют компиляции на Railway.

**Решение:** обновить `requirements.txt` на совместимые версии:

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.6.0
```

Эти версии имеют **предкомпилированные wheels** для Python 3.13 и устанавливаются быстро без ошибок.

---

## Практические задания (рекомендуется)
1. Добавьте тесты с помощью `pytest` для проверки работы API endpoints.
2. Подключите линтер `ruff` или `flake8` и добавьте проверку в CI.
3. Перенесите хранение корзины в файл или простую базу данных (например SQLite).
4. Добавьте логирование в приложение.

---

## Советы и замечания
- В текущем учебном проекте корзина и заказы хранятся в памяти — данные теряются при перезапуске.
- Для продакшена используйте базу данных и хранение секретов через `GH Secrets` или переменные окружения.
- ID товаров — индекс в `shop.json` (начинается с 0).

---

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
- **Локальная проверка:** перед пушем можно выполнить те же команды локально:

```bash
python -m pip install --upgrade pip
pip install fastapi pydantic uvicorn
python -m py_compile main.py
python -c "import main; print('imported OK')"
```

- **Советы по улучшению:** добавить `requirements.txt`, линтер (`flake8`, `ruff`) и тесты (`pytest`) в workflow для более строгой проверки.
