from app.db.base import Base
from app.db.session import engine
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.command import CommandRecord  # noqa: F401
from app.models.order import Order, OrderStatusHistory  # noqa: F401
from app.models.store import Store  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()

