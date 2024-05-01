from fastapi import status
from httpx import AsyncClient

from utils.auth import AUTH_COOKIE_KEY, create_token
from utils.tests import check_response_status_code

BASE_URL = "/api/v1/botfarm/auth"


async def test_auth_login(client: AsyncClient):
    response = await client.post(f"{BASE_URL}.login")
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_200_OK,
        response_status_code=response.status_code,
        response_body=response_body,
    )

    access_token = await create_token()

    assert response_body == "OK"
    assert response.cookies[AUTH_COOKIE_KEY] == access_token


async def test_auth_logout(client: AsyncClient):
    response = await client.post(f"{BASE_URL}.logout")
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_200_OK,
        response_status_code=response.status_code,
        response_body=response_body,
    )

    assert response_body == "OK"
    assert response.cookies.get(AUTH_COOKIE_KEY) is None
