import structlog
from fastapi import Request, HTTPException
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.errors import build_error

logger = structlog.get_logger()


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "validation_error",
        errors=exc.errors(),
        path=request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=build_error(
            code="VALIDATION_ERROR",
            message="Invalid request data",
            details={"errors": exc.errors()},
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        "http_exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "unhandled_exception",
        error=str(exc),
        path=request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_error(
            code="INTERNAL_SERVER_ERROR",
            message="Something went wrong",
        ),
    )


class NotFoundError(HTTPException):
    def __init__(self, message="Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
