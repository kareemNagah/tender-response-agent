from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import Settings


@dataclass(frozen=True)
class Container:
    sessionmaker: async_sessionmaker


def build_container(settings: Settings, sessionmaker: async_sessionmaker) -> Container:
    return Container(sessionmaker=sessionmaker)
