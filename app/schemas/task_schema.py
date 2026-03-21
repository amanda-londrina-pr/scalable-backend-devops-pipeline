from typing import List
from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from app.models.task_model import Task
from app.schemas.meta_schema import MetaSchema


# Pydantic Schema
class TaskBase(BaseModel):
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    title: str


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    title: str
    completed: bool


TaskSchema = pydantic_model_creator(Task)
TaskListSchema = pydantic_queryset_creator(Task)


class PaginatedTaskResponse(BaseModel):
    data: List[TaskSchema]
    meta: MetaSchema

# class PaginatedTaskResponse(BaseModel):
#     data: TaskListSchema
#     meta: MetaSchema
