from fastapi import APIRouter, HTTPException, status

from src.api.v1.auth.deps import PasswordForm
from src.api.v1.auth.schemas import AccessTokenResponse
from src.api.v1.users.schemas import UserPasswordResetRequest, UserRegistrationRequest
from src.api.v1.users.service import get_user_by_email, is_email_registered, register_user, update_password
from src.api.v1.verification.service import expire_otp_if_correct
from src.db.deps import Session
from src.i18n import gettext as _
from src.security import create_access_token, is_valid_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(args: UserRegistrationRequest, session: Session) -> AccessTokenResponse:
    if is_email_registered(session, args.email):
        raise HTTPException(status.HTTP_409_CONFLICT, _("Email already registered."))
    if not expire_otp_if_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))

    user = register_user(session, args)
    return create_access_token(user.id)


@router.post("/login")
async def login(form: PasswordForm, session: Session) -> AccessTokenResponse:
    email = form.username  # The OAuth2 spec requires the exact name `username`.
    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("User not found."))
    if not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _("Inactive user."))
    if not is_valid_password(form.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _("Incorrect password."))

    return create_access_token(user.id)


@router.patch("/reset-password")
def reset_password(args: UserPasswordResetRequest, session: Session) -> AccessTokenResponse:
    user = get_user_by_email(session, args.email)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("User not found."))
    if not expire_otp_if_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))

    update_password(session, user, args.password)

    return create_access_token(user.id)
