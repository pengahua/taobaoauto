from urllib.parse import parse_qs, urlparse

from app.integrations.taobao.oauth import build_authorization_url
from app.integrations.taobao.signing import attach_signature, sign_top_request


def test_build_authorization_url_encodes_oauth_params() -> None:
    url = build_authorization_url(
        app_key="app-1",
        redirect_uri="https://example.com/callback?a=1",
        state="state with space",
    )

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    assert parsed.netloc == "oauth.taobao.com"
    assert query["response_type"] == ["code"]
    assert query["client_id"] == ["app-1"]
    assert query["redirect_uri"] == ["https://example.com/callback?a=1"]
    assert query["state"] == ["state with space"]


def test_top_signature_is_stable_and_ignores_existing_sign() -> None:
    params = {
        "method": "taobao.trade.fullinfo.get",
        "app_key": "123",
        "timestamp": "2026-06-08 18:30:00",
        "format": "json",
        "v": "2.0",
        "sign_method": "md5",
        "tid": "456",
        "sign": "OLD",
    }

    signature = sign_top_request(params, "secret")

    assert signature == sign_top_request({k: v for k, v in params.items() if k != "sign"}, "secret")
    assert signature.isupper()
    assert len(signature) == 32


def test_attach_signature_returns_copy() -> None:
    params = {"method": "taobao.test", "app_key": "app"}

    signed = attach_signature(params, "secret")

    assert "sign" in signed
    assert "sign" not in params

