import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.api_call_log import ApiCallLog


def stable_hash(payload: dict) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class ApiCallLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def append(
        self,
        *,
        store_id: str,
        api_name: str,
        request_payload: dict,
        trace_id: str,
        response_code: str | None = None,
        error_code: str | None = None,
        latency_ms: int = 0,
    ) -> ApiCallLog:
        record = ApiCallLog(
            store_id=store_id,
            api_name=api_name,
            request_hash=stable_hash(request_payload),
            response_code=response_code,
            error_code=error_code,
            latency_ms=latency_ms,
            trace_id=trace_id,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def list_recent(self, limit: int = 50) -> list[ApiCallLog]:
        statement = select(ApiCallLog).order_by(ApiCallLog.id.desc()).limit(limit)
        return list(self.db.scalars(statement))

