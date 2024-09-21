from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

__oauth2_bearer = OAuth2PasswordBearer("api/v1/auth/login")

PasswordBearer = Annotated[str, Depends(__oauth2_bearer)]
PasswordForm = Annotated[OAuth2PasswordRequestForm, Depends()]
