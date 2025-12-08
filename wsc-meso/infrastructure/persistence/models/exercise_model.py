"""
MongoDB Model: Exercise

MongoDB document model for Exercise entity.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ExerciseModel(BaseModel):
    """MongoDB Exercise document model"""
    
    id: int = Field(alias="_id")
    name: str
    number: str
    muscle_group: str
    type: str
    primary_muscles: List[str]
    secondary_muscles: List[str] = Field(default_factory=list)
    antagonist_muscles: List[str] = Field(default_factory=list)
    execution: Optional[str] = None
    comments: Optional[str] = None
    common_mistakes: List[str] = Field(default_factory=list)
    variants: List[str] = Field(default_factory=list)
    pdf_page: Optional[int] = None
    difficulty: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
