from pydantic import BaseModel, Field, SecretStr

from app.shared.types import Token


class AccessLogin(BaseModel):
    username: int
    password: SecretStr


class AccessCredential(BaseModel):
    token: Token | str = Field(..., title="Access token", alias='token')
    type: str = Field("bearer", title="Token type", alias='type')


class AccessCredentialForm(BaseModel):
    access_token: Token | str = Field(..., title="Access token")
    token_type: str = Field("bearer", title="Token type")
