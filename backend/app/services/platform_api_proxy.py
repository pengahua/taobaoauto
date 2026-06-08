from sqlalchemy.orm import Session

from app.integrations.taobao.client import PreparedTopRequest
from app.repositories.api_logs import ApiCallLogRepository


class PlatformApiProxy:
    def __init__(self, db: Session) -> None:
        self.logs = ApiCallLogRepository(db)

    def record_prepared_request(
        self,
        *,
        store_id: str,
        api_name: str,
        prepared: PreparedTopRequest,
    ) -> None:
        self.logs.append(
            store_id=store_id,
            api_name=api_name,
            request_payload=prepared.signed_params,
            trace_id=prepared.trace_id,
            response_code="prepared",
            latency_ms=0,
        )

