# liteit

**liteit** scaffolds **Litestar + Granian** ASGI APIs. It is a CLI generator: the created project does not import `liteit` at runtime.

Inspired by [flaskit](https://github.com/mghorbani2357/flaskit) (Flask + Flask-Smorest + Bjoern).

```bash
pip install liteit
liteit init myapi
```

Then follow the [Quick start](quickstart.md) from virtualenv through Swagger.

## Highlights

- Modular `app/controllers/` with automatic `Controller` discovery
- Pydantic v2 settings via `.env` (`pydantic-settings`)
- OpenAPI / Swagger UI at `/docs`
- structlog JSON logging with timezone-aware ISO-8601 timestamps
- JWT auth stub (opt-in) under `app/core/security.py`
- Multi-stage Dockerfile running Granian

## Customize

Wire databases, JWT guards, Redis, and other capabilities in `create_app` — see [Extending](extending.md).

## Publish

Package releases and PyPI: [Publish](publishing.md).

## License

GPL-3.0-or-later — see the repository `LICENSE` file.
