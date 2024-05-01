from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.connection import get_db_sessionmaker
from database.controllers.users import create_user, get_users_list, lock_user, unlock_user
from schemas.v1.users import User, UserCreatingData, UserOperationOk
from utils.auth import check_token

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_list_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    _: Annotated[None, Depends(check_token)],
) -> list[User]:
    """Return all users list"""
    return await get_users_list(db_sessionmaker=db_sessionmaker)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    _: Annotated[None, Depends(check_token)],
    user_data: UserCreatingData,
) -> User:
    """Create and return a new user"""
    return await create_user(db_sessionmaker=db_sessionmaker, user_data=user_data)


@router.patch("/{id}.acquireLock", status_code=status.HTTP_200_OK)
async def acquire_lock_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    _: Annotated[None, Depends(check_token)],
    id: UUID,
) -> UserOperationOk:
    """Lock user with the required id and return user id"""
    return await lock_user(db_sessionmaker=db_sessionmaker, id=id)


@router.patch("/{id}.releaseLock", status_code=status.HTTP_200_OK)
async def release_lock_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
    _: Annotated[None, Depends(check_token)],
    id: UUID,
) -> UserOperationOk:
    """Unlock user with the required id and return user id"""
    return await unlock_user(db_sessionmaker=db_sessionmaker, id=id)
