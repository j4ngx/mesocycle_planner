# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictBool, StrictStr  # noqa: F401
from typing import Any, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.complete_workout_request import CompleteWorkoutRequest  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.list_workouts200_response import ListWorkouts200Response  # noqa: F401
from openapi_server.models.workout import Workout  # noqa: F401
from openapi_server.models.workout_create import WorkoutCreate  # noqa: F401


def test_complete_workout(client: TestClient):
    """Test case for complete_workout

    Mark workout as completed
    """
    complete_workout_request = openapi_server.CompleteWorkoutRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/workouts/{workout_id}/complete".format(workout_id='workout_id_example'),
    #    headers=headers,
    #    json=complete_workout_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_workout(client: TestClient):
    """Test case for create_workout

    Create a new workout
    """
    workout_create = {"split":"push","notes":"notes","mesocycle_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","microcycle_id":0,"name":"name","description":"description","scheduled_date":"2000-01-23T04:56:07.000+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/workouts",
    #    headers=headers,
    #    json=workout_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_workout(client: TestClient):
    """Test case for delete_workout

    Delete workout
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/workouts/{workout_id}".format(workout_id='workout_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_workout(client: TestClient):
    """Test case for get_workout

    Get workout by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/workouts/{workout_id}".format(workout_id='workout_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_workouts(client: TestClient):
    """Test case for list_workouts

    List workouts
    """
    params = [("mesocycle_id", 'mesocycle_id_example'),     ("completed", True),     ("page", 1),     ("limit", 20)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/workouts",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_workout(client: TestClient):
    """Test case for update_workout

    Update workout
    """
    workout_create = {"split":"push","notes":"notes","mesocycle_id":"046b6c7f-0b8a-43b9-b35d-6489e6daee91","microcycle_id":0,"name":"name","description":"description","scheduled_date":"2000-01-23T04:56:07.000+00:00"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/workouts/{workout_id}".format(workout_id='workout_id_example'),
    #    headers=headers,
    #    json=workout_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

