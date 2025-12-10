from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import AppReport
from ..services import ReportService

router = APIRouter()


@router.get("/{tenant_id}", response_model=List[AppReport])
def list_reports(tenant_id: int, session: Session = Depends(get_session)) -> List[AppReport]:
    return ReportService(session).list(tenant_id)


@router.post("/{tenant_id}", response_model=AppReport)
def generate_report(tenant_id: int, session: Session = Depends(get_session)) -> AppReport:
    return ReportService(session).snapshot(tenant_id)
