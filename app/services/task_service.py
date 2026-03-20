from typing import List

from tortoise.exceptions import DoesNotExist

from app.models.task_model import Task


async def create_task(data) -> Task:
    return await Task.create(**data.dict())


async def list_tasks() -> List[Task]:
    return await Task.all()


async def get_task(task_id: int) -> Task | None:
    try:
        return await Task.filter(id=task_id).first()
    except DoesNotExist:
        return None
