# Modern Project (FastAPI + Vue 3)

This folder contains a greenfield rewrite of the legacy Java-based O365 admin panel using a modern full-stack toolkit:

- **Backend**: FastAPI, SQLModel, MSAL, and httpx for Microsoft Graph integration
- **Frontend**: Vue 3, Vite, Pinia, Vue Router, and Element Plus for a streamlined management UI

The goal is feature parity with the original system: multi-tenant configuration, user CRUD, license assignment, invitation flows, reporting, and optional WeChat-backed login approval.

## Structure
- `backend/`: FastAPI app with modular routers and services
- `frontend/`: Vite + Vue 3 single-page application

Refer to the backend and frontend READMEs for local development steps.
