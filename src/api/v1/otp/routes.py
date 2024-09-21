from fastapi import APIRouter, HTTPException, Response, status

from src.api.v1.otp.mailings import send_verification_message
from src.api.v1.otp.schemas import OTPResponse, OTPVerifyRequest
from src.api.v1.otp.service import is_otp_correct
from src.api.v1.users.schemas import UserEmailRequest
from src.i18n import gettext as _

router = APIRouter(prefix="/otp", tags=["One-Time Password (OTP)"])


@router.post("/verify")
def verify_otp(args: OTPVerifyRequest) -> Response:
    if not is_otp_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/send")
async def send_otp(args: UserEmailRequest) -> OTPResponse:
    expires_at = await send_verification_message(args.email)
    return OTPResponse(expires_at=expires_at)
