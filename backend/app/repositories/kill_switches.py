from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.kill_switch import KillSwitchRecord


class KillSwitchRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create(self, store_id: str = "global") -> KillSwitchRecord:
        statement = select(KillSwitchRecord).where(KillSwitchRecord.store_id == store_id)
        existing = self.db.scalar(statement)
        if existing:
            return existing

        record = KillSwitchRecord(store_id=store_id)
        self.db.add(record)
        self.db.flush()
        return record

