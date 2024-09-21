from datetime import datetime

from pydantic import BaseModel, Field

from src.config import settings


class AuditResponse(BaseModel):
    """Represents a response containing the auto-generated create and update timestamps."""

    created_at: datetime
    updated_at: datetime


class OTPRequest(BaseModel):
    """Represents a request with a One-Time Password (OTP)."""

    otp: int = Field(ge=settings.otp.min, le=settings.otp.max)
