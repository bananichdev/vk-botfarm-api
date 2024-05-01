from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import UserModel
from schemas.v1.users import User, UserCreatingData
from utils.auth import AUTH_COOKIE_KEY, create_token
from utils.tests import check_response_status_code

BASE_URL = "/api/v1/botfarm/users/"


@pytest.mark.parametrize(
    "user_data",
    [
        UserCreatingData(
            login="example1@test.com", password="test_password", project_id=uuid4(), domain="canary"
        ),
        UserCreatingData(
            login="example1@test.com",
            password="test_password",
            project_id=uuid4(),
            domain="regular",
        ),
    ],
)
async def test_post_user_success(
    client: AsyncClient, db_sessionmaker: async_sessionmaker, user_data: UserCreatingData
):
    access_token = await create_token()
    client.cookies = {AUTH_COOKIE_KEY: access_token}
    response = await client.post(
        BASE_URL, json=user_data.model_dump(mode="json")
    )
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_201_CREATED,
        response_status_code=response.status_code,
        response_body=response_body,
    )

    async with db_sessionmaker.begin() as session:
        user_entity = await session.scalar(
            select(UserModel).where(UserModel.login == user_data.login)
        )

    assert User(**response_body) == User(**user_entity.as_dict(exclude=["password"]))


@pytest.mark.parametrize(
    "bad_data",
    [
        {"user": "123"},
        {
            "login": "123",
            "password": "test_password",
            "project_id": str(uuid4()),
            "domain": "regular",
        },
    ],
)
async def test_post_user_bad_request(client: AsyncClient, bad_data: dict):
    access_token = await create_token()
    client.cookies = {AUTH_COOKIE_KEY: access_token}
    response = await client.post(BASE_URL, json=bad_data)
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_400_BAD_REQUEST,
        response_status_code=response.status_code,
        response_body=response_body,
    )


async def test_post_user_unauthorized(client: AsyncClient):
    client.cookies = {}
    response = await client.post(BASE_URL)
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_401_UNAUTHORIZED,
        response_status_code=response.status_code,
        response_body=response_body,
    )


async def test_post_user_forbidden(client: AsyncClient):
    client.cookies = {AUTH_COOKIE_KEY: "123"}
    response = await client.post(BASE_URL)
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_403_FORBIDDEN,
        response_status_code=response.status_code,
        response_body=response_body,
    )
