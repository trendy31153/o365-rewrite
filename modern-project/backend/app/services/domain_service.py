from __future__ import annotations

from app import models
from app.repositories.in_memory import store
from app.services.ms_graph import MicrosoftGraphGateway


graph = MicrosoftGraphGateway()


class DomainService:
    async def list_domains(self) -> list[models.Domain]:
        if store.domains:
            return list(store.domains.values())
        return await graph.domains()

    async def organization(self) -> models.Organization:
        if store.org:
            return store.org
        return await graph.organization()


domain_service = DomainService()
