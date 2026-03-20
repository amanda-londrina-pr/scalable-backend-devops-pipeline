from typing import List

from app.models.task_model import Task


async def create_task(data) -> Task:
    return await Task.create(**data.dict())


async def list_tasks() -> List[Task]:
    return await Task.all()
