# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.progression_table import ProgressionTable  # noqa: F401
from openapi_server.models.training_goal import TrainingGoal  # noqa: F401


def test_get_progression_table(client: TestClient):
    """Test case for get_progression_table

    Standard progression tables by training goal
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/progression/{goal}".format(goal=openapi_server.TrainingGoal()),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

