import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from api.v1 import app as api_v1_app
from database.connection import get_db_sessionmaker
from database.models import BaseModel
from main import app as main_app
from settings import TEST_DB_FULL_URL
from utils.auth import AUTH_COOKIE_KEY, create_token


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=main_app), base_url="http://testserver") as client:
        access_token = await create_token()
        client.cookies = {AUTH_COOKIE_KEY: access_token}
        yield client


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    return create_async_engine(TEST_DB_FULL_URL)


@pytest.fixture(scope="session")
def db_sessionmaker(db_engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        db_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


@pytest.fixture(autouse=True)
async def prepare_db_tables(db_engine: AsyncEngine):
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
def dependency_overrides(db_sessionmaker: async_sessionmaker):
    api_v1_app.dependency_overrides[get_db_sessionmaker] = lambda: db_sessionmaker
