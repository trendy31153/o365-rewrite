from fastapi import APIRouter

from app import models
from app.services.domain_service import domain_service

router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("", response_model=list[models.Domain])
async def list_domains():
    return await domain_service.list_domains()


@router.get("/organization", response_model=models.Organization)
async def organization():
    return await domain_service.organization()
