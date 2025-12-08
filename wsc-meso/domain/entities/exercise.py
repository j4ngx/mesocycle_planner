"""
Domain Entity: Exercise

Represents a musculation exercise with biomechanical details.
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum


class MuscleGroup(str, Enum):
    PECTORALS = "pectorals"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    LEGS = "legs"
    ABS = "abs"


class ExerciseType(str, Enum):
    FREE_WEIGHT = "free_weight"
    MACHINE = "machine"
    CABLE = "cable"
    SMITH_MACHINE = "smith_machine"
    BODYWEIGHT = "bodyweight"
    OTHER = "other"


class Exercise:
    """Exercise entity with biomechanical information"""
    
    def __init__(
        self,
        id: int,
        name: str,
        number: str,
        muscle_group: MuscleGroup,
        primary_muscles: List[str],
        type: ExerciseType,
        secondary_muscles: Optional[List[str]] = None,
        antagonist_muscles: Optional[List[str]] = None,
        execution: Optional[str] = None,
        comments: Optional[str] = None,
        common_mistakes: Optional[List[str]] = None,
        variants: Optional[List[str]] = None,
        pdf_page: Optional[int] = None,
        difficulty: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.number = number
        self.muscle_group = muscle_group
        self.primary_muscles = primary_muscles
        self.type = type
        self.secondary_muscles = secondary_muscles or []
        self.antagonist_muscles = antagonist_muscles or []
        self.execution = execution
        self.comments = comments
        self.common_mistakes = common_mistakes or []
        self.variants = variants or []
        self.pdf_page = pdf_page
        self.difficulty = difficulty
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_compound_exercise(self) -> bool:
        """Check if exercise works multiple muscle groups"""
        return len(self.primary_muscles) > 1 or len(self.secondary_muscles) > 0
    
    def get_all_muscles_worked(self) -> List[str]:
        """Get all muscles worked by this exercise"""
        return self.primary_muscles + self.secondary_muscles
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Exercise):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
