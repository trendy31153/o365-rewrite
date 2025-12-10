from __future__ import annotations

from app import models


class SystemService:
    def __init__(self) -> None:
        self.state = models.SystemStatus()

    async def status(self) -> models.SystemStatus:
        return self.state

    async def update(self, payload: models.SystemStatus) -> models.SystemStatus:
        self.state = payload
        return self.state


system_service = SystemService()
