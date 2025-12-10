from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .routers import auth, invites, licenses, reports, settings, tenants, users
from .security import get_current_user

app = FastAPI(title=get_settings().app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(users.router, prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])
app.include_router(licenses.router, prefix="/licenses", tags=["licenses"], dependencies=[Depends(get_current_user)])
app.include_router(invites.router, prefix="/invites", tags=["invites"], dependencies=[Depends(get_current_user)])
app.include_router(reports.router, prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)])
app.include_router(settings.router, prefix="/settings", tags=["settings"], dependencies=[Depends(get_current_user)])


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
