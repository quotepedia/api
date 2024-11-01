from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from PIL import Image

from src.api.v1.otp.service import expire_otp_if_correct
from src.api.v1.users.deps import UserServiceDepends
from src.api.v1.users.me.deps import CurrentUser
from src.api.v1.users.me.schemas import CurrentUserEmailUpdateRequest, CurrentUserResponse
from src.api.v1.users.models import User
from src.api.v1.users.schemas import UserPasswordRequest
from src.config import settings
from src.i18n import gettext as _
from src.storage import fs, mimetype

router = APIRouter(prefix="/me")


@router.get("", response_model=CurrentUserResponse)
def get_current_user(current_user: CurrentUser) -> User:
    return current_user


@router.patch("/email", response_model=CurrentUserResponse)
def update_current_user_email(
    args: CurrentUserEmailUpdateRequest,
    current_user: CurrentUser,
    service: UserServiceDepends,
) -> User:
    if service.is_email_registered(args.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, _("Email is already taken."))
    if not expire_otp_if_correct(args.email, args.otp):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, _("The One-Time Password (OTP) is incorrect or expired."))

    service.update_email(current_user, args.email)

    return current_user


@router.patch("/password", response_model=CurrentUserResponse)
def update_current_user_password(
    args: UserPasswordRequest,
    current_user: CurrentUser,
    service: UserServiceDepends,
) -> User:
    service.update_password(current_user, args.password.get_secret_value())

    return current_user


@router.patch("/avatar", response_model=CurrentUserResponse)
def update_current_user_avatar(
    file: Annotated[UploadFile, File()],
    current_user: CurrentUser,
    service: UserServiceDepends,
):
    if not fs.is_size_in_range(file.file, max_size=settings.api.max_avatar_size):
        mb = settings.api.max_avatar_size / (1024 * 1024)
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            _("File size exceeded maximum avatar size: %s MB.") % (mb,),
        )

    if not mimetype.is_image(file.content_type):
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            _("Unsupported avatar image type. Make sure you're uploading a correct file."),
        )

    image = Image.open(file.file)
    service.update_avatar(current_user, image)

    return current_user


@router.delete("/avatar", response_model=CurrentUserResponse)
def delete_current_user_avatar(current_user: CurrentUser, service: UserServiceDepends):
    if not current_user.avatar_url:
        raise HTTPException(status.HTTP_404_NOT_FOUND, _("Avatar not found."))

    service.delete_avatar(current_user)

    return current_user
