from pydantic import BaseModel


# Pydantic Schema

class TaskCreate(BaseModel):
    title: str
    description: str | None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
