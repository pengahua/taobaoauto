from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class Command:
    command_type: str
    store_id: str
    biz_key: str
    idempotency_key: str
    payload: dict
    command_id: str = ""

    def __post_init__(self) -> None:
        if not self.command_id:
            object.__setattr__(self, "command_id", str(uuid4()))

