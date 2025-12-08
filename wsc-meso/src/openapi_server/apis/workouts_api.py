# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.workouts_api_base import BaseWorkoutsApi
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
from pydantic import Field, StrictBool, StrictStr
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.complete_workout_request import CompleteWorkoutRequest
from openapi_server.models.error import Error
from openapi_server.models.list_workouts200_response import ListWorkouts200Response
from openapi_server.models.workout import Workout
from openapi_server.models.workout_create import WorkoutCreate
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/workouts/{workout_id}/complete",
    responses={
        200: {"model": Workout, "description": "Workout marked as completed"},
        404: {"model": Error, "description": "Workout not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Workouts"],
    summary="Mark workout as completed",
    response_model_by_alias=True,
)
async def complete_workout(
    workout_id: StrictStr = Path(..., description=""),
    complete_workout_request: Optional[CompleteWorkoutRequest] = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Workout:
    if not BaseWorkoutsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWorkoutsApi.subclasses[0]().complete_workout(workout_id, complete_workout_request)


@router.post(
    "/workouts",
    responses={
        201: {"model": Workout, "description": "Workout created successfully"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Workouts"],
    summary="Create a new workout",
    response_model_by_alias=True,
)
async def create_workout(
    workout_create: WorkoutCreate = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Workout:
    if not BaseWorkoutsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWorkoutsApi.subclasses[0]().create_workout(workout_create)


@router.delete(
    "/workouts/{workout_id}",
    responses={
        204: {"description": "Workout deleted successfully"},
        404: {"model": Error, "description": "Workout not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Workouts"],
    summary="Delete workout",
    response_model_by_alias=True,
)
async def delete_workout(
    workout_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseWorkoutsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWorkoutsApi.subclasses[0]().delete_workout(workout_id)


@router.get(
    "/workouts/{workout_id}",
    responses={
        200: {"model": Workout, "description": "Workout details"},
        404: {"model": Error, "description": "Workout not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Workouts"],
    summary="Get workout by ID",
    response_model_by_alias=True,
)
async def get_workout(
    workout_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Workout:
    if not BaseWorkoutsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWorkoutsApi.subclasses[0]().get_workout(workout_id)


@router.get(
    "/workouts",
    responses={
        200: {"model": ListWorkouts200Response, "description": "List of workouts"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Workouts"],
    summary="List workouts",
    response_model_by_alias=True,
)
async def list_workouts(
    mesocycle_id: Optional[StrictStr] = Query(None, description="", alias="mesocycle_id"),
    completed: Optional[StrictBool] = Query(None, description="", alias="completed"),
    page: Optional[Annotated[int, Field(strict=True, ge=1)]] = Query(1, description="", alias="page", ge=1),
    limit: Optional[Annotated[int, Field(le=100, strict=True)]] = Query(20, description="", alias="limit", le=100),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ListWorkouts200Response:
    if not BaseWorkoutsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWorkoutsApi.subclasses[0]().list_workouts(mesocycle_id, completed, page, limit)


@router.put(
    "/workouts/{workout_id}",
    responses={
        200: {"model": Workout, "description": "Workout updated successfully"},
        404: {"model": Error, "description": "Workout not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Workouts"],
    summary="Update workout",
    response_model_by_alias=True,
)
async def update_workout(
    workout_id: StrictStr = Path(..., description=""),
    workout_create: WorkoutCreate = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Workout:
    if not BaseWorkoutsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWorkoutsApi.subclasses[0]().update_workout(workout_id, workout_create)
