from __future__ import annotations

from datetime import datetime, timedelta
import secrets

from app import models


class AuthService:
    def __init__(self) -> None:
        self._token: models.TokenResponse | None = None

    async def login(self) -> models.TokenResponse:
        now = datetime.utcnow()
        self._token = models.TokenResponse(
            access_token=secrets.token_urlsafe(32),
            refresh_token=secrets.token_urlsafe(16),
            expires_at=now + timedelta(hours=1),
        )
        return self._token

    async def token(self) -> models.TokenResponse:
        if not self._token:
            return await self.login()
        if self._token.expires_at <= datetime.utcnow():
            return await self.login()
        return self._token


auth_service = AuthService()
