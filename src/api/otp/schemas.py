from datetime import datetime

from pydantic import BaseModel

from src.api.schemas import OTPRequest
from src.api.users.schemas import UserEmailRequest


class OTPVerifyRequest(UserEmailRequest, OTPRequest):
    """Represents a request for verifying a One-Time Password (OTP)."""


class OTPResponse(BaseModel):
    """Represents a response containing One-Time Password (OTP) expiration datetime."""

    expires_at: datetime
