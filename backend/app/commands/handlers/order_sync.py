from sqlalchemy.orm import Session

from app.audit.service import AuditEvent
from app.domain.commands import Command
from app.repositories.audit import AuditRepository
from app.repositories.commands import CommandRepository
from app.repositories.orders import OrderRepository


class OrderSyncHandler:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.orders = OrderRepository(db)
        self.commands = CommandRepository(db)
        self.audit = AuditRepository(db)

    def handle(self, command: Command) -> dict:
        record = self.commands.create_or_get(command)
        if record.status == "succeeded":
            return {"status": "duplicate", "command_id": record.id}

        payload = command.payload
        order = self.orders.upsert_order(
            store_id=command.store_id,
            tid=str(payload["tid"]),
            status=str(payload.get("status", "UNKNOWN")),
            payment=float(payload.get("payment", 0)),
            buyer_open_id=payload.get("buyer_open_id"),
            risk_level=str(payload.get("risk_level", "L1")),
            raw_json=payload.get("raw_json"),
            source="command",
            event_id=command.command_id,
        )
        result = {"status": "synced", "order_id": order.id, "tid": order.tid}
        self.commands.mark_succeeded(record, result)
        self.audit.append(
            AuditEvent(
                actor_type="system",
                action="order.sync",
                target_type="order",
                target_id=order.tid,
                store_id=command.store_id,
                trace_id=command.command_id,
                metadata=result,
            )
        )
        self.db.commit()
        return result

