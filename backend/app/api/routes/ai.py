from fastapi import APIRouter

from app.schemas.ai import (
    CustomerAutoReplyRequest,
    CustomerAutoReplyResponse,
    ReplyDraftRequest,
    ReplyDraftResponse,
)
from app.services.ai_orchestrator import draft_auto_reply, draft_customer_reply

router = APIRouter()


@router.post("/reply-draft", response_model=ReplyDraftResponse)
def create_reply_draft(request: ReplyDraftRequest) -> ReplyDraftResponse:
    return draft_customer_reply(request)


@router.post("/customer-auto-reply", response_model=CustomerAutoReplyResponse)
def create_customer_auto_reply(request: CustomerAutoReplyRequest) -> CustomerAutoReplyResponse:
    return draft_auto_reply(request)
