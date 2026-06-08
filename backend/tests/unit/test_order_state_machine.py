from app.domain.orders import can_auto_ship, can_transition


def test_paid_order_can_move_to_pending_shipment() -> None:
    assert can_transition("WAIT_BUYER_PAY", "WAIT_SELLER_SEND_GOODS") is True


def test_finished_order_cannot_reopen_to_pending_shipment() -> None:
    assert can_transition("TRADE_FINISHED", "WAIT_SELLER_SEND_GOODS") is False


def test_refunding_order_cannot_auto_ship() -> None:
    assert can_auto_ship("WAIT_SELLER_SEND_GOODS", refund_status="WAIT_SELLER_AGREE") is False


def test_top_hold_order_cannot_auto_ship() -> None:
    assert can_auto_ship("WAIT_SELLER_SEND_GOODS", refund_status="NO_REFUND", top_hold=True) is False
