from fastapi import APIRouter, HTTPException, status

from src.api.auth.deps import OAuth2PasswordRequestFormDepends
from src.api.auth.schemas import AccessTokenResponse
from src.api.otp.service import expire_otp_if_correct
from src.api.users import UserServiceDepends
from src.api.users.schemas import UserPasswordResetRequest, UserRegistrationRequest
from src.i18n import gettext as _
from src.security import create_access_token, is_valid_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(args: UserRegistrationRequest, service: UserServiceDepends) -> AccessTokenResponse:
    if service.is_email_registered(args.email):
        raise HTTPException(status.HTTP_409_CONFLICT, _("Email already registered."))
    if not expire_otp_if_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))

    user = service.register_user(args)

    return create_access_token(user.id)


@router.post("/login")
async def login(form: OAuth2PasswordRequestFormDepends, service: UserServiceDepends) -> AccessTokenResponse:
    email = form.username  # The OAuth2 spec requires the exact name `username`.
    user = service.get_user_by_email(email)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("User not found."))
    if not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _("Inactive user."))
    if not is_valid_password(form.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _("Incorrect password."))

    return create_access_token(user.id)


@router.patch("/reset-password")
def reset_password(args: UserPasswordResetRequest, service: UserServiceDepends) -> AccessTokenResponse:
    user = service.get_user_by_email(args.email)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("User not found."))
    if not expire_otp_if_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))

    service.update_password(user, args.password.get_secret_value())

    return create_access_token(user.id)
