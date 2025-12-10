from fastapi import APIRouter

from app import models
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=models.TokenResponse)
async def login():
    return await auth_service.login()


@router.get("/token", response_model=models.TokenResponse)
async def token():
    return await auth_service.token()
