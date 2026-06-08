from dataclasses import dataclass
from datetime import datetime, UTC
from uuid import uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    store_id: str
    aggregate_type: str
    aggregate_id: str
    payload: dict
    event_id: str = ""
    occurred_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.event_id:
            object.__setattr__(self, "event_id", str(uuid4()))
        if self.occurred_at is None:
            object.__setattr__(self, "occurred_at", datetime.now(UTC))

