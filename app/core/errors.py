def build_error(code: str, message: str, details: dict | None = None):
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }
