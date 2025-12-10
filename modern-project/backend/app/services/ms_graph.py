from __future__ import annotations

import uuid
from datetime import datetime, timedelta

from app import models


class MicrosoftGraphGateway:
    """Thin abstraction for Microsoft Graph operations.

    Real implementations should exchange tokens, call Graph endpoints, and map
    responses back into our Pydantic models. The service layer consumes this
    gateway to keep API handlers decoupled from HTTP concerns.
    """

    async def acquire_app_token(self) -> models.TokenResponse:
        now = datetime.utcnow()
        return models.TokenResponse(
            access_token=f"fake-token-{uuid.uuid4()}",
            refresh_token=None,
            expires_at=now + timedelta(hours=1),
        )

    async def list_users(self) -> list[models.User]:  # pragma: no cover - demo stub
        return []

    async def create_user(self, payload: models.CreateUserRequest) -> models.User:
        return models.User(
            id=str(uuid.uuid4()),
            user_principal_name=payload.user_principal_name,
            display_name=payload.display_name,
            usage_location=payload.usage_location,
            license_skus=payload.license_skus,
            roles=["User"],
            invited=False,
            status="active",
        )

    async def update_user(self, user_id: str, payload: models.UpdateUserRequest) -> models.User:
        raise NotImplementedError

    async def delete_user(self, user_id: str) -> None:
        raise NotImplementedError

    async def list_licenses(self) -> list[models.LicensePlan]:
        raise NotImplementedError

    async def assign_license(self, user_id: str, sku_ids: list[str]) -> list[str]:
        raise NotImplementedError

    async def create_invite(self, email: str, role: str | None) -> models.Invite:
        now = datetime.utcnow()
        return models.Invite(
            id=str(uuid.uuid4()),
            email=email,
            redeem_url=f"https://invite/{uuid.uuid4()}",
            created_at=now,
            expires_at=now + timedelta(days=7),
            role=role,
        )

    async def domains(self) -> list[models.Domain]:
        raise NotImplementedError

    async def organization(self) -> models.Organization:
        raise NotImplementedError

    async def report(self, report_type: models.Report) -> models.Report:
        raise NotImplementedError
