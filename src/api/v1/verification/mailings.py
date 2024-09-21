from datetime import datetime, timedelta, timezone

from fastapi_mail import MessageSchema, MessageType

from src.api.v1.verification.service import set_code
from src.config import settings
from src.i18n import gettext as _
from src.mail import fm
from src.template import render

__VERIFICATION_TEMPLATE_FILENAME = "verification.jinja"


async def send_verification_message(recipient: str) -> datetime:
    code = set_code(recipient)
    expires_at = generate_code_expiration_timestamp()
    message = generate_verification_message(recipient, code, expires_at)

    await fm.send_message(message)

    return expires_at


def generate_code_expiration_timestamp() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=settings.otp.expire_minutes)


def generate_verification_message(recipient: str, code: int, expires_at: datetime) -> MessageSchema:
    subject = _("Verification")

    context = {
        "code": code,
        "expires_at": expires_at,
        "recipient": recipient,
    }

    body = render(__VERIFICATION_TEMPLATE_FILENAME, context)

    return MessageSchema(recipients=[recipient], subject=subject, body=body, subtype=MessageType.html)
