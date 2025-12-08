# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.progression_api_base import BaseProgressionApi
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
from openapi_server.models.error import Error
from openapi_server.models.progression_table import ProgressionTable
from openapi_server.models.training_goal import TrainingGoal


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/progression/{goal}",
    responses={
        200: {"model": ProgressionTable, "description": "Progression table for goal"},
        404: {"model": Error, "description": "Goal not found"},
    },
    tags=["Progression"],
    summary="Standard progression tables by training goal",
    response_model_by_alias=True,
)
async def get_progression_table(
    goal: TrainingGoal = Path(..., description=""),
) -> ProgressionTable:
    if not BaseProgressionApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressionApi.subclasses[0]().get_progression_table(goal)
