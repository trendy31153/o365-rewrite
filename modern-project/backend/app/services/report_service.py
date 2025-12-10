from __future__ import annotations

from datetime import datetime

from app import models


class ReportService:
    async def generate(self, report_type: models.Report) -> models.Report:
        return models.Report(type=report_type.type, content=report_type.content, generated_at=datetime.utcnow())


report_service = ReportService()
