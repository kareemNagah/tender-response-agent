from typing import NewType
from uuid import UUID, uuid4

TenderId = NewType("TenderId", UUID)


def new_tender_id() -> TenderId:
    return TenderId(uuid4())
