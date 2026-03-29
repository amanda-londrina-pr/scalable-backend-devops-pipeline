from app.domain.enums.task_status import TaskStatus
from app.domain.errors import InvalidStatusTransitionError

ALLOWED_TRANSITIONS = {
    TaskStatus.PENDING: [TaskStatus.IN_PROGRESS, TaskStatus.DONE],
    TaskStatus.IN_PROGRESS: [TaskStatus.DONE],
    TaskStatus.DONE: [TaskStatus.IN_PROGRESS],  # permite reopen
}


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    if not isinstance(current, TaskStatus):
        raise TypeError(f"current must be TaskStatus, got {type(current)}")

    if not isinstance(new, TaskStatus):
        raise TypeError(f"new must be TaskStatus, got {type(new)}")

    allowed = ALLOWED_TRANSITIONS.get(current, [])

    if new not in allowed:
        raise InvalidStatusTransitionError(
            f"Invalid status transition: {current} → {new}"
        )
