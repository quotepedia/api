from fastapi import APIRouter, HTTPException, Response, status

from src.api.otp.mailings import send_verification_message
from src.api.otp.schemas import OTPResponse, OTPVerifyRequest
from src.api.otp.service import is_otp_correct
from src.api.tags import Tags
from src.api.users.schemas import UserEmailRequest
from src.i18n.deps import Translator

router = APIRouter(prefix="/otp", tags=[Tags.OTP])


@router.post("/verify")
def verify_otp(args: OTPVerifyRequest, translator: Translator) -> Response:
    if not is_otp_correct(args.email, args.otp):
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, translator.gettext("The One-Time Password (OTP) is incorrect or expired.")
        )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/send")
async def send_otp(args: UserEmailRequest, translator: Translator) -> OTPResponse:
    expires_at = await send_verification_message(args.email, translator)
    return OTPResponse(expires_at=expires_at)
