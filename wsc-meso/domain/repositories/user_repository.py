"""
Repository Interface: User Repository

Defines the contract for user persistence operations.
This is a port in hexagonal architecture.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.user import User


class IUserRepository(ABC):
    """User repository interface"""
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user"""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        pass
    
    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update a user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user"""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        pass
