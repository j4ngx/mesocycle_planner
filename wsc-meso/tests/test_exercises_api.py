# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt, StrictStr  # noqa: F401
from typing import List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.exercise import Exercise  # noqa: F401
from openapi_server.models.exercise_summary import ExerciseSummary  # noqa: F401
from openapi_server.models.exercise_type import ExerciseType  # noqa: F401
from openapi_server.models.list_exercises200_response import ListExercises200Response  # noqa: F401
from openapi_server.models.muscle_group import MuscleGroup  # noqa: F401
from openapi_server.models.training_level import TrainingLevel  # noqa: F401


def test_get_exercise(client: TestClient):
    """Test case for get_exercise

    Complete exercise details with biomechanical execution
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/exercises/{exercise_id}".format(exercise_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_recommended_exercises(client: TestClient):
    """Test case for get_recommended_exercises

    Top recommended exercises per muscle group
    """
    params = [("level", openapi_server.TrainingLevel())]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/exercises/{group}/recommended".format(group=openapi_server.MuscleGroup()),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_exercises(client: TestClient):
    """Test case for list_exercises

    List exercises with advanced filtering
    """
    params = [("group", openapi_server.MuscleGroup()),     ("type", openapi_server.ExerciseType()),     ("page", 1),     ("limit", 20)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/exercises",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_search_exercises(client: TestClient):
    """Test case for search_exercises

    Full-text search exercises
    """
    params = [("q", 'bench press'),     ("limit", 20)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/exercises/search",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

