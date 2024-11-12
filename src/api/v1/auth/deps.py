from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

TOKEN_URL = "api/v1/auth/login"

OAUTH2_BEARER = OAuth2PasswordBearer(TOKEN_URL)
OPTIONAL_OAUTH2_BEARER = OAuth2PasswordBearer(TOKEN_URL, auto_error=False)

OAuth2BearerDepends = Annotated[str, Depends(OAUTH2_BEARER)]
OptionalOAuth2BearerDepends = Annotated[str | None, Depends(OPTIONAL_OAUTH2_BEARER)]

OAuth2PasswordRequestFormDepends = Annotated[OAuth2PasswordRequestForm, Depends()]
