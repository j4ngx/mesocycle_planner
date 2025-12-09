"""Workouts API Implementation (non-generated).
"""
from typing import Optional
from fastapi import HTTPException

from openapi_server.apis.workouts_api_base import BaseWorkoutsApi
from openapi_server.models.workout import Workout as WorkoutModel
from openapi_server.models.workout_create import WorkoutCreate
from openapi_server.models.list_workouts200_response import ListWorkouts200Response

from infrastructure.config.database import get_database_config
from infrastructure.persistence.repositories.workout_repository_impl import WorkoutRepository
from domain.entities.workout import Workout as DomainWorkout

_db_initialized = False


class WorkoutsApiImpl(BaseWorkoutsApi):
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
            self.repository = WorkoutRepository(db_config.database)
        return self.repository

    async def complete_workout(self, workout_id: str, complete_workout_request) -> WorkoutModel:
        repo = await self._get_repository()
        workout = await repo.find_by_id(workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")
        workout.mark_completed(duration_minutes=getattr(complete_workout_request, "duration_minutes", None), notes=getattr(complete_workout_request, "notes", None))
        updated = await repo.update(workout)
        return WorkoutModel.from_dict(updated.__dict__)

    async def create_workout(self, workout_create: WorkoutCreate) -> WorkoutModel:
        repo = await self._get_repository()
        domain = DomainWorkout.create(
            mesocycle_id=workout_create.mesocycle_id,
            name=workout_create.name,
            scheduled_date=workout_create.scheduled_date,
            microcycle_id=workout_create.microcycle_id,
            description=workout_create.description,
            split=workout_create.split,
            notes=workout_create.notes,
        )
        saved = await repo.save(domain)
        return WorkoutModel.from_dict(saved.__dict__)

    async def delete_workout(self, workout_id: str) -> None:
        repo = await self._get_repository()
        deleted = await repo.delete(workout_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Workout not found")

    async def get_workout(self, workout_id: str) -> WorkoutModel:
        repo = await self._get_repository()
        workout = await repo.find_by_id(workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")
        return WorkoutModel.from_dict(workout.__dict__)

    async def list_workouts(self, mesocycle_id: Optional[str], completed: Optional[bool], page: Optional[int], limit: Optional[int]) -> ListWorkouts200Response:
        repo = await self._get_repository()
        page = page or 1
        limit = limit or 20
        offset = (page - 1) * limit
        workouts = await repo.find_by_mesocycle_id(mesocycle_id, completed, limit=limit, offset=offset)
        items = [WorkoutModel.from_dict(w.__dict__) for w in workouts]
        total = await repo.count_by_mesocycle_id(mesocycle_id, completed)
        total_pages = (total + limit - 1) // limit if limit > 0 else 0
        return ListWorkouts200Response(workouts=items, total_count=total, page=page, total_pages=total_pages)

    async def update_workout(self, workout_id: str, workout_create: WorkoutCreate) -> WorkoutModel:
        repo = await self._get_repository()
        workout = await repo.find_by_id(workout_id)
        if not workout:
            raise HTTPException(status_code=404, detail="Workout not found")
        workout.name = workout_create.name
        workout.description = workout_create.description
        workout.scheduled_date = workout_create.scheduled_date
        updated = await repo.update(workout)
        return WorkoutModel.from_dict(updated.__dict__)
