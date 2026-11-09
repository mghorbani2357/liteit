# Configuration

Settings live in `app/config.py` as a `pydantic_settings.BaseSettings` model. Values come from environment variables and optional `.env` (copy from `.env.example`).

## Variables

| Env var | Setting field | Default | Notes |
|---------|---------------|---------|--------|
| `APP_NAME` | `app_name` | project folder name | OpenAPI title |
| `APP_VERSION` | `app_version` | `0.1.0` | OpenAPI version |
| `DEBUG` | `debug` | `false` | Litestar debug |
| `HOST` | `host` | `127.0.0.1` | Documented bind host |
| `PORT` | `port` | `8000` | Documented bind port |
| `TIMEZONE` | `timezone` | `UTC` | IANA name for log timestamps |
| `JWT_SECRET` | `jwt_secret` | `change-me-in-production` | JWT stub |
| `JWT_ALGORITHM` | `jwt_algorithm` | `HS256` | JWT stub |
| `JWT_EXPIRATION_SECONDS` | `jwt_expiration_seconds` | `3600` | JWT stub |

Field names are case-insensitive for env lookup (pydantic-settings default).

## Example `.env`

```env
APP_NAME=myapi
APP_VERSION=0.1.0
DEBUG=true
HOST=127.0.0.1
PORT=8000
TIMEZONE=Asia/Tehran
JWT_SECRET=replace-me
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=3600
```

## Runtime bind address

`HOST` / `PORT` in settings document intent. **`liteit run`** uses its own `--host` / `--port` flags (defaults `127.0.0.1:8000`). Align them or read settings in a custom entrypoint if you prefer a single source of truth.
