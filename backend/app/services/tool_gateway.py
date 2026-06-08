from dataclasses import dataclass

from app.schemas.policy import PolicyDecisionRequest
from app.services.policy_engine import evaluate_policy


@dataclass(frozen=True)
class ToolRequest:
    store_id: str
    tool_name: str
    payload: dict
    risk_level: str
    idempotency_key: str | None = None


class ToolGateway:
    def authorize(self, request: ToolRequest) -> None:
        decision = evaluate_policy(
            PolicyDecisionRequest(
                store_id=request.store_id,
                scene="tool_call",
                action=request.tool_name,
                risk_level=request.risk_level,
                has_verified_facts=bool(request.payload.get("verified_facts")),
            )
        )
        if decision.human_required:
            raise PermissionError("; ".join(decision.reasons))

    def execute(self, request: ToolRequest) -> dict:
        self.authorize(request)
        return {"status": "accepted", "tool": request.tool_name}

