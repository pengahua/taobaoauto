from enum import StrEnum


class OrderStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    WAIT_BUYER_PAY = "WAIT_BUYER_PAY"
    WAIT_SELLER_SEND_GOODS = "WAIT_SELLER_SEND_GOODS"
    SELLER_CONSIGNED_PART = "SELLER_CONSIGNED_PART"
    WAIT_BUYER_CONFIRM_GOODS = "WAIT_BUYER_CONFIRM_GOODS"
    TRADE_FINISHED = "TRADE_FINISHED"
    TRADE_CLOSED = "TRADE_CLOSED"
    REFUNDING = "REFUNDING"


ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.UNKNOWN: {
        OrderStatus.WAIT_BUYER_PAY,
        OrderStatus.WAIT_SELLER_SEND_GOODS,
        OrderStatus.WAIT_BUYER_CONFIRM_GOODS,
        OrderStatus.TRADE_FINISHED,
        OrderStatus.TRADE_CLOSED,
        OrderStatus.REFUNDING,
    },
    OrderStatus.WAIT_BUYER_PAY: {
        OrderStatus.WAIT_SELLER_SEND_GOODS,
        OrderStatus.TRADE_CLOSED,
    },
    OrderStatus.WAIT_SELLER_SEND_GOODS: {
        OrderStatus.SELLER_CONSIGNED_PART,
        OrderStatus.WAIT_BUYER_CONFIRM_GOODS,
        OrderStatus.REFUNDING,
        OrderStatus.TRADE_CLOSED,
    },
    OrderStatus.SELLER_CONSIGNED_PART: {
        OrderStatus.WAIT_BUYER_CONFIRM_GOODS,
        OrderStatus.REFUNDING,
    },
    OrderStatus.WAIT_BUYER_CONFIRM_GOODS: {
        OrderStatus.TRADE_FINISHED,
        OrderStatus.REFUNDING,
    },
    OrderStatus.REFUNDING: {
        OrderStatus.WAIT_SELLER_SEND_GOODS,
        OrderStatus.WAIT_BUYER_CONFIRM_GOODS,
        OrderStatus.TRADE_CLOSED,
        OrderStatus.TRADE_FINISHED,
    },
    OrderStatus.TRADE_FINISHED: set(),
    OrderStatus.TRADE_CLOSED: set(),
}


def can_transition(from_status: str, to_status: str) -> bool:
    source = OrderStatus(from_status)
    target = OrderStatus(to_status)
    return target in ALLOWED_TRANSITIONS[source]


def can_auto_ship(status: str, refund_status: str | None = None, top_hold: bool = False) -> bool:
    if top_hold:
        return False
    if refund_status and refund_status.upper() not in {"NO_REFUND", "NONE", ""}:
        return False
    return status == OrderStatus.WAIT_SELLER_SEND_GOODS

