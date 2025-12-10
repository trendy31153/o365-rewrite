from fastapi import APIRouter

from app import models
from app.services.license_service import license_service

router = APIRouter(prefix="/licenses", tags=["licenses"])


@router.get("", response_model=list[models.LicensePlan])
async def list_licenses():
    return await license_service.list_licenses()
