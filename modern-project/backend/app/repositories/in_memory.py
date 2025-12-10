from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from app import models


class InMemoryStore:
    def __init__(self) -> None:
        self.users: dict[str, models.User] = {}
        self.invites: dict[str, models.Invite] = {}
        self.licenses: dict[str, models.LicensePlan] = {}
        self.domains: dict[str, models.Domain] = {}
        self.org: models.Organization | None = None

    def seed(self) -> None:
        default_license = models.LicensePlan(sku_id="O365_E5", name="Office 365 E5", available=100)
        self.licenses[default_license.sku_id] = default_license
        contoso = models.Domain(id="contoso.onmicrosoft.com", name="contoso.onmicrosoft.com", verified=True, default=True)
        self.domains[contoso.id] = contoso
        self.org = models.Organization(id="org-1", display_name="Contoso", tenant_id="0000-0000", domains=[contoso])

    def add_user(self, user: models.User) -> models.User:
        self.users[user.id] = user
        return user

    def update_user(self, user_id: str, updates: dict) -> models.User:
        user = self.users[user_id]
        new_user = user.copy(update=updates)
        self.users[user_id] = new_user
        return new_user

    def remove_user(self, user_id: str) -> None:
        self.users.pop(user_id, None)

    def add_invite(self, invite: models.Invite) -> models.Invite:
        self.invites[invite.id] = invite
        return invite

    def consume_invite(self, invite_id: str) -> models.Invite:
        invite = self.invites[invite_id]
        invite = invite.copy(update={"redeemed": True})
        self.invites[invite_id] = invite
        return invite

    def active_invites(self) -> Iterable[models.Invite]:
        now = datetime.utcnow()
        for invite in self.invites.values():
            if invite.expires_at and invite.expires_at < now:
                continue
            yield invite

    def provision_default_invite(self, email: str) -> models.Invite:
        now = datetime.utcnow()
        invite = models.Invite(
            id=f"inv-{len(self.invites)+1}",
            email=email,
            redeem_url=f"https://portal.office.com/invite/{email}",
            created_at=now,
            expires_at=now + timedelta(days=7),
            role="User",
        )
        return self.add_invite(invite)


store = InMemoryStore()
store.seed()
