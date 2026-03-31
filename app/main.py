# app.main.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from tortoise import Tortoise
from tortoise.contrib.fastapi import tortoise_exception_handlers

from app.api.v1.task_router import router as task_router
from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler, domain_exception_handler)
from app.core.middleware import logging_middleware
from app.core.settings import get_settings
from app.domain.errors import DomainError, InvalidStatusTransitionError
from app.domain.handlers.task_status_handler import invalid_transition_handler
from app.scripts.seed import seed_tasks

logger = structlog.get_logger()
log_level = "DEBUG" if get_settings().DEBUG else "INFO"
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(log_level)
)


@asynccontextmanager
async def lifespan(my_app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()

    await Tortoise.init(config=settings.TORTOISE_ORM, _enable_global_fallback=True)
    await Tortoise.generate_schemas()

    if settings.is_dev and settings.SEED_ON_START:
        try:
            await seed_tasks()
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("seed_failure", exc_info=True)

    yield
    await Tortoise.close_connections()


app = FastAPI(
    title=get_settings().PROJECT_NAME,
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)

app.include_router(task_router)
app.middleware("http")(logging_middleware)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(InvalidStatusTransitionError, invalid_transition_handler)

@app.get("/")
async def root():
    return {"message": "FastAPI with Tortoise ORM running!"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")
