from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shared.ids import TenderId
from app.domain.shared.value_objects import Sha256
from app.domain.tendering.tender import Tender
from app.infrastructure.persistence.mappers import (
    tender_from_row,
    tender_to_row,
)
from app.infrastructure.persistence.orm import TenderRow


class SqlAlchemyTenderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        # Track both the domain entity and its ORM row together
        self._tracked: dict[
            TenderId,
            tuple[Tender, TenderRow],
        ] = {}

    def _to_domain(self, row: TenderRow) -> Tender:

        tender_id = TenderId(row.id)

        tracked = self._tracked.get(tender_id)

        if tracked is not None:
            return tracked[0]  # return the domain entity if exists in memory

        tender = tender_from_row(row)

        self._tracked[tender_id] = (tender, row)

        return tender

    async def get(self, tender_id: TenderId) -> Tender | None:

        row = await self._session.get(
            TenderRow,
            TenderId,
        )

        if row is None:
            return None

        return self._to_domain(row)

    async def get_by_sha256(
        self,
        sha: Sha256,
    ) -> Tender | None:

        statement = select(TenderRow).where(TenderRow.sha256 == sha.value)

        result = await self._session.execute(statement)

        row = result.scalar_one_or_none()

        if row is None:
            return None

        return self._to_domain(row)

    async def add(self, tender: Tender) -> None:

        row = tender_to_row(tender)

        self._session.add(row)

        self._tracked[tender.id] = (tender, row)

    def sync_to_rows(self) -> None:
        """Copy changes from domain entities to tracked ORM rows."""

        for tender, row in self._tracked.values():
            row.filename = tender.filename
            row.sha256 = tender.sha256.value
            row.storage_key = tender.storage_key
            row.status = tender.status.value
            row.pages = tender.pages
