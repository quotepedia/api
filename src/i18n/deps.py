from typing import Annotated

from fastapi import Depends, Header

from src.i18n import DEFAULT_ISO_639


def get_accept_language(accept_language: str = Header(DEFAULT_ISO_639)) -> str:
    return accept_language


AcceptLanguage = Annotated[str, Depends(get_accept_language)]


__all__ = ["get_accept_language", "AcceptLanguage"]
