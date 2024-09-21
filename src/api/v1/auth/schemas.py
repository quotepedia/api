from datetime import datetime

from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    """Represents a response containing access token and its expiration datetime."""

    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class JWT(BaseModel):
    """Represents the contents of a [JWT](https://wikipedia.org/wiki/JSON_Web_Token)."""

    exp: datetime | None = None
    sub: int | str | None = None
