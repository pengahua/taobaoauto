from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatusHistory


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_tid(self, store_id: str, tid: str) -> Order | None:
        statement = select(Order).where(Order.store_id == store_id, Order.tid == tid)
        return self.db.scalar(statement)

    def upsert_order(
        self,
        *,
        store_id: str,
        tid: str,
        status: str,
        payment: float = 0,
        buyer_open_id: str | None = None,
        risk_level: str = "L1",
        raw_json: str | None = None,
        source: str = "sync",
        event_id: str | None = None,
    ) -> Order:
        existing = self.get_by_tid(store_id, tid)
        previous_status = existing.status if existing else None

        if existing is None:
            existing = Order(
                store_id=store_id,
                tid=tid,
                status=status,
                payment=payment,
                buyer_open_id=buyer_open_id,
                risk_level=risk_level,
                raw_json=raw_json,
            )
            self.db.add(existing)
        else:
            existing.status = status
            existing.payment = payment
            existing.buyer_open_id = buyer_open_id
            existing.risk_level = risk_level
            existing.raw_json = raw_json
            existing.version += 1

        if previous_status != status:
            self.db.add(
                OrderStatusHistory(
                    store_id=store_id,
                    tid=tid,
                    from_status=previous_status,
                    to_status=status,
                    source=source,
                    event_id=event_id,
                )
            )

        self.db.flush()
        return existing

    def list_recent(self, store_id: str | None = None, limit: int = 50) -> list[Order]:
        statement = select(Order).order_by(Order.id.desc()).limit(limit)
        if store_id:
            statement = statement.where(Order.store_id == store_id)
        return list(self.db.scalars(statement))

