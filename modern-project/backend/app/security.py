from datetime import datetime, timedelta
from typing import List, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlmodel import Session

from .config import get_settings
from .database import get_session
from .models import LocalAccount

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, roles: List[str]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.auth_exp_minutes)
    payload = {"sub": subject, "roles": roles, "exp": expire}
    return jwt.encode(payload, settings.auth_secret, algorithm=settings.auth_algorithm)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session: Session = Depends(get_session),
) -> LocalAccount:
    try:
        payload = jwt.decode(credentials.credentials, settings.auth_secret, algorithms=[settings.auth_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    username: Optional[str] = payload.get("sub")
    roles: List[str] = payload.get("roles", [])
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    account = session.get(LocalAccount, username)
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account not found")
    account.roles = roles
    return account


def require_admin(account: LocalAccount = Depends(get_current_user)) -> LocalAccount:
    if "admin" not in account.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return account
