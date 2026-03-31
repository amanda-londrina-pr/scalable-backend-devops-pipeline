# app/domain/handlers/task_status_handler.py

from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from app.domain.errors import InvalidStatusTransitionError


async def invalid_transition_handler(
        request: Request,
        exc: InvalidStatusTransitionError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )
