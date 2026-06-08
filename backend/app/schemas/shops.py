from pydantic import BaseModel, Field


class ShopAuthorizationRequest(BaseModel):
    app_key: str = Field(min_length=1)
    redirect_uri: str = Field(min_length=1)
    state: str = Field(min_length=1)


class ShopAuthorizationResponse(BaseModel):
    authorization_url: str
    state: str

