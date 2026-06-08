from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class KillSwitchRecord(Base):
    __tablename__ = "kill_switches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[str] = mapped_column(String(64), index=True, default="global")
    global_pause: Mapped[bool] = mapped_column(Boolean, default=False)
    customer_message_pause: Mapped[bool] = mapped_column(Boolean, default=False)
    waybill_pause: Mapped[bool] = mapped_column(Boolean, default=False)
    shipment_pause: Mapped[bool] = mapped_column(Boolean, default=False)
    refund_pause: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_by: Mapped[str] = mapped_column(String(128), default="system")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

