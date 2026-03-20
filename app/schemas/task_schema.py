from typing import Optional

from pydantic import BaseModel


# Pydantic Schema
class TaskBase(BaseModel):
    description: Optional[str] = None


class TaskCreate(TaskBase):
    title: str


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    title: str
    completed: bool
