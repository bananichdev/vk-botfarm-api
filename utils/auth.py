from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyCookie
from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas.v1.errors import AccessDeniedError, TokenIncorrectError, TokenNotFoundError
from settings import ALGORITHM, HASH_ROUNDS, SECRET_KEY

AUTH_COOKIE_KEY = "authorization"

cookie_apikey = APIKeyCookie(name=AUTH_COOKIE_KEY, auto_error=False)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=HASH_ROUNDS)


async def create_token() -> str:
    """Create and return a JWT token"""
    to_encode = {"can_use": True}
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


async def check_token(access_token: Annotated[str, Depends(cookie_apikey)]) -> None:
    """Check JWT token"""
    if access_token is None:
        raise TokenNotFoundError()

    try:
        can_use = jwt.decode(access_token, SECRET_KEY, ALGORITHM).get("can_use")
        if not can_use:
            raise AccessDeniedError()
    except JWTError as e:
        raise TokenIncorrectError() from e
