# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.progress_api_base import BaseProgressApi
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
from datetime import date
from pydantic import Field, StrictStr, field_validator
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.get_progress_analytics200_response import GetProgressAnalytics200Response
from openapi_server.models.list_progress200_response import ListProgress200Response
from openapi_server.models.progress import Progress
from openapi_server.models.progress_create import ProgressCreate
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/progress",
    responses={
        201: {"model": Progress, "description": "Progress entry created successfully"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Progress"],
    summary="Create a new progress entry",
    response_model_by_alias=True,
)
async def create_progress(
    progress_create: ProgressCreate = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Progress:
    if not BaseProgressApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressApi.subclasses[0]().create_progress(progress_create)


@router.delete(
    "/progress/{progress_id}",
    responses={
        204: {"description": "Progress entry deleted successfully"},
        404: {"model": Error, "description": "Progress entry not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Progress"],
    summary="Delete progress entry",
    response_model_by_alias=True,
)
async def delete_progress(
    progress_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseProgressApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressApi.subclasses[0]().delete_progress(progress_id)


@router.get(
    "/progress/{progress_id}",
    responses={
        200: {"model": Progress, "description": "Progress entry details"},
        404: {"model": Error, "description": "Progress entry not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Progress"],
    summary="Get progress entry by ID",
    response_model_by_alias=True,
)
async def get_progress(
    progress_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Progress:
    if not BaseProgressApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressApi.subclasses[0]().get_progress(progress_id)


@router.get(
    "/progress/analytics",
    responses={
        200: {"model": GetProgressAnalytics200Response, "description": "Progress analytics"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Progress"],
    summary="Get progress analytics",
    response_model_by_alias=True,
)
async def get_progress_analytics(
    metric_type: StrictStr = Query(None, description="", alias="metric_type"),
    start_date: Optional[date] = Query(None, description="", alias="start_date"),
    end_date: Optional[date] = Query(None, description="", alias="end_date"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> GetProgressAnalytics200Response:
    if not BaseProgressApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressApi.subclasses[0]().get_progress_analytics(metric_type, start_date, end_date)


@router.get(
    "/progress",
    responses={
        200: {"model": ListProgress200Response, "description": "List of progress entries"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Progress"],
    summary="List progress entries",
    response_model_by_alias=True,
)
async def list_progress(
    metric_type: Optional[StrictStr] = Query(None, description="", alias="metric_type"),
    start_date: Optional[date] = Query(None, description="", alias="start_date"),
    end_date: Optional[date] = Query(None, description="", alias="end_date"),
    page: Optional[Annotated[int, Field(strict=True, ge=1)]] = Query(1, description="", alias="page", ge=1),
    limit: Optional[Annotated[int, Field(le=100, strict=True)]] = Query(20, description="", alias="limit", le=100),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ListProgress200Response:
    if not BaseProgressApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressApi.subclasses[0]().list_progress(metric_type, start_date, end_date, page, limit)


@router.put(
    "/progress/{progress_id}",
    responses={
        200: {"model": Progress, "description": "Progress entry updated successfully"},
        404: {"model": Error, "description": "Progress entry not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Progress"],
    summary="Update progress entry",
    response_model_by_alias=True,
)
async def update_progress(
    progress_id: StrictStr = Path(..., description=""),
    progress_create: ProgressCreate = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Progress:
    if not BaseProgressApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseProgressApi.subclasses[0]().update_progress(progress_id, progress_create)
