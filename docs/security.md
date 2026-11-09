# Security (JWT)

`app/core/security.py` ships a **Litestar `JWTAuth` stub**. It is **not** registered on the app by default so scaffolds stay open for local exploration.

## What's included

- `retrieve_user_handler` — returns `{"id": token.sub}` (replace with a real user lookup)
- `jwt_auth` — configured from `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRATION_SECONDS`
- `create_access_token(user_id=...)` — helper for login stubs

## Wire it into the app

```python
from app.core.security import jwt_auth

app = Litestar(
    route_handlers=discover_controllers(),
    on_app_init=[jwt_auth.on_app_init],
    # ...
)
```

Protect individual handlers with Litestar security dependencies / guards as documented for your Litestar version. Rotate `JWT_SECRET` in every non-local environment.
