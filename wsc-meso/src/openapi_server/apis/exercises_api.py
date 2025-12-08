# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.exercises_api_base import BaseExercisesApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
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


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/exercises/{exercise_id}",
    responses={
        200: {"model": Exercise, "description": "Full exercise specification"},
        404: {"model": Error, "description": "Exercise not found"},
    },
    tags=["Exercises"],
    summary="Complete exercise details with biomechanical execution",
    response_model_by_alias=True,
)
async def get_exercise(
    exercise_id: StrictInt = Path(..., description=""),
) -> Exercise:
    if not BaseExercisesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseExercisesApi.subclasses[0]().get_exercise(exercise_id)


@router.get(
    "/exercises/{group}/recommended",
    responses={
        200: {"model": List[Exercise], "description": "Recommended exercises by group"},
    },
    tags=["Exercises"],
    summary="Top recommended exercises per muscle group",
    response_model_by_alias=True,
)
async def get_recommended_exercises(
    group: MuscleGroup = Path(..., description=""),
    level: Optional[TrainingLevel] = Query(None, description="", alias="level"),
) -> List[Exercise]:
    if not BaseExercisesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseExercisesApi.subclasses[0]().get_recommended_exercises(group, level)


@router.get(
    "/exercises",
    responses={
        200: {"model": ListExercises200Response, "description": "Paginated exercise list"},
    },
    tags=["Exercises"],
    summary="List exercises with advanced filtering",
    response_model_by_alias=True,
)
async def list_exercises(
    group: Optional[MuscleGroup] = Query(None, description="", alias="group"),
    type: Optional[ExerciseType] = Query(None, description="", alias="type"),
    page: Optional[Annotated[int, Field(strict=True, ge=1)]] = Query(1, description="", alias="page", ge=1),
    limit: Optional[Annotated[int, Field(le=100, strict=True)]] = Query(20, description="", alias="limit", le=100),
) -> ListExercises200Response:
    if not BaseExercisesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseExercisesApi.subclasses[0]().list_exercises(group, type, page, limit)


@router.get(
    "/exercises/search",
    responses={
        200: {"model": List[ExerciseSummary], "description": "Search results"},
    },
    tags=["Exercises"],
    summary="Full-text search exercises",
    response_model_by_alias=True,
)
async def search_exercises(
    q: StrictStr = Query(None, description="", alias="q"),
    limit: Optional[Annotated[int, Field(le=100, strict=True)]] = Query(20, description="", alias="limit", le=100),
) -> List[ExerciseSummary]:
    if not BaseExercisesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseExercisesApi.subclasses[0]().search_exercises(q, limit)
