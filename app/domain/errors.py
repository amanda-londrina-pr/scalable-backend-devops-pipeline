def build_error(code: str, message: str, details: dict | None = None):
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }


class DomainError(Exception):
    pass


class NotFoundError(DomainError):
    def __init__(self, message: str = "Resource not found!"):
        self.message = message
        super().__init__(message)
