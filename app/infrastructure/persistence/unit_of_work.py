from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.persistence.repositories import (
    SqlAlchemyTenderRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        sessionmaker: async_sessionmaker,
    ) -> None:

        self._session: AsyncSession = sessionmaker()

        self.tenders = SqlAlchemyTenderRepository(self._session)

        self._committed = False

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":  # noqa: PYI034
        return self

    async def __aexit__(self, *exc: object) -> None:

        exception_occurred = bool(exc) and exc[0] is not None

        try:
            if exception_occurred or not self._committed:
                await self._session.rollback()

        finally:
            await self._session.close()

    async def commit(self) -> None:

        self.tenders.sync_to_rows()

        await self._session.commit()

        self._committed = True
