# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBool, StrictStr
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.complete_workout_request import CompleteWorkoutRequest
from openapi_server.models.error import Error
from openapi_server.models.list_workouts200_response import ListWorkouts200Response
from openapi_server.models.workout import Workout
from openapi_server.models.workout_create import WorkoutCreate
from openapi_server.security_api import get_token_bearerAuth

class BaseWorkoutsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseWorkoutsApi.subclasses = BaseWorkoutsApi.subclasses + (cls,)
    async def complete_workout(
        self,
        workout_id: StrictStr,
        complete_workout_request: Optional[CompleteWorkoutRequest],
    ) -> Workout:
        ...


    async def create_workout(
        self,
        workout_create: WorkoutCreate,
    ) -> Workout:
        ...


    async def delete_workout(
        self,
        workout_id: StrictStr,
    ) -> None:
        ...


    async def get_workout(
        self,
        workout_id: StrictStr,
    ) -> Workout:
        ...


    async def list_workouts(
        self,
        mesocycle_id: Optional[StrictStr],
        completed: Optional[StrictBool],
        page: Optional[Annotated[int, Field(strict=True, ge=1)]],
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> ListWorkouts200Response:
        ...


    async def update_workout(
        self,
        workout_id: StrictStr,
        workout_create: WorkoutCreate,
    ) -> Workout:
        ...
