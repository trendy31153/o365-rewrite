# Modern Project (FastAPI + Vue 3)
This folder contains a greenfield rewrite of the legacy Java-based O365 admin panel using a modern full-stack toolkit:
- **Backend**: FastAPI, SQLModel, MSAL, and httpx for Microsoft Graph integration
- **Frontend**: Vue 3, Vite, Pinia, Vue Router, and Element Plus for a streamlined management UI
The goal is feature parity with the original system: multi-tenant configuration, user CRUD, license assignment, invitation flows, reporting, and optional WeChat-backed login approval.

## Structure
- `backend/`: FastAPI app with modular routers and services
- `frontend/`: Vite + Vue 3 single-page application

## Quick start (local development)
1. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   # configure Microsoft Graph app credentials in environment variables or .env if desired
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`. OpenAPI docs live at `/docs`.

2. **Frontend**
   ```bash
   cd frontend
   npm install
   # point the SPA to your backend (defaults to http://localhost:8000)
   echo "VITE_API_BASE=http://localhost:8000" > .env.local
   npm run dev
   ```
   Vite will print the local URL (default `http://localhost:5173`). Log in with a backend-issued token flow.

3. **Preview or build**
   ```bash
   cd frontend
   npm run build   # production bundle into dist/
   npm run preview # serve the built bundle locally
   ```

For more detail on each side, check `backend/README.md` and `frontend/README.md`.
