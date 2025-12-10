from __future__ import annotations

import uuid

from app import models
from app.repositories.in_memory import store
from app.services.ms_graph import MicrosoftGraphGateway


graph = MicrosoftGraphGateway()


class UserService:
    async def list_users(self) -> list[models.User]:
        if store.users:
            return list(store.users.values())
        return await graph.list_users()

    async def search_users(self, keyword: str, limit: int = 10) -> list[models.User]:
        matches = [user for user in store.users.values() if keyword.lower() in user.user_principal_name.lower()]
        return matches[:limit]

    async def create_user(self, payload: models.CreateUserRequest) -> models.User:
        user = await graph.create_user(payload)
        store.add_user(user)
        return user

    async def update_user(self, user_id: str, payload: models.UpdateUserRequest) -> models.User:
        if user_id in store.users:
            return store.update_user(user_id, payload.model_dump(exclude_unset=True))
        updated = await graph.update_user(user_id, payload)
        store.add_user(updated)
        return updated

    async def delete_user(self, user_id: str) -> None:
        store.remove_user(user_id)
        try:
            await graph.delete_user(user_id)
        except NotImplementedError:
            pass

    async def bulk_create(self, request: models.BulkUserRequest) -> list[models.User]:
        created: list[models.User] = []
        for req in request.users:
            if request.license_sku and request.license_sku not in req.license_skus:
                req.license_skus.append(request.license_sku)
            created.append(await self.create_user(req))
        return created

    async def invite_user(self, email: str, role: str | None) -> models.Invite:
        invite = await graph.create_invite(email, role)
        store.add_invite(invite)
        return invite

    async def accept_invite(self, invite_id: str, display_name: str) -> models.User:
        invite = store.consume_invite(invite_id)
        new_user = models.CreateUserRequest(
            user_principal_name=invite.email,
            display_name=display_name,
            password=f"Temp-{uuid.uuid4()}",
            license_skus=[],
        )
        user = await self.create_user(new_user)
        user = user.copy(update={"invited": True})
        store.update_user(user.id, user.model_dump())
        return user

    async def default_password(self, user_id: str) -> str:
        return f"ChangeMe-{user_id[:8]}"

    async def get_roles(self) -> list[str]:
        return ["Global Administrator", "User", "Helpdesk Administrator"]


user_service = UserService()
