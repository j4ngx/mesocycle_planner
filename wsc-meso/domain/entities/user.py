"""
Domain Entity: User

Represents a user in the system with authentication capabilities.
This is an aggregate root in the domain model.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum


class TrainingLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


class User:
    """User aggregate root"""
    
    def __init__(
        self,
        id: UUID,
        email: str,
        username: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        training_level: TrainingLevel = TrainingLevel.INTERMEDIATE,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.training_level = training_level
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        email: str,
        username: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        training_level: TrainingLevel = TrainingLevel.INTERMEDIATE,
    ) -> "User":
        """Factory method to create a new user"""
        return cls(
            id=uuid4(),
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            training_level=training_level,
        )
    
    def update_profile(
        self,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        training_level: Optional[TrainingLevel] = None,
    ) -> None:
        """Update user profile information"""
        if username is not None:
            self.username = username
        if full_name is not None:
            self.full_name = full_name
        if email is not None:
            self.email = email
        if training_level is not None:
            self.training_level = training_level
        self.updated_at = datetime.utcnow()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
