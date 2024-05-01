from uuid import UUID

from fastapi import HTTPException, status


class DBAPICallError(HTTPException):
    def __init__(self, msg: str = "..."):
        super().__init__(
            detail=f"DB api call failed: {msg}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class UserError(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )


class UserNotFoundError(UserError):
    def __init__(self, id: UUID):
        super().__init__(
            detail=f"User with id={id} was not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UserAlreadyExistsError(UserError):
    def __init__(self, login: str):
        super().__init__(
            detail=f"User with login={login} already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UserAlreadyLockedError(UserError):
    def __init__(self, id: UUID):
        super().__init__(
            detail=f"User with id={id} already locked", status_code=status.HTTP_400_BAD_REQUEST
        )


class AuthError(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            detail=detail,
            status_code=status_code,
        )


class TokenNotFoundError(AuthError):
    def __init__(self):
        super().__init__(
            detail="Token was not found",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class TokenIncorrectError(AuthError):
    def __init__(self):
        super().__init__(
            detail="Token incorrect",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class AccessDeniedError(AuthError):
    def __init__(self):
        super().__init__(
            detail="Token denied",
            status_code=status.HTTP_403_FORBIDDEN,
        )
