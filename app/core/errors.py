from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status


class APIError(Exception):
    def __init__(self, code: str, message: str, details: str = "", http_status: int = 400):
        self.code = code
        self.message = message
        self.details = details
        self.http_status = http_status


def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.http_status,
        content={
            "status": "error",
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "SERVER_ERROR",
                "message": "Error interno del servidor",
                "details": str(exc),
            },
        },
    )