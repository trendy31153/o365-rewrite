# Auth API Quick Debug Guide

Use these steps to verify the local login flow without the frontend. Commands assume you run them from `modern-project/backend` in one terminal.

## 1. Start the API server

```bash
uvicorn app.main:app --reload --port 8000
```

- The server seeds a default admin account (`admin` / `admin`) on startup if it does not exist.
- You can confirm the service is up with:

```bash
curl -sf http://localhost:8000/health
```

## 2. Request a token

```bash
curl -sf -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

- On success you should see JSON like `{ "access_token": "<jwt>", "token_type": "bearer" }`.
- If you get `401`, verify the credentials or delete `modern-project/backend/data.db` to let the app reseed the default admin.

## 3. Call an authenticated endpoint

Use the token from step 2:

```bash
TOKEN="<paste_access_token_here>"
curl -sf http://localhost:8000/auth/me \
  -H "Authorization: Bearer ${TOKEN}"
```

Expected response:

```json
{ "username": "admin", "roles": ["admin"] }
```

If this succeeds, the backend login flow works and any remaining issues are likely in the frontend or network path to the API.

## 4. Optional: create your own account

You can create a new account with an interactive snippet:

```bash
python - <<'PY'
from app.database import get_session
from app.services import AccountService
with get_session() as session:
    AccountService(session).create("demo", "demo", roles=["admin"])
print("created user 'demo'")
PY
```

Then repeat steps 2–3 using the new credentials.
