# coding: utf-8

"""
Exercises API Implementation

Connects auto-generated API with hexagonal architecture repositories.
"""

from typing import List, Optional
from fastapi import HTTPException
from pydantic import StrictInt, StrictStr, Field
from typing_extensions import Annotated

from openapi_server.apis.exercises_api_base import BaseExercisesApi
from openapi_server.models.exercise import Exercise as ExerciseModel
from openapi_server.models.exercise_summary import ExerciseSummary
from openapi_server.models.exercise_type import ExerciseType
from openapi_server.models.list_exercises200_response import ListExercises200Response
from openapi_server.models.muscle_group import MuscleGroup
from openapi_server.models.training_level import TrainingLevel

from infrastructure.config.database import get_database_config, init_database
from infrastructure.persistence.repositories.exercise_repository_impl import ExerciseRepository
from domain.entities.exercise import MuscleGroup as DomainMuscleGroup, ExerciseType as DomainExerciseType


# Global database initialization flag
_db_initialized = False


class ExercisesApiImpl(BaseExercisesApi):
    """Implementation of Exercises API using repository pattern"""
    
    def __init__(self):
        self.repository = None
    
    async def _get_repository(self):
        """Lazy initialization of repository"""
        global _db_initialized
        
        if not _db_initialized:
            # Initialize database connection with authentication
            db_config = get_database_config()
            db_config.connection_string = "mongodb://admin:password123@localhost:27017"
            db_config.database_name = "mesocycle_planner"
            await db_config.connect()
            _db_initialized = True
        
        if self.repository is None:
            db_config = get_database_config()
            self.repository = ExerciseRepository(db_config.database)
        
        return self.repository
    
    def _domain_to_api_model(self, domain_exercise) -> ExerciseModel:
        """Convert domain Exercise to API Exercise model"""
        return ExerciseModel(
            id=domain_exercise.id,
            name=domain_exercise.name,
            number=domain_exercise.number,
            muscle_group=MuscleGroup(domain_exercise.muscle_group.value),
            type=ExerciseType(domain_exercise.type.value),
            primary_muscles=domain_exercise.primary_muscles,
            secondary_muscles=domain_exercise.secondary_muscles,
            antagonist_muscles=domain_exercise.antagonist_muscles,
            execution=domain_exercise.execution,
            comments=domain_exercise.comments,
            common_mistakes=domain_exercise.common_mistakes,
            variants=domain_exercise.variants,
            pdf_page=domain_exercise.pdf_page,
            difficulty=domain_exercise.difficulty,
        )
    
    async def get_exercise(self, exercise_id: StrictInt) -> ExerciseModel:
        """Get exercise by ID"""
        repo = await self._get_repository()
        exercise = await repo.find_by_id(exercise_id)
        
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise {exercise_id} not found")
        
        return self._domain_to_api_model(exercise)
    
    async def get_recommended_exercises(
        self,
        group: MuscleGroup,
        level: Optional[TrainingLevel],
    ) -> List[ExerciseModel]:
        """Get recommended exercises for muscle group"""
        repo = await self._get_repository()
        
        # Convert API enum to domain enum
        domain_group = DomainMuscleGroup(group.value)
        training_level = level.value if level else "intermediate"
        
        exercises = await repo.find_recommended_by_muscle_group(
            domain_group,
            training_level,
            limit=8
        )
        
        return [self._domain_to_api_model(ex) for ex in exercises]
    
    async def list_exercises(
        self,
        group: Optional[MuscleGroup],
        type: Optional[ExerciseType],
        page: Optional[Annotated[int, Field(strict=True, ge=1)]],
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> ListExercises200Response:
        """List exercises with pagination and filters"""
        repo = await self._get_repository()
        
        # Convert API enums to domain enums
        domain_group = DomainMuscleGroup(group.value) if group else None
        domain_type = DomainExerciseType(type.value) if type else None
        
        # Calculate offset
        page = page or 1
        limit = limit or 20
        offset = (page - 1) * limit
        
        # Fetch exercises
        exercises = await repo.find_all(
            muscle_group=domain_group,
            exercise_type=domain_type,
            limit=limit,
            offset=offset
        )
        
        # Get total count
        total_count = await repo.count(
            muscle_group=domain_group,
            exercise_type=domain_type
        )
        
        # Calculate total pages
        total_pages = (total_count + limit - 1) // limit if limit > 0 else 0
        
        # Convert to ExerciseSummary for list response
        exercise_summaries = [
            ExerciseSummary(
                id=ex.id,
                name=ex.name,
                muscle_group=MuscleGroup(ex.muscle_group.value),
                type=ExerciseType(ex.type.value),
                primary_muscles=ex.primary_muscles,
            )
            for ex in exercises
        ]
        
        return ListExercises200Response(
            exercises=exercise_summaries,
            total_count=total_count,
            page=page,
            total_pages=total_pages
        )
    
    async def search_exercises(
        self,
        q: StrictStr,
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> List[ExerciseSummary]:
        """Search exercises by query"""
        repo = await self._get_repository()
        
        limit = limit or 20
        exercises = await repo.search(q, limit=limit)
        
        # Convert to ExerciseSummary
        return [
            ExerciseSummary(
                id=ex.id,
                name=ex.name,
                muscle_group=MuscleGroup(ex.muscle_group.value),
                type=ExerciseType(ex.type.value),
                primary_muscles=ex.primary_muscles,
            )
            for ex in exercises
        ]
