from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import LicenseAssignment
from ..services import LicenseService

router = APIRouter()


@router.get("/{tenant_id}", response_model=List[LicenseAssignment])
def list_licenses(tenant_id: int, session: Session = Depends(get_session)) -> List[LicenseAssignment]:
    return LicenseService(session).list(tenant_id)


@router.put("/{tenant_id}", response_model=List[LicenseAssignment])
def upsert_licenses(tenant_id: int, payload: List[LicenseAssignment], session: Session = Depends(get_session)) -> List[LicenseAssignment]:
    return LicenseService(session).upsert(tenant_id, payload)
