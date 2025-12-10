# Modern O365 management backend

This FastAPI backend re-imagines the original Java-based O365 admin panel with a modern Python stack. It exposes RESTful endpoints for tenant configuration, Microsoft Graph authorization, user lifecycle operations, license assignments, invitation codes, reporting, and system settings.  The service uses SQLModel on SQLite for persistence and MSAL + httpx for Microsoft Graph connectivity.

Key features
- Multi-tenant app registration management with client credentials and per-tenant scopes.
- Local administrator authentication with JWT-based bearer tokens.
- User CRUD, bulk creation strategies, enable/disable, role promotion, and license assignment.
- Invitation code creation/consumption flows for delegated user onboarding.
- Snapshot-style reporting APIs for tenant health and usage summaries.
- Configurable webhooks and safety toggles for optional WeChat login approval.

Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
