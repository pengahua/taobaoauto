from app.risk.levels import RiskLevel


def requires_human_approval(action: str, risk_level: str, amount: float | None = None) -> bool:
    if risk_level in {RiskLevel.L2, RiskLevel.L3, "L2", "L3"}:
        return True
    if action in {"approve_refund", "refuse_refund", "change_address", "compensate"}:
        return True
    return amount is not None and amount > 20

