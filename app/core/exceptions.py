import structlog
from fastapi import Request, HTTPException
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from structlog.contextvars import get_contextvars

from app.domain.error_codes import ErrorCode
from app.domain.errors import build_error, DomainError

logger = structlog.get_logger()


def get_request_id():
    context = get_contextvars()
    return context.get("request_id")


def get_status_code(code: ErrorCode) -> int:
    if code == ErrorCode.TASK_NOT_FOUND:
        return status.HTTP_404_NOT_FOUND

    return status.HTTP_400_BAD_REQUEST


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = get_request_id()

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=build_error(
            code=ErrorCode.VALIDATION_ERROR,
            message="Invalid request data!",
            request_id=request_id,
            details={"errors": exc.errors()},
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = get_request_id()

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error(
            code=ErrorCode.DOMAIN_ERROR,
            message=exc.detail,
            request_id=request_id,
        ),
    )


async def global_exception_handler(request: Request, exc: Exception):
    request_id = get_request_id()

    logger.exception(
        "unhandled_exception",
        error=str(exc),
        request_id=request_id,
        path=request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_error(
            code=ErrorCode.INTERNAL_ERROR,
            message="Something went wrong!",
            request_id=request_id,
        ),
    )


async def domain_exception_handler(request: Request, exc: DomainError):
    request_id = get_request_id()

    logger.warning(
        "domain_error",
        error=str(exc),
        code=exc.code,
        request_id=request_id,
        path=request.url.path,
    )

    return JSONResponse(
        status_code=get_status_code(exc.code),
        content=build_error(
            code=exc.code,
            message=exc.message,
            request_id=request_id,
        ),
    )
