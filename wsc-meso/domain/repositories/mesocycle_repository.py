"""
Repository Interface: Mesocycle Repository

Defines the contract for mesocycle persistence operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.mesocycle import Mesocycle, MesocycleStatus


class IMesocycleRepository(ABC):
    """Mesocycle repository interface"""
    
    @abstractmethod
    async def save(self, mesocycle: Mesocycle) -> Mesocycle:
        """Save a mesocycle"""
        pass
    
    @abstractmethod
    async def find_by_id(self, mesocycle_id: UUID) -> Optional[Mesocycle]:
        """Find mesocycle by ID"""
        pass
    
    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: UUID,
        status: Optional[MesocycleStatus] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Mesocycle]:
        """Find mesocycles by user ID with optional status filter"""
        pass
    
    @abstractmethod
    async def update(self, mesocycle: Mesocycle) -> Mesocycle:
        """Update a mesocycle"""
        pass
    
    @abstractmethod
    async def delete(self, mesocycle_id: UUID) -> bool:
        """Delete a mesocycle"""
        pass
    
    @abstractmethod
    async def count_by_user_id(
        self,
        user_id: UUID,
        status: Optional[MesocycleStatus] = None,
    ) -> int:
        """Count mesocycles for a user"""
        pass
    
    @abstractmethod
    async def find_active_by_user_id(self, user_id: UUID) -> Optional[Mesocycle]:
        """Find active mesocycle for a user"""
        pass
