# app.main.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from tortoise import Tortoise
from tortoise.contrib.fastapi import tortoise_exception_handlers

from app.api.v1.task_router import router as task_router
from app.core.settings import settings


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


@app.get("/")
async def root():
    return {"message": "FastAPI with Tortoise ORM running!"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")
