from typing import Optional
from typing import Tuple, List

import structlog

from app.domain.enums.task_status import TaskStatus
from app.domain.errors import NotFoundError, EmptyUpdateError
from app.domain.services.task_status_service import validate_status_transition
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate

logger = structlog.get_logger()


def sanitize_create_payload(data: dict) -> dict:
    data = data.copy()
    data.pop("status", None)
    return data


ALLOWED_UPDATE_FIELDS = {"title", "description"}


def sanitize_update_payload(data: dict) -> dict:
    allowed = {}
    ignored = []

    for field, value in data.items():
        if field in ALLOWED_UPDATE_FIELDS:
            allowed[field] = value
        else:
            ignored.append(field)

    if ignored:
        logger.warning("update_ignored_fields", fields=ignored)

    return allowed


async def create(data: TaskCreate) -> Task:
    logger.info("service_task_create", title=data.title, description=data.description)

    payload = sanitize_create_payload(data.to_orm())
    payload.pop("status", None)

    result = await Task.create(**payload, status=TaskStatus.PENDING)

    logger.info("service_task_create_success", id=result.id, result=result)
    return result


async def list_paginated(page: int, size: int) -> Tuple[List[Task], int, int]:
    # Parameters validation:
    page = max(page, 1)
    size = max(size, 1)
    logger.info("service_list_paginated_start", page=page, size=size)
    query = Task.all()
    logger.info("service_list_paginated_query", query=query)

    total = await query.count()
    offset = (page - 1) * size
    tasks = await query.offset(offset).limit(size)
    total_pages = (total + size - 1) // size

    logger.info("service_list_paginated_success",
                page=page,
                size=size,
                result=(tasks, total, total_pages))

    return tasks, total, total_pages


async def get_by_id(task_id: int) -> Task:
    logger.info("service_get", task_id=task_id)
    task = await Task.filter(id=task_id).first()
    if not task:
        raise NotFoundError("Task not found!")

    logger.info("service_get_success", task_id=task_id, result=task)
    return task


async def update(task_id: int, data: TaskUpdate) -> Optional[Task]:
    logger.info("service_update", task_id=task_id)

    task = await Task.filter(id=task_id).first()
    if not task:
        raise NotFoundError("Task not found!")

    raw_payload = data.to_orm()
    payload = sanitize_update_payload(raw_payload)

    if not payload:
        raise EmptyUpdateError("Update payload cannot be empty!")

    for field, value in payload.items():
        setattr(task, field, value)

    await task.save()

    logger.info("service_update_success", task_id=task.id)
    return task


async def complete_task(task_id: int) -> Task:
    task = await Task.filter(id=task_id).first()

    if not task:
        raise NotFoundError("Task not found!")

    validate_status_transition(task.status, TaskStatus.DONE)

    task.status = TaskStatus.DONE
    await task.save()

    logger.info("task_completed", task_id=task.id)

    return task


async def reopen_task(task_id: int) -> Task:
    task = await Task.filter(id=task_id).first()

    if not task:
        raise NotFoundError("Task not found!")

    old_status = task.status

    validate_status_transition(old_status, TaskStatus.IN_PROGRESS)

    task.status = TaskStatus.IN_PROGRESS
    await task.save()

    logger.info(
        "reopen_task_success",
        task_id=task.id,
        from_status=str(old_status),
        to_status=str(task.status),
    )

    return task


async def delete_by_id(task_id: int) -> None:
    logger.info("service_delete", task_id=task_id)
    deleted_count = await Task.filter(id=task_id).delete()

    if deleted_count == 0:
        raise NotFoundError("Task not found!")

    logger.info("service_delete_success", task_id=task_id)
