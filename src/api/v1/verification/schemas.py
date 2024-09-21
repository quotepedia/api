from datetime import datetime

from pydantic import BaseModel

from src.api.v1.schemas import OTP
from src.api.v1.users.schemas import UserEmail


class OTPVerify(OTP, UserEmail):
    pass


class OTPResponse(BaseModel):
    expires_at: datetime
