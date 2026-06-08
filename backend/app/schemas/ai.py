from pydantic import BaseModel, Field


class ReplyDraftRequest(BaseModel):
    store_id: str
    thread_id: str
    buyer_message: str = Field(min_length=1)
    order_tid: str | None = None
    verified_facts: dict[str, str] = Field(default_factory=dict)
    allow_auto_send: bool = False


class ReplyDraftResponse(BaseModel):
    draft: str
    risk_level: str
    auto_send_allowed: bool
    required_facts: list[str]
    escalation_reason: str | None = None
    provider: str
    model: str
    redacted: bool = True
    intent: str


class CustomerAutoReplyRequest(ReplyDraftRequest):
    conversation_history: list[str] = Field(default_factory=list)


class CustomerAutoReplyResponse(ReplyDraftResponse):
    decision: str
    next_action: str
