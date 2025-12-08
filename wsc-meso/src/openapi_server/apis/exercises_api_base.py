# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing import List, Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.exercise import Exercise
from openapi_server.models.exercise_summary import ExerciseSummary
from openapi_server.models.exercise_type import ExerciseType
from openapi_server.models.list_exercises200_response import ListExercises200Response
from openapi_server.models.muscle_group import MuscleGroup
from openapi_server.models.training_level import TrainingLevel


class BaseExercisesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseExercisesApi.subclasses = BaseExercisesApi.subclasses + (cls,)
    async def get_exercise(
        self,
        exercise_id: StrictInt,
    ) -> Exercise:
        ...


    async def get_recommended_exercises(
        self,
        group: MuscleGroup,
        level: Optional[TrainingLevel],
    ) -> List[Exercise]:
        ...


    async def list_exercises(
        self,
        group: Optional[MuscleGroup],
        type: Optional[ExerciseType],
        page: Optional[Annotated[int, Field(strict=True, ge=1)]],
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> ListExercises200Response:
        ...


    async def search_exercises(
        self,
        q: StrictStr,
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> List[ExerciseSummary]:
        ...
