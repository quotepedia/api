from typing import Annotated

from fastapi import Depends

from src.api.v1.authors.service import AuthorService

AuthorServiceDepends = Annotated[AuthorService, Depends(AuthorService)]
