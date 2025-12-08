# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

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

class BaseProgressApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProgressApi.subclasses = BaseProgressApi.subclasses + (cls,)
    async def create_progress(
        self,
        progress_create: ProgressCreate,
    ) -> Progress:
        ...


    async def delete_progress(
        self,
        progress_id: StrictStr,
    ) -> None:
        ...


    async def get_progress(
        self,
        progress_id: StrictStr,
    ) -> Progress:
        ...


    async def get_progress_analytics(
        self,
        metric_type: StrictStr,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> GetProgressAnalytics200Response:
        ...


    async def list_progress(
        self,
        metric_type: Optional[StrictStr],
        start_date: Optional[date],
        end_date: Optional[date],
        page: Optional[Annotated[int, Field(strict=True, ge=1)]],
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> ListProgress200Response:
        ...


    async def update_progress(
        self,
        progress_id: StrictStr,
        progress_create: ProgressCreate,
    ) -> Progress:
        ...
