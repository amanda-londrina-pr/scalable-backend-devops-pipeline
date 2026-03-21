from app.models.task_model import Task
from app.schemas.task_schema import TaskResponse


def to_response(task: Task) -> TaskResponse:
    return TaskResponse.model_validate(task)

def to_response_list(tasks: list[Task]) -> list[TaskResponse]:
    return [TaskResponse.model_validate(t) for t in tasks]