# Logging

`app/core/logging.py` configures **structlog** for JSON lines on stdout with timezone-aware ISO-8601 timestamps.

## Behavior

- Processors merge contextvars, add log level / logger name, then render JSON
- Timestamp uses `ZoneInfo(settings.timezone)`
- Extra fields: `timezone`, `tz_offset`

`create_app()` calls `configure_logging()` before building the Litestar app.

## Usage in handlers

```python
import structlog

logger = structlog.get_logger(__name__)

async def list_users(self):
    logger.info("listing_users")
    return []
```

## Customize

Common extensions:

- Add `structlog.processors.TimeStamper` alternatives or redact keys
- Attach Litestar middleware that binds `request_id` into contextvars
- Dual-write to a file with a second `PrintLoggerFactory` / stdlib handler

Keep JSON structure stable if you ship logs to aggregators (ELK, Loki, CloudWatch).
