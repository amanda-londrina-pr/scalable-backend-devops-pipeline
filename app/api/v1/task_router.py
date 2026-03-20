# app.api.v1.task_router.py
from fastapi import APIRouter

from app.schemas.task_schema import TaskCreate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def list_all():
    return await task_service.list_tasks()


@router.post("/")
async def create(data: TaskCreate):
    return await task_service.create_task(data)
