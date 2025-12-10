# Modern O365 management frontend (Vue 3 + Vite)

This SPA consumes the FastAPI backend to manage tenants, users, licenses, invites, reports, and settings.

## Prerequisites
- Node.js 18+
- npm (bundled with Node)

## Local development
```bash
cd modern-project/frontend
npm install
# optional: point to a different backend API base
cat > .env.local <<'ENV'
VITE_API_BASE=http://localhost:8000
ENV
npm run dev
```
Vite will print the local dev URL (default `http://localhost:5173`). Log in using a bearer token issued by the backend auth flow; the SPA attaches it to requests automatically.

## Build and preview
```bash
npm run build   # outputs static assets to dist/
npm run preview # serves the built bundle locally
```

## Deployment notes
- The build output in `dist/` can be hosted on any static file server or CDN.
- Set `VITE_API_BASE` at build time to point to your deployed FastAPI host (e.g., `https://api.example.com`).
- Ensure CORS on the backend allows the chosen frontend origin.
