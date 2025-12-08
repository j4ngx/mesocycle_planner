# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.error import Error
from openapi_server.models.update_current_user_request import UpdateCurrentUserRequest
from openapi_server.models.user import User
from openapi_server.security_api import get_token_bearerAuth

class BaseUsersApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseUsersApi.subclasses = BaseUsersApi.subclasses + (cls,)
    async def get_current_user(
        self,
    ) -> User:
        ...


    async def update_current_user(
        self,
        update_current_user_request: UpdateCurrentUserRequest,
    ) -> User:
        ...
