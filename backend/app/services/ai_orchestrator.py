from app.schemas.ai import ReplyDraftRequest, ReplyDraftResponse


def draft_customer_reply(request: ReplyDraftRequest) -> ReplyDraftResponse:
    """Create a safe placeholder reply draft until LLM integration is enabled."""
    if request.order_tid:
        return ReplyDraftResponse(
            draft="亲，已收到您的问题。我正在根据订单信息为您核实，请稍等。",
            risk_level="L1",
            auto_send_allowed=False,
            required_facts=["order_detail"],
            escalation_reason="LLM provider and RAG are not connected yet",
        )

    return ReplyDraftResponse(
        draft="亲，已收到您的消息。我先为您核实后再回复。",
        risk_level="L1",
        auto_send_allowed=False,
        required_facts=["knowledge_base"],
        escalation_reason="LLM provider and RAG are not connected yet",
    )

