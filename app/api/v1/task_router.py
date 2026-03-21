# app.api.v1.task_router.py

import structlog
from fastapi import APIRouter
from fastapi import Query
from fastapi import Response, status

from app.mappers.task_mapper import to_response, to_response_list
from app.schemas.task_schema import TaskPage, TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = structlog.get_logger()


@router.get("/", response_model=TaskPage)
async def list_paginated(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100)
):
    tasks, total, total_pages = await task_service.list_paginated(page, size)
    result = TaskPage(
        data=to_response_list(tasks),
        total=total,
        page=page,
        page_size=size,
        total_pages=total_pages
    )

    logger.info("tasks_paginated_success", page=page, page_size=size)
    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create(data: TaskCreate):
    task = await task_service.create(data)
    result = to_response(task)

    logger.info("task_create_success", task_id=task.id)
    return result


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = await task_service.get_by_id(task_id)
    return to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update(task_id: int, data: TaskUpdate):
    task = await task_service.update(task_id, data)
    result = to_response(task)

    logger.info("task_update_success", task_id=task_id)
    return result


@router.delete("/{task_id}", response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: int):
    await task_service.delete_by_id(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
