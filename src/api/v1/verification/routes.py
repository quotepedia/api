from fastapi import APIRouter, HTTPException, Response, status

from src.api.v1.users.schemas import UserEmail
from src.api.v1.verification.mailings import send_verification_message
from src.api.v1.verification.schemas import CodeResponse, CodeVerify
from src.api.v1.verification.service import is_code_correct
from src.i18n import gettext as _

router = APIRouter(prefix="/verification", tags=["Verification"])


@router.post("/verify")
def verify_code(schema: CodeVerify) -> Response:
    if not is_code_correct(schema.email, schema.code):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/request")
async def request_code(schema: UserEmail) -> CodeResponse:
    expires_at = await send_verification_message(schema.email)
    return CodeResponse(expires_at=expires_at)
