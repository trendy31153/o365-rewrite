# Modern O365 Admin Panel (FastAPI + Vue 3)

This folder contains a ground-up rewrite of the Java/Spring based Microsoft 365 admin panel using a modern stack:

- **Backend:** FastAPI with typed services for Microsoft Graph, invitations, licensing, and tenant configuration.
- **Frontend:** Vue 3 + Vite + TypeScript + Pinia for a responsive management UI.

## Backend

### Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

### Key modules
- `app/main.py` mounts routers for users, licenses, invites, domains, reports, and system settings.
- `app/services/ms_graph.py` is the gateway abstraction to Microsoft Graph; swap in a real implementation for production.
- `app/repositories/in_memory.py` provides an in-memory store that mirrors the Spring data repositories used in the legacy code.
- `app/models.py` collects the shared schemas for users, licenses, invites, and configuration.

## Frontend

### Run locally

```bash
cd frontend
npm install
npm run dev
```

### Structure
- `src/views/DashboardView.vue` hosts tabs for user CRUD, license assignment, invite codes, and tenant settings.
- `src/stores` contains Pinia stores for user/tenant state with API bindings to the FastAPI backend.
- `src/components` includes presentational components such as `UserTable` and `InviteDrawer`.

The frontend points to `http://localhost:8000` by default; update `API_BASE_URL` in `src/stores/api.ts` when deploying.
