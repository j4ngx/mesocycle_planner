"""
Domain Entity: Workout

Represents a training workout session.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum


class TrainingSplit(str, Enum):
    PUSH = "push"
    PULL = "pull"
    LEGS = "legs"
    FULLBODY = "fullbody"
    UPPER = "upper"
    LOWER = "lower"


class Workout:
    """Workout entity"""
    
    def __init__(
        self,
        id: UUID,
        mesocycle_id: UUID,
        name: str,
        scheduled_date: datetime,
        microcycle_id: Optional[int] = None,
        description: Optional[str] = None,
        completed: bool = False,
        completed_at: Optional[datetime] = None,
        duration_minutes: Optional[int] = None,
        notes: Optional[str] = None,
        split: Optional[TrainingSplit] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.mesocycle_id = mesocycle_id
        self.microcycle_id = microcycle_id
        self.name = name
        self.description = description
        self.scheduled_date = scheduled_date
        self.completed = completed
        self.completed_at = completed_at
        self.duration_minutes = duration_minutes
        self.notes = notes
        self.split = split
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def create(
        cls,
        mesocycle_id: UUID,
        name: str,
        scheduled_date: datetime,
        microcycle_id: Optional[int] = None,
        description: Optional[str] = None,
        split: Optional[TrainingSplit] = None,
        notes: Optional[str] = None,
    ) -> "Workout":
        """Factory method to create a new workout"""
        return cls(
            id=uuid4(),
            mesocycle_id=mesocycle_id,
            name=name,
            scheduled_date=scheduled_date,
            microcycle_id=microcycle_id,
            description=description,
            split=split,
            notes=notes,
        )
    
    def mark_completed(self, duration_minutes: Optional[int] = None, notes: Optional[str] = None) -> None:
        """Mark workout as completed"""
        if self.completed:
            raise ValueError("Workout is already completed")
        
        self.completed = True
        self.completed_at = datetime.utcnow()
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.utcnow()
    
    def is_overdue(self) -> bool:
        """Check if workout is overdue"""
        return not self.completed and datetime.utcnow() > self.scheduled_date
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Workout):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
