# Architecture

liteit is a **generator**. The CLI depends on Click, Rich, and Jinja2. Generated apps depend on Litestar, Granian, Pydantic, structlog, and friends — **not** on the `liteit` package.

```text
liteit init / generate
        │
        ▼
  Jinja templates
        │
        ▼
  Litestar project  ──liteit run──►  Granian (ASGI)
```

## Generated layout

```text
<project>/
├── app/
│   ├── main.py              # create_app() + discover_controllers()
│   ├── config.py            # Settings (BaseSettings)
│   ├── controllers/         # Controller classes (pkgutil discovery)
│   ├── schemas/             # Pydantic DTOs
│   └── core/
│       ├── logging.py
│       └── security.py      # JWT stub
├── tests/
├── .env.example
├── requirements.txt
└── Dockerfile
```

## Controller discovery

`app/main.py` walks `app.controllers` with `pkgutil.iter_modules` + `importlib`, collects subclasses of `litestar.Controller` defined in those modules, and passes them to `Litestar(route_handlers=...)`.

Adding `app/controllers/foo.py` with a `FooController` is enough — no central import list.

## Blocking vs async

Granian runs ASGI apps with a Python event loop and a **blocking thread pool** (`--blocking-threads`, default `4` via `liteit run`).

| Handler style | Where it runs |
|---------------|---------------|
| `async def` | Event loop |
| sync `def` | Blocking thread pool |

Prefer `async def` for I/O. Use sync `def` for CPU-bound or blocking library calls (and consider `sync_to_thread` where Litestar requires it).

## OpenAPI

`OpenAPIConfig(path="/docs", render_plugins=[SwaggerRenderPlugin()])` serves Swagger under `/docs`. See [OpenAPI / Swagger](openapi.md).
