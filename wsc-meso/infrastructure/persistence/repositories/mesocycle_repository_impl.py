"""
Mesocycle Repository Implementation

MongoDB implementation of IMesocycleRepository.
"""
from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.mesocycle import Mesocycle, MesocycleStatus, TrainingGoal, PeriodizationModel
from domain.repositories.mesocycle_repository import IMesocycleRepository
from infrastructure.persistence.models.mesocycle_model import MesocycleModel


class MesocycleRepository(IMesocycleRepository):
    """MongoDB implementation of Mesocycle repository"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.mesocycles
    
    async def save(self, mesocycle: Mesocycle) -> Mesocycle:
        """Save a mesocycle"""
        mesocycle_model = MesocycleModel(
            _id=mesocycle.id,
            user_id=mesocycle.user_id,
            name=mesocycle.name,
            description=mesocycle.description,
            periodization_model=mesocycle.periodization_model.value,
            goal=mesocycle.goal.value,
            duration_weeks=mesocycle.duration_weeks,
            start_date=mesocycle.start_date,
            end_date=mesocycle.end_date,
            status=mesocycle.status.value,
            training_level=mesocycle.training_level,
            weekly_frequency=mesocycle.weekly_frequency,
            deload_weeks=mesocycle.deload_weeks,
            created_at=mesocycle.created_at,
            updated_at=mesocycle.updated_at,
        )
        
        await self.collection.insert_one(mesocycle_model.model_dump(by_alias=True))
        return mesocycle
    
    async def find_by_id(self, mesocycle_id: UUID) -> Optional[Mesocycle]:
        """Find mesocycle by ID"""
        doc = await self.collection.find_one({"_id": mesocycle_id})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def find_by_user_id(
        self,
        user_id: UUID,
        status: Optional[MesocycleStatus] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Mesocycle]:
        """Find mesocycles by user ID"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status.value
        
        cursor = self.collection.find(query).skip(offset).limit(limit).sort("created_at", -1)
        docs = await cursor.to_list(length=limit)
        return [self._to_entity(doc) for doc in docs]
    
    async def update(self, mesocycle: Mesocycle) -> Mesocycle:
        """Update a mesocycle"""
        mesocycle_model = MesocycleModel(
            _id=mesocycle.id,
            user_id=mesocycle.user_id,
            name=mesocycle.name,
            description=mesocycle.description,
            periodization_model=mesocycle.periodization_model.value,
            goal=mesocycle.goal.value,
            duration_weeks=mesocycle.duration_weeks,
            start_date=mesocycle.start_date,
            end_date=mesocycle.end_date,
            status=mesocycle.status.value,
            training_level=mesocycle.training_level,
            weekly_frequency=mesocycle.weekly_frequency,
            deload_weeks=mesocycle.deload_weeks,
            created_at=mesocycle.created_at,
            updated_at=mesocycle.updated_at,
        )
        
        await self.collection.replace_one(
            {"_id": mesocycle.id},
            mesocycle_model.model_dump(by_alias=True)
        )
        return mesocycle
    
    async def delete(self, mesocycle_id: UUID) -> bool:
        """Delete a mesocycle"""
        result = await self.collection.delete_one({"_id": mesocycle_id})
        return result.deleted_count > 0
    
    async def count_by_user_id(
        self,
        user_id: UUID,
        status: Optional[MesocycleStatus] = None,
    ) -> int:
        """Count mesocycles for a user"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status.value
        return await self.collection.count_documents(query)
    
    async def find_active_by_user_id(self, user_id: UUID) -> Optional[Mesocycle]:
        """Find active mesocycle for a user"""
        doc = await self.collection.find_one({"user_id": user_id, "status": "active"})
        if not doc:
            return None
        return self._to_entity(doc)
    
    def _to_entity(self, doc: dict) -> Mesocycle:
        """Convert MongoDB document to Mesocycle entity"""
        return Mesocycle(
            id=doc["_id"],
            user_id=doc["user_id"],
            name=doc["name"],
            description=doc.get("description"),
            periodization_model=PeriodizationModel(doc["periodization_model"]),
            goal=TrainingGoal(doc["goal"]),
            duration_weeks=doc["duration_weeks"],
            start_date=doc["start_date"],
            end_date=doc["end_date"],
            status=MesocycleStatus(doc["status"]),
            training_level=doc["training_level"],
            weekly_frequency=doc["weekly_frequency"],
            deload_weeks=doc.get("deload_weeks", []),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )
