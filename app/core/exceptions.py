import structlog
from fastapi import Request, HTTPException
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.errors import build_error, DomainError, NotFoundError

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


async def domain_exception_handler(request: Request, exc: DomainError):
    logger.warning(
        "domain_error",
        error=str(exc),
        path=request.url.path,
    )

    if isinstance(exc, NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=build_error(
                code="NOT_FOUND",
                message=exc.message,
            ),
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=build_error(
            code="DOMAIN_ERROR",
            message=str(exc),
        ),
    )
