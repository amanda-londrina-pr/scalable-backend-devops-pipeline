from typing import List
from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.task_model import Task


# Pydantic Schema
class TaskBase(BaseModel):
    description: Optional[str] = None

    def to_orm(self):
        return self.model_dump(exclude_unset=True, exclude_none=True)

    class Config:
        from_attributes = True


class TaskCreateInput(TaskBase):
    title: str


class TaskUpdateInput(TaskBase):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskPageOutput(BaseModel):
    data: List[TaskSchemaOutput]
    total: int
    page: int
    page_size: int
    total_pages: int


TaskSchemaOutput = pydantic_model_creator(Task)
