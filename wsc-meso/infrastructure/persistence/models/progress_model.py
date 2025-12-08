"""
MongoDB Model: Progress

MongoDB document model for Progress entity.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class ProgressModel(BaseModel):
    """MongoDB Progress document model"""
    
    id: UUID = Field(alias="_id")
    user_id: UUID
    date: date
    metric_type: str
    value: float
    unit: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
