from fastapi import APIRouter

from app import models
from app.repositories.in_memory import store
from app.services.user_service import user_service

router = APIRouter(prefix="/invites", tags=["invites"])


@router.get("", response_model=list[models.Invite])
async def list_invites():
    return list(store.active_invites())


@router.post("", response_model=models.Invite, status_code=201)
async def create_invite(email: str, role: str | None = None):
    return await user_service.invite_user(email, role)


@router.post("/{invite_id}/accept", response_model=models.User)
async def accept_invite(invite_id: str, display_name: str):
    return await user_service.accept_invite(invite_id, display_name)
