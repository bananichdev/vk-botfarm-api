from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import UserModel
from schemas.v1.users import User
from settings import ENV
from utils.tests import check_response_status_code

BASE_URL = "/api/v1/botfarm/users/"


@pytest.mark.parametrize(
    "user_entities_list",
    [
        [
            UserModel(
                login="example_1@test.com",
                password="test_password",
                project_id=uuid4(),
                env=ENV,
                domain="regular",
            ),
            UserModel(
                login="example_2@test.com",
                password="test_password",
                project_id=uuid4(),
                env=ENV,
                domain="canary",
                locktime=datetime.now(timezone.utc),
            ),
            UserModel(
                login="example_3@test.com",
                password="test_password",
                project_id=uuid4(),
                env=ENV,
                domain="regular",
            ),
        ],
    ],
)
async def test_get_user_entities_list(
    client: AsyncClient, db_sessionmaker: async_sessionmaker, user_entities_list: list[UserModel]
):
    async with db_sessionmaker.begin() as session:
        created_ad = datetime.now(timezone.utc)
        for user_entity in user_entities_list:
            user_entity.created_ad = created_ad
            session.add(user_entity)

    response = await client.get(BASE_URL)
    response_body = response.json()

    check_response_status_code(
        expect_status_code=status.HTTP_200_OK,
        response_status_code=response.status_code,
        response_body=response_body,
    )

    assert [User(**user) for user in response_body] == [
        User(**user_entity.as_dict(exclude=["password"])) for user_entity in user_entities_list
    ]
