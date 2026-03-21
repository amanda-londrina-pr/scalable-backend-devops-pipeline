# app.api.v1.task_router.py
import structlog
from fastapi import APIRouter, HTTPException
from fastapi import Query
from fastapi import Response, status

from app.schemas.task_schema import (
    TaskCreateInput,
    TaskUpdateInput,
    TaskSchemaOutput,
    TaskPageOutput)
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = structlog.get_logger()


@router.get("/", response_model=TaskPageOutput)
async def list_paginated(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100)
):
    tasks, total, total_pages = await task_service.list_paginated(page, size)
    task_output = TaskPageOutput(
        data=[TaskSchemaOutput.from_orm(t) for t in tasks],
        total=total,
        page=page,
        page_size=size,
        total_pages=total_pages
    )

    logger.info("tasks_paginated")
    return task_output


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskSchemaOutput)
async def create(data: TaskCreateInput):
    task = await task_service.create(data)
    logger.info("task_created", task_id=task.id)
    return await TaskSchemaOutput.from_tortoise_orm(task)


@router.get("/{task_id}", response_model=TaskSchemaOutput)
async def get_task(task_id: int):
    task = await task_service.get_by_id(task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")

    logger.info("task_recovered", task_id=task_id)
    return await TaskSchemaOutput.from_tortoise_orm(task)


@router.put("/{task_id}", response_model=TaskSchemaOutput)
async def update(task_id: int, data: TaskUpdateInput):
    task = await task_service.update(task_id, data)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")

    logger.info("task_updated", task_id=task_id)
    return await TaskSchemaOutput.from_tortoise_orm(task)


@router.delete("/{task_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: int):
    success = await task_service.delete_by_id(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!")

    logger.info("task_deleted", task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
