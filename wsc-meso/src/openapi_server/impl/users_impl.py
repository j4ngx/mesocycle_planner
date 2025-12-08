# coding: utf-8

"""
Users API Implementation

Handles user profile operations.
"""

from typing import Optional
from fastapi import HTTPException, Header

from openapi_server.apis.users_api_base import BaseUsersApi
from openapi_server.models.user import User as UserModel
from openapi_server.models.update_current_user_request import UpdateCurrentUserRequest

from infrastructure.config.database import get_database_config
from infrastructure.persistence.repositories.user_repository_impl import UserRepository
from domain.entities.user import User, TrainingLevel
from openapi_server.utils.auth import get_current_user_id


# Global database initialization flag
_db_initialized = False


class UsersApiImpl(BaseUsersApi):
    """Implementation of Users API"""
    
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
            self.repository = UserRepository(db_config.database)
        
        return self.repository
    
    def _domain_to_api_model(self, domain_user: User) -> UserModel:
        """Convert domain User to API User model"""
        return UserModel(
            id=domain_user.id,
            email=domain_user.email,
            username=domain_user.username,
            full_name=domain_user.full_name,
            training_level=domain_user.training_level.value if domain_user.training_level else None,
            created_at=domain_user.created_at,
            updated_at=domain_user.updated_at,
        )
    
    async def get_current_user(
        self,
        authorization: Optional[str] = Header(None),
    ) -> UserModel:
        """Get current authenticated user"""
        # Extract user_id from JWT token
        user_id = get_current_user_id(authorization)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        repo = await self._get_repository()
        user = await repo.find_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return self._domain_to_api_model(user)
    
    async def update_current_user(
        self,
        update_current_user_request: UpdateCurrentUserRequest,
        authorization: Optional[str] = Header(None),
    ) -> UserModel:
        """Update current authenticated user"""
        # Extract user_id from JWT token
        user_id = get_current_user_id(authorization)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        repo = await self._get_repository()
        user = await repo.find_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update fields
        if update_current_user_request.full_name is not None:
            user.full_name = update_current_user_request.full_name
        
        if update_current_user_request.training_level is not None:
            user.training_level = TrainingLevel(update_current_user_request.training_level)
        
        # Save updated user
        updated_user = await repo.update(user)
        
        return self._domain_to_api_model(updated_user)
