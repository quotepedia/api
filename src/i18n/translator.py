from gettext import NullTranslations, translation

from src.config import settings
from src.template import env

DOMAIN_NAME = "messages"


class Translator:
    def __init__(self):
        self.translations: NullTranslations

    def activate(self, language: str) -> None:
        self.translations = translation(
            domain=DOMAIN_NAME,
            localedir=settings.path.locales,
            languages=[language],
            fallback=True,
        )

        self.translations.install()

        # This funciton is added at runtime after adding the i18n extension from the jinja2.ext module.
        env.install_gettext_translations(self.translations, newstyle=True)  # type: ignore

    def gettext(self, message: str) -> str:
        return self.translations.gettext(message)

    def ngettext(self, msgid1: str, msgid2: str, n: int) -> str:
        return self.translations.ngettext(msgid1, msgid2, n)

    def npgettext(self, context: str, msgid1: str, msgid2: str, n: int) -> str:
        return self.translations.npgettext(context, msgid1, msgid2, n)

    def pgettext(self, context: str, message: str) -> str:
        return self.translations.pgettext(context, message)


__all__ = [
    "Translator",
]
