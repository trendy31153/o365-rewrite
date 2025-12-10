from fastapi import APIRouter

from app import models
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=models.Report)
async def generate_report(payload: models.Report):
    return await report_service.generate(payload)
