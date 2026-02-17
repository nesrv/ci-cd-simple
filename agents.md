измени cd/cd для github actions и railway с учетом postgres в докере 

в бд есть таблица
 TABLE video_cards (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    price       NUMERIC(12,2) NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL
);

измени @app.get("/products") в main.py для получения списка видекарт из бд


@app.get("/products")

asyncdefget_products():

    returnPRODUCTS


для данного проекта сделай самый простой docker-compose для postgesql 17
в main.py сделай подключение к бд в контейнере

Deploy to Railway

- Ошибка была: `railway up --service` без значения. Нужно передать имя сервиса.
- В workflow теперь: `railway up --service ${{ secrets.RAILWAY_SERVICE || 'web' }}` — по умолчанию сервис **web** (как при `railway link`).
- Опционально: в GitHub → Settings → Secrets → Actions можно задать `RAILWAY_SERVICE` = `web` (или другое имя), иначе используется `web`.

Раньше:
Run railway up --service
error: a value is required for '--service `<SERVICE>`' but none was supplied

For more information, try '--help'.

Error: Process completed with exit code 1.

PS C:\W26\project\CI-CD-SIMPLE> railway link

> Select a workspace Серов Николай's Projects
> Select a project luminous-curiosity
> Select an environment production
> Select a service `<esc to skip>` web

Project luminous-curiosity linked successfully! 🎉

**Пояснение:** luminous-curiosity — это **проект** (project). **Сервис** (service) внутри него — **web**. Для деплоя нужен именно сервис: `--service web`.

git Actions дает ошибку

Run black --check .
  black --check .
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.13.12/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.13.12/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.13.12/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.13.12/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.13.12/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.13.12/x64/lib
would reformat /home/runner/work/ci-cd-simple/ci-cd-simple/STEP-1/main-0.py
would reformat /home/runner/work/ci-cd-simple/ci-cd-simple/main.py
would reformat /home/runner/work/ci-cd-simple/ci-cd-simple/STEP-1/main.py
would reformat /home/runner/work/ci-cd-simple/ci-cd-simple/STEP-1/main-1.py
would reformat /home/runner/work/ci-cd-simple/ci-cd-simple/test_main.py

Oh no! 💥 💔 💥
5 files would be reformatted.
Error: Process completed with exit code 1.

old_yml\ci-0.yml
можно ли в учебных целях сделать короче и с комментами?

LECTION\lect-1.md
отформатируй и проверь ошибки не меняя смысл контента

на основе текста лекции LECTION\lection.md
сделай 40 слайдов презентации в формате md

8 картинок в исходнике тоже будут слайдами

LECTION\lection-part1.md
улучши и актуализируй контент для лектора (доктор наук, грейн синьор)
сделай форматирование
сделай на основе lection-part1.md
40 слайдов для презентации в отдельном файле

по необходимости
для сложных английских слов и фраз
добавь русский перевод
