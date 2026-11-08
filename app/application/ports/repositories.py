from typing import Protocol

from app.domain.shared.ids import TenderId
from app.domain.shared.value_objects import Sha256
from app.domain.tendering.tender import Tender


class TenderRepository(Protocol):
    async def get(
        self,
        tender_id: TenderId,
    ) -> Tender | None: ...

    async def get_by_sha256(self, sha256: Sha256) -> Tender | None: ...

    async def add(self, tender: Tender) -> None: ...
