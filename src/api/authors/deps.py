from typing import Annotated

from fastapi import Depends

from src.api.authors.service import AuthorService

AuthorServiceDepends = Annotated[AuthorService, Depends(AuthorService)]
