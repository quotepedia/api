from typing import Annotated

from fastapi import Depends, Header

from src.i18n.constants import DEFAULT_ISO_639
from src.i18n.spec import get_preferred_iso_639
from src.i18n.translator import Translator as _Translator


def get_accept_language(accept_language: str = Header(DEFAULT_ISO_639)) -> str:
    language = get_preferred_iso_639(accept_language)
    return language


AcceptLanguage = Annotated[str, Depends(get_accept_language)]


def get_translator(language: AcceptLanguage):
    translator = _Translator()
    translator.activate(language)

    return translator


Translator = Annotated[_Translator, Depends(get_translator)]


__all__ = ["get_accept_language", "AcceptLanguage", "get_translator", "Translator"]
