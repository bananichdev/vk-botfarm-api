from datetime import datetime
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette import status

from database.models import UserModel
from settings import ENV
from utils.auth import create_token, AUTH_COOKIE_KEY
from utils.tests import check_response_status_code

BASE_URL = "/api/v1/botfarm/users/{0}.releaseLock"


@pytest.mark.parametrize(
    "user_entity",
    [
        UserModel(
            login="example_1@test.com",
            password="test_password",
            project_id=uuid4(),
            env=ENV,
            domain="regular",
            locktime=datetime.now(),
        ),
        UserModel(
            login="example_2@test.com",
            password="test_password",
            project_id=uuid4(),
            env=ENV,
            domain="canary",
            locktime=datetime.now(),
        ),
    ],
)
async def test_unlock_user_success(client: AsyncClient, db_sessionmaker: async_sessionmaker, user_entity: UserModel):
    async with db_sessionmaker.begin() as session:
        session.add(user_entity)

    access_token = await create_token()
    client.cookies = {AUTH_COOKIE_KEY: access_token}
    response = await client.patch(BASE_URL.format(str(user_entity.id)))
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_200_OK,
        response_status_code=response.status_code,
        response_body=response_body,
    )

    async with db_sessionmaker.begin() as session:
        user_entity = await session.scalar(
            select(UserModel).where(UserModel.id == user_entity.id)
        )

    assert response_body["id"] == str(user_entity.id)
    assert user_entity.locktime is None


@pytest.mark.parametrize(
    "bad_id",
    [
        "123",
        "abcdef",
    ],
)
async def test_unlock_user_bad_request(client: AsyncClient, bad_id: str):
    access_token = await create_token()
    client.cookies = {AUTH_COOKIE_KEY: access_token}
    response = await client.patch(BASE_URL.format(bad_id))
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_400_BAD_REQUEST,
        response_status_code=response.status_code,
        response_body=response_body,
    )


async def test_unlock_user_unauthorized(client: AsyncClient):
    client.cookies = {}
    response = await client.patch(BASE_URL.format(uuid4()))
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_401_UNAUTHORIZED,
        response_status_code=response.status_code,
        response_body=response_body,
    )


async def test_unlock_user_forbidden(client: AsyncClient):
    client.cookies = {AUTH_COOKIE_KEY: "123"}
    response = await client.patch(BASE_URL.format(uuid4()))
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_403_FORBIDDEN,
        response_status_code=response.status_code,
        response_body=response_body,
    )
