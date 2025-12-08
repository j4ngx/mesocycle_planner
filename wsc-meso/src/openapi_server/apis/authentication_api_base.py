# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.error import Error
from openapi_server.models.token import Token
from openapi_server.models.user import User
from openapi_server.models.user_create import UserCreate
from openapi_server.models.user_login import UserLogin


class BaseAuthenticationApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthenticationApi.subclasses = BaseAuthenticationApi.subclasses + (cls,)
    async def login_user(
        self,
        user_login: UserLogin,
    ) -> Token:
        ...


    async def register_user(
        self,
        user_create: UserCreate,
    ) -> User:
        ...
