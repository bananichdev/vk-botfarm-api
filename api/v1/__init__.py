from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.connection import get_db_sessionmaker
from database.controllers.ping import ping_database
from settings import NAME
from utils.errors import __validation_exception_handler

from .auth import router as auth_router
from .users import router as users_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    return __validation_exception_handler(exc)


app.include_router(
    users_router,
    prefix="/users",
)

app.include_router(
    auth_router,
    prefix="/auth",
)


@app.get("/ping")
async def ping_handler() -> str:
    """Return string if service is alive"""
    return f"Ping service {NAME}"


@app.get("/checkPerformance")
async def check_performance_handler(
    db_sessionmaker: Annotated[async_sessionmaker, Depends(get_db_sessionmaker)],
) -> str:
    """Return string if service is ready to process requests"""
    await ping_database(db_sessionmaker=db_sessionmaker)
    return f"Service {NAME} is ready to process requests"
