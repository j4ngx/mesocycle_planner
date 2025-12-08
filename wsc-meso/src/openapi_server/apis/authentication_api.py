# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.authentication_api_base import BaseAuthenticationApi
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
from openapi_server.models.token import Token
from openapi_server.models.user import User
from openapi_server.models.user_create import UserCreate
from openapi_server.models.user_login import UserLogin


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/auth/login",
    responses={
        200: {"model": Token, "description": "Login successful"},
        401: {"model": Error, "description": "Invalid credentials"},
    },
    tags=["Authentication"],
    summary="Login user",
    response_model_by_alias=True,
)
async def login_user(
    user_login: UserLogin = Body(None, description=""),
) -> Token:
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().login_user(user_login)


@router.post(
    "/auth/register",
    responses={
        201: {"model": User, "description": "User created successfully"},
        400: {"model": Error, "description": "Invalid input"},
        409: {"model": Error, "description": "User already exists"},
    },
    tags=["Authentication"],
    summary="Register a new user",
    response_model_by_alias=True,
)
async def register_user(
    user_create: UserCreate = Body(None, description=""),
) -> User:
    if not BaseAuthenticationApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthenticationApi.subclasses[0]().register_user(user_create)
