from app.core.config import settings
from app.integrations.deepseek.client import ChatMessage, DeepSeekClient
from app.integrations.llm.redaction import redact_facts, redact_text
from app.schemas.ai import (
    CustomerAutoReplyRequest,
    CustomerAutoReplyResponse,
    ReplyDraftRequest,
    ReplyDraftResponse,
)

HIGH_RISK_KEYWORDS = {
    "退款",
    "退货",
    "赔偿",
    "赔付",
    "投诉",
    "差评",
    "平台介入",
    "律师",
    "起诉",
    "改地址",
    "补发",
}

ORDER_KEYWORDS = {"订单", "物流", "发货", "快递", "开通", "账号", "会员", "权益"}


def classify_intent(message: str) -> str:
    if any(keyword in message for keyword in {"物流", "快递", "发货"}):
        return "logistics_query"
    if any(keyword in message for keyword in {"开通", "账号", "会员", "权益"}):
        return "entitlement_query"
    if any(keyword in message for keyword in {"退款", "退货", "售后"}):
        return "after_sales"
    return "general_faq"


def classify_risk(message: str) -> str:
    if any(keyword in message for keyword in HIGH_RISK_KEYWORDS):
        return "L2"
    if any(keyword in message for keyword in ORDER_KEYWORDS):
        return "L1"
    return "L0"


def required_facts_for_intent(intent: str) -> list[str]:
    if intent == "logistics_query":
        return ["order_detail", "logistics_status"]
    if intent == "entitlement_query":
        return ["order_detail", "entitlement_status"]
    if intent == "after_sales":
        return ["order_detail", "after_sales_policy"]
    return ["knowledge_base"]


def build_messages(
    *,
    buyer_message: str,
    facts: dict[str, str],
    history: list[str] | None = None,
) -> list[ChatMessage]:
    history = history or []
    facts_text = "\n".join(f"- {key}: {value}" for key, value in facts.items()) or "- 暂无已验证事实"
    history_text = "\n".join(f"- {item}" for item in history[-6:]) or "- 暂无历史对话"
    return [
        ChatMessage(
            role="system",
            content=(
                "你是淘宝店铺客服助手。必须礼貌、简短、准确。"
                "只能基于已验证事实和店铺规则回复；不得承诺退款、赔付、必达、改地址。"
                "遇到退款、投诉、差评、法律、平台介入、地址变更、补发等场景，"
                "只能安抚并说明会转人工核实。"
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                f"历史对话:\n{history_text}\n\n"
                f"已验证事实:\n{facts_text}\n\n"
                f"买家消息:\n{buyer_message}\n\n"
                "请生成一条可发送给买家的中文回复，不要输出分析过程。"
            ),
        ),
    ]


def safe_fallback_reply(intent: str, has_order: bool) -> str:
    if intent == "logistics_query":
        return "亲，已收到您的物流问题。我先为您核实订单和快递状态，请稍等。"
    if intent == "entitlement_query":
        return "亲，已收到您的开通问题。我正在为您核实订单和权益状态，请稍等。"
    if intent == "after_sales":
        return "亲，您的售后问题已收到，我会先为您核实订单情况，再按平台规则协助处理。"
    if has_order:
        return "亲，已收到您的问题。我正在结合订单信息为您核实，请稍等。"
    return "亲，已收到您的消息，我先为您核实后再回复。"


def create_deepseek_client() -> DeepSeekClient:
    return DeepSeekClient(
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
        model=settings.deepseek_model,
    )


def draft_customer_reply(request: ReplyDraftRequest) -> ReplyDraftResponse:
    response = draft_auto_reply(
        CustomerAutoReplyRequest(**request.model_dump(), conversation_history=[])
    )
    return ReplyDraftResponse(**response.model_dump(exclude={"decision", "next_action"}))


def draft_auto_reply(request: CustomerAutoReplyRequest) -> CustomerAutoReplyResponse:
    intent = classify_intent(request.buyer_message)
    risk_level = classify_risk(request.buyer_message)
    required_facts = required_facts_for_intent(intent)
    redacted_message = redact_text(request.buyer_message)
    redacted_facts = redact_facts(request.verified_facts)
    client = create_deepseek_client()

    if client.is_configured:
        draft = client.chat_completion(
            build_messages(
                buyer_message=redacted_message,
                facts=redacted_facts,
                history=[redact_text(item) for item in request.conversation_history],
            )
        )
        provider = "deepseek"
    else:
        draft = safe_fallback_reply(intent, has_order=bool(request.order_tid))
        provider = "safe-fallback"

    auto_send_allowed = (
        settings.ai_auto_send_enabled
        and request.allow_auto_send
        and risk_level == "L0"
        and bool(request.verified_facts or intent == "general_faq")
    )
    escalation_reason = None
    decision = "draft_only"
    next_action = "review_and_send"

    if risk_level in {"L1", "L2", "L3"}:
        escalation_reason = "risk policy requires human or verified business facts before auto-send"
        next_action = "human_review"
    elif not auto_send_allowed:
        escalation_reason = "auto-send is disabled or not requested"

    if auto_send_allowed:
        decision = "auto_send_allowed"
        next_action = "send_qianniu_message"

    return CustomerAutoReplyResponse(
        draft=draft,
        risk_level=risk_level,
        auto_send_allowed=auto_send_allowed,
        required_facts=required_facts,
        escalation_reason=escalation_reason,
        provider=provider,
        model=settings.deepseek_model,
        redacted=True,
        intent=intent,
        decision=decision,
        next_action=next_action,
    )
