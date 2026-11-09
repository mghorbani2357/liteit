# Controllers

## Generate

```bash
liteit generate controller users
liteit gen controller order_items
```

Produces:

| File | Contents |
|------|----------|
| `app/controllers/<name>.py` | `<Name>Controller` with CRUD stubs |
| `app/schemas/<name>.py` | `<Name>CreateDTO`, `<Name>UpdateDTO`, `<Name>ResponseDTO` |

Class prefix is TitleCase from snake_case (`order_items` → `OrderItems`).

## Stub endpoints

For `users`:

| Method | Path | Handler |
|--------|------|---------|
| `GET` | `/users` | `list_users` → `[]` |
| `GET` | `/users/{item_id}` | `get_by_id` → 404 stub |
| `POST` | `/users` | `create` → echo DTO with nil UUID |
| `DELETE` | `/users/{item_id}` | `delete_item` → 404 stub |

Replace stubs with real persistence. Keep response/request types as Pydantic models so OpenAPI stays accurate.

## Discovery contract

A module under `app/controllers/` is registered when it defines a class that:

1. subclasses `litestar.Controller`
2. is defined in that module (not imported from elsewhere)

`health.py` ships with `HealthController` (`GET /health`).

## Tests

Generated `tests/conftest.py` provides an `AsyncTestClient` fixture. `tests/test_health.py` asserts `GET /health` returns `{"status": "ok"}`.

```bash
pytest
```
