from typing import Annotated

from fastapi import Depends

from src.api.collections.service import CollectionService

CollectionServiceDepends = Annotated[CollectionService, Depends(CollectionService)]
