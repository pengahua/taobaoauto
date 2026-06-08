from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.db.session import get_db
from app.repositories.kill_switches import KillSwitchRepository
from app.schemas.risk import KillSwitchState, KillSwitchUpdate

router = APIRouter()


def to_state(record) -> KillSwitchState:
    return KillSwitchState(
        store_id=record.store_id,
        global_pause=record.global_pause,
        customer_message_pause=record.customer_message_pause,
        waybill_pause=record.waybill_pause,
        shipment_pause=record.shipment_pause,
        refund_pause=record.refund_pause,
    )


@router.get("/kill-switches", response_model=KillSwitchState)
def get_kill_switches(store_id: str = "global", db: Session = Depends(get_db)) -> KillSwitchState:
    init_db()
    record = KillSwitchRepository(db).get_or_create(store_id)
    db.commit()
    return to_state(record)


@router.post("/kill-switches", response_model=KillSwitchState)
def update_kill_switches(
    request: KillSwitchUpdate,
    db: Session = Depends(get_db),
) -> KillSwitchState:
    init_db()
    record = KillSwitchRepository(db).get_or_create(request.store_id)
    for field in [
        "global_pause",
        "customer_message_pause",
        "waybill_pause",
        "shipment_pause",
        "refund_pause",
    ]:
        value = getattr(request, field)
        if value is not None:
            setattr(record, field, value)
    record.updated_by = request.updated_by
    db.commit()
    db.refresh(record)
    return to_state(record)
