# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.users_api_base import BaseUsersApi
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
from openapi_server.models.update_current_user_request import UpdateCurrentUserRequest
from openapi_server.models.user import User
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/users/me",
    responses={
        200: {"model": User, "description": "User profile"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Users"],
    summary="Get current user profile",
    response_model_by_alias=True,
)
async def get_current_user(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> User:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().get_current_user()


@router.put(
    "/users/me",
    responses={
        200: {"model": User, "description": "User updated successfully"},
        400: {"model": Error, "description": "Invalid input"},
        401: {"model": Error, "description": "Unauthorized"},
    },
    tags=["Users"],
    summary="Update current user profile",
    response_model_by_alias=True,
)
async def update_current_user(
    update_current_user_request: UpdateCurrentUserRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> User:
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().update_current_user(update_current_user_request)
