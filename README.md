# liteit

[![License](https://img.shields.io/github/license/mghorbani2357/liteit)](https://raw.githubusercontent.com/mghorbani2357/liteit/master/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/mghorbani2357/liteit/ci.yml?branch=master&logo=github)](https://github.com/mghorbani2357/liteit/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/liteit)](https://pypi.org/project/liteit/)
[![Python versions](https://img.shields.io/pypi/pyversions/liteit)](https://pypi.org/project/liteit/)
[![Documentation Status](https://readthedocs.org/projects/liteit/badge/?version=latest)](https://liteit.readthedocs.io/en/latest/?badge=latest)

CLI scaffolding for **Litestar + Granian** ASGI APIs: modular controllers, automatic discovery, OpenAPI/Swagger at `/docs`, structlog JSON logging, and a production Dockerfile.

Inspired by [flaskit](https://github.com/mghorbani2357/flaskit) (Flask + Flask-Smorest + Bjoern).

**Documentation:** [liteit.readthedocs.io](https://liteit.readthedocs.io/) · source under [`docs/`](docs/)

```bash
pip install -e ".[docs]"
python -m mkdocs serve
```

Requires Python **3.10+** for the CLI. Generated apps target **Python 3.11+**.

## Install

```bash
pip install liteit
# or from source
pip install -e .
pip install -e ".[test]"
```

Then use the `liteit` command (same as any other CLI). If Windows says the command is not found, your Python **Scripts** folder is not on `PATH` — use a venv, or see [Installation](https://liteit.readthedocs.io/en/latest/installation/).

## Quick start

```bash
liteit init myapi
cd myapi
python -m venv .venv
# activate .venv, then:
pip install -U pip && pip install -r requirements.txt
cp .env.example .env
liteit generate controller users
liteit run --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI. Health check: `GET /health`. Full walkthrough: [Quick start](https://liteit.readthedocs.io/en/latest/quickstart/).

## CLI

| Command | Description |
|---------|-------------|
| `liteit init <project_name>` | Scaffold a full Litestar project tree |
| `liteit generate controller <name>` | Create controller + Pydantic schemas (`gen` alias) |
| `liteit run [--host] [--port] [--reload] [--workers]` | Serve with Granian (`app.main:app`) |

```bash
liteit init myapi
liteit generate controller users
liteit gen controller order_items
liteit run --host 0.0.0.0 --port 8000 --reload
```

## Generated layout

```text
<project_name>/
├── app/
│   ├── main.py              # factory + controller auto-loader
│   ├── config.py            # Pydantic BaseSettings (.env)
│   ├── controllers/         # Litestar Controllers (auto-discovered)
│   ├── schemas/             # Pydantic DTOs
│   └── core/                # logging + JWT stub
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

Controllers under `app/controllers/` are registered automatically — no manual import list.

**Blocking vs async:** sync `def` handlers run in Granian's blocking thread pool; `async def` handlers run on the event loop.

## Publish (maintainers)

Push a tag `v*` to trigger [`.github/workflows/publish.yml`](.github/workflows/publish.yml). Set repository secret **`PYPI_API_TOKEN`**. Details: [Publish](https://liteit.readthedocs.io/en/latest/publishing/).

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
