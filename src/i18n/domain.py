from gettext import NullTranslations, translation

from src.config import settings
from src.template import env

DOMAIN_NAME = "messages"

_translations: NullTranslations


def activate(language: str) -> None:
    global _translations

    _translations = translation(
        domain=DOMAIN_NAME,
        localedir=settings.path.locales,
        languages=[language],
        fallback=True,
    )

    _translations.install()

    # This funciton is added at runtime after adding the i18n extension from the jinja2.ext module.
    env.install_gettext_translations(_translations, newstyle=True)  # type: ignore


def gettext(message: str) -> str:
    return _translations.gettext(message)


def ngettext(msgid1: str, msgid2: str, n: int) -> str:
    return _translations.ngettext(msgid1, msgid2, n)


def npgettext(context: str, msgid1: str, msgid2: str, n: int) -> str:
    return _translations.npgettext(context, msgid1, msgid2, n)


def pgettext(context: str, message: str) -> str:
    return _translations.pgettext(context, message)


__all__ = [
    "activate",
    "gettext",
    "ngettext",
    "npgettext",
    "pgettext",
    "DOMAIN_NAME",
]
