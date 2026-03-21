# app/schemas/task_schema.py

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.domain.enums.task_status import TaskStatus
from app.models.task_model import Task


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

    def to_orm(self):
        return self.model_dump(exclude_unset=True, exclude_none=True)

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskPage(BaseModel):
    data: List[TaskSchema]
    total: int
    page: int
    page_size: int
    total_pages: int


class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


TaskSchema = pydantic_model_creator(Task)
