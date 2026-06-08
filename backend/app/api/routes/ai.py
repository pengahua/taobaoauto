from fastapi import APIRouter

from app.schemas.ai import ReplyDraftRequest, ReplyDraftResponse
from app.services.ai_orchestrator import draft_customer_reply

router = APIRouter()


@router.post("/reply-draft", response_model=ReplyDraftResponse)
def create_reply_draft(request: ReplyDraftRequest) -> ReplyDraftResponse:
    return draft_customer_reply(request)

