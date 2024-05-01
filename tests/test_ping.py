from fastapi import status
from httpx import AsyncClient

from settings import NAME
from utils.tests import check_response_status_code

BASE_URL = "/api/v1/botfarm"


async def test_botfarm_ping(client: AsyncClient):
    response = await client.get(f"{BASE_URL}/ping")
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_200_OK,
        response_status_code=response.status_code,
        response_body=response_body,
    )
    assert response_body == f"Ping service {NAME}"


async def test_botfarm_checkPerformance(client: AsyncClient):
    response = await client.get(f"{BASE_URL}/checkPerformance")
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_200_OK,
        response_status_code=response.status_code,
        response_body=response_body,
    )
    assert response_body == f"Service {NAME} is ready to process requests"
