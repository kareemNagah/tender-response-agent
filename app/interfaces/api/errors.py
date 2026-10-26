import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

log = structlog.get_logger(__name__)

ERROR_TYPE_BASE = "https://rfp-agent.dev/errors"


class AppError(Exception):
    """Base class for expected errors. Subclasses override the class attributes."""

    status_code: int = 500
    code: str = "internal_error"
    title: str = "Internal Server Error"
    default_detail: str = "An internal error occurred"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class ValidationFailed(AppError):
    status_code = 422
    code = "validation_failed"
    title = "Validation Failed"
    default_detail = "Validation failed"


class Conflict(AppError):
    status_code = 409
    code = "conflict"
    title = "Conflict"
    default_detail = "Resource conflict"


class NotFound(AppError):
    status_code = 404
    code = "not_found"
    title = "Not Found"
    default_detail = "Resource not found"


def register_error_handlers(app: FastAPI) -> None:
    """Convert any AppError into an RFC 7807 problem+json response."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        log_fn = log.error if exc.status_code >= 500 else log.warning
        log_fn(
            "app_error",
            code=exc.code,
            status=exc.status_code,
            detail=exc.detail,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": f"{ERROR_TYPE_BASE}/{exc.code}",
                "title": exc.title,
                "status": exc.status_code,
                "detail": exc.detail,
                "instance": request.url.path,
            },
            media_type="application/problem+json",
        )
