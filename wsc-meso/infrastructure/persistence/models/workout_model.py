"""
MongoDB Model: Workout

MongoDB document model for Workout entity.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class WorkoutModel(BaseModel):
    """MongoDB Workout document model"""
    
    id: UUID = Field(alias="_id")
    mesocycle_id: UUID
    microcycle_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    scheduled_date: datetime
    completed: bool = False
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    split: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
