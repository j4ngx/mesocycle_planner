"""
MongoDB Model: Mesocycle

MongoDB document model for Mesocycle entity.
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class MesocycleModel(BaseModel):
    """MongoDB Mesocycle document model"""
    
    id: UUID = Field(alias="_id")
    user_id: UUID
    name: str
    description: Optional[str] = None
    periodization_model: str
    goal: str
    duration_weeks: int
    start_date: date
    end_date: date
    status: str
    training_level: str
    weekly_frequency: int
    deload_weeks: List[int] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
