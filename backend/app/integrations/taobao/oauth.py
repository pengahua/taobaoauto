from urllib.parse import urlencode


TAOBAO_OAUTH_AUTHORIZE_URL = "https://oauth.taobao.com/authorize"


def build_authorization_url(
    *,
    app_key: str,
    redirect_uri: str,
    state: str,
    view: str = "web",
) -> str:
    query = urlencode(
        {
            "response_type": "code",
            "client_id": app_key,
            "redirect_uri": redirect_uri,
            "state": state,
            "view": view,
        }
    )
    return f"{TAOBAO_OAUTH_AUTHORIZE_URL}?{query}"

