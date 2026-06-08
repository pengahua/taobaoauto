from pydantic import BaseModel, Field


class ReplyDraftRequest(BaseModel):
    store_id: str
    thread_id: str
    buyer_message: str = Field(min_length=1)
    order_tid: str | None = None


class ReplyDraftResponse(BaseModel):
    draft: str
    risk_level: str
    auto_send_allowed: bool
    required_facts: list[str]
    escalation_reason: str | None = None

