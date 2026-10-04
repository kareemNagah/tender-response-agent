from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.health import health_router
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.engine = create_async_engine(
        url=settings.database_url.get_secret_value(),
        pool_pre_ping=True,
    )
    app.state.sessionmaker = async_sessionmaker(
        bind=app.state.engine,
        expire_on_commit=False,
    )
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

    app = FastAPI(
        title="RFP Agent",
        description="RFP Agent API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(health_router)
    # app.include_router(api_v1_router, prefix="/api/v1")

    return app