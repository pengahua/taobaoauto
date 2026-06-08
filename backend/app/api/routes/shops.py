from fastapi import APIRouter

from app.integrations.taobao.oauth import build_authorization_url
from app.schemas.shops import (
    ShopAuthorizationCallback,
    ShopAuthorizationCallbackResponse,
    ShopAuthorizationRequest,
    ShopAuthorizationResponse,
)

router = APIRouter()


@router.post("/authorize", response_model=ShopAuthorizationResponse)
def create_authorization(request: ShopAuthorizationRequest) -> ShopAuthorizationResponse:
    return ShopAuthorizationResponse(
        authorization_url=build_authorization_url(
            app_key=request.app_key,
            redirect_uri=request.redirect_uri,
            state=request.state,
        ),
        state=request.state,
    )


@router.post("/oauth/callback", response_model=ShopAuthorizationCallbackResponse)
def handle_authorization_callback(
    request: ShopAuthorizationCallback,
) -> ShopAuthorizationCallbackResponse:
    return ShopAuthorizationCallbackResponse(
        status="accepted",
        state=request.state,
        next_action="exchange_code_for_session_key",
    )


@router.get("")
def list_shops() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
