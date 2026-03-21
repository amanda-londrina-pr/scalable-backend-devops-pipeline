from enum import Enum


class ErrorCode(str, Enum):
    # Generic
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DOMAIN_ERROR = "DOMAIN_ERROR"

    # Task
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
