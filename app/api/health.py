from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import DbSession, RedisDep

health_router = APIRouter(prefix="/health", tags=["health"])


# Live health check
@health_router.get("/live", status_code=status.HTTP_200_OK)
async def live() -> dict[str, str]:
    return {"status": "ok"}


# Ready health check for database and redis
@health_router.get("/ready")
async def ready(session: DbSession, redis: RedisDep) -> JSONResponse:

    checks: dict[str, str] = {}

    try:
        await session.execute(text("SELECT 1"))
        checks["database"] = "up"
    except (SQLAlchemyError, OSError):
        checks["database"] = "down"

    try:
        await redis.ping()
        checks["redis"] = "up"
    except (OSError, RedisError):
        checks["redis"] = "down"

    healthy = all(v == "up" for v in checks.values())

    return JSONResponse(
        status_code=(status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE),
        content={"status": "ok" if healthy else "unavailable", **checks},
        headers={"Cache-Control": "no-store, must-revalidate"},
    )
