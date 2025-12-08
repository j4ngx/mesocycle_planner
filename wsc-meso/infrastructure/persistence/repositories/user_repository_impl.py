"""
User Repository Implementation

MongoDB implementation of IUserRepository.
"""
from typing import Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.user import User, TrainingLevel
from domain.repositories.user_repository import IUserRepository
from infrastructure.persistence.models.user_model import UserModel


class UserRepository(IUserRepository):
    """MongoDB implementation of User repository"""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.users
    
    async def save(self, user: User) -> User:
        """Save a user"""
        user_model = UserModel(
            _id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            training_level=user.training_level.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        
        await self.collection.insert_one(user_model.model_dump(by_alias=True))
        return user
    
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID"""
        doc = await self.collection.find_one({"_id": user_id})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email"""
        doc = await self.collection.find_one({"email": email})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        doc = await self.collection.find_one({"username": username})
        if not doc:
            return None
        return self._to_entity(doc)
    
    async def update(self, user: User) -> User:
        """Update a user"""
        user_model = UserModel(
            _id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            training_level=user.training_level.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        
        await self.collection.replace_one(
            {"_id": user.id},
            user_model.model_dump(by_alias=True)
        )
        return user
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user"""
        result = await self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
    
    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        count = await self.collection.count_documents({"email": email})
        return count > 0
    
    async def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        count = await self.collection.count_documents({"username": username})
        return count > 0
    
    def _to_entity(self, doc: dict) -> User:
        """Convert MongoDB document to User entity"""
        return User(
            id=doc["_id"],
            email=doc["email"],
            username=doc["username"],
            hashed_password=doc["hashed_password"],
            full_name=doc.get("full_name"),
            training_level=TrainingLevel(doc.get("training_level", "intermediate")),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
        )
