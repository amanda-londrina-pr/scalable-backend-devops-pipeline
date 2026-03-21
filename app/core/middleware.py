import time
import uuid

import structlog
from fastapi import Request
from structlog.contextvars import bind_contextvars, clear_contextvars

from app.core.settings import settings

logger = structlog.get_logger()


async def logging_middleware(request: Request, call_next):
    clear_contextvars()
    request_id = str(uuid.uuid4())
    bind_contextvars(
        env=settings.ENV,
        service=settings.PROJECT_NAME,
        request_id=request_id,
        path=request.url.path,
        method=request.method,
    )
    start_time = time.time()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            "http_request",
            status_code=response.status_code,
            duration=duration,
            query_params=str(request.query_params),
        )

        return response

    except Exception:
        duration = time.time() - start_time

        logger.exception(
            "http_request_failed",
            duration=duration,
        )

        raise
