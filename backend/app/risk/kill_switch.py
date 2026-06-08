from dataclasses import dataclass


@dataclass
class KillSwitches:
    global_pause: bool = False
    customer_message_pause: bool = False
    waybill_pause: bool = False
    shipment_pause: bool = False
    refund_pause: bool = True

    def is_action_paused(self, action: str) -> bool:
        if self.global_pause:
            return True
        if action == "send_qianniu_message":
            return self.customer_message_pause
        if action == "create_waybill":
            return self.waybill_pause
        if action == "mark_order_shipped":
            return self.shipment_pause
        if "refund" in action:
            return self.refund_pause
        return False

