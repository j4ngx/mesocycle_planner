# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.update_current_user_request import UpdateCurrentUserRequest  # noqa: F401
from openapi_server.models.user import User  # noqa: F401


def test_get_current_user(client: TestClient):
    """Test case for get_current_user

    Get current user profile
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/users/me",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_current_user(client: TestClient):
    """Test case for update_current_user

    Update current user profile
    """
    update_current_user_request = openapi_server.UpdateCurrentUserRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/users/me",
    #    headers=headers,
    #    json=update_current_user_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

