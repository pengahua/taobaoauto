from app.integrations.taobao.client import PreparedTopRequest, TopClient, TopRequest


class TaobaoOrderAdapter:
    def __init__(self, client: TopClient) -> None:
        self.client = client

    def prepare_sold_orders_request(
        self,
        *,
        session_key: str,
        start_modified: str,
        end_modified: str,
        page_no: int = 1,
        page_size: int = 40,
    ) -> PreparedTopRequest:
        return self.client.prepare(
            TopRequest(
                method="taobao.trades.sold.get",
                session_key=session_key,
                params={
                    "fields": "tid,status,payment,modified,buyer_nick",
                    "start_modified": start_modified,
                    "end_modified": end_modified,
                    "page_no": page_no,
                    "page_size": page_size,
                },
            )
        )

    def prepare_order_detail_request(self, *, session_key: str, tid: str) -> PreparedTopRequest:
        return self.client.prepare(
            TopRequest(
                method="taobao.trade.fullinfo.get",
                session_key=session_key,
                params={
                    "fields": "tid,status,payment,orders,receiver_name,receiver_mobile,receiver_address",
                    "tid": tid,
                },
            )
        )

