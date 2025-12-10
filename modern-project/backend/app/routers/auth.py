from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from ..database import get_session
from ..security import create_access_token, get_current_user
from ..services import AccountService

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
    account = AccountService(session).authenticate(payload.username, payload.password)
    token = create_access_token(account.username, account.roles)
    return TokenResponse(access_token=token)


class AccountResponse(BaseModel):
    username: str
    roles: list[str]


@router.get("/me", response_model=AccountResponse)
def me(account=Depends(get_current_user)) -> AccountResponse:  # type: ignore[override]
    return AccountResponse(username=account.username, roles=account.roles)
