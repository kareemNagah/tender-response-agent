import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.shared.errors import (
    Conflict,
    DomainError,
    InvalidTransition,
    InvalidValue,
    NotFound,
)

log = structlog.get_logger(__name__)

STATUS: dict[type[DomainError], tuple[int, str]] = {
    NotFound: (404, "Not found"),
    InvalidValue: (422, "Invalid value"),
    InvalidTransition: (409, "Invalid state transition"),
    Conflict: (409, "Conflict"),
}

ERROR_TYPE_BASE = "https://api.rfp-agent/errors"


def _problem(
    request: Request,
    status: int,
    title: str,
    detail: str,
    code: str,
    **extra: object,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={
            "type": f"{ERROR_TYPE_BASE}/{code}",
            "title": title,
            "status": status,
            "detail": detail,
            "instance": request.url.path,
            **extra,
        },
    )


async def domain_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if not isinstance(exc, DomainError):
        return await unhandled_error_handler(request, exc)

    status, title = next(
        (
            value
            for cls, value in STATUS.items()
            if isinstance(exc, cls)
        ),
        (400, "Domain error"),
    )

    log.warning(
        "domain_error",
        code=exc.code,
        status=status,
        detail=exc.detail,
    )

    return _problem(
        request,
        status,
        title,
        exc.detail,
        exc.code,
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:

    log.exception("unhandled_error")
    request_id = getattr(request.state, "request_id", None)
    return _problem(
        request,
        500,
        "Internal server error",
        "An unexpected error occurred",
        "internal_error",
        request_id=request_id,
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
