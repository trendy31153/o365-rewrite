from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import auth, domains, invites, licenses, reports, system, users
from app.config import settings

app = FastAPI(title="Modern O365 Admin Panel", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(licenses.router)
app.include_router(invites.router)
app.include_router(domains.router)
app.include_router(reports.router)
app.include_router(system.router)


@app.get("/health")
async def health():
    return {"status": "ok", "tenant": settings.tenant_id}
