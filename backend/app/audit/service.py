from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class AuditEvent:
    actor_type: str
    action: str
    target_type: str
    target_id: str
    store_id: str
    trace_id: str
    metadata: dict
    event_id: str = ""
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.event_id:
            object.__setattr__(self, "event_id", str(uuid4()))
        if self.created_at is None:
            object.__setattr__(self, "created_at", datetime.now(UTC))


class InMemoryAuditSink:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)


class AuditService:
    def __init__(self, sink: InMemoryAuditSink | None = None) -> None:
        self.sink = sink or InMemoryAuditSink()

    def record(self, event: AuditEvent) -> None:
        self.sink.append(event)

