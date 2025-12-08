# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing import Optional
from typing_extensions import Annotated
from openapi_server.models.error import Error
from openapi_server.models.get_user_progress_stats200_response import GetUserProgressStats200Response
from openapi_server.models.smart_log_session200_response import SmartLogSession200Response
from openapi_server.models.smart_log_session_request import SmartLogSessionRequest
from openapi_server.models.training_session import TrainingSession
from openapi_server.security_api import get_token_bearerAuth

class BaseTrackingApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseTrackingApi.subclasses = BaseTrackingApi.subclasses + (cls,)
    async def get_user_progress_stats(
        self,
        user_id: StrictStr,
        exercise_id: Optional[StrictInt],
        weeks_back: Optional[Annotated[int, Field(le=52, strict=True)]],
    ) -> GetUserProgressStats200Response:
        ...


    async def log_session(
        self,
        training_session: TrainingSession,
    ) -> TrainingSession:
        ...


    async def smart_log_session(
        self,
        smart_log_session_request: SmartLogSessionRequest,
    ) -> SmartLogSession200Response:
        ...
