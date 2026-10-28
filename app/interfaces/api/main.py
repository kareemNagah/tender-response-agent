from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.bootstrap import build_container
from app.config import get_settings
from app.infrastructure.observability.logging import configure_logging
from app.interfaces.api.errors import register_error_handlers
from app.interfaces.api.health import health_router
from app.interfaces.api.middleware import add_request_context


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    engine = create_async_engine(
        url=settings.database_url.get_secret_value(),
        pool_pre_ping=True,
    )

    sessionmaker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    app.state.engine = engine
    app.state.container = build_container(settings, sessionmaker)

    app.state.redis_client = aioredis.from_url(
        url=settings.redis_url.get_secret_value(),
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
    )

    yield

    await app.state.engine.dispose()
    await app.state.redis_client.close()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(level=settings.log_level, log_format=settings.log_format)

    app = FastAPI(
        title="RFP Agent",
        description="RFP Agent API",
        version="0.1.0",
        lifespan=lifespan,
    )

    add_request_context(app)
    register_error_handlers(app)
    app.include_router(health_router)
    # app.include_router(api_v1_router, prefix="/api/v1")

    return app
