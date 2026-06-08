from pydantic import BaseModel


class KillSwitchState(BaseModel):
    store_id: str
    global_pause: bool
    customer_message_pause: bool
    waybill_pause: bool
    shipment_pause: bool
    refund_pause: bool


class KillSwitchUpdate(BaseModel):
    store_id: str = "global"
    global_pause: bool | None = None
    customer_message_pause: bool | None = None
    waybill_pause: bool | None = None
    shipment_pause: bool | None = None
    refund_pause: bool | None = None
    updated_by: str = "operator"

