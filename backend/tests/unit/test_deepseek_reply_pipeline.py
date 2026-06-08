from fastapi.testclient import TestClient

from app.integrations.llm.redaction import redact_facts, redact_text
from app.main import app
from app.schemas.ai import CustomerAutoReplyRequest
from app.services.ai_orchestrator import classify_intent, classify_risk, draft_auto_reply


def test_redact_text_masks_phone_and_order_id() -> None:
    redacted = redact_text("我的手机号是13812345678，订单123456789012345")

    assert "13812345678" not in redacted
    assert "123456789012345" not in redacted
    assert "[ORDER_ID]" in redacted


def test_redact_facts_masks_sensitive_keys() -> None:
    facts = redact_facts({"mobile": "13812345678", "order_status": "已付款"})

    assert facts["mobile"] == "[REDACTED]"
    assert facts["order_status"] == "已付款"


def test_intent_and_risk_classification() -> None:
    assert classify_intent("我的快递到哪了") == "logistics_query"
    assert classify_intent("会员还没开通") == "entitlement_query"
    assert classify_risk("我要退款并投诉") == "L2"


def test_auto_reply_uses_safe_fallback_without_api_key() -> None:
    response = draft_auto_reply(
        CustomerAutoReplyRequest(
            store_id="s1",
            thread_id="t1",
            buyer_message="我的会员怎么还没开通？",
            order_tid="tid-1",
            verified_facts={"order_status": "已付款"},
        )
    )

    assert response.provider == "safe-fallback"
    assert response.intent == "entitlement_query"
    assert response.auto_send_allowed is False
    assert response.next_action == "human_review"


def test_customer_auto_reply_api() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/ai/customer-auto-reply",
        json={
            "store_id": "s1",
            "thread_id": "t1",
            "buyer_message": "物流到哪了？",
            "verified_facts": {"order_status": "已发货"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "logistics_query"
    assert body["provider"] in {"safe-fallback", "deepseek"}

