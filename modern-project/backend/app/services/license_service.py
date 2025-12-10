from __future__ import annotations

from app import models
from app.repositories.in_memory import store
from app.services.ms_graph import MicrosoftGraphGateway


graph = MicrosoftGraphGateway()


class LicenseService:
    async def list_licenses(self) -> list[models.LicensePlan]:
        if store.licenses:
            return list(store.licenses.values())
        return await graph.list_licenses()

    async def assign(self, user_id: str, sku_ids: list[str]) -> list[str]:
        if user_id in store.users:
            user = store.users[user_id]
            updated_skus = list(set(user.license_skus + sku_ids))
            store.update_user(user_id, {"license_skus": updated_skus})
            return updated_skus
        return await graph.assign_license(user_id, sku_ids)


license_service = LicenseService()
