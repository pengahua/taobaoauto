from app.schemas.policy import PolicyDecisionRequest, PolicyDecisionResponse


HIGH_RISK_ACTIONS = {
    "approve_refund",
    "refuse_refund",
    "change_address",
    "reship",
    "compensate",
    "close_trade",
}


def evaluate_policy(request: PolicyDecisionRequest) -> PolicyDecisionResponse:
    reasons: list[str] = []

    if request.action in HIGH_RISK_ACTIONS:
        reasons.append("high risk action requires human approval")

    if request.risk_level in {"L2", "L3"}:
        reasons.append(f"risk level {request.risk_level} is not fully automatic")

    if not request.has_verified_facts:
        reasons.append("verified facts are required before execution")

    if request.amount is not None and request.amount > 20:
        reasons.append("amount exceeds default automatic threshold")

    if reasons:
        return PolicyDecisionResponse(decision="hold", human_required=True, reasons=reasons)

    return PolicyDecisionResponse(decision="allow", human_required=False, reasons=["policy passed"])

