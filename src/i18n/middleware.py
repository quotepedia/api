from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.i18n import DEFAULT_ISO_639, activate
from src.i18n.spec import get_preferred_iso_639


class I18nMiddleware(BaseHTTPMiddleware):
    """
    Represents a middleware for setting the language during the request based on the Accept-Language request header.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        accept_language = request.headers.get("Accept-Language", DEFAULT_ISO_639)
        language = get_preferred_iso_639(accept_language)
        activate(language)

        response = await call_next(request)
        return response


__all__ = ["I18nMiddleware"]
