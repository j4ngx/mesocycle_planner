# coding: utf-8

"""
Authentication API Implementation

Handles user registration and login with JWT tokens.
"""

from typing import Optional
from fastapi import HTTPException
from pydantic import StrictStr

from openapi_server.apis.authentication_api_base import BaseAuthenticationApi
from openapi_server.models.token import Token
from openapi_server.models.user import User as UserModel
from openapi_server.models.user_create import UserCreate
from openapi_server.models.user_login import UserLogin

from infrastructure.config.database import get_database_config
from infrastructure.persistence.repositories.user_repository_impl import UserRepository
from domain.entities.user import User, TrainingLevel
from openapi_server.utils.auth import hash_password, verify_password, create_access_token


# Global database initialization flag
_db_initialized = False


class AuthenticationApiImpl(BaseAuthenticationApi):
    """Implementation of Authentication API"""
    
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
    
    async def login_user(
        self,
        user_login: UserLogin,
    ) -> Token:
        """User login"""
        repo = await self._get_repository()
        
        # Find user by email
        user = await repo.find_by_email(user_login.email)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token = create_access_token(data={"user_id": str(user.id)})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=60 * 24 * 7  # 7 days in minutes
        )
    
    async def register_user(
        self,
        user_create: UserCreate,
    ) -> User:
        """User registration"""
        repo = await self._get_repository()
        
        # Check if email already exists
        existing_user = await repo.find_by_email(user_create.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_user = await repo.find_by_username(user_create.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Hash password
        password_hash = hash_password(user_create.password)
        
        # Create user entity
        training_level = TrainingLevel(user_create.training_level) if user_create.training_level else TrainingLevel.BEGINNER
        
        user = User.create(
            email=user_create.email,
            username=user_create.username,
            hashed_password=password_hash,
            full_name=user_create.full_name,
            training_level=training_level
        )
        
        # Save to database
        created_user = await repo.save(user)
        
        return self._domain_to_api_model(created_user)

