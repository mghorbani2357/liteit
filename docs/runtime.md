# Runtime

## Development

Preferred:

```bash
liteit run --reload
```

Equivalent Granian invocation:

```bash
granian --interface asgi app.main:app \
  --host 127.0.0.1 --port 8000 \
  --workers 1 \
  --runtime-threads 1 \
  --blocking-threads 4 \
  --reload
```

## Production notes

- Prefer multiple `--workers` behind a reverse proxy (or container orchestrator)
- Keep `--reload` off in production
- Sync handlers consume blocking threads; size `--blocking-threads` for your mix of sync vs async work
- Set `DEBUG=false` and a strong `JWT_SECRET` when JWT is enabled

## ASGI target

Module-level `app = create_app()` in `app/main.py` is the Granian target: `app.main:app`.
