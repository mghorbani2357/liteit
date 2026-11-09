# Quick start

Install liteit → create a project → configure `.env` → add a controller → run with Granian → open Swagger.

## 1. Install liteit

```bash
pip install liteit
liteit --version
```

## 2. Create a project

```bash
liteit init myapi
cd myapi
```

Layout:

```text
myapi/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── controllers/
│   ├── schemas/
│   └── core/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── pytest.ini
└── README.md
```

## 3. Virtualenv and dependencies

Generated apps need **Python 3.11+**.

```bash
python -m venv .venv
```

Activate `.venv`, then:

```bash
pip install -U pip
pip install -r requirements.txt
cp .env.example .env
```

## 4. Configure `.env`

`app/config.py` loads `.env` via pydantic-settings. Example:

```env
APP_NAME=myapi
APP_VERSION=0.1.0
DEBUG=true
HOST=127.0.0.1
PORT=8000
TIMEZONE=UTC
JWT_SECRET=change-me-in-production
```

Full variable list: [Configuration](configuration.md).

## 5. Generate a controller

```bash
liteit generate controller users
# alias:
liteit gen controller users
```

Creates:

```text
app/controllers/users.py   # UsersController CRUD stubs
app/schemas/users.py       # CreateDTO / UpdateDTO / ResponseDTO
```

Controllers are discovered on startup — no manual import list.

## 6. Run the app

```bash
liteit run --reload
```

Or call Granian directly:

```bash
granian --interface asgi app.main:app --reload
```

## 7. Open Swagger and try a call

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
- Users list stub: http://127.0.0.1:8000/users

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/users
```

## 8. What to do next

| Goal | Where |
|------|--------|
| Change env settings | Edit `.env` → [Configuration](configuration.md) |
| Add fields / real handlers | Edit controller + schemas → [Controllers](controllers.md) |
| JWT / DI / DB | [Extending](extending.md), [Security](security.md) |
| Production image | [Docker](docker.md) |
| Logging | [Logging](logging.md) |
