from app.schemas.policy import PolicyDecisionRequest
from app.services.policy_engine import evaluate_policy


def test_high_risk_action_requires_human() -> None:
    decision = evaluate_policy(
        PolicyDecisionRequest(
            store_id="s1",
            scene="refund",
            action="approve_refund",
            risk_level="L3",
            amount=100,
            has_verified_facts=True,
        )
    )

    assert decision.decision == "hold"
    assert decision.human_required is True


def test_low_risk_verified_action_allowed() -> None:
    decision = evaluate_policy(
        PolicyDecisionRequest(
            store_id="s1",
            scene="customer_service",
            action="send_faq_reply",
            risk_level="L0",
            has_verified_facts=True,
        )
    )

    assert decision.decision == "allow"
    assert decision.human_required is False

