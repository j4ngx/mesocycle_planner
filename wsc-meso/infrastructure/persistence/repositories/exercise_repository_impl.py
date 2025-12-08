"""
Exercise Repository Implementation

MongoDB implementation of IExerciseRepository.
"""
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.exercise import Exercise, MuscleGroup, ExerciseType
from domain.repositories.exercise_repository import IExerciseRepository
from infrastructure.persistence.models.exercise_model import ExerciseModel


class ExerciseRepository(IExerciseRepository):
    """MongoDB implementation of Exercise repository"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.exercises
    
    async def find_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """Find exercise by ID"""
        doc = await self.collection.find_one({"_id": exercise_id})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def find_all(
        self,
        muscle_group: Optional[MuscleGroup] = None,
        exercise_type: Optional[ExerciseType] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Exercise]:
        """Find all exercises with optional filtering"""
        query = {}
        if muscle_group:
            query["muscle_group"] = muscle_group.value
        if exercise_type:
            query["type"] = exercise_type.value
        
        cursor = self.collection.find(query).skip(offset).limit(limit).sort("name", 1)
        docs = await cursor.to_list(length=limit)
        return [self._to_entity(doc) for doc in docs]
    
    async def search(self, query: str, limit: int = 20) -> List[Exercise]:
        """Search exercises by name or description"""
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"execution": {"$regex": query, "$options": "i"}},
                {"comments": {"$regex": query, "$options": "i"}}
            ]
        }
        
        cursor = self.collection.find(search_query).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self._to_entity(doc) for doc in docs]
    
    async def find_recommended_by_muscle_group(
        self,
        muscle_group: MuscleGroup,
        training_level: str,
        limit: int = 8,
    ) -> List[Exercise]:
        """Find recommended exercises for a muscle group"""
        query = {
            "muscle_group": muscle_group.value,
            "difficulty": training_level
        }
        
        cursor = self.collection.find(query).limit(limit)
        docs = await cursor.to_list(length=limit)
        
        # If not enough exercises with exact difficulty, get any from muscle group
        if len(docs) < limit:
            remaining = limit - len(docs)
            query = {"muscle_group": muscle_group.value}
            cursor = self.collection.find(query).limit(remaining)
            additional_docs = await cursor.to_list(length=remaining)
            docs.extend(additional_docs)
        
        return [self._to_entity(doc) for doc in docs]
    
    async def count(
        self,
        muscle_group: Optional[MuscleGroup] = None,
        exercise_type: Optional[ExerciseType] = None,
    ) -> int:
        """Count exercises with optional filtering"""
        query = {}
        if muscle_group:
            query["muscle_group"] = muscle_group.value
        if exercise_type:
            query["type"] = exercise_type.value
        
        return await self.collection.count_documents(query)
    
    def _to_entity(self, doc: dict) -> Exercise:
        """Convert MongoDB document to Exercise entity"""
        return Exercise(
            id=doc["_id"],
            name=doc["name"],
            number=doc["number"],
            muscle_group=MuscleGroup(doc["muscle_group"]),
            primary_muscles=doc["primary_muscles"],
            type=ExerciseType(doc["type"]),
            secondary_muscles=doc.get("secondary_muscles", []),
            antagonist_muscles=doc.get("antagonist_muscles", []),
            execution=doc.get("execution"),
            comments=doc.get("comments"),
            common_mistakes=doc.get("common_mistakes", []),
            variants=doc.get("variants", []),
            pdf_page=doc.get("pdf_page"),
            difficulty=doc.get("difficulty"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )
