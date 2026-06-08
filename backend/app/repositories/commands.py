import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.commands import Command
from app.models.command import CommandRecord


class CommandRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_or_get(self, command: Command) -> CommandRecord:
        statement = select(CommandRecord).where(
            CommandRecord.store_id == command.store_id,
            CommandRecord.command_type == command.command_type,
            CommandRecord.idempotency_key == command.idempotency_key,
        )
        existing = self.db.scalar(statement)
        if existing:
            return existing

        record = CommandRecord(
            store_id=command.store_id,
            command_type=command.command_type,
            biz_key=command.biz_key,
            idempotency_key=command.idempotency_key,
            status="pending",
            payload_json=json.dumps(command.payload, ensure_ascii=False),
        )
        self.db.add(record)
        self.db.flush()
        return record

    def mark_succeeded(self, record: CommandRecord, result: dict) -> CommandRecord:
        record.status = "succeeded"
        record.result_json = json.dumps(result, ensure_ascii=False)
        self.db.flush()
        return record

    def list_recent(self, limit: int = 50) -> list[CommandRecord]:
        statement = select(CommandRecord).order_by(CommandRecord.id.desc()).limit(limit)
        return list(self.db.scalars(statement))

