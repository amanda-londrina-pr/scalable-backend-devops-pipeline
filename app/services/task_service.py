from typing import List, Optional

from tortoise.exceptions import DoesNotExist

from app.models.task_model import Task


async def create(data) -> Task:
    return await Task.create(**data.dict())


async def list_all() -> List[Task]:
    return await Task.all()


async def get_by_id(task_id: int) -> Optional[Task]:
    try:
        return await Task.filter(id=task_id).first()
    except DoesNotExist:
        return None


async def update(task_id: int, data: dict) -> Optional[Task]:
    try:
        task = await Task.filter(id=task_id).first()
    except DoesNotExist:
        return None

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    await task.save()
    return task
