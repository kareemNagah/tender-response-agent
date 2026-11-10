from dataclasses import dataclass
from enum import StrEnum

from app.domain.shared.errors import InvalidTransition
from app.domain.shared.ids import TenderId
from app.domain.shared.value_objects import Sha256


class TenderStatus(StrEnum):
    UPLOADED = "uploaded"
    PARSED = "parsed"
    EXTRACTED = "extracted"
    FAILED = "failed"


@dataclass(slots=True)
class Tender:
    id: TenderId
    filename: str
    sha256: Sha256
    storage_key: str
    status: TenderStatus = TenderStatus.UPLOADED
    pages: int | None = None

    def mark_parsed(self, pages: int) -> None:

        if self.status is not TenderStatus.UPLOADED:
            raise InvalidTransition(
                f"Cannot mark tender as parsed from status {self.status.value}"
            )

        self.status = TenderStatus.PARSED
        self.pages = pages
