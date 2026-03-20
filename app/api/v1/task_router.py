# app.api.v1.task_router.py
from fastapi import APIRouter, HTTPException

from app.schemas.task_schema import TaskCreate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def list_all():
    return await task_service.list_tasks()


@router.post("/")
async def create(data: TaskCreate):
    return await task_service.create_task(data)


@router.get("/{task_id}")
async def get_task(task_id: int):
    task = await task_service.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
