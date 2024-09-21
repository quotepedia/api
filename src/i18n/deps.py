from typing import Annotated

from fastapi import Depends, Header


def get_accept_language(accept_language: str = Header("en")) -> str:
    return accept_language


AcceptLanguage = Annotated[str, Depends(get_accept_language)]


__all__ = ["get_accept_language", "AcceptLanguage"]
