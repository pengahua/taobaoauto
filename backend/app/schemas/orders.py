from pydantic import BaseModel


class OrderDetail(BaseModel):
    tid: str
    store_id: str
    status: str
    risk_level: str
    automation_allowed: bool


class OrderListResponse(BaseModel):
    items: list[OrderDetail]

