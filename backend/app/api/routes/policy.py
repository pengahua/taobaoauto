from fastapi import APIRouter

from app.schemas.policy import PolicyDecisionRequest, PolicyDecisionResponse
from app.services.policy_engine import evaluate_policy

router = APIRouter()


@router.post("/evaluate", response_model=PolicyDecisionResponse)
def evaluate(request: PolicyDecisionRequest) -> PolicyDecisionResponse:
    return evaluate_policy(request)

