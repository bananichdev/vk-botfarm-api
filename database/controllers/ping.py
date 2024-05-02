from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker

from schemas.v1.errors import DBAPICallError


async def ping_database(
    db_sessionmaker: async_sessionmaker,
) -> None:
    """Ping the database and return None"""
    try:
        async with db_sessionmaker.begin():
            return
    except DBAPIError as e:
        raise DBAPICallError(msg="database is dead") from e
