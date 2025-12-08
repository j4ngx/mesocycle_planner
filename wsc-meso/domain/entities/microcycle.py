"""
Domain Entity: Microcycle

Represents a training microcycle within a mesocycle.
"""
from typing import Optional
from enum import Enum


class TrainingPhase(str, Enum):
    ACCUMULATION = "accumulation"
    TRANSMUTATION = "transmutation"
    REALIZATION = "realization"
    COMPETITION = "competition"
    DELOAD = "deload"


class IntensityRange:
    """Value object for intensity range"""
    
    def __init__(self, min_pct: float, max_pct: float):
        if not (0.0 <= min_pct <= 1.0) or not (0.0 <= max_pct <= 1.0):
            raise ValueError("Intensity percentages must be between 0 and 1")
        if min_pct > max_pct:
            raise ValueError("Min intensity cannot be greater than max intensity")
        
        self.min_pct = min_pct
        self.max_pct = max_pct
    
    def __repr__(self) -> str:
        return f"IntensityRange({self.min_pct:.1%}-{self.max_pct:.1%})"


class Microcycle:
    """Microcycle entity"""
    
    def __init__(
        self,
        id: int,
        mesocycle_id: str,
        microcycle_number: int,
        week_start: int,
        week_end: int,
        phase: TrainingPhase,
        intensity_range: IntensityRange,
        reps_range: str,
        sets_range: str,
        rir: int,  # Reps In Reserve
        weekly_volume_multiplier: float,
        frequency_per_week: int,
    ):
        self.id = id
        self.mesocycle_id = mesocycle_id
        self.microcycle_number = microcycle_number
        self.week_start = week_start
        self.week_end = week_end
        self.phase = phase
        self.intensity_range = intensity_range
        self.reps_range = reps_range
        self.sets_range = sets_range
        self.rir = rir
        self.weekly_volume_multiplier = weekly_volume_multiplier
        self.frequency_per_week = frequency_per_week
        
        # Validate
        if rir < 0 or rir > 5:
            raise ValueError("RIR must be between 0 and 5")
        if weekly_volume_multiplier < 0.5 or weekly_volume_multiplier > 2.0:
            raise ValueError("Volume multiplier must be between 0.5 and 2.0")
    
    def get_duration_weeks(self) -> int:
        """Get the duration of this microcycle in weeks"""
        return self.week_end - self.week_start + 1
    
    def is_deload(self) -> bool:
        """Check if this is a deload microcycle"""
        return self.phase == TrainingPhase.DELOAD
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Microcycle):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
