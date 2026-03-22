from app.domain.error_codes import ErrorCode


def build_error(
        code: str,
        message: str,
        request_id: str | None = None,
        details: dict | None = None):
    return {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id,
            "details": details or {},
        }
    }


class DomainError(Exception):
    def __init__(self, message: str, code: ErrorCode = ErrorCode.DOMAIN_ERROR):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(DomainError):
    def __init__(self, message: str = "Resource not found!"):
        super().__init__(message, code=ErrorCode.TASK_NOT_FOUND)


class EmptyUpdateError(DomainError):
    pass

class InvalidStatusTransitionError(DomainError):
    pass
