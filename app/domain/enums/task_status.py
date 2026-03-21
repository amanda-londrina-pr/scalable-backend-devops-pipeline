from enum import Enum


# app/domain/enums/task_status.py

# used in workflows (kanban, pipeline), audit report and business rules
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
