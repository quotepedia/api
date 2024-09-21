from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    """JSON payload containing access token."""

    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class JWT(BaseModel):
    """Contents of JWT."""

    exp: datetime | None = None
    sub: int | str | None = None
