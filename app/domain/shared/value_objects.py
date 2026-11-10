import re
from dataclasses import dataclass

from app.domain.shared.errors import InvalidValue


@dataclass(frozen=True, slots=True)
class Sha256:
    value: str

    def __post_init__(self) -> None:

        if not re.fullmatch(r"[0-9a-f]{64}", self.value):
            raise InvalidValue("sha256 must be 64 lowercase hex characters")
