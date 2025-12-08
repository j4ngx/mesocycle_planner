"""
Repository Interface: Workout Repository

Defines the contract for workout persistence operations.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from domain.entities.workout import Workout


class IWorkoutRepository(ABC):
    """Workout repository interface"""
    
    @abstractmethod
    async def save(self, workout: Workout) -> Workout:
        """Save a workout"""
        pass
    
    @abstractmethod
    async def find_by_id(self, workout_id: UUID) -> Optional[Workout]:
        """Find workout by ID"""
        pass
    
    @abstractmethod
    async def find_by_mesocycle_id(
        self,
        mesocycle_id: UUID,
        completed: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Workout]:
        """Find workouts by mesocycle ID"""
        pass
    
    @abstractmethod
    async def find_by_date_range(
        self,
        mesocycle_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Workout]:
        """Find workouts in a date range"""
        pass
    
    @abstractmethod
    async def update(self, workout: Workout) -> Workout:
        """Update a workout"""
        pass
    
    @abstractmethod
    async def delete(self, workout_id: UUID) -> bool:
        """Delete a workout"""
        pass
    
    @abstractmethod
    async def count_by_mesocycle_id(
        self,
        mesocycle_id: UUID,
        completed: Optional[bool] = None,
    ) -> int:
        """Count workouts for a mesocycle"""
        pass
