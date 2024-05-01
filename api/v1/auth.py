from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from settings import DEFAULT_COOKIE_SETTINGS
from utils.auth import AUTH_COOKIE_KEY, create_token

router = APIRouter()


@router.post(".login", status_code=status.HTTP_200_OK)
async def login_handler() -> JSONResponse:
    """Return OK response with a token in a cookies"""
    access_token = await create_token()
    response = JSONResponse(content="OK")
    response.set_cookie(AUTH_COOKIE_KEY, access_token, **DEFAULT_COOKIE_SETTINGS)

    return response


@router.post(".logout", status_code=status.HTTP_200_OK)
async def logout_handler() -> JSONResponse:
    """Return OK response and remove a token from a cookies"""
    response = JSONResponse(content="OK")
    response.delete_cookie(AUTH_COOKIE_KEY, **DEFAULT_COOKIE_SETTINGS)

    return response
