# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt, StrictStr  # noqa: F401
from typing import Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.get_user_progress_stats200_response import GetUserProgressStats200Response  # noqa: F401
from openapi_server.models.smart_log_session200_response import SmartLogSession200Response  # noqa: F401
from openapi_server.models.smart_log_session_request import SmartLogSessionRequest  # noqa: F401
from openapi_server.models.training_session import TrainingSession  # noqa: F401


def test_get_user_progress_stats(client: TestClient):
    """Test case for get_user_progress_stats

    User strength progression analytics
    """
    params = [("exercise_id", 56),     ("weeks_back", 12)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/stats/progress/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_log_session(client: TestClient):
    """Test case for log_session

    Log completed training session
    """
    training_session = {"date":"2000-01-23","mesocycle_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","microcycle_id":6,"id":0,"week_number":1,"exercises_performed":[{"exercise_id":5,"planned_sets":5,"sets_performed":[{"weight_kg":80.0,"reps_in_reserve":2,"reps_achieved":10,"actual_rpe":8},{"weight_kg":80.0,"reps_in_reserve":2,"reps_achieved":10,"actual_rpe":8}]},{"exercise_id":5,"planned_sets":5,"sets_performed":[{"weight_kg":80.0,"reps_in_reserve":2,"reps_achieved":10,"actual_rpe":8},{"weight_kg":80.0,"reps_in_reserve":2,"reps_achieved":10,"actual_rpe":8}]}]}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/sessions",
    #    headers=headers,
    #    json=training_session,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_smart_log_session(client: TestClient):
    """Test case for smart_log_session

    Smart session logging with AI progression adjustment
    """
    smart_log_session_request = openapi_server.SmartLogSessionRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/sessions/smart-log",
    #    headers=headers,
    #    json=smart_log_session_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

