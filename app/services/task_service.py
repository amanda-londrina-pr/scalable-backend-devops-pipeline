from typing import Optional

from fastapi_pagination import Page
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import apaginate as tortoise_paginate
from tortoise.exceptions import DoesNotExist

from app.models.task_model import Task


async def create(data) -> Task:
    return await Task.create(**data.dict())


async def list_all(page: int, size: int) -> Page[Task]:
    return await tortoise_paginate(Task, Params(page=page, size=size))


async def get_by_id(task_id: int) -> Optional[Task]:
    try:
        return await Task.filter(id=task_id).first()
    except DoesNotExist:
        return None


async def update(task_id: int, data: dict) -> Optional[Task]:
    try:
        task = await Task.filter(id=task_id).first()
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.completed = data.get("completed", task.completed)

        await task.save()
        return task
    except DoesNotExist:
        return None


async def delete_by_id(task_id: int) -> bool:
    try:
        task = await Task.filter(id=task_id).first()
        await task.delete()
        return True
    except DoesNotExist:
        return False
