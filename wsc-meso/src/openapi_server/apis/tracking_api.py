# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.tracking_api_base import BaseTrackingApi
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
from typing import Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.get_user_progress_stats200_response import GetUserProgressStats200Response
from openapi_server.models.smart_log_session200_response import SmartLogSession200Response
from openapi_server.models.smart_log_session_request import SmartLogSessionRequest
from openapi_server.models.training_session import TrainingSession
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/stats/progress/{user_id}",
    responses={
        200: {"model": GetUserProgressStats200Response, "description": "Complete progression analytics"},
        404: {"model": Error, "description": "User not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Tracking"],
    summary="User strength progression analytics",
    response_model_by_alias=True,
)
async def get_user_progress_stats(
    user_id: StrictStr = Path(..., description=""),
    exercise_id: Optional[StrictInt] = Query(None, description="", alias="exercise_id"),
    weeks_back: Optional[Annotated[int, Field(le=52, strict=True)]] = Query(12, description="", alias="weeks_back", le=52),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> GetUserProgressStats200Response:
    if not BaseTrackingApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTrackingApi.subclasses[0]().get_user_progress_stats(user_id, exercise_id, weeks_back)


@router.post(
    "/sessions",
    responses={
        201: {"model": TrainingSession, "description": "Session recorded successfully"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Tracking"],
    summary="Log completed training session",
    response_model_by_alias=True,
)
async def log_session(
    training_session: TrainingSession = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> TrainingSession:
    if not BaseTrackingApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTrackingApi.subclasses[0]().log_session(training_session)


@router.post(
    "/sessions/smart-log",
    responses={
        200: {"model": SmartLogSession200Response, "description": "Session logged + next session recommendations"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Tracking"],
    summary="Smart session logging with AI progression adjustment",
    response_model_by_alias=True,
)
async def smart_log_session(
    smart_log_session_request: SmartLogSessionRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> SmartLogSession200Response:
    if not BaseTrackingApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTrackingApi.subclasses[0]().smart_log_session(smart_log_session_request)
