from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.exception_task import ExceptionTaskRecord


class ExceptionTaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def seed_defaults(self) -> None:
        defaults = [
            ExceptionTaskRecord(
                id="perm-qn-msg",
                type="missing_permission",
                title="确认千牛消息接口权限",
                severity="high",
                owner_role="Taobao Integration",
                next_action="在开放平台控制台核验千牛消息读写能力",
            ),
            ExceptionTaskRecord(
                id="risk-refund-auto",
                type="policy_hold",
                title="退款自动化保持关闭",
                severity="critical",
                owner_role="Risk Lead",
                next_action="只允许售后建议和人工确认，不开放自动同意/拒绝退款",
            ),
        ]
        for item in defaults:
            if self.db.get(ExceptionTaskRecord, item.id) is None:
                self.db.add(item)
        self.db.flush()

    def list_open(self) -> list[ExceptionTaskRecord]:
        statement = (
            select(ExceptionTaskRecord)
            .where(ExceptionTaskRecord.status == "open")
            .order_by(ExceptionTaskRecord.severity.desc(), ExceptionTaskRecord.created_at.desc())
        )
        return list(self.db.scalars(statement))

