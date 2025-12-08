# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt, StrictStr  # noqa: F401
from typing import Any, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.generate_ai_mesocycle_request import GenerateAIMesocycleRequest  # noqa: F401
from openapi_server.models.get_mesocycle_dashboard200_response import GetMesocycleDashboard200Response  # noqa: F401
from openapi_server.models.get_mesocycle_progression200_response import GetMesocycleProgression200Response  # noqa: F401
from openapi_server.models.get_microcycle200_response import GetMicrocycle200Response  # noqa: F401
from openapi_server.models.list_mesocycles200_response import ListMesocycles200Response  # noqa: F401
from openapi_server.models.mesocycle import Mesocycle  # noqa: F401
from openapi_server.models.mesocycle_create import MesocycleCreate  # noqa: F401
from openapi_server.models.mesocycle_status import MesocycleStatus  # noqa: F401


def test_create_mesocycle(client: TestClient):
    """Test case for create_mesocycle

    Create a new mesocycle
    """
    mesocycle_create = {"end_date":"2000-01-23","periodization_model":"linear","goal":"strength","microcycles":[{"phase":"accumulation","reps_range":"12-15","microcycle_number":1,"weekly_volume_multiplier":1.2,"frequency_per_week":5,"mesocycle_id":6,"rir":2,"id":0,"week_start":1,"week_end":2,"sets_range":"3-4","intensity_range":{"max_pct":0.7,"min_pct":0.6}},{"phase":"accumulation","reps_range":"12-15","microcycle_number":1,"weekly_volume_multiplier":1.2,"frequency_per_week":5,"mesocycle_id":6,"rir":2,"id":0,"week_start":1,"week_end":2,"sets_range":"3-4","intensity_range":{"max_pct":0.7,"min_pct":0.6}}],"name":"name","description":"description","weekly_frequency":3,"duration_weeks":11,"start_date":"2000-01-23"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/mesocycles",
    #    headers=headers,
    #    json=mesocycle_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_mesocycle(client: TestClient):
    """Test case for delete_mesocycle

    Delete mesocycle
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/mesocycles/{mesocycle_id}".format(mesocycle_id='mesocycle_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_generate_ai_mesocycle(client: TestClient):
    """Test case for generate_ai_mesocycle

    AI Periodized Mesocycle Generator (DUP/Block optimized)
    """
    generate_ai_mesocycle_request = openapi_server.GenerateAIMesocycleRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/mesocycles/ai-generate",
    #    headers=headers,
    #    json=generate_ai_mesocycle_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_mesocycle(client: TestClient):
    """Test case for get_mesocycle

    Get mesocycle by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/mesocycles/{mesocycle_id}".format(mesocycle_id='mesocycle_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_mesocycle_dashboard(client: TestClient):
    """Test case for get_mesocycle_dashboard

    Mesocycle progress dashboard + charts data
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/mesocycles/{mesocycle_id}/dashboard".format(mesocycle_id='mesocycle_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_mesocycle_progression(client: TestClient):
    """Test case for get_mesocycle_progression

    Auto-progression recommendations for next week
    """
    params = [("week", 56)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/mesocycles/{mesocycle_id}/progression".format(mesocycle_id='mesocycle_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_microcycle(client: TestClient):
    """Test case for get_microcycle

    Current microcycle details + weekly programming
    """
    params = [("week", 56)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/mesocycles/{mesocycle_id}/microcycle/{microcycle_number}".format(mesocycle_id='mesocycle_id_example', microcycle_number=56),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_mesocycles(client: TestClient):
    """Test case for list_mesocycles

    List all mesocycles for current user
    """
    params = [("status", openapi_server.MesocycleStatus()),     ("page", 1),     ("limit", 20)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/mesocycles",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_mesocycle(client: TestClient):
    """Test case for update_mesocycle

    Update mesocycle
    """
    mesocycle_create = {"end_date":"2000-01-23","periodization_model":"linear","goal":"strength","microcycles":[{"phase":"accumulation","reps_range":"12-15","microcycle_number":1,"weekly_volume_multiplier":1.2,"frequency_per_week":5,"mesocycle_id":6,"rir":2,"id":0,"week_start":1,"week_end":2,"sets_range":"3-4","intensity_range":{"max_pct":0.7,"min_pct":0.6}},{"phase":"accumulation","reps_range":"12-15","microcycle_number":1,"weekly_volume_multiplier":1.2,"frequency_per_week":5,"mesocycle_id":6,"rir":2,"id":0,"week_start":1,"week_end":2,"sets_range":"3-4","intensity_range":{"max_pct":0.7,"min_pct":0.6}}],"name":"name","description":"description","weekly_frequency":3,"duration_weeks":11,"start_date":"2000-01-23"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/mesocycles/{mesocycle_id}".format(mesocycle_id='mesocycle_id_example'),
    #    headers=headers,
    #    json=mesocycle_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

