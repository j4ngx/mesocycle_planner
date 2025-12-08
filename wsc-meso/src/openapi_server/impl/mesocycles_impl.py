"""Mesocycles API Implementation (non-generated).

Provides concrete implementations for the Mesocycles API using the
infrastructure repositories. Keep implementation minimal and non-invasive.
"""
from typing import Optional
from fastapi import HTTPException

from openapi_server.apis.mesocycles_api_base import BaseMesocyclesApi
from openapi_server.models.mesocycle import Mesocycle as MesocycleModel
from openapi_server.models.mesocycle_create import MesocycleCreate
from openapi_server.models.get_mesocycle_dashboard200_response import GetMesocycleDashboard200Response
from openapi_server.models.get_mesocycle_progression200_response import GetMesocycleProgression200Response
from openapi_server.models.get_microcycle200_response import GetMicrocycle200Response
from openapi_server.models.list_mesocycles200_response import ListMesocycles200Response

from infrastructure.config.database import get_database_config
from infrastructure.persistence.repositories.mesocycle_repository_impl import MesocycleRepository
from domain.entities.mesocycle import Mesocycle as DomainMesocycle, PeriodizationModel, TrainingGoal
from openapi_server.utils.auth import get_current_user_id

# Global DB init flag
_db_initialized = False


class MesocyclesApiImpl(BaseMesocyclesApi):
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
            self.repository = MesocycleRepository(db_config.database)
        return self.repository

    async def create_mesocycle(self, mesocycle_create: MesocycleCreate) -> MesocycleModel:
        user_id = get_current_user_id(None) or "00000000-0000-0000-0000-000000000000"
        repo = await self._get_repository()

        domain = DomainMesocycle.create(
            user_id=user_id,
            name=mesocycle_create.name,
            periodization_model=PeriodizationModel(mesocycle_create.periodization_model),
            goal=TrainingGoal(mesocycle_create.goal),
            duration_weeks=mesocycle_create.duration_weeks,
            start_date=mesocycle_create.start_date,
            end_date=mesocycle_create.end_date,
            training_level=mesocycle_create.training_level or "intermediate",
            weekly_frequency=mesocycle_create.weekly_frequency or 4,
            description=mesocycle_create.description,
            deload_weeks=mesocycle_create.deload_weeks,
        )

        saved = await repo.save(domain)
        return MesocycleModel.from_dict(saved.__dict__)

    async def delete_mesocycle(self, mesocycle_id: str) -> None:
        repo = await self._get_repository()
        deleted = await repo.delete(mesocycle_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Mesocycle not found")

    async def generate_ai_mesocycle(self, generate_ai_mesocycle_request) -> MesocycleModel:
        # Minimal stub: create a mesocycle with provided fields
        repo = await self._get_repository()
        domain = DomainMesocycle.create(
            user_id=generate_ai_mesocycle_request.user_id or "00000000-0000-0000-0000-000000000000",
            name=generate_ai_mesocycle_request.name or "AI Mesocycle",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.STRENGTH,
            duration_weeks=generate_ai_mesocycle_request.duration_weeks or 8,
            start_date=generate_ai_mesocycle_request.start_date,
            end_date=generate_ai_mesocycle_request.end_date,
            training_level=generate_ai_mesocycle_request.training_level or "intermediate",
            weekly_frequency=4,
        )
        saved = await repo.save(domain)
        return MesocycleModel.from_dict(saved.__dict__)

    async def get_mesocycle(self, mesocycle_id: str) -> MesocycleModel:
        repo = await self._get_repository()
        meso = await repo.find_by_id(mesocycle_id)
        if not meso:
            raise HTTPException(status_code=404, detail="Mesocycle not found")
        return MesocycleModel.from_dict(meso.__dict__)

    async def get_mesocycle_dashboard(self, mesocycle_id: str) -> GetMesocycleDashboard200Response:
        # Minimal dashboard stub
        return GetMesocycleDashboard200Response(chart_data=[])

    async def get_mesocycle_progression(self, mesocycle_id: str, week: Optional[int]) -> GetMesocycleProgression200Response:
        return GetMesocycleProgression200Response(recommendations=[])

    async def get_microcycle(self, mesocycle_id: str, microcycle_number: int, week: Optional[int]) -> GetMicrocycle200Response:
        return GetMicrocycle200Response(microcycle={})

    async def list_mesocycles(self, status, page, limit) -> ListMesocycles200Response:
        repo = await self._get_repository()
        user_id = "00000000-0000-0000-0000-000000000000"
        mesocycles = await repo.find_by_user_id(user_id, status=None, limit=limit or 20, offset=((page or 1)-1)*(limit or 20))
        items = [MesocycleModel.from_dict(m.__dict__) for m in mesocycles]
        total = await repo.count_by_user_id(user_id, status=None)
        total_pages = (total + (limit or 20) - 1) // (limit or 20)
        return ListMesocycles200Response(mesocycles=items, total_count=total, page=page or 1, total_pages=total_pages)

    async def update_mesocycle(self, mesocycle_id: str, mesocycle_create: MesocycleCreate) -> MesocycleModel:
        repo = await self._get_repository()
        meso = await repo.find_by_id(mesocycle_id)
        if not meso:
            raise HTTPException(status_code=404, detail="Mesocycle not found")
        meso.name = mesocycle_create.name
        meso.description = mesocycle_create.description
        updated = await repo.update(meso)
        return MesocycleModel.from_dict(updated.__dict__)
