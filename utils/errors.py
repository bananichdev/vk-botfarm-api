from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def __validation_exception_handler(exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        content=exc.errors(),
        status_code=status.HTTP_400_BAD_REQUEST,
    )
