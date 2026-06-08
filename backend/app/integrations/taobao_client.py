class TaobaoClient:
    """TOP API adapter placeholder.

    Production implementation must centralize signing, rate limits, retries,
    response normalization, and audit logging here.
    """

    def __init__(self, app_key: str, app_secret: str) -> None:
        self.app_key = app_key
        self.app_secret = app_secret

    def execute(self, method: str, params: dict, session_key: str | None = None) -> dict:
        raise NotImplementedError("TOP adapter is not connected yet")

