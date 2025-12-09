"""Progression API Implementation
"""
from openapi_server.apis.progression_api_base import BaseProgressionApi
from openapi_server.models.progression_table import ProgressionTable
from openapi_server.models.training_goal import TrainingGoal


class ProgressionApiImpl(BaseProgressionApi):
    async def get_progression_table(self, goal: TrainingGoal) -> ProgressionTable:
        # Provide a small hard-coded progression table per goal
        if goal == TrainingGoal.STRENGTH:
            return ProgressionTable(goal=goal, intensity_pct="85%", repetitions="3-5", sets_recommended=4, rest_interval="2-3 min", rir_target=1)
        if goal == TrainingGoal.HYPERTROPHY:
            return ProgressionTable(goal=goal, intensity_pct="70%", repetitions="8-12", sets_recommended=4, rest_interval="60-90s", rir_target=2)
        # Default fallback
        return ProgressionTable(goal=goal, intensity_pct="75%", repetitions="6-10", sets_recommended=3, rest_interval="90s", rir_target=2)
