class DomainError(Exception):
    code = "domain_error"

    def __init__(self, detail: str = "") -> None:
        super().__init__(detail)
        self.detail = detail


class NotFound(DomainError):
    code = "not_found"


class InvalidValue(DomainError):
    code = "invalid_value"


class InvalidTransition(DomainError):
    code = "invalid_transition"


class Conflict(DomainError):
    code = "conflict"
