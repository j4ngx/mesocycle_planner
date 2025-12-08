"""
Domain Entity: Mesocycle

Represents a training mesocycle with periodization model.
This is an aggregate root that contains microcycles.
"""
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum


class MesocycleStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"


class TrainingGoal(str, Enum):
    STRENGTH = "strength"
    HYPERTROPHY = "hypertrophy"
    POWER = "power"
    ENDURANCE = "endurance"
    DEFINITION = "definition"


class PeriodizationModel(str, Enum):
    LINEAR = "linear"
    DAILY_UNDULATING = "daily_undulating"
    BLOCK = "block"
    POLARIZED = "polarized"


class Mesocycle:
    """Mesocycle aggregate root"""
    
    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        name: str,
        periodization_model: PeriodizationModel,
        goal: TrainingGoal,
        duration_weeks: int,
        start_date: date,
        end_date: date,
        status: MesocycleStatus,
        training_level: str,
        weekly_frequency: int,
        description: Optional[str] = None,
        deload_weeks: Optional[List[int]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.periodization_model = periodization_model
        self.goal = goal
        self.duration_weeks = duration_weeks
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.training_level = training_level
        self.weekly_frequency = weekly_frequency
        self.description = description
        self.deload_weeks = deload_weeks or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        # Validate business rules
        self._validate()
    
    def _validate(self) -> None:
        """Validate business rules"""
        if self.duration_weeks < 4 or self.duration_weeks > 16:
            raise ValueError("Duration must be between 4 and 16 weeks")
        
        if self.weekly_frequency < 3 or self.weekly_frequency > 6:
            raise ValueError("Weekly frequency must be between 3 and 6")
        
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
    
    @classmethod
    def create(
        cls,
        user_id: UUID,
        name: str,
        periodization_model: PeriodizationModel,
        goal: TrainingGoal,
        duration_weeks: int,
        start_date: date,
        end_date: date,
        training_level: str,
        weekly_frequency: int,
        description: Optional[str] = None,
        deload_weeks: Optional[List[int]] = None,
    ) -> "Mesocycle":
        """Factory method to create a new mesocycle"""
        return cls(
            id=uuid4(),
            user_id=user_id,
            name=name,
            periodization_model=periodization_model,
            goal=goal,
            duration_weeks=duration_weeks,
            start_date=start_date,
            end_date=end_date,
            status=MesocycleStatus.PLANNED,
            training_level=training_level,
            weekly_frequency=weekly_frequency,
            description=description,
            deload_weeks=deload_weeks,
        )
    
    def start(self) -> None:
        """Start the mesocycle"""
        if self.status != MesocycleStatus.PLANNED:
            raise ValueError("Can only start a planned mesocycle")
        self.status = MesocycleStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def complete(self) -> None:
        """Complete the mesocycle"""
        if self.status != MesocycleStatus.ACTIVE:
            raise ValueError("Can only complete an active mesocycle")
        self.status = MesocycleStatus.COMPLETED
        self.updated_at = datetime.utcnow()
    
    def pause(self) -> None:
        """Pause the mesocycle"""
        if self.status != MesocycleStatus.ACTIVE:
            raise ValueError("Can only pause an active mesocycle")
        self.status = MesocycleStatus.PAUSED
        self.updated_at = datetime.utcnow()
    
    def resume(self) -> None:
        """Resume a paused mesocycle"""
        if self.status != MesocycleStatus.PAUSED:
            raise ValueError("Can only resume a paused mesocycle")
        self.status = MesocycleStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def is_deload_week(self, week_number: int) -> bool:
        """Check if given week is a deload week"""
        return week_number in self.deload_weeks
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mesocycle):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
