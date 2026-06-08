from fastapi import APIRouter

from app.schemas.shops import ShopAuthorizationRequest, ShopAuthorizationResponse

router = APIRouter()


@router.post("/authorize", response_model=ShopAuthorizationResponse)
def create_authorization(request: ShopAuthorizationRequest) -> ShopAuthorizationResponse:
    return ShopAuthorizationResponse(
        authorization_url=(
            "https://oauth.taobao.com/authorize"
            f"?response_type=code&client_id={request.app_key}"
            f"&redirect_uri={request.redirect_uri}&state={request.state}&view=web"
        ),
        state=request.state,
    )


@router.get("")
def list_shops() -> dict[str, list[dict[str, str]]]:
    return {"items": []}

