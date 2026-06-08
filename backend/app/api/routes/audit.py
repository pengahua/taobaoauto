from fastapi import APIRouter

router = APIRouter()


@router.get("/events")
def list_audit_events() -> dict[str, list[dict[str, str]]]:
    return {"items": []}

