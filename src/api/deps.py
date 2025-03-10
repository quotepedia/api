from typing import Annotated

from fastapi import Depends

from src.api.params import SearchParams

SearchParamsDepends = Annotated[SearchParams, Depends(SearchParams)]
