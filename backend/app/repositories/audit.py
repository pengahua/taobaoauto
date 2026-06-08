import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit.service import AuditEvent
from app.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def append(self, event: AuditEvent) -> AuditLog:
        record = AuditLog(
            store_id=event.store_id,
            actor_type=event.actor_type,
            actor_id=None,
            action=event.action,
            target_type=event.target_type,
            target_id=event.target_id,
            trace_id=event.trace_id,
            metadata_json=json.dumps(event.metadata, ensure_ascii=False),
        )
        self.db.add(record)
        self.db.flush()
        return record

    def list_recent(self, limit: int = 50) -> list[AuditLog]:
        statement = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
        return list(self.db.scalars(statement))

