from app.domain.shared.ids import TenderId
from app.domain.shared.value_objects import Sha256
from app.domain.tendering.tender import Tender, TenderStatus
from app.infrastructure.persistence.orm import TenderRow


# orm -> domain
def tender_from_row(row: TenderRow) -> Tender:

    return Tender(
        id=TenderId(row.id),
        filename=row.filename,
        sha256=Sha256(row.sha256),
        storage_key=row.storage_key,
        status=TenderStatus(row.status),
        pages=row.pages,
    )


# domain -> orm
# .value needed because ORM expects strings, not value objects


def tender_to_row(tender: Tender) -> TenderRow:
    return TenderRow(
        id=tender.id,
        filename=tender.filename,
        sha256=tender.sha256.value,
        storage_key=tender.storage_key,
        status=tender.status.value,
        pages=tender.pages,
    )
