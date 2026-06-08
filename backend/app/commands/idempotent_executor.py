from dataclasses import dataclass

from app.domain.commands import Command


@dataclass
class ExecutionRecord:
    command: Command
    status: str
    result: dict


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str, str], ExecutionRecord] = {}

    def get(self, command: Command) -> ExecutionRecord | None:
        return self._records.get((command.store_id, command.command_type, command.idempotency_key))

    def save(self, record: ExecutionRecord) -> None:
        key = (
            record.command.store_id,
            record.command.command_type,
            record.command.idempotency_key,
        )
        self._records[key] = record


class IdempotentExecutor:
    def __init__(self, store: InMemoryIdempotencyStore | None = None) -> None:
        self.store = store or InMemoryIdempotencyStore()

    def execute(self, command: Command, fn) -> ExecutionRecord:
        existing = self.store.get(command)
        if existing is not None:
            return existing

        result = fn(command)
        record = ExecutionRecord(command=command, status="succeeded", result=result)
        self.store.save(record)
        return record

