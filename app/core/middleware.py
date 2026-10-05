import re 
import time 
import uuid 
from collections.abc import Awaitable, Callable



import structlog 
from fastapi import FastAPI, Request, Response 

log = structlog.get_logger(__name__)

_SAFE_ID = re.compile(r"[A-Za-z0-9._-]{1,64}")


def add_request_context(app: FastAPI) -> None:
    
    @app.middleware("http")
    async def request_context(request:Request, call_next:Callable[[Request], Awaitable[Response]]) -> Response:
        
        incoming = request.headers.get("x-request-id","")
        request_id = incoming if _SAFE_ID.fullmatch(incoming) else str(uuid.uuid4())


        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            log.exception("request_failed", method=request.method, path=request.url.path)
            raise

        log.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round((time.perf_counter() - start) * 1000, 1),
        )
        response.headers["X-Request-ID"] = request_id
        return response        
            
            
