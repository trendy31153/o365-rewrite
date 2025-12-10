from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models import TenantConfig
from ..security import require_admin
from ..services import TenantService

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/", response_model=List[TenantConfig])
def list_tenants(session: Session = Depends(get_session)) -> List[TenantConfig]:
    return TenantService(session).list()


@router.post("/", response_model=TenantConfig)
def create_tenant(payload: TenantConfig, session: Session = Depends(get_session)) -> TenantConfig:
    return TenantService(session).create(payload)


@router.put("/{tenant_id}", response_model=TenantConfig)
def update_tenant(tenant_id: int, payload: TenantConfig, session: Session = Depends(get_session)) -> TenantConfig:
    return TenantService(session).update(tenant_id, payload)


@router.delete("/{tenant_id}", status_code=204)
def delete_tenant(tenant_id: int, session: Session = Depends(get_session)) -> None:
    TenantService(session).delete(tenant_id)
