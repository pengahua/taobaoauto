from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ExceptionTaskRecord(Base):
    __tablename__ = "exception_tasks"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    store_id: Mapped[str] = mapped_column(String(64), index=True, default="global")
    type: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(256))
    severity: Mapped[str] = mapped_column(String(32), index=True)
    owner_role: Mapped[str] = mapped_column(String(64))
    next_action: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

