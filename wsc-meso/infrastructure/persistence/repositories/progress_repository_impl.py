"""
Progress Repository Implementation

MongoDB implementation of IProgressRepository.
"""
from datetime import date
from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.progress import Progress, MetricType
from domain.repositories.progress_repository import IProgressRepository
from infrastructure.persistence.models.progress_model import ProgressModel


class ProgressRepository(IProgressRepository):
    """MongoDB implementation of Progress repository"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.progress
    
    async def save(self, progress: Progress) -> Progress:
        """Save a progress entry"""
        progress_model = ProgressModel(
            _id=progress.id,
            user_id=progress.user_id,
            date=progress.date,
            metric_type=progress.metric_type.value,
            value=progress.value,
            unit=progress.unit,
            notes=progress.notes,
            created_at=progress.created_at,
        )
        
        await self.collection.insert_one(progress_model.model_dump(by_alias=True))
        return progress
    
    async def find_by_id(self, progress_id: UUID) -> Optional[Progress]:
        """Find progress entry by ID"""
        doc = await self.collection.find_one({"_id": progress_id})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def find_by_user_id(
        self,
        user_id: UUID,
        metric_type: Optional[MetricType] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Progress]:
        """Find progress entries by user ID with optional filters"""
        query = {"user_id": user_id}
        
        if metric_type:
            query["metric_type"] = metric_type.value
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["date"] = date_query
        
        cursor = self.collection.find(query).skip(offset).limit(limit).sort("date", -1)
        docs = await cursor.to_list(length=limit)
        return [self._to_entity(doc) for doc in docs]
    
    async def update(self, progress: Progress) -> Progress:
        """Update a progress entry"""
        progress_model = ProgressModel(
            _id=progress.id,
            user_id=progress.user_id,
            date=progress.date,
            metric_type=progress.metric_type.value,
            value=progress.value,
            unit=progress.unit,
            notes=progress.notes,
            created_at=progress.created_at,
        )
        
        await self.collection.replace_one(
            {"_id": progress.id},
            progress_model.model_dump(by_alias=True)
        )
        return progress
    
    async def delete(self, progress_id: UUID) -> bool:
        """Delete a progress entry"""
        result = await self.collection.delete_one({"_id": progress_id})
        return result.deleted_count > 0
    
    async def count_by_user_id(
        self,
        user_id: UUID,
        metric_type: Optional[MetricType] = None,
    ) -> int:
        """Count progress entries for a user"""
        query = {"user_id": user_id}
        if metric_type:
            query["metric_type"] = metric_type.value
        return await self.collection.count_documents(query)
    
    def _to_entity(self, doc: dict) -> Progress:
        """Convert MongoDB document to Progress entity"""
        return Progress(
            id=doc["_id"],
            user_id=doc["user_id"],
            date=doc["date"],
            metric_type=MetricType(doc["metric_type"]),
            value=doc["value"],
            unit=doc.get("unit"),
            notes=doc.get("notes"),
            created_at=doc.get("created_at"),
        )
