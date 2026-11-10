from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker

from app.application.ports.unit_of_work import UnitOfWork
from app.config import Settings
from app.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
)


@dataclass(frozen=True)
class Container:
    uow: Callable[[], UnitOfWork]


def build_container(
    settings: Settings,
    sessionmaker: async_sessionmaker,
) -> Container:

    return Container(uow=lambda: SqlAlchemyUnitOfWork(sessionmaker))
