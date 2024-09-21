from fastapi import APIRouter, HTTPException, Response, status

from src.api.v1.users.schemas import UserEmailRequest
from src.api.v1.verification.mailings import send_verification_message
from src.api.v1.verification.schemas import OTPResponse, OTPVerifyRequest
from src.api.v1.verification.service import is_otp_correct
from src.i18n import gettext as _

router = APIRouter(prefix="/verification", tags=["Verification"])


@router.post("/verify")
def verify_code(args: OTPVerifyRequest) -> Response:
    if not is_otp_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/request")
async def request_code(args: UserEmailRequest) -> OTPResponse:
    expires_at = await send_verification_message(args.email)
    return OTPResponse(expires_at=expires_at)
