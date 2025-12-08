# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.token import Token  # noqa: F401
from openapi_server.models.user import User  # noqa: F401
from openapi_server.models.user_create import UserCreate  # noqa: F401
from openapi_server.models.user_login import UserLogin  # noqa: F401


def test_login_user(client: TestClient):
    """Test case for login_user

    Login user
    """
    user_login = {"password":"password","email":"email"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/login",
    #    headers=headers,
    #    json=user_login,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_register_user(client: TestClient):
    """Test case for register_user

    Register a new user
    """
    user_create = {"password":"password","full_name":"full_name","training_level":"beginner","email":"email","username":"username"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/register",
    #    headers=headers,
    #    json=user_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

