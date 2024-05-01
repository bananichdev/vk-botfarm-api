from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import UserModel
from schemas.v1.errors import (
    DBAPICallError,
    UserAlreadyExistsError,
    UserAlreadyLockedError,
    UserNotFoundError,
)
from schemas.v1.users import User, UserCreatingData, UserOperationOk
from settings import ENV
from utils.auth import password_context


async def get_user_by_id(
    db_sessionmaker: async_sessionmaker,
    id: UUID,
) -> User:
    try:
        async with db_sessionmaker.begin() as session:
            if (
                user_entity := await session.scalar(select(UserModel).where(UserModel.id == id))
            ) is None:
                raise UserNotFoundError(id=id)
    except DBAPIError as e:
        raise DBAPICallError(msg=f"can not get user with id={id}") from e

    return User(**user_entity.as_dict(exclude=["password"]))


async def get_users_list(
    db_sessionmaker: async_sessionmaker,
) -> list[User]:
    try:
        async with db_sessionmaker.begin() as session:
            user_entities_list = await session.scalars(select(UserModel))
    except DBAPIError as e:
        raise DBAPICallError(msg=f"can not get users list") from e

    return [User(**user_entity.as_dict(exclude=["password"])) for user_entity in user_entities_list]


async def create_user(
    db_sessionmaker: async_sessionmaker,
    user_data: UserCreatingData,
) -> User:
    try:
        async with db_sessionmaker.begin() as session:
            password = password_context.hash(user_data.password)
            user_entity = UserModel(
                **user_data.model_dump(exclude={"password"}), password=password, env=ENV
            )
            session.add(user_entity)
    except IntegrityError as e:
        raise UserAlreadyExistsError(login=user_data.login) from e
    except DBAPIError as e:
        raise DBAPICallError(msg=f"can not create user") from e

    return User(**user_entity.as_dict(exclude=["password"]))


async def lock_user(
    db_sessionmaker: async_sessionmaker,
    id: UUID,
) -> UserOperationOk:
    user = await get_user_by_id(db_sessionmaker=db_sessionmaker, id=id)
    if user.locktime is not None:
        raise UserAlreadyLockedError(id=id)

    try:
        async with db_sessionmaker.begin() as session:
            await session.execute(
                update(UserModel).where(UserModel.id == id).values(locktime=func.now())
            )
    except DBAPIError as e:
        await session.rollback()
        raise DBAPICallError(msg=f"can not lock user") from e

    return UserOperationOk(id=id)


async def unlock_user(
    db_sessionmaker: async_sessionmaker,
    id: UUID,
) -> UserOperationOk:
    await get_user_by_id(db_sessionmaker=db_sessionmaker, id=id)

    try:
        async with db_sessionmaker.begin() as session:
            await session.execute(update(UserModel).where(UserModel.id == id).values(locktime=None))
    except DBAPIError as e:
        await session.rollback()
        raise DBAPICallError(msg=f"can not unlock user") from e

    return UserOperationOk(id=id)
