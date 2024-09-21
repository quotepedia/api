from pydantic import BaseModel, Field

from src.config import settings


class OTP(BaseModel):
    otp: int = Field(ge=settings.otp.min, le=settings.otp.max)


class Message(BaseModel):
    detail: str
