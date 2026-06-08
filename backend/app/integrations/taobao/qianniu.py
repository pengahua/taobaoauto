from app.integrations.taobao.client import PreparedTopRequest, TopClient, TopRequest


class QianniuMessageAdapter:
    def __init__(self, client: TopClient) -> None:
        self.client = client

    def prepare_send_message_request(
        self,
        *,
        session_key: str,
        receiver_id: str,
        content: str,
        biz_id: str,
    ) -> PreparedTopRequest:
        return self.client.prepare(
            TopRequest(
                method="taobao.jindoucloud.message.send",
                session_key=session_key,
                params={
                    "receiver_id": receiver_id,
                    "content": content,
                    "biz_id": biz_id,
                },
            )
        )
