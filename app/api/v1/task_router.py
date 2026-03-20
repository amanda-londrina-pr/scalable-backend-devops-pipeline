# app.api.v1.task_router.py
from fastapi import APIRouter, HTTPException

from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def list_all():
    return await task_service.list_all()


@router.post("/")
async def create(data: TaskCreate):
    return await task_service.create(data)


@router.get("/{task_id}")
async def get_task(task_id: int):
    task = await task_service.get_by_id(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}")
async def update(task_id: int, data: TaskUpdate):
    task = await task_service.update(task_id, data.model_dump(exclude_unset=True))

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
