from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.commands.handlers.order_sync import OrderSyncHandler
from app.db.base import Base
from app.domain.commands import Command
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.command import CommandRecord  # noqa: F401
from app.models.order import Order, OrderStatusHistory  # noqa: F401
from app.models.store import Store  # noqa: F401


def make_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


def test_order_sync_handler_upserts_order_and_audits() -> None:
    db = make_session()
    handler = OrderSyncHandler(db)
    command = Command(
        command_type="order_sync",
        store_id="s1",
        biz_key="tid-1",
        idempotency_key="order_sync:s1:tid-1",
        payload={"tid": "tid-1", "status": "WAIT_SELLER_SEND_GOODS", "payment": 99.5},
    )

    result = handler.handle(command)

    assert result["status"] == "synced"
    assert db.query(Order).count() == 1
    assert db.query(OrderStatusHistory).count() == 1
    assert db.query(CommandRecord).count() == 1
    assert db.query(AuditLog).count() == 1


def test_order_sync_handler_is_idempotent() -> None:
    db = make_session()
    handler = OrderSyncHandler(db)
    command = Command(
        command_type="order_sync",
        store_id="s1",
        biz_key="tid-1",
        idempotency_key="order_sync:s1:tid-1",
        payload={"tid": "tid-1", "status": "WAIT_SELLER_SEND_GOODS", "payment": 99.5},
    )

    first = handler.handle(command)
    second = handler.handle(command)

    assert first["status"] == "synced"
    assert second["status"] == "duplicate"
    assert db.query(Order).count() == 1
    assert db.query(CommandRecord).count() == 1

