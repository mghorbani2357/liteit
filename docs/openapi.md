# OpenAPI / Swagger

Generated apps enable Litestar OpenAPI with Swagger UI.

## URLs

With default config (`OpenAPIConfig(path="/docs", ...)`):

| URL | Purpose |
|-----|---------|
| `/docs` | OpenAPI root (Swagger when using `SwaggerRenderPlugin`) |
| `/docs/swagger` | Swagger UI |
| `/docs/openapi.json` | OpenAPI schema |

## Configuration

In `app/main.py`:

```python
openapi_config=OpenAPIConfig(
    title=settings.app_name,
    version=settings.app_version,
    path="/docs",
    render_plugins=[SwaggerRenderPlugin()],
)
```

Change `path` if you need a different docs prefix. Add more render plugins (Redoc, Scalar, …) as needed for your Litestar version.

## Controllers and schemas

Docstrings and Pydantic return/body types drive the schema. Keep DTOs in `app/schemas/` and annotate handler signatures so Swagger stays useful without extra decorators.
