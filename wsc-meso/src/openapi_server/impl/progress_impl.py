"""Progress API Implementation (non-generated).
"""
from typing import Optional
from fastapi import HTTPException

from openapi_server.apis.progress_api_base import BaseProgressApi
from openapi_server.models.progress import Progress as ProgressModel
from openapi_server.models.progress_create import ProgressCreate
from openapi_server.models.list_progress200_response import ListProgress200Response
from openapi_server.models.get_progress_analytics200_response import GetProgressAnalytics200Response

from infrastructure.config.database import get_database_config
from infrastructure.persistence.repositories.progress_repository_impl import ProgressRepository
from domain.entities.progress import Progress as DomainProgress, MetricType

_db_initialized = False


class ProgressApiImpl(BaseProgressApi):
    def __init__(self):
        self.repository = None

    async def _get_repository(self):
        global _db_initialized
        if not _db_initialized:
            db_config = get_database_config()
            db_config.connection_string = "mongodb://admin:password123@localhost:27017"
            db_config.database_name = "mesocycle_planner"
            await db_config.connect()
            _db_initialized = True

        if self.repository is None:
            db_config = get_database_config()
            self.repository = ProgressRepository(db_config.database)
        return self.repository

    async def create_progress(self, progress_create: ProgressCreate) -> ProgressModel:
        repo = await self._get_repository()
        domain = DomainProgress.create(
            user_id=progress_create.user_id,
            date=progress_create.date,
            metric_type=MetricType(progress_create.metric_type),
            value=progress_create.value,
            unit=progress_create.unit,
            notes=progress_create.notes,
        )
        saved = await repo.save(domain)
        return ProgressModel.from_dict(saved.__dict__)

    async def delete_progress(self, progress_id: str) -> None:
        repo = await self._get_repository()
        deleted = await repo.delete(progress_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Progress entry not found")

    async def get_progress(self, progress_id: str) -> ProgressModel:
        repo = await self._get_repository()
        p = await repo.find_by_id(progress_id)
        if not p:
            raise HTTPException(status_code=404, detail="Progress entry not found")
        return ProgressModel.from_dict(p.__dict__)

    async def get_progress_analytics(self, metric_type: str, start_date, end_date) -> GetProgressAnalytics200Response:
        # Minimal analytics stub
        return GetProgressAnalytics200Response(stats={})

    async def list_progress(self, metric_type: Optional[str], start_date, end_date, page: Optional[int], limit: Optional[int]) -> ListProgress200Response:
        repo = await self._get_repository()
        page = page or 1
        limit = limit or 20
        offset = (page - 1) * limit
        user_id = "00000000-0000-0000-0000-000000000000"
        entries = await repo.find_by_user_id(user_id, MetricType(metric_type) if metric_type else None, start_date, end_date, limit=limit, offset=offset)
        items = [ProgressModel.from_dict(e.__dict__) for e in entries]
        total = await repo.count_by_user_id(user_id, MetricType(metric_type) if metric_type else None)
        total_pages = (total + limit - 1) // limit if limit > 0 else 0
        return ListProgress200Response(progress=items, total_count=total, page=page, total_pages=total_pages)

    async def update_progress(self, progress_id: str, progress_create: ProgressCreate) -> ProgressModel:
        repo = await self._get_repository()
        p = await repo.find_by_id(progress_id)
        if not p:
            raise HTTPException(status_code=404, detail="Progress entry not found")
        p.value = progress_create.value
        p.unit = progress_create.unit
        p.notes = progress_create.notes
        updated = await repo.update(p)
        return ProgressModel.from_dict(updated.__dict__)
