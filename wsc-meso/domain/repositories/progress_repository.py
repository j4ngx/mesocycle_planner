"""
Repository Interface: Progress Repository

Defines the contract for progress persistence operations.
"""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from uuid import UUID

from domain.entities.progress import Progress, MetricType


class IProgressRepository(ABC):
    """Progress repository interface"""
    
    @abstractmethod
    async def save(self, progress: Progress) -> Progress:
        """Save a progress entry"""
        pass
    
    @abstractmethod
    async def find_by_id(self, progress_id: UUID) -> Optional[Progress]:
        """Find progress entry by ID"""
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def update(self, progress: Progress) -> Progress:
        """Update a progress entry"""
        pass
    
    @abstractmethod
    async def delete(self, progress_id: UUID) -> bool:
        """Delete a progress entry"""
        pass
    
    @abstractmethod
    async def count_by_user_id(
        self,
        user_id: UUID,
        metric_type: Optional[MetricType] = None,
    ) -> int:
        """Count progress entries for a user"""
        pass
