manual.md

Создай директорию для workflows:

```bash
mkdir -p .github/workflows
```

## Первый CI pipeline

### для main.py создай Минимальный CI pipeline workflow для GitHub Actions

Создан минимальный workflow: `.github/workflows/ci.yml` — он проверяет синтаксис и импортирует `main.py`.

Файл workflow (пример):

```yaml
name: CI

on:
	push:
		branches: [ main ]
	pull_request:
		branches: [ main ]

jobs:
	check:
		name: Syntax and import check
		runs-on: ubuntu-latest

		steps:
			- name: Checkout
				uses: actions/checkout@v4

			- name: Setup Python
				uses: actions/setup-python@v4
				with:
					python-version: '3.13'

			- name: Install dependencies
				run: |
					python -m pip install --upgrade pip
					pip install fastapi pydantic uvicorn

			- name: Syntax check
				run: python -m py_compile main.py

			- name: Import app
				run: |
					python -c "import main; print('imported OK')"
```

Этот workflow минимален и подходит для быстрого CI: он убеждается, что `main.py` синтактически корректен и что модуль можно импортировать без ошибок.

После пуша в ветку `main` или создания PR GitHub Actions автоматически выполнит эти шаги.

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
