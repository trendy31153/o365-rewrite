from fastapi import APIRouter

from app import models
from app.services.system_service import system_service

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status", response_model=models.SystemStatus)
async def status():
    return await system_service.status()


@router.put("/status", response_model=models.SystemStatus)
async def update_status(payload: models.SystemStatus):
    return await system_service.update(payload)
