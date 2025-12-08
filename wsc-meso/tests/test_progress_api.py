# coding: utf-8

from fastapi.testclient import TestClient


from datetime import date  # noqa: F401
from pydantic import Field, StrictStr, field_validator  # noqa: F401
from typing import Any, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.get_progress_analytics200_response import GetProgressAnalytics200Response  # noqa: F401
from openapi_server.models.list_progress200_response import ListProgress200Response  # noqa: F401
from openapi_server.models.progress import Progress  # noqa: F401
from openapi_server.models.progress_create import ProgressCreate  # noqa: F401


def test_create_progress(client: TestClient):
    """Test case for create_progress

    Create a new progress entry
    """
    progress_create = {"date":"2000-01-23","unit":"unit","notes":"notes","metric_type":"weight","value":0.8008282}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/progress",
    #    headers=headers,
    #    json=progress_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_progress(client: TestClient):
    """Test case for delete_progress

    Delete progress entry
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/progress/{progress_id}".format(progress_id='progress_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_progress(client: TestClient):
    """Test case for get_progress

    Get progress entry by ID
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/progress/{progress_id}".format(progress_id='progress_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_progress_analytics(client: TestClient):
    """Test case for get_progress_analytics

    Get progress analytics
    """
    params = [("metric_type", 'metric_type_example'),     ("start_date", '2013-10-20'),     ("end_date", '2013-10-20')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/progress/analytics",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_progress(client: TestClient):
    """Test case for list_progress

    List progress entries
    """
    params = [("metric_type", 'metric_type_example'),     ("start_date", '2013-10-20'),     ("end_date", '2013-10-20'),     ("page", 1),     ("limit", 20)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/progress",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_progress(client: TestClient):
    """Test case for update_progress

    Update progress entry
    """
    progress_create = {"date":"2000-01-23","unit":"unit","notes":"notes","metric_type":"weight","value":0.8008282}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/progress/{progress_id}".format(progress_id='progress_id_example'),
    #    headers=headers,
    #    json=progress_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

