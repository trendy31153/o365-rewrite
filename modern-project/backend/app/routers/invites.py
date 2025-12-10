from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from ..database import get_session
from ..models import InviteCode
from ..services import InviteService

router = APIRouter()


class InviteCreateRequest(BaseModel):
    expires_in_hours: int = 24
    max_usage: int = 1


@router.get("/{tenant_id}", response_model=List[InviteCode])
def list_invites(tenant_id: int, session: Session = Depends(get_session)) -> List[InviteCode]:
    return InviteService(session).list(tenant_id)


@router.post("/{tenant_id}", response_model=InviteCode)
def create_invite(tenant_id: int, payload: InviteCreateRequest, session: Session = Depends(get_session)) -> InviteCode:
    return InviteService(session).create(tenant_id, payload.expires_in_hours, payload.max_usage)


@router.post("/redeem/{code}", response_model=InviteCode)
def redeem_invite(code: str, session: Session = Depends(get_session)) -> InviteCode:
    return InviteService(session).redeem(code)
