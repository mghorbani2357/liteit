# CLI reference

```bash
liteit -h
liteit --help
python -m liteit -h
liteit --version
```

## `liteit init <project_name>`

Scaffold a project under `project_name/`. The folder name becomes the default `APP_NAME`.

Creates (among others):

| Path | Purpose |
|------|---------|
| `app/main.py` | Factory, OpenAPI, controller discovery |
| `app/config.py` | Pydantic BaseSettings (`.env`) |
| `app/controllers/` | Litestar Controllers (auto-discovered) |
| `app/schemas/` | Pydantic DTOs |
| `app/core/logging.py` | structlog JSON setup |
| `app/core/security.py` | JWT stub (not wired by default) |
| `tests/` | Async Litestar test client + health test |
| `.env.example` | Environment template |
| `requirements.txt` | App dependencies |
| `Dockerfile` | Multi-stage Granian image |
| `pytest.ini` | `asyncio_mode = auto` |

Refuses non-empty destination directories and existing scaffold files.

```bash
liteit init myapi
liteit init ./services/payments
liteit init -h
```

## `liteit generate controller <name>`

Alias: **`liteit gen controller <name>`**

Create:

- `app/controllers/<name>.py` — `Controller` with list / get_by_id / create / delete stubs
- `app/schemas/<name>.py` — `CreateDTO` / `UpdateDTO` / `ResponseDTO`

| Rule | Detail |
|------|--------|
| Name | snake_case starting with a letter (`users`, `order_items`) |
| `--path` | Project root containing `app/controllers/` (default `.`) |

```bash
liteit generate controller users
liteit gen controller order_items --path ./myapi
liteit generate controller -h
```

Restart the app after generating so discovery and OpenAPI pick up the controller.

## `liteit run`

Wraps Granian for `app.main:app`:

| Flag | Default | Notes |
|------|---------|--------|
| `--host` | `127.0.0.1` | Bind address |
| `--port` | `8000` | Bind port |
| `--workers` | `1` | Worker processes |
| `--reload` | off | Dev auto-reload |
| `--app` | `app.main:app` | ASGI target |
| `--path` | `.` | Project root |

Always passes `--interface asgi`, `--runtime-threads 1`, and `--blocking-threads 4`.

```bash
liteit run
liteit run --reload
liteit run --host 0.0.0.0 --port 8000 --workers 2
liteit run -h
```
