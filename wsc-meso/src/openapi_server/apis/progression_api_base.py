# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.error import Error
from openapi_server.models.progression_table import ProgressionTable
from openapi_server.models.training_goal import TrainingGoal


class BaseProgressionApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProgressionApi.subclasses = BaseProgressionApi.subclasses + (cls,)
    async def get_progression_table(
        self,
        goal: TrainingGoal,
    ) -> ProgressionTable:
        ...
