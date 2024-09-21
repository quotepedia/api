from datetime import datetime

from pydantic import BaseModel, Field

from src.api.v1.users.schemas import UserEmail
from src.config import settings


class Code(BaseModel):
    code: int = Field(ge=settings.otp.min, le=settings.otp.max)


class CodeVerify(Code, UserEmail):
    pass


class CodeResponse(BaseModel):
    expires_at: datetime
