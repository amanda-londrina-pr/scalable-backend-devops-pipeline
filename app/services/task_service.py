from typing import Optional

import structlog

from app.core.exceptions import NotFoundError
from app.domain.enums.task_status import TaskStatus
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate

logger = structlog.get_logger()


async def create(data: TaskCreate) -> Task:
    logger.info("service_task_create", title=data.title, description=data.description)
    result = await Task.create(**data.to_orm(), status=TaskStatus.PENDING)

    logger.info("service_task_create_success", id=result.id, result=result)
    return result


async def list_paginated(page: int, size: int):
    # Parameters validation:
    page = max(page, 1)
    size = max(size, 1)
    logger.info("service_list_paginated", page=page, size=size)

    query = Task.all()
    logger.info("service_list_paginated", query=query)

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

    for field, value in data.to_orm().items():
        setattr(task, field, value)

    await task.save()
    logger.info("service_update_success", task_id=task_id, result=task)
    return task


async def delete_by_id(task_id: int) -> None:
    logger.info("service_delete", task_id=task_id)
    deleted_count = await Task.filter(id=task_id).delete()

    if deleted_count == 0:
        raise NotFoundError("Task not found!")

    logger.info("service_delete_success", task_id=task_id)
