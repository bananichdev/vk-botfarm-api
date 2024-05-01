from functools import lru_cache

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import DB_FULL_URL


@lru_cache
def get_db_sessionmaker() -> async_sessionmaker:
    return async_sessionmaker(
        create_async_engine(DB_FULL_URL),
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
