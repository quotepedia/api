from typing import Annotated

from fastapi import Depends

from src.api.v1.collections.service import CollectionService

CollectionServiceDepends = Annotated[CollectionService, Depends(CollectionService)]
