from pydantic import BaseModel, Field


class ShopAuthorizationRequest(BaseModel):
    app_key: str = Field(min_length=1)
    redirect_uri: str = Field(min_length=1)
    state: str = Field(min_length=1)


class ShopAuthorizationResponse(BaseModel):
    authorization_url: str
    state: str


class ShopAuthorizationCallback(BaseModel):
    code: str
    state: str


class ShopAuthorizationCallbackResponse(BaseModel):
    status: str
    state: str
    next_action: str
