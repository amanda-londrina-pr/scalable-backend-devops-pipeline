from typing import Optional

import structlog

from app.models.task_model import Task
from app.schemas.task_schema import TaskCreateInput, TaskUpdateInput

logger = structlog.get_logger()


async def create(data: TaskCreateInput) -> Task:
    return await Task.create(**data.to_orm())


async def list_paginated(page: int, size: int):
    # Parameters validation:
    page = max(page, 1)
    size = max(size, 1)

    query = Task.all()
    total = await query.count()
    offset = (page - 1) * size
    tasks = await query.offset(offset).limit(size)
    total_pages = (total + size - 1) // size

    return tasks, total, total_pages


async def get_by_id(task_id: int) -> Optional[Task]:
    return await Task.filter(id=task_id).first()


async def update(task_id: int, data: TaskUpdateInput) -> Optional[Task]:
    task = await Task.filter(id=task_id).first()
    if not task:
        logger.info("task_update", task_id=task_id)
        return None

    for field, value in data.to_orm().items():
        setattr(task, field, value)

    await task.save()
    return task


async def delete_by_id(task_id: int) -> bool:
    deleted_count = await Task.filter(id=task_id).delete()
    return deleted_count > 0
