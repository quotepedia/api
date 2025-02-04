from datetime import datetime, timedelta, timezone

from fastapi_mail import MessageSchema, MessageType

from src.api.otp.service import set_otp
from src.config import settings
from src.i18n.translator import Translator
from src.mail import fm
from src.template import render


async def send_verification_message(recipient: str, translator: Translator) -> datetime:
    otp = set_otp(recipient)
    expires_at = generate_code_expiration_timestamp()
    message = generate_verification_message(recipient, otp, expires_at, translator)

    await fm.send_message(message)

    return expires_at


def generate_code_expiration_timestamp() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=settings.otp.expire_minutes)


def generate_verification_message(
    recipient: str, otp: int, expires_at: datetime, translator: Translator
) -> MessageSchema:
    subject = translator.gettext("Verification")

    context = {
        "otp": str(otp).zfill(settings.otp.length),
        "expires_at": expires_at,
        "recipient": recipient,
        "_": translator.gettext,
    }

    body = render("otp.jinja", context)

    return MessageSchema(recipients=[recipient], subject=subject, body=body, subtype=MessageType.html)
