"""
Domain Entity: TrainingSession

Represents a completed training session with performance data.
"""
from datetime import date
from typing import List, Optional
from uuid import UUID


class SetPerformed:
    """Value object for a performed set"""
    
    def __init__(
        self,
        weight_kg: float,
        reps_achieved: int,
        actual_rpe: int,
        reps_in_reserve: int,
    ):
        if weight_kg < 0:
            raise ValueError("Weight cannot be negative")
        if reps_achieved < 0:
            raise ValueError("Reps cannot be negative")
        if not (1 <= actual_rpe <= 10):
            raise ValueError("RPE must be between 1 and 10")
        if reps_in_reserve < 0:
            raise ValueError("RIR cannot be negative")
        
        self.weight_kg = weight_kg
        self.reps_achieved = reps_achieved
        self.actual_rpe = actual_rpe
        self.reps_in_reserve = reps_in_reserve
    
    def calculate_volume(self) -> float:
        """Calculate volume (weight × reps)"""
        return self.weight_kg * self.reps_achieved
    
    def estimate_1rm(self) -> float:
        """Estimate 1RM using Epley formula"""
        if self.reps_achieved == 1:
            return self.weight_kg
        return self.weight_kg * (1 + self.reps_achieved / 30.0)


class ExercisePerformed:
    """Value object for an exercise performed in a session"""
    
    def __init__(
        self,
        exercise_id: int,
        planned_sets: int,
        sets_performed: List[SetPerformed],
    ):
        self.exercise_id = exercise_id
        self.planned_sets = planned_sets
        self.sets_performed = sets_performed
    
    def get_total_volume(self) -> float:
        """Calculate total volume for this exercise"""
        return sum(s.calculate_volume() for s in self.sets_performed)
    
    def get_average_rpe(self) -> float:
        """Calculate average RPE across all sets"""
        if not self.sets_performed:
            return 0.0
        return sum(s.actual_rpe for s in self.sets_performed) / len(self.sets_performed)


class TrainingSession:
    """Training session entity"""
    
    def __init__(
        self,
        id: int,
        mesocycle_id: UUID,
        date: date,
        microcycle_id: Optional[int] = None,
        week_number: Optional[int] = None,
        exercises_performed: Optional[List[ExercisePerformed]] = None,
    ):
        self.id = id
        self.mesocycle_id = mesocycle_id
        self.microcycle_id = microcycle_id
        self.week_number = week_number
        self.date = date
        self.exercises_performed = exercises_performed or []
    
    def add_exercise(self, exercise_performed: ExercisePerformed) -> None:
        """Add an exercise to the session"""
        self.exercises_performed.append(exercise_performed)
    
    def get_total_session_volume(self) -> float:
        """Calculate total volume for the entire session"""
        return sum(ex.get_total_volume() for ex in self.exercises_performed)
    
    def get_average_session_rpe(self) -> float:
        """Calculate average RPE for the entire session"""
        if not self.exercises_performed:
            return 0.0
        
        total_rpe = sum(ex.get_average_rpe() for ex in self.exercises_performed)
        return total_rpe / len(self.exercises_performed)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrainingSession):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
