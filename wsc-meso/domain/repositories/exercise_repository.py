"""
Repository Interface: Exercise Repository

Defines the contract for exercise persistence operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.exercise import Exercise, MuscleGroup, ExerciseType


class IExerciseRepository(ABC):
    """Exercise repository interface"""
    
    @abstractmethod
    async def find_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """Find exercise by ID"""
        pass
    
    @abstractmethod
    async def find_all(
        self,
        muscle_group: Optional[MuscleGroup] = None,
        exercise_type: Optional[ExerciseType] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Exercise]:
        """Find all exercises with optional filtering"""
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 20) -> List[Exercise]:
        """Search exercises by name or description"""
        pass
    
    @abstractmethod
    async def find_recommended_by_muscle_group(
        self,
        muscle_group: MuscleGroup,
        training_level: str,
        limit: int = 8,
    ) -> List[Exercise]:
        """Find recommended exercises for a muscle group"""
        pass
    
    @abstractmethod
    async def count(
        self,
        muscle_group: Optional[MuscleGroup] = None,
        exercise_type: Optional[ExerciseType] = None,
    ) -> int:
        """Count exercises with optional filtering"""
        pass
