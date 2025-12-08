# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

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

class BaseMesocyclesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseMesocyclesApi.subclasses = BaseMesocyclesApi.subclasses + (cls,)
    async def create_mesocycle(
        self,
        mesocycle_create: MesocycleCreate,
    ) -> Mesocycle:
        ...


    async def delete_mesocycle(
        self,
        mesocycle_id: StrictStr,
    ) -> None:
        ...


    async def generate_ai_mesocycle(
        self,
        generate_ai_mesocycle_request: GenerateAIMesocycleRequest,
    ) -> Mesocycle:
        ...


    async def get_mesocycle(
        self,
        mesocycle_id: StrictStr,
    ) -> Mesocycle:
        ...


    async def get_mesocycle_dashboard(
        self,
        mesocycle_id: StrictStr,
    ) -> GetMesocycleDashboard200Response:
        ...


    async def get_mesocycle_progression(
        self,
        mesocycle_id: StrictStr,
        week: Optional[Annotated[int, Field(strict=True, ge=1)]],
    ) -> GetMesocycleProgression200Response:
        ...


    async def get_microcycle(
        self,
        mesocycle_id: StrictStr,
        microcycle_number: StrictInt,
        week: Optional[Annotated[int, Field(strict=True, ge=1)]],
    ) -> GetMicrocycle200Response:
        ...


    async def list_mesocycles(
        self,
        status: Optional[MesocycleStatus],
        page: Optional[Annotated[int, Field(strict=True, ge=1)]],
        limit: Optional[Annotated[int, Field(le=100, strict=True)]],
    ) -> ListMesocycles200Response:
        ...


    async def update_mesocycle(
        self,
        mesocycle_id: StrictStr,
        mesocycle_create: MesocycleCreate,
    ) -> Mesocycle:
        ...
