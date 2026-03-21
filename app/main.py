# app.main.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

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
from app.core.settings import settings
from app.domain.errors import DomainError


@asynccontextmanager
async def lifespan(my_app: FastAPI) -> AsyncGenerator[None, None]:
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={'models': ['app.models.task_model']},
        _enable_global_fallback=True
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)

app.include_router(task_router)
app.middleware("http")(logging_middleware)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
async def root():
    return {"message": "FastAPI with Tortoise ORM running!"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")
