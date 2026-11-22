from typing import Annotated

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine

from app.application.ports.unit_of_work import UnitOfWork
from app.config import Settings, get_settings


async def get_engine(request: Request) -> AsyncEngine:
    return request.app.state.engine


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis_client


async def get_uow(request: Request) -> UnitOfWork:
    return request.app.state.container.uow()


# Dependencies
DbEngine = Annotated[AsyncEngine, Depends(get_engine)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
RedisDep = Annotated[Redis, Depends(get_redis)]
UowDep = Annotated[UnitOfWork, Depends(get_uow)]
