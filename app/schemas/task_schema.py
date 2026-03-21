# app/schemas/task_schema.py

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.domain.enums.task_status import TaskStatus


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class TaskBase(BaseSchema):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

    def to_orm(self):
        return self.model_dump(exclude_unset=True, exclude_none=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class TaskPage(BaseSchema):
    data: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
