"""
MongoDB Model: User

MongoDB document model for User entity.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class UserModel(BaseModel):
    """MongoDB User document model"""
    
    id: UUID = Field(alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    training_level: str = "intermediate"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "athlete123",
                "hashed_password": "$2b$12$...",
                "full_name": "John Doe",
                "training_level": "intermediate",
            }
        }
