from pydantic import BaseModel


class PolicyDecisionRequest(BaseModel):
    store_id: str
    scene: str
    action: str
    risk_level: str
    amount: float | None = None
    has_verified_facts: bool = False


class PolicyDecisionResponse(BaseModel):
    decision: str
    human_required: bool
    reasons: list[str]

