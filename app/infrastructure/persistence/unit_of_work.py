from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.ports.repositories import TenderRepository
from app.infrastructure.persistence.repositories import (
    SqlAlchemyTenderRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session = sessionmaker()

        self._tenders_impl = SqlAlchemyTenderRepository(self._session)
        self.tenders: TenderRepository = self._tenders_impl

        self._committed = False

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":  # noqa: PYI034
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None or not self._committed:
                await self._session.rollback()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        self._tenders_impl.sync_to_rows()

        await self._session.commit()

        self._committed = True
