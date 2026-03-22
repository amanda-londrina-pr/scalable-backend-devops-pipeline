# app.api.v1.task_router.py

import structlog
from fastapi import APIRouter, Depends
from fastapi import Query
from fastapi import Response, status

from app.core.settings import get_settings, Settings
from app.mappers.task_mapper import to_response, to_response_list
from app.schemas.task_schema import TaskPage, TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = structlog.get_logger()


@router.get("/", response_model=TaskPage)
async def list_paginated_endpoint(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100),
        settings: Settings = Depends(get_settings)):
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
async def create_endpoint(
        data: TaskCreate,
        settings: Settings = Depends(get_settings)):
    task = await task_service.create(data)
    result = to_response(task)

    logger.info("task_create_success", task_id=task.id)
    return result


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
        task_id: int,
        settings: Settings = Depends(get_settings)):
    task = await task_service.get_by_id(task_id)
    return to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_endpoint(
        task_id: int, data: TaskUpdate,
        settings: Settings = Depends(get_settings)):
    task = await task_service.update(task_id, data)
    result = to_response(task)

    logger.info("task_update_success", task_id=task_id)
    return result


@router.delete("/{task_id}", response_model=None,
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_endpoint(
        task_id: int,
        settings: Settings = Depends(get_settings)):
    await task_service.delete_by_id(task_id)
    logger.info("task_delete_success", task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
async def complete_task_endpoint(
        task_id: int,
        settings: Settings = Depends(get_settings)):
    task = await task_service.complete_task(task_id)
    result = to_response(task)
    logger.info("complete_task_success", task_id=task_id, status=str(task.status))
    return result


@router.patch(
    "/{task_id}/reopen",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
async def reopen_task_endpoint(task_id: int):
    task = await task_service.reopen_task(task_id)
    response = to_response(task)
    logger.info("reopen_task_success", task_id=task_id, status=str(task.status))
    return response
