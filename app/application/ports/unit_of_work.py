from typing import Protocol

from app.application.ports.repositories import TenderRepository


class UnitOfWork(Protocol):
    tenders: TenderRepository

    async def __aenter__(self) -> "UnitOfWork": ...  # noqa: PYI034

    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    async def commit(self) -> None: ...
