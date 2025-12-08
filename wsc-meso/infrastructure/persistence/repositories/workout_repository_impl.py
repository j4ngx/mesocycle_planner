"""
Workout Repository Implementation

MongoDB implementation of IWorkoutRepository.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.workout import Workout, TrainingSplit
from domain.repositories.workout_repository import IWorkoutRepository
from infrastructure.persistence.models.workout_model import WorkoutModel


class WorkoutRepository(IWorkoutRepository):
    """MongoDB implementation of Workout repository"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.workouts
    
    async def save(self, workout: Workout) -> Workout:
        """Save a workout"""
        workout_model = WorkoutModel(
            _id=workout.id,
            mesocycle_id=workout.mesocycle_id,
            microcycle_id=workout.microcycle_id,
            name=workout.name,
            description=workout.description,
            scheduled_date=workout.scheduled_date,
            completed=workout.completed,
            completed_at=workout.completed_at,
            duration_minutes=workout.duration_minutes,
            notes=workout.notes,
            split=workout.split.value if workout.split else None,
            created_at=workout.created_at,
            updated_at=workout.updated_at,
        )
        
        await self.collection.insert_one(workout_model.model_dump(by_alias=True))
        return workout
    
    async def find_by_id(self, workout_id: UUID) -> Optional[Workout]:
        """Find workout by ID"""
        doc = await self.collection.find_one({"_id": workout_id})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def find_by_mesocycle_id(
        self,
        mesocycle_id: UUID,
        completed: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Workout]:
        """Find workouts by mesocycle ID"""
        query = {"mesocycle_id": mesocycle_id}
        if completed is not None:
            query["completed"] = completed
        
        cursor = self.collection.find(query).skip(offset).limit(limit).sort("scheduled_date", -1)
        docs = await cursor.to_list(length=limit)
        return [self._to_entity(doc) for doc in docs]
    
    async def find_by_date_range(
        self,
        mesocycle_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Workout]:
        """Find workouts in a date range"""
        query = {
            "mesocycle_id": mesocycle_id,
            "scheduled_date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        
        cursor = self.collection.find(query).sort("scheduled_date", 1)
        docs = await cursor.to_list(length=None)
        return [self._to_entity(doc) for doc in docs]
    
    async def update(self, workout: Workout) -> Workout:
        """Update a workout"""
        workout_model = WorkoutModel(
            _id=workout.id,
            mesocycle_id=workout.mesocycle_id,
            microcycle_id=workout.microcycle_id,
            name=workout.name,
            description=workout.description,
            scheduled_date=workout.scheduled_date,
            completed=workout.completed,
            completed_at=workout.completed_at,
            duration_minutes=workout.duration_minutes,
            notes=workout.notes,
            split=workout.split.value if workout.split else None,
            created_at=workout.created_at,
            updated_at=workout.updated_at,
        )
        
        await self.collection.replace_one(
            {"_id": workout.id},
            workout_model.model_dump(by_alias=True)
        )
        return workout
    
    async def delete(self, workout_id: UUID) -> bool:
        """Delete a workout"""
        result = await self.collection.delete_one({"_id": workout_id})
        return result.deleted_count > 0
    
    async def count_by_mesocycle_id(
        self,
        mesocycle_id: UUID,
        completed: Optional[bool] = None,
    ) -> int:
        """Count workouts for a mesocycle"""
        query = {"mesocycle_id": mesocycle_id}
        if completed is not None:
            query["completed"] = completed
        return await self.collection.count_documents(query)
    
    def _to_entity(self, doc: dict) -> Workout:
        """Convert MongoDB document to Workout entity"""
        return Workout(
            id=doc["_id"],
            mesocycle_id=doc["mesocycle_id"],
            microcycle_id=doc.get("microcycle_id"),
            name=doc["name"],
            description=doc.get("description"),
            scheduled_date=doc["scheduled_date"],
            completed=doc.get("completed", False),
            completed_at=doc.get("completed_at"),
            duration_minutes=doc.get("duration_minutes"),
            notes=doc.get("notes"),
            split=TrainingSplit(doc["split"]) if doc.get("split") else None,
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )
