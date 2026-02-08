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

## Практические задания (рекомендуется)
1. Добавьте `requirements.txt` и обновите workflow для установки зависимостей из него.
2. Добавьте `pytest` и простой тест на импорт и ответ `GET /health`.
3. Подключите линтер `ruff` или `flake8` и добавьте проверку в CI.
4. Перенесите хранение корзины в файл или простую базу данных (например SQLite).

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
