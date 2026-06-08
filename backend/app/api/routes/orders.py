from fastapi import APIRouter

from app.schemas.orders import OrderDetail, OrderListResponse

router = APIRouter()


@router.get("", response_model=OrderListResponse)
def list_orders() -> OrderListResponse:
    return OrderListResponse(items=[])


@router.get("/{tid}", response_model=OrderDetail)
def get_order(tid: str) -> OrderDetail:
    return OrderDetail(
        tid=tid,
        store_id="demo-store",
        status="UNKNOWN",
        risk_level="L2",
        automation_allowed=False,
    )

