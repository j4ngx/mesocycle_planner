# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.mesocycles_api_base import BaseMesocyclesApi
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
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.generate_ai_mesocycle_request import GenerateAIMesocycleRequest
from openapi_server.models.get_mesocycle_dashboard200_response import GetMesocycleDashboard200Response
from openapi_server.models.get_mesocycle_progression200_response import GetMesocycleProgression200Response
from openapi_server.models.get_microcycle200_response import GetMicrocycle200Response
from openapi_server.models.list_mesocycles200_response import ListMesocycles200Response
from openapi_server.models.mesocycle import Mesocycle
from openapi_server.models.mesocycle_create import MesocycleCreate
from openapi_server.models.mesocycle_status import MesocycleStatus
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/mesocycles",
    responses={
        201: {"model": Mesocycle, "description": "Mesocycle created successfully"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Create a new mesocycle",
    response_model_by_alias=True,
)
async def create_mesocycle(
    mesocycle_create: MesocycleCreate = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Mesocycle:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().create_mesocycle(mesocycle_create)


@router.delete(
    "/mesocycles/{mesocycle_id}",
    responses={
        204: {"description": "Mesocycle deleted successfully"},
        404: {"model": Error, "description": "Mesocycle not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Delete mesocycle",
    response_model_by_alias=True,
)
async def delete_mesocycle(
    mesocycle_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().delete_mesocycle(mesocycle_id)


@router.post(
    "/mesocycles/ai-generate",
    responses={
        200: {"model": Mesocycle, "description": "Complete AI-generated periodized mesocycle"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="AI Periodized Mesocycle Generator (DUP/Block optimized)",
    response_model_by_alias=True,
)
async def generate_ai_mesocycle(
    generate_ai_mesocycle_request: GenerateAIMesocycleRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Mesocycle:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().generate_ai_mesocycle(generate_ai_mesocycle_request)


@router.get(
    "/mesocycles/{mesocycle_id}",
    responses={
        200: {"model": Mesocycle, "description": "Mesocycle details"},
        404: {"model": Error, "description": "Mesocycle not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Get mesocycle by ID",
    response_model_by_alias=True,
)
async def get_mesocycle(
    mesocycle_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Mesocycle:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().get_mesocycle(mesocycle_id)


@router.get(
    "/mesocycles/{mesocycle_id}/dashboard",
    responses={
        200: {"model": GetMesocycleDashboard200Response, "description": "Dashboard data with analytics"},
        404: {"model": Error, "description": "Mesocycle not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Mesocycle progress dashboard + charts data",
    response_model_by_alias=True,
)
async def get_mesocycle_dashboard(
    mesocycle_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> GetMesocycleDashboard200Response:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().get_mesocycle_dashboard(mesocycle_id)


@router.get(
    "/mesocycles/{mesocycle_id}/progression",
    responses={
        200: {"model": GetMesocycleProgression200Response, "description": "Progression recommendations"},
        404: {"model": Error, "description": "Mesocycle not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Auto-progression recommendations for next week",
    response_model_by_alias=True,
)
async def get_mesocycle_progression(
    mesocycle_id: StrictStr = Path(..., description=""),
    week: Optional[Annotated[int, Field(strict=True, ge=1)]] = Query(None, description="", alias="week", ge=1),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> GetMesocycleProgression200Response:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().get_mesocycle_progression(mesocycle_id, week)


@router.get(
    "/mesocycles/{mesocycle_id}/microcycle/{microcycle_number}",
    responses={
        200: {"model": GetMicrocycle200Response, "description": "Microcycle details with training days"},
        404: {"model": Error, "description": "Microcycle not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Current microcycle details + weekly programming",
    response_model_by_alias=True,
)
async def get_microcycle(
    mesocycle_id: StrictStr = Path(..., description=""),
    microcycle_number: StrictInt = Path(..., description=""),
    week: Optional[Annotated[int, Field(strict=True, ge=1)]] = Query(None, description="", alias="week", ge=1),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> GetMicrocycle200Response:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().get_microcycle(mesocycle_id, microcycle_number, week)


@router.get(
    "/mesocycles",
    responses={
        200: {"model": ListMesocycles200Response, "description": "List of mesocycles"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="List all mesocycles for current user",
    response_model_by_alias=True,
)
async def list_mesocycles(
    status: Optional[MesocycleStatus] = Query(None, description="", alias="status"),
    page: Optional[Annotated[int, Field(strict=True, ge=1)]] = Query(1, description="", alias="page", ge=1),
    limit: Optional[Annotated[int, Field(le=100, strict=True)]] = Query(20, description="", alias="limit", le=100),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ListMesocycles200Response:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().list_mesocycles(status, page, limit)


@router.put(
    "/mesocycles/{mesocycle_id}",
    responses={
        200: {"model": Mesocycle, "description": "Mesocycle updated successfully"},
        404: {"model": Error, "description": "Mesocycle not found"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Mesocycles"],
    summary="Update mesocycle",
    response_model_by_alias=True,
)
async def update_mesocycle(
    mesocycle_id: StrictStr = Path(..., description=""),
    mesocycle_create: MesocycleCreate = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Mesocycle:
    if not BaseMesocyclesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMesocyclesApi.subclasses[0]().update_mesocycle(mesocycle_id, mesocycle_create)
