# Docker

`liteit init` writes a multi-stage **Debian slim** Dockerfile.

## Build and run

```bash
docker build -t myapi .
docker run --rm -p 8000:8000 myapi
```

The image:

1. Builds wheels from `requirements.txt` in a builder stage
2. Installs wheels into a slim runtime image as non-root `appuser`
3. Copies `app/`
4. Runs Granian: `app.main:app` on `0.0.0.0:8000` with `--runtime-threads 1` and `--blocking-threads 4`

## Tips

- Pass secrets via environment (`-e JWT_SECRET=...`) or your orchestrator — do not bake `.env` into the image
- Expose / map port `8000`
- For multi-worker deployments, override `CMD` or use a process manager / multiple replicas
