from dataclasses import dataclass
from datetime import datetime, UTC
from uuid import uuid4

from app.integrations.taobao.signing import attach_signature


@dataclass(frozen=True)
class TopRequest:
    method: str
    params: dict[str, object]
    session_key: str | None = None
    trace_id: str = ""

    def __post_init__(self) -> None:
        if not self.trace_id:
            object.__setattr__(self, "trace_id", str(uuid4()))


@dataclass(frozen=True)
class PreparedTopRequest:
    endpoint: str
    signed_params: dict[str, object]
    trace_id: str


class TopClient:
    def __init__(self, *, app_key: str, app_secret: str, endpoint: str = "https://eco.taobao.com/router/rest") -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.endpoint = endpoint

    def prepare(self, request: TopRequest) -> PreparedTopRequest:
        params: dict[str, object] = {
            "method": request.method,
            "app_key": self.app_key,
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
            "format": "json",
            "v": "2.0",
            "sign_method": "md5",
            **request.params,
        }
        if request.session_key:
            params["session"] = request.session_key

        return PreparedTopRequest(
            endpoint=self.endpoint,
            signed_params=attach_signature(params, self.app_secret),
            trace_id=request.trace_id,
        )

