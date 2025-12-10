from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from ..database import get_session
from ..models import DirectoryUser
from ..services import UserService

router = APIRouter()


class BulkCreateRequest(BaseModel):
    prefix: str
    count: int
    strategy: str = "random"


class RoleUpdateRequest(BaseModel):
    roles: List[str]


class StatusUpdateRequest(BaseModel):
    enabled: bool


class LicenseUpdateRequest(BaseModel):
    sku_id: str


@router.get("/{tenant_id}", response_model=List[DirectoryUser])
def list_users(tenant_id: int, session: Session = Depends(get_session)) -> List[DirectoryUser]:
    return UserService(session).list(tenant_id)


@router.post("/{tenant_id}", response_model=DirectoryUser)
def create_user(tenant_id: int, payload: DirectoryUser, session: Session = Depends(get_session)) -> DirectoryUser:
    return UserService(session).create(tenant_id, payload)


@router.post("/{tenant_id}/bulk", response_model=List[DirectoryUser])
def bulk_create(tenant_id: int, payload: BulkCreateRequest, session: Session = Depends(get_session)) -> List[DirectoryUser]:
    return UserService(session).bulk_create(tenant_id, payload.prefix, payload.count, payload.strategy)


@router.put("/{tenant_id}/{user_id}/roles", response_model=DirectoryUser)
def update_roles(tenant_id: int, user_id: int, payload: RoleUpdateRequest, session: Session = Depends(get_session)) -> DirectoryUser:
    return UserService(session).update_roles(tenant_id, user_id, payload.roles)


@router.put("/{tenant_id}/{user_id}/status", response_model=DirectoryUser)
def update_status(tenant_id: int, user_id: int, payload: StatusUpdateRequest, session: Session = Depends(get_session)) -> DirectoryUser:
    return UserService(session).update_status(tenant_id, user_id, payload.enabled)


@router.put("/{tenant_id}/{user_id}/licenses", response_model=DirectoryUser)
def update_license(tenant_id: int, user_id: int, payload: LicenseUpdateRequest, session: Session = Depends(get_session)) -> DirectoryUser:
    return UserService(session).assign_license(tenant_id, user_id, payload.sku_id)


@router.delete("/{tenant_id}/{user_id}", status_code=204)
def delete_user(tenant_id: int, user_id: int, session: Session = Depends(get_session)) -> None:
    UserService(session).delete(tenant_id, user_id)
