"""
Domain Entity: Progress

Represents progress tracking metrics.
"""
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum


class MetricType(str, Enum):
    WEIGHT = "weight"
    BODY_FAT = "body_fat"
    MEASUREMENT = "measurement"
    STRENGTH = "strength"
    ENDURANCE = "endurance"


class Progress:
    """Progress tracking entity"""
    
    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        date: date,
        metric_type: MetricType,
        value: float,
        unit: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.metric_type = metric_type
        self.value = value
        self.unit = unit
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        
        # Validate
        if value < 0:
            raise ValueError("Progress value cannot be negative")
    
    @classmethod
    def create(
        cls,
        user_id: UUID,
        date: date,
        metric_type: MetricType,
        value: float,
        unit: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> "Progress":
        """Factory method to create a new progress entry"""
        return cls(
            id=uuid4(),
            user_id=user_id,
            date=date,
            metric_type=metric_type,
            value=value,
            unit=unit,
            notes=notes,
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Progress):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
