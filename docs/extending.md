# Extending

The scaffold is intentionally thin. Extend inside the generated project — do not add runtime coupling to the `liteit` package.

## Application factory

Edit `create_app()` in `app/main.py` to register:

- middleware / exception handlers
- `on_startup` / `on_shutdown` hooks
- DI providers (`Provide`)
- plugins (SQLAlchemy, Redis, …)
- `jwt_auth.on_app_init` — see [Security](security.md)

## Controllers and schemas

```bash
liteit generate controller products
```

Then replace stub bodies, expand DTOs, and add repository/service layers as modules under `app/` (for example `app/services/`). Discovery only requires Controller subclasses under `app/controllers/`.

## Settings

Add fields to `Settings` in `app/config.py` and document them in `.env.example`. Prefer typed settings over scattered `os.getenv` calls.

## Dependencies

Pin or bump packages in `requirements.txt`. Keep Granian as the production server unless you intentionally switch ASGI servers (update Dockerfile and `liteit run` usage accordingly).
