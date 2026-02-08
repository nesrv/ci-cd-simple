manual.md

РЎРѕР·РґР°Р№ РґРёСЂРµРєС‚РѕСЂРёСЋ РґР»СЏ workflows:

```bash
mkdir -p .github/workflows
```

## РџРµСЂРІС‹Р№ CI pipeline

### РґР»СЏ main.py СЃРѕР·РґР°Р№ РњРёРЅРёРјР°Р»СЊРЅС‹Р№ CI pipeline workflow РґР»СЏ GitHub Actions

РЎРѕР·РґР°РЅ РјРёРЅРёРјР°Р»СЊРЅС‹Р№ workflow: `.github/workflows/ci.yml` вЂ” РѕРЅ РїСЂРѕРІРµСЂСЏРµС‚ СЃРёРЅС‚Р°РєСЃРёСЃ Рё РёРјРїРѕСЂС‚РёСЂСѓРµС‚ `main.py`.

Р¤Р°Р№Р» workflow (РїСЂРёРјРµСЂ):

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

Р­С‚РѕС‚ workflow РјРёРЅРёРјР°Р»РµРЅ Рё РїРѕРґС…РѕРґРёС‚ РґР»СЏ Р±С‹СЃС‚СЂРѕРіРѕ CI: РѕРЅ СѓР±РµР¶РґР°РµС‚СЃСЏ, С‡С‚Рѕ `main.py` СЃРёРЅС‚Р°РєС‚РёС‡РµСЃРєРё РєРѕСЂСЂРµРєС‚РµРЅ Рё С‡С‚Рѕ РјРѕРґСѓР»СЊ РјРѕР¶РЅРѕ РёРјРїРѕСЂС‚РёСЂРѕРІР°С‚СЊ Р±РµР· РѕС€РёР±РѕРє.

РџРѕСЃР»Рµ РїСѓС€Р° РІ РІРµС‚РєСѓ `main` РёР»Рё СЃРѕР·РґР°РЅРёСЏ PR GitHub Actions Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё РІС‹РїРѕР»РЅРёС‚ СЌС‚Рё С€Р°РіРё.

### РљР°Рє СЌС‚Рѕ РїСЂРѕРёСЃС…РѕРґРёС‚ (РєСЂР°С‚РєРѕ)

- **РўСЂРёРіРіРµСЂ:** РїСѓС€ РІ РІРµС‚РєСѓ `main` РёР»Рё РѕС‚РєСЂС‹С‚РёРµ/РѕР±РЅРѕРІР»РµРЅРёРµ Pull Request РІ `main` Р·Р°РїСѓСЃРєР°РµС‚ workflow.
- **РЁР°РіРё РІ CI:**
	- `actions/checkout` вЂ” РїРѕР»СѓС‡Р°РµС‚ РєРѕРґ СЂРµРїРѕР·РёС‚РѕСЂРёСЏ.
	- `actions/setup-python` вЂ” СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚ Python 3.13.
	- РЈСЃС‚Р°РЅРѕРІРєР° Р·Р°РІРёСЃРёРјРѕСЃС‚РµР№ С‡РµСЂРµР· `pip` (FastAPI, Pydantic, Uvicorn).
	- `python -m py_compile main.py` вЂ” Р±С‹СЃС‚СЂР°СЏ РїСЂРѕРІРµСЂРєР° СЃРёРЅС‚Р°РєСЃРёСЃР°.
	- `python -c "import main"` вЂ” РїСЂРѕР±РЅС‹Р№ РёРјРїРѕСЂС‚ РјРѕРґСѓР»СЏ, С‡С‚РѕР±С‹ СѓР±РµРґРёС‚СЊСЃСЏ, С‡С‚Рѕ РёРјРїРѕСЂС‚ РЅРµ РїР°РґР°РµС‚.
- **Р“РґРµ СЃРјРѕС‚СЂРµС‚СЊ СЂРµР·СѓР»СЊС‚Р°С‚С‹:** Р—Р°Р№РґРё РІ РІРєР»Р°РґРєСѓ `Actions` РЅР° GitHub, РІС‹Р±РµСЂРё workflow `CI` Рё РѕС‚РєСЂРѕР№ РїРѕСЃР»РµРґРЅРёР№ Р·Р°РїСѓСЃРє вЂ” С‚Р°Рј Р»РѕРіРё РїРѕ РєР°Р¶РґРѕРјСѓ С€Р°РіСѓ.
- **РђСЂС‚РµС„Р°РєС‚С‹:** Р’ РјРёРЅРёРјР°Р»СЊРЅРѕРј РІР°СЂРёР°РЅС‚Рµ Р°СЂС‚РµС„Р°РєС‚РѕРІ РЅРµС‚; РјРѕР¶РЅРѕ РґРѕР±Р°РІРёС‚СЊ С€Р°РіРё РґР»СЏ СЃРѕС…СЂР°РЅРµРЅРёСЏ Р»РѕРіРѕРІ/СЂРµР·СѓР»СЊС‚Р°С‚РѕРІ С‚РµСЃС‚РѕРІ РїСЂРё РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё.
- **Р›РѕРєР°Р»СЊРЅР°СЏ РїСЂРѕРІРµСЂРєР°:** РїРµСЂРµРґ РїСѓС€РµРј РјРѕР¶РЅРѕ РІС‹РїРѕР»РЅРёС‚СЊ С‚Рµ Р¶Рµ РєРѕРјР°РЅРґС‹ Р»РѕРєР°Р»СЊРЅРѕ:

```bash
python -m pip install --upgrade pip
pip install fastapi pydantic uvicorn
python -m py_compile main.py
python -c "import main; print('imported OK')"
```

- **РЎРѕРІРµС‚С‹ РїРѕ СѓР»СѓС‡С€РµРЅРёСЋ:** РґРѕР±Р°РІРёС‚СЊ `requirements.txt`, Р»РёРЅС‚РµСЂ (`flake8`, `ruff`) Рё С‚РµСЃС‚С‹ (`pytest`) РІ workflow РґР»СЏ Р±РѕР»РµРµ СЃС‚СЂРѕРіРѕР№ РїСЂРѕРІРµСЂРєРё.

