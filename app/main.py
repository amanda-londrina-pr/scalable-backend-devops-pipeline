# app.main.py

from fastapi import FastAPI
from tortoise import Tortoise

from app.core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)


# app.include_router(task_routes)

# Initialize Tortoise-ORM
async def init_db():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={'models': ['app.models']}  # Point to your models module
    )
    await Tortoise.generate_schemas()


# Startup event
@app.on_event("startup")
async def startup():
    await init_db()


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
