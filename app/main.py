# app.main.py

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.fastapi import tortoise_exception_handlers

from app.core.settings import settings


@asynccontextmanager
async def lifespan(my_app: FastAPI) -> AsyncGenerator[None, None]:
    # Initialize Tortoise ORM
    register_tortoise(
        app=my_app,
        db_url="sqlite://:memory:",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    yield  # Application runs here
    # Cleanup: Close database connections
    await Tortoise.close_connections()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)


@app.get("/")
async def root():
    return {"message": "FastAPI with Tortoise ORM running!"}
