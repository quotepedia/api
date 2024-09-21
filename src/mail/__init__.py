from fastapi_mail import FastMail

from src.config import settings

fm = FastMail(settings.MAIL_CONNECTION_CONF)
